import json
import logging
import os
import uuid
from datetime import datetime, timezone

import requests
from flask import Flask, jsonify, request
from jsonschema import ValidationError, validate
from openai import OpenAI

app = Flask(__name__)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("dns-soc-ai-bridge")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-terra")
OPENAI_TIMEOUT_SECONDS = float(os.getenv("OPENAI_TIMEOUT_SECONDS", "30"))
SPLUNK_HEC_URL = os.getenv("SPLUNK_HEC_URL")
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")
SPLUNK_HEC_TIMEOUT_SECONDS = float(
    os.getenv("SPLUNK_HEC_TIMEOUT_SECONDS", "10")
)
SPLUNK_HEC_VERIFY_TLS = (
    os.getenv("SPLUNK_HEC_VERIFY_TLS", "true").lower() == "true"
)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    timeout=OPENAI_TIMEOUT_SECONDS,
)

ALERT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "alert_id",
        "alert_name",
        "scenario",
        "severity",
        "event_time",
        "evidence",
    ],
    "properties": {
        "alert_id": {"type": "string", "minLength": 1},
        "alert_name": {"type": "string", "minLength": 1},
        "scenario": {"type": "string", "minLength": 1},
        "severity": {
            "type": "string",
            "enum": ["informational", "low", "medium", "high", "critical"],
        },
        "event_time": {"type": "string", "minLength": 1},
        "source": {"type": ["string", "null"]},
        "evidence": {
            "type": "object",
            "additionalProperties": True,
        },
    },
}

AI_RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "summary",
        "observed_indicators",
        "network_context",
        "suspicion_reasons",
        "mitre_attack",
        "cyber_kill_chain",
        "missing_evidence",
        "response_considerations",
        "confidence",
    ],
    "properties": {
        "summary": {"type": "string"},
        "observed_indicators": {
            "type": "array",
            "items": {"type": "string"},
        },
        "network_context": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "primary_osi_layer",
                "related_layers",
                "protocols",
                "explanation",
            ],
            "properties": {
                "primary_osi_layer": {"type": "string"},
                "related_layers": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "protocols": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "explanation": {"type": "string"},
            },
        },
        "suspicion_reasons": {
            "type": "array",
            "items": {"type": "string"},
        },
        "mitre_attack": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "tactic",
                "technique_id",
                "technique_name",
                "explanation",
            ],
            "properties": {
                "tactic": {"type": "string"},
                "technique_id": {"type": "string"},
                "technique_name": {"type": "string"},
                "explanation": {"type": "string"},
            },
        },
        "cyber_kill_chain": {
            "type": "object",
            "additionalProperties": False,
            "required": ["stage", "explanation"],
            "properties": {
                "stage": {"type": "string"},
                "explanation": {"type": "string"},
            },
        },
        "missing_evidence": {
            "type": "array",
            "items": {"type": "string"},
        },
        "response_considerations": {
            "type": "array",
            "items": {"type": "string"},
        },
        "confidence": {
            "type": "string",
            "enum": ["low", "medium", "high"],
        },
    },
}


def send_to_splunk(event):
    if not SPLUNK_HEC_URL or not SPLUNK_HEC_TOKEN:
        raise RuntimeError("Splunk HEC configuration missing")

    payload = {
        "event": event,
        "index": "dns_soc_ai",
        "sourcetype": "dns_soc:ai:triage",
        "source": "dns-soc-ai-bridge",
    }

    response = requests.post(
        SPLUNK_HEC_URL,
        headers={
            "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=SPLUNK_HEC_TIMEOUT_SECONDS,
        verify=SPLUNK_HEC_VERIFY_TLS,
    )
    response.raise_for_status()

    body = response.json()
    if body.get("code") != 0:
        raise RuntimeError(f"Splunk HEC rejected event: {body}")

    return body


def normalize_alert_payload(payload):
    """Accept either the common contract or Splunk's native webhook envelope."""
    if isinstance(payload, dict) and "result" in payload:
        result = payload.get("result")
        if not isinstance(result, dict):
            raise ValueError("splunk_result_must_be_an_object")

        evidence_raw = result.get("evidence_json", "{}")
        if isinstance(evidence_raw, str):
            try:
                evidence = json.loads(evidence_raw)
            except json.JSONDecodeError as exc:
                raise ValueError("evidence_json_is_invalid") from exc
        elif isinstance(evidence_raw, dict):
            evidence = evidence_raw
        else:
            raise ValueError("evidence_json_must_be_json_object")

        return {
            "alert_id": str(result.get("alert_id", "")),
            "alert_name": str(
                result.get("alert_name") or payload.get("search_name") or ""
            ),
            "scenario": str(result.get("scenario", "")),
            "severity": str(result.get("severity", "")).lower(),
            "event_time": str(result.get("event_time", "")),
            "source": (
                str(result.get("source"))
                if result.get("source") not in (None, "")
                else None
            ),
            "evidence": evidence,
        }

    return payload


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "dns-soc-ai-bridge",
            "model": OPENAI_MODEL,
        }
    ), 200


