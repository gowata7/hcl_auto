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
        sleep(20)  
        self.driver.maximize_window()

    def __del__(self):
        self.driver.quit() # clean up driver when we are cleaned up


thread_local = threading.local()

# 웹페이지 로그인 제공


def login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath):
    try:
        # Grafana 로그인 페이지로 이동
        driver.get(url)
        sleep(20)   
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

        
        sleep(20)            
    
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
    "01_SG_lb(f5)": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "02_SG_fw_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "03_SG_total_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "04_SG_host_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "05_SG_vm_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "06_SG_database_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "07_SG_mongo": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "08_SG_storage_1": {
        "url": "https://10.107.48.110/sysmgr/v4/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/div[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/div[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/div[3]/nwf-loading-button/button'
    },
    "09_SG_storage_2": {
        "url": "https://10.107.48.130/sysmgr/v4/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/div[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/div[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/div[3]/nwf-loading-button/button'
    },
    "10_SG_netapp_info": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "11_SG_cluster_info_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "12_SG_cluster_info_2": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "13_SG_cluster_info_3": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "14_SG_cluster_info_4": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "15_SG_cluster_info_5": {
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
            "01_SG_lb(f5)": "http://10.11.67.29:3000/d/sjElzXFVk/sg_f5_monitor?orgId=1",
            "02_SG_fw_1": "http://10.11.67.29:3000/d/0kQdZuFVk/sg-fw-monitor?orgId=1",
            "03_SG_total_1": "http://10.11.67.29:3000/d/qstVWXF4z/sg-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1",
            "04_SG_host_1": "http://10.11.67.29:3000/d/dPViDjKVk/sg-bm-and-netapp-resource?orgId=1",
            "05_SG_vm_1": "http://10.11.67.29:3000/d/5bY3CrK4z/sg-vm-resource?orgId=1",
            "06_SG_database_1": "http://10.11.67.29:3000/d/RJrKguFVz/sg-prd-db-resource-usage-top-20?orgId=1",
            "07_SG_mongo": "http://10.11.67.29:3000/d/1Igbn754k/na_mongodb?orgId=1",
            "08_SG_storage_1": "https://10.107.48.110/sysmgr/v4/",
            "09_SG_storage_2": "https://10.107.48.130/sysmgr/v4/",
            "10_SG_netapp_info": "http://10.11.67.29:3000/d/Bh1NWuF4k/sg-netapp-dash-board?orgId=1",
            "11_SG_cluster_info_1": "http://10.11.67.29:3000/d/s-HlRO5Vk/coc-k8s-summary-dashboard-alert-system-1?orgId=1",
            "12_SG_cluster_info_2": "http://10.11.67.29:3000/d/6bgugO5Vk/coc-k8s-summary-dashboard-alert-system-2?orgId=1",
            "13_SG_cluster_info_3": "http://10.11.67.29:3000/d/26t9gdcVz/coc-k8s-summary-dashboard-alert-system-3?orgId=1",
            "14_SG_cluster_info_4": "http://10.11.67.29:3000/d/1R13gO54k/coc-k8s-summary-dashboard-alert-system-4?orgId=1",
            "15_SG_cluster_info_5": "http://10.11.67.29:3000/d/bxw6gOc4z/coc-k8s-summary-dashboard-alert-system-5?orgId=1",
        }
        filename = f'{screenshots_path}/{bot}_{datetime.now().strftime("%Y%m%d_%H%M")}.png'
        url = urls.get(bot)

        if url: 

            if bot == "08_SG_storage_1" or bot == "09_SG_storage_2":
          
                sleep(20)  
                driver.execute_script("document.body.style.zoom=0.80")
                sleep(20)  
                sleep(20)
                driver.save_screenshot(filename)    
                driver.close()
                driver.quit()
                print('스토리지 캡')

            else:
                driver.get(url)
                sleep(20)  
                driver.set_window_size(1920, 1080)
                driver.maximize_window()
                
                sleep(50)
                driver.execute_script("document.body.style.zoom=0.75")
                sleep(30)
                driver.save_screenshot(filename)
                driver.close()
                driver.quit()
        else: 
            print("fucking error")
            
        


       
        print("----"+bot+"캡처함수종료-----")
    # 예외 처리
    except Exception as e:
        print(f"Error occurred: {e}")
        print("\n... Program Stopped Manually!")
        return


def main_capture():

    number_threads = 8
    

    bots = [
        "01_SG_lb(f5)",
        "02_SG_fw_1",
        "03_SG_total_1",
        "04_SG_host_1",
        "05_SG_vm_1",
        "06_SG_database_1",
        "07_SG_mongo",
        "08_SG_storage_1",
        "09_SG_storage_2",
        "10_SG_netapp_info",
        "11_SG_cluster_info_1",
        "12_SG_cluster_info_2",
        "13_SG_cluster_info_3",
        "14_SG_cluster_info_4",
        "15_SG_cluster_info_5",
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

    del thread_local

    # 메모리 캐시 삭제
    import gc
    gc.collect() # a little extra insurance
    print("---------------------------end----------------------------")