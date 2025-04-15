import os
import time
from datetime import datetime
from time import sleep
from selenium import webdriver
from threading import Event
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ThreadPoolExecutor
import threading
import sys
exit_event = Event()

screenshots_path = 'ScreenShots'

isExist = os.path.exists(screenshots_path)
if not isExist:
    os.makedirs(screenshots_path)
    print("The new directory is created!")

# 웹드라이버 클래스 (생성자/소멸자)
class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        options.add_argument("disable-infobars")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        self.driver.set_window_size(1920,1080) 
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def __del__(self):
        self.driver.quit() # clean up driver when we are cleaned up


thread_local = threading.local()

# 웹페이지 로그인 제공


def login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath):
    try:
        # Grafana 로그인 페이지로 이동
        driver.get(url)
        driver.implicitly_wait(30)  
        driver.switch_to.default_content()
        driver.switch_to.parent_frame()

        try:
                  
            # 고급 버튼 클릭
            driver.find_element('xpath', '//*[@id="details-button"]').click()
            driver.implicitly_wait(10)  

            # 이동 버튼 클릭
            driver.find_element('xpath', '//*[@id="proceed-link"]').click()
            driver.implicitly_wait(10)  

            # Hcloud 추가
            driver.find_element('xpath', '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div[2]/div[2]/a').click() 
            driver.implicitly_wait(10)  

        except Exception as e:
            print(e)

        
        driver.implicitly_wait(3)           
    
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
    "01_k8s_cluster_1center_ccskr-rancher-prd": {
        "url": "https://hubble-apne2-prd.platform.hcloud.io/grafana/login/generic_oauth",
        "userid": "cocop",
        "passwd": "cocop",
        "userid_xpath": '//*[@id="username"]',
        "passwd_xpath": '//*[@id="password"]',
        "login_xpath": '//*[@id="kc-form-login"]/button'
    },
    "02_k8s_cluster_1center_ccskr-devworks-prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "03_k8s_cluster_1center_ccskr-dkc2hpkr-prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    }
}

def create_driver(bot):
    the_driver = getattr(thread_local, 'the_driver', None)
    
    if the_driver is None:
        try:
            the_driver = Driver()
            setattr(thread_local, 'the_driver', the_driver)

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



def take_screenshot(bot):
    
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
            "01_KR_k8s_cluster_1center_ccskr-rancher-prd": 'https://hubble-apne2-prd.platform.hcloud.io/grafana/d/coBoVkG4z/kr-apne1-rancher-local?orgId=27',
            "02_KR_k8s_cluster_1center_ccskr-devworks-prd": 'http://10.11.67.29:3000/d/1HihRd54k/coc-k8s-summary-dashboard-alert-system-kr1-kr_devworks_prd_cluster?orgId=1',
            "03_KR_k8s_cluster_1center_ccskr-dkc2hpkr-prd": 'http://10.11.67.29:3000/d/oOYkgdc4z/coc-k8s-summary-dashboard-alert-system-kr1-dkc2-hpkr?orgId=1'
        }
        filename = f'{screenshots_path}/{bot}_{datetime.now().strftime("%Y%m%d_%H%M")}.png'
        url = urls.get(bot)
        if url:
            driver.get(url)
            driver.implicitly_wait(30)  
            driver.set_window_size(1920, 1080)
            driver.implicitly_wait(10)  
            driver.maximize_window()
            sleep(15)
            driver.execute_script("document.body.style.zoom=0.80")
            driver.implicitly_wait(3)  
            driver.save_screenshot(filename)
        else:
            print("----"+bot+"캡처함수error-----")

        print("----"+bot+"캡처함수종료-----")
    # 예외 처리
    except Exception as e:
        print(f"Error occurred: {e}")
        print("\n... Program Stopped Manually!")
        return


def process_screencapture():

    number_threads = 3
    

    bots = [
        "01_k8s_cluster_1center_ccskr-rancher-prd",
        "02_k8s_cluster_1center_ccskr-devworks-prd",
        "03_k8s_cluster_1center_ccskr-dkc2hpkr-prd",
    ]

    with ThreadPoolExecutor(max_workers=number_threads) as pool:
        try:
            pool.map(take_screenshot, bots)
        except KeyboardInterrupt:
            print('Caught keyboardinterrupt')
            pass

if __name__ == "__main__":
    try:
        process_screencapture()
    except KeyboardInterrupt:
        print('Caught keyboardinterrupt')
        pass

    del thread_local

    # 메모리 캐시 삭제
    import gc
    gc.collect() # a little extra insurance