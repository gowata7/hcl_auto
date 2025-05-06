import subprocess

VPN_NAME = "KR2"
USERNAME = "spark"
PASSWORD = "tmvkzm1!"

def is_vpn_connected(vpn_name):
    result = subprocess.run(['rasdial'], capture_output=True, text=True)
    return vpn_name.lower() in result.stdout.lower()

def connect_vpn(vpn_name, username, password):
    subprocess.run(['rasdial', vpn_name, username, password])

if not is_vpn_connected(VPN_NAME):
    print("VPN not connected. Connecting...")
    connect_vpn(VPN_NAME, USERNAME, PASSWORD)
else:
    print("VPN already connected.")