from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver
from threading import Event
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess
import platform
import certifi
import threading
import sys
import urllib3
import zipfile
import os
import shutil
import time

screenshots_path = 'ScreenShots'
isExist = os.path.exists(screenshots_path)

if not isExist:
    os.makedirs(screenshots_path)
    print("The new directory is created!")

# Chrome 버전 변경 시, Chrome webdriver 설치
# https://googlechromelabs.github.io/chrome-for-testing/#stable

import winreg
import requests

def get_chrome_version_from_registry():
    reg_paths = [
        r"SOFTWARE\Google\Chrome\BLBeacon",  # 일반 설치
        r"SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon"  # 32bit 설치 경로
    ]

    for reg_path in reg_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
            version, _ = winreg.QueryValueEx(reg_key, "version")
            winreg.CloseKey(reg_key)
            return version
        except FileNotFoundError:
            continue

    print("[ERROR] Chrome version not found in registry.")
    return None

# 📌 2. 다운로드 및 설치
def download_and_install_chromedriver(chrome_version):
    major_version = chrome_version.split('.')[0]
    # base_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{chrome_version}/win64/chromedriver-win64.zip"
    base_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"

    print(f"[INFO] Downloading ChromeDriver for version {chrome_version}...")
    r = requests.get(base_url, stream=True)
    if r.status_code != 200:
        print(f"[ERROR] Failed to download chromedriver from {base_url}")
        sys.exit(1)

    zip_path = 'chromedriver.zip'
    with open(zip_path, 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()

    # chromedriver 위치로 이동
    shutil.move("chromedriver-win64/chromedriver.exe", "./chromedriver.exe")
    shutil.rmtree("chromedriver-win64")
    os.remove(zip_path)
    print("[INFO] ChromeDriver installed successfully.")

chrome_version = get_chrome_version_from_registry()
print(f"[INFO] Detected Chrome version: {chrome_version}")
download_and_install_chromedriver(chrome_version)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
exit_event = Event()
os.environ['WDM_SSL_VERIFY'] = '0'
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# driver.implicitly_wait(60)

# 웹드라이버 클래스 (생성자/소멸자)
class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # 최신 headless 모드
        options.add_argument("--disable-gpu")  # 필요 시 제거
        options.add_argument("--enable-unsafe-swiftshader")
        options.add_argument("--use-gl=swiftshader")
        # options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")

        try:
            # 🔥 핵심: ChromeDriverManager로 설치하고 service로 넘김
            # service = Service(ChromeDriverManager().install())
            service = Service(executable_path="C:/Beomjun/chromedriver.exe")
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print("❌ WebDriver 생성 실패:", e)
            raise
        # service = Service(executable_path='chromedriver')  # 또는 전체 경로
        # self.driver = webdriver.Chrome(service=service, options=options)
        # self.driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        self.driver.set_window_size(1920,1080) 
        sleep(10)
        self.driver.maximize_window()

    def __del__(self):
        try:   
            self.driver.quit() # clean up driver when we are cleaned up
        except Exception:
            pass

thread_local = threading.local()

# 웹페이지 로그인 제공
def login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath):
    try:
        # Grafana 로그인 페이지로 이동
        driver.get(url)
        driver.switch_to.default_content()
        driver.switch_to.parent_frame()

        try:
            # 고급 버튼 클릭
            driver.find_element('xpath', '//*[@id="details-button"]').click()

            # 이동 버튼 클릭
            driver.find_element('xpath', '//*[@id="proceed-link"]').click()

            # Hcloud 추가
            driver.find_element('xpath', '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div[2]/div[2]/a').click() 

        except Exception as e:
            print(e)

     
        username = driver.find_element('xpath', userid_xpath)    
        print("id입력 성공"+url)    
        username.clear()
        username.send_keys(userid)
        sleep(3)
        
        password = driver.find_element('xpath', passwd_xpath)
        print("pw입력 성공"+url) 
        password.clear()
        password.send_keys(passwd)
        sleep(3)

        # Login 버튼 클릭
        driver.find_element('xpath', login_xpath).click()
        print("login시도중---->>"+url)
        sleep(3)
   
    except Exception as e:
        return None
        
    return driver


# 로그인 정보 딕셔너리
login_info = {
    "01_EU_Hcloud_Storage": {
        "url": "https://hubble-euce.platform.hcloud.io/grafana/login/generic_oauth",
        # "url": "https://sso.hcloud.hmc.co.kr/auth/realms/hcloud/protocol/openid-connect/auth?client_id=iam-client&redirect_uri=http%3A%2F%2Fhubble-euce.platform.hcloud.io%2Fgrafana%2Flogin%2Fgeneric_oauth&response_type=code&scope=openid+email+profile&state=6kBGz08USQFE2sxJSKZl9LSlao6N9aQCqaBfpIM03cs%3D",
        "userid": "cocop",
        "passwd": "cocop",
        "userid_xpath": '//*[@id="username"]',
        "passwd_xpath": '//*[@id="password"]',
        "login_xpath": '//*[@id="kc-form-login"]/button'
    },
}

