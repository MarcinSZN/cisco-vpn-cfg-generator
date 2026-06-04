# Automated Site-to-Site VPN Configuration Generator

A Python-based Network Automation tool that gets network infrastructure variables from a YAML file, executes strict data validation boundaries, and dynamically generates structured Cisco Site-to-Site VPN Policy-Based configuration snippets using Jinja2 templates.

This repository serves as a portfolio demonstration of Python programming fundamentals, defensive data validation, and template-driven infrastructure-as-code (IaC) principles for NetDevOps.

---

## 🚀 Key Features

* **Strict Input Validation:** Utilizes Python's native `ipaddress` library to ensure network identifiers, IPv4 addresses, and subnet masks are syntactically valid before configuration generation.
* **Network Boundary Guardrails:** Implements algorithmic range validation to ensure critical values (VLAN IDs, Crypto Map sequences, IKEv2/IPSec lifetimes) conform strictly to network protocol limits.
* **Fail-Safe Operations:** Enforces Jinja2 `StrictUndefined` rendering to instantly crash the script with a descriptive error code (`sys.exit(1)`) if the source variable file lacks a parameter required by the template.
* **Automated File Output:** Automatically renders, displays, and archives the ready-to-deploy configuration snippet into a localized `.txt` file.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.x
* **Data Serialization:** PyYAML (for structured variable ingestion)
* **Templating Engine:** Jinja2 (for dynamic configuration parsing)
* **Core Libraries:** `ipaddress`, `sys`, `os`, `pyyaml`

---

## 📂 Repository Structure

```text
├── templates/
│   └── s2s_vpn_template.j2    # The source reusable Jinja2 VPN configuration template
├── vars.yaml                  # Input file containing network-specific variables
├── vpn_generator.py           # Core Python execution and data validation script
├── .gitignore                 # Excludes local environments and python bytecode cache
└── README.md                  # Project documentation
```


💻 How To Run the Script
1. Clone the repository

```bash
git clone (https://github.com/MarcinSZN/cisco-vpn-cfg-generator.git)
```

2. Install dependencies
Ensure you have PyYAML and Jinja2 installed
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python vpn_cfg_generator.py
```

📊 Example Output

Terminal Output (Successful Validation)

```plaintext
---- START VERIFICATION OF DATA ----

Variable [ikev2_lifetime] value [14400] verified OK.
Variable [ipsec_lifetime] value [1880] verified OK.
Variable [crypto_map_number] value [120] verified OK.
IP address [10.10.10.10] verified OK.
IP address [172.16.1.1] verified OK.
Netmask [255.255.255.252] verified OK.
Value of PFS group: [group15] verified OK.

---- END VERIFICATION OF DATA ----

################################################################################

---- PRINTING PREPARED TEMPLATE ----

crypto ikev2 keyring KR_DEMO
  peer DEMO
    address 172.16.1.1
    pre-shared-key # PUT HERE PRE_SHARED KEY #
!
crypto ikev2 profile PROFILE_NAME_DEMO
  match identity remote address 172.16.1.1 255.255.255.252
  identity local address 10.10.10.10
  authentication remote pre-share
  authentication local pre-share
  keyring local KR_DEMO
  lifetime 14400

crypto map MAP_DEVICE 120 ipsec-isakmp
  description --- DEMO ---
  set peer 172.16.1.1
  set security-association lifetime seconds 1880
  set transform-set DEMO_TRANSFORM_SET_NAME
  set pfs group15
  set ikev2-profile PROFILE_NAME_DEMO
  match address # PUT ACL NAME FOR VPN HERE #

Config saved in /Path/to/vpn_generated_cfg.txt.
```

## Disclaimer
Script **might not** work for every possible S2S Tunnel configuration, might crash by oversight, script also generates only part of the configuration, and eventually might be extended with more features by me or any volunteer.
Script should be tested in staging/lab environment first before using it on production systems.
