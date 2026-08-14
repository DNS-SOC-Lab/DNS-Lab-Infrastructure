# Splunk Build

**Status:** Planned — implementation has not started yet.

This folder will become the technical record for the Splunk Enterprise deployment after the EC2 foundation is ready. It will contain only work that has actually been implemented and validated, including:

- Splunk Enterprise Docker deployment;
- indexes and sourcetypes used by the lab;
- Universal Forwarder onboarding;
- AWS log inputs as they are connected;
- validation searches for timestamps, hosts, sources and fields;
- DNS SOC dashboards and saved searches;
- data-health and troubleshooting notes.

The project design expects Splunk to act as the central analytics platform. A data source is not considered onboarded just because events appear; the team should validate the index, sourcetype, time, host identity and fields required by the detection use case.
