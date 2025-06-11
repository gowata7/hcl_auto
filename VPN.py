import subprocess

VPN_FR2_NAME = "FR2"
VPN_FR7_NAME = "FR7"
USERNAME = "spark"
PASSWORD = "tmvkzm1!"

# VPN 관련 함수
def is_vpn_connected(vpn_name):
    result = subprocess.run(['rasdial'], capture_output=True, text=True)
    return vpn_name.lower() in result.stdout.lower()

def connect_vpn(vpn_name, username, password):
    print(f"[INFO] Connecting to VPN: {vpn_name}")
    subprocess.run(['rasdial', vpn_name, username, password])

def disconnect_vpn(vpn_name):
    print(f"[INFO] Disconnecting VPN: {vpn_name}")
    subprocess.run(['rasdial', vpn_name, '/disconnect'])

if is_vpn_connected(VPN_FR2_NAME):
    print("FR2 VPN not connected. Connecting...")
    connect_vpn(VPN_FR2_NAME, USERNAME, PASSWORD)
    print("FR7 VPN disconnecting")
    disconnect_vpn(VPN_FR7_NAME)
else if is_vpn_connected(VPN_FR7_NAME):

else if not is_vpn_connected    
    print("VPN already connected.")