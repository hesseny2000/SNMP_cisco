This project provides a structured and automated approach to retrieve the operational information of network devices—traditionally accessed via CLI commands—by using SNMP OIDs instead.
The main objective is to map common and critical CLI commands (such as routing neighbors, interface status, hardware inventory, MPLS, and protocol summaries) to their equivalent SNMP MIBs and OIDs, enabling programmatic data collection without direct CLI access.

The project focuses on enterprise and service-provider network devices (e.g., Cisco IOS-XR / ASR platforms) and delivers:

Identification of the correct standard and vendor-specific MIBs corresponding to each CLI command

Reliable data retrieval using SNMPv2c / SNMPv3

Normalization of SNMP outputs into human-readable, CLI-like formats

Automation through Python scripts for scalable monitoring and auditing

Reduction of dependency on interactive CLI access, improving security and operational efficiency

This solution is particularly useful for network monitoring systems, compliance checks, capacity planning, and large-scale automation, where consistent, read-only access to device state is required across heterogeneous network environments.