def create_driver(bot):
    the_driver = getattr(thread_local, 'the_driver', None)
    print(the_driver)
    # if the_driver is None:
    try:
        the_driver = Driver()
        setattr(thread_local, 'the_driver', the_driver)
        print("새드라이버 생성중~")
    except Exception as e:
        print(e)
        return None

    driver = the_driver.driver

    print("-----create_driver="+bot+"------")
    sleep(3)

    try:
        login_data = login_info.get(bot)
        if login_data:
            url = login_data["url"]
            userid = login_data["userid"]
            passwd = login_data["passwd"]
            userid_xpath = login_data["userid_xpath"]
            passwd_xpath = login_data["passwd_xpath"]
            login_xpath = login_data["login_xpath"]
            driver=login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)
            if driver is None: 
                return None
    except Exception as e:
        print(e)

    return driver


def capture_screen(bot):
    
    try:
        driver = create_driver(bot)
        
        if driver is None:
            print("드라이버 생성 실패")
            return  # 드라이버 생성 실패 시 함수 종료
        print("----"+bot+"캡처함수시작---")
        print(f"Capturing the screens started at {datetime.now()}")
        
        start_time = time.time()
        # 최종(대시보드) 페이지 및 저장파일 이름 설정
        urls = {
            "01_EU_Hcloud_Storage": "https://hubble-euce.platform.hcloud.io/grafana/d/dongheon-euce/netapp-euce-summary?orgId=41&viewPanel=2&from=now-3h&to=now",
        }
        filename = f'{screenshots_path}/{bot}_{datetime.now().strftime("%Y%m%d_%H%M")}.png'
        url = urls.get(bot)
        print("url:",url)
        print("bot:",bot)

        if url: 
            if bot == '01_EU_Hcloud_Storage':
                driver.get(url)
                # driver.implicitly_wait(30)
                sleep(30)
                
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="mega-menu-toggle"]'))
                ).click()
                # driver.execute_script("document.querySelector('#mega-menu-toggle').click();")
                sleep(5)
                driver.set_window_size(1920, 1300)
                # driver.maximize_window()

                # sleep(30)
                # driver.execute_script("document.body.style.zoom=0.75")
                # element = driver.find_element('xpath', '//*[@id="mega-menu-toggle"]')
                # if element.is_displayed():
                #     element.click()
                #     print("click success!")
                # else:
                #     print("Element is not visible in headless mode")


                # driver.set_window_size(1920, 1500)
                # driver.maximize_window()
                # sleep(10)
                # get total page dimensions
                # total_width = driver.execute_script("return document.body.scrollWidth")
                # total_height = driver.execute_script("return document.body.scrollHeight")

                # set to full size
                # driver.set_window_size(total_width, total_height)
                # sleep(2)

                # zoom out
                sleep(5)
                # driver.execute_script("document.body.style.zoom='0.50'")
                # sleep(2)
                # driver.execute_script("document.body.style.zoom='0.75'")
                # sleep(10)
                driver.save_screenshot(filename)    
                driver.close()
                driver.quit()
                print('스토리지 캡쳐 완료!')

            else:
                
                driver.get(url)
                sleep(30)
                driver.set_window_size(1920, 1080)
                driver.maximize_window()
               
                sleep(50)
                driver.execute_script("document.body.style.zoom=0.75")
                sleep(30)
                driver.save_screenshot(filename)
                driver.close()
                driver.quit()
        else: 
            print("Error occurred while capture!!")
        print("----"+bot+"캡처함수종료-----")
    # 예외 처리
    except Exception as e:
        print(f"Error occurred: {e}")
        print("\n... Program Stopped Manually!")
        return

def main_capture():

    number_threads = 1
    
    bots = [
        '01_EU_Hcloud_Storage',
    ]

    with ThreadPoolExecutor(max_workers=number_threads) as pool:
        try:
            pool.map(capture_screen, bots)
        except KeyboardInterrupt:
            print('Caught keyboardinterrupt')
            pass

if __name__ == "__main__":
    try:
        main_capture()
    except KeyboardInterrupt:
        print('Caught keyboardinterrupt')
        pass

    import gc
    gc.collect() # a little extra insurance
    print("---------------------------end----------------------------")