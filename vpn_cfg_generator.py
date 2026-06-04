from jinja2 import Environment, FileSystemLoader, StrictUndefined
from jinja2.exceptions import UndefinedError, TemplateNotFound
import ipaddress
import sys
import yaml
import os


FILE_VARS = 'vars.yaml'
FILE_TEMPLATE_FOLDER = 'templates/'
FILE_TEMPLATE = 's2s_vpn_template.j2'
FILE_TEMPLATE_OUTPUT = 'vpn_generated_cfg.txt'


def check_variable(key, var_value, range_start=0, range_stop=0):
    if not isinstance(var_value, int):
        print(f"ERROR: {key} variable: value [{var_value}] not a number! '{var_value}' == {type(var_value)}")
        sys.exit(1)


    if not range_start <= var_value <= range_stop:
        print(f"ERROR: [{key}] value [{var_value}] out of range {range_start}-{range_stop}")
        sys.exit(1)
        
    print(f"Variable [{key}] value [{var_value}] verified OK.")


def verify_ip_addr(ip_addr):
    """Function for verifying validity of an IP address provided by user."""
    try:
        ip_addr = ipaddress.IPv4Interface(ip_addr)
        print(f"IP address [{ip_addr.ip}] verified OK.")
        return ip_addr
    except (ipaddress.AddressValueError, ValueError, KeyError) as e:
        print(f"ERROR: Wrong IP address provided: {e}")
        sys.exit(1)


def verify_netmask_addr(ip_addr):
    """Function to verify validity of a netmask address provided by user."""
    try:
        ip_addr_mask = ipaddress.IPv4Interface(f"0.0.0.0/{ip_addr}")
        print(f"Netmask [{ip_addr_mask.netmask}] verified OK.")
        return ip_addr_mask
    except (ipaddress.AddressValueError, ValueError) as e:
        print(f"ERROR: Wrong netmask address provided: {e}")
        sys.exit(1)


# Load YAML variables
def get_variable_values(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: file '{filename}' not found in '{os.getcwd()}' folder.")
        sys.exit(1)


def main():
    variable_allowed_range = {
        'ikev2_lifetime': (120,86400),
        'ipsec_lifetime': (120, 2592000),
        'crypto_map_number': (1, 65535)
    }


    allowed_pfs_group = {'group14', 'group15'}


    vpn_vars = get_variable_values(FILE_VARS)


    # Validation of data
    print("\n---- START VERIFICATION OF DATA ----\n")
    for key, ranges in variable_allowed_range.items():
        if key not in vpn_vars:
            print(f"ERROR: required key [{key}] missing from '{FILE_VARS}'")
            sys.exit(1)
        check_variable(key, vpn_vars[key], ranges[0], ranges[1])


    try:
        verify_ip_addr(vpn_vars['local_ip_addr'])
        verify_ip_addr(vpn_vars['remote_peer_ip'])
        verify_netmask_addr(vpn_vars['remote_peer_mask'])

        if vpn_vars['pfs_group_var'] not in allowed_pfs_group:
            print(f"ERROR: Wrong name of PFS group: [{vpn_vars['pfs_group_var']}]")
            sys.exit(1)
        print(f"Value of PFS group: [{vpn_vars['pfs_group_var']}] verified OK.")
    except KeyError as e:
        print(f"ERROR: key {e} does not exists!")
        sys.exit(1)

    print("\n---- END VERIFICATION OF DATA ----")


    # Generating template
    environment = Environment(
        loader=FileSystemLoader(FILE_TEMPLATE_FOLDER),
        undefined=StrictUndefined
        )

    print("\n" + "#"*80)


    try:
        template = environment.get_template(FILE_TEMPLATE)
        print("\n---- PRINTING PREPARED TEMPLATE ----\n")
        content = template.render(**vpn_vars)
        print(content)

        with open(FILE_TEMPLATE_OUTPUT, 'w') as f:
            f.write(content)
        print(f"\nConfig saved in {os.path.abspath(FILE_TEMPLATE_OUTPUT)}.")

    except TemplateNotFound:
        print(f"\nERROR: Template file [{FILE_TEMPLATE}] was not found in '{FILE_TEMPLATE_FOLDER}' folder!")
        sys.exit(1)
    except (UndefinedError, UnboundLocalError) as e:
        print(f"\nERROR in template generate due to: {e}!")
        sys.exit(1)

if __name__ == "__main__":
    main()