@app.post("/splunk-webhook")
def splunk_webhook():
    request_id = str(uuid.uuid4())

    if not request.is_json:
        return jsonify(
            {
                "status": "error",
                "request_id": request_id,
                "error": "content_type_must_be_application_json",
            }
        ), 415

    incoming_payload = request.get_json(silent=True)
    if incoming_payload is None:
        return jsonify(
            {
                "status": "error",
                "request_id": request_id,
                "error": "invalid_json",
            }
        ), 400

    try:
        payload = normalize_alert_payload(incoming_payload)
    except ValueError as exc:
        return jsonify(
            {
                "status": "error",
                "request_id": request_id,
                "error": "payload_normalization_failed",
                "detail": str(exc),
            }
        ), 400

    try:
        validate(instance=payload, schema=ALERT_SCHEMA)
    except ValidationError as exc:
        return jsonify(
            {
                "status": "error",
                "request_id": request_id,
                "error": "schema_validation_failed",
                "detail": exc.message,
            }
        ), 400

    instructions = """
You are an advisory SOC alert triage assistant.
Analyze only the evidence supplied in the alert payload.

Rules:
- Never declare an alert definitively true-positive or false-positive.
- Never claim evidence that is not present.
- Clearly identify missing, weak, or ambiguous evidence.
- Do not authorize or execute containment.
- Response actions are analyst considerations only.
- Framework mappings are analyst context, not final classifications.

Network context:
- Explain the likely OSI/network layer or layers involved.
- Distinguish the application protocol from supporting network and transport evidence.
- Identify protocols only when supported by supplied evidence.

MITRE ATT&CK:
- Suggest tactic and technique only when reasonably supported.
- If uncertain, use "Uncertain".
- Explain why supplied evidence may support the mapping.

Cyber Kill Chain:
- Suggest a stage only when reasonably supported.
- If uncertain, use "Uncertain".
- Explain why the evidence may fit that stage.

Analysis quality:
- Prefer uncertainty over unsupported assumptions.
- Explicitly list evidence required for stronger analyst confidence.
"""

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=instructions,
            input=json.dumps(payload),
            text={
                "format": {
                    "type": "json_schema",
                    "name": "soc_triage_result",
                    "strict": True,
                    "schema": AI_RESPONSE_SCHEMA,
                }
            },
        )
        ai_result = json.loads(response.output_text)
        validate(instance=ai_result, schema=AI_RESPONSE_SCHEMA)
    except Exception:
        logger.exception("OpenAI processing failed request_id=%s", request_id)
        return jsonify(
            {
                "status": "error",
                "request_id": request_id,
                "error": "ai_processing_failed",
            }
        ), 502

    result = {
        "request_id": request_id,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "alert": payload,
        "ai": ai_result,
        "human_validation_required": True,
    }

    try:
        send_to_splunk(result)
    except Exception:
        logger.exception("Splunk HEC delivery failed request_id=%s", request_id)
        return jsonify(
            {
                "status": "error",
                "request_id": request_id,
                "error": "splunk_hec_delivery_failed",
            }
        ), 502

    return jsonify(
        {
            "status": "success",
            "request_id": request_id,
            "human_validation_required": True,
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
