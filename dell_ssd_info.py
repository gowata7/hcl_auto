import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

# ====== 설정 ======
USERNAME1 = "root"
PASSWORD1 = "Ipmiroot1!"
USERNAME2 = "spark"
PASSWORD2 = "TldhTl1!"
# PRIVATE_KEY = "./id_rsa_dell"
OUTPUT_FILE = "dell_disk_info.csv"
INVENTORY_FILE = "inventory.ini"
MAX_THREADS = 20

# ====== Inventory 파일 읽기 ======
with open(INVENTORY_FILE, 'r') as file:
    DEVICE_LIST = [line.strip() for line in file.readlines() if line.strip()]

# ====== CSV 파일 초기화 ======
with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IP", "DiskID", "Manufacturer", "Revision"])

# SSH로 정보 수집
def collect_disk_info(ip):
    try:
        # key = paramiko.RSAKey(filename=PRIVATE_KEY)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"[INFO] Trying to connect to {ip} with USERNAME1...")
        # ====== 첫 번째 시도 ======
        try:
            client.connect(ip, username=USERNAME1, password=PASSWORD1, timeout=10)
        except (paramiko.AuthenticationException, paramiko.SSHException, paramiko.ssh_exception.NoValidConnectionsError) as e:
            print(f"[WARN] Connection failed with USERNAME1 for {ip}. Trying USERNAME2...")

            # ====== 두 번째 시도 ======
            try:
                client.connect(ip, username=USERNAME2, password=PASSWORD2, timeout=10)
            except Exception as e:
                print(f"[ERROR] Connection failed with USERNAME2 for {ip}. Skipping...")
                return None

        stdin, stdout, stderr = client.exec_command("racadm storage get pdisks -o")
        output = stdout.read().decode()
        
        data = []
        current_disk = None
        
        for line in output.splitlines():
            if "Disk" in line and "Bay" in line:
                current_disk = line.strip()
            if "Manufacturer" in line:
                manufacturer = line.split('=')[-1].strip()
            if "Revision" in line:
                revision = line.split('=')[-1].strip()
                
                # CSV에 작성할 데이터
                if current_disk:
                    data.append((ip, current_disk, manufacturer, revision))
        
        client.close()
        return data
    except Exception as e:
        print(f"[ERROR] {ip}: {e}")
        return None

# ====== 병렬 실행 ======
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(collect_disk_info, ip) for ip in DEVICE_LIST]

    with open(OUTPUT_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        for future in as_completed(futures):
            result = future.result()
            if result:
                writer.writerows(result)

print(f"[INFO] 모든 디스크 정보를 '{OUTPUT_FILE}'에 저장했습니다.")
