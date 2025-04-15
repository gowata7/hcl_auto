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
        sleep(25)
        self.driver.maximize_window()

    def __del__(self):
        self.driver.quit() # clean up driver when we are cleaned up


thread_local = threading.local()

# 웹페이지 로그인 제공


def login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath):
    try:
        # Grafana 로그인 페이지로 이동
        driver.get(url)
        sleep(25)
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

        
        sleep(25)       
    
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
    
    "01_NA_lb(a10)": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "02_NA_fw_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "03_NA_total_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "04_NA_host_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "05_NA_vm_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "06_NA_database_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "07_NA_mongo": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "08_NA_netapp_info": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "09_NA_storage_1": {
        "url": "https://10.7.0.231/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": "//*[@id=\"nwf-login-form\"]/dl/dd[1]/input",
        "passwd_xpath": "//*[@id=\"nwf-login-form\"]/dl/dd[2]/input",
        "login_xpath": "//*[@id=\"nwf-login-form\"]/button"
    },
    "10_NA_storage_2": {
        "url": "https://10.7.0.231/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": "//*[@id=\"nwf-login-form\"]/dl/dd[1]/input",
        "passwd_xpath": "//*[@id=\"nwf-login-form\"]/dl/dd[2]/input",
        "login_xpath": "//*[@id=\"nwf-login-form\"]/button"
    },
    "11_NA_cluster_info_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "12_NA_cluster_info_2": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "13_NA_cluster_info_3": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "14_NA_cluster_info_4": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
    },
    "15_NA_cluster_info_5": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "passwd_xpath": "//*[@id=\"current-password\"]",
        "login_xpath": "//*[@id=\"reactRoot\"]/div/main/div[3]/div/div[2]/div/div/form/button"
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
        
    "01_NA_lb(a10)": "http://10.11.67.29:3000/d/EHCxmuK4k/natms-a10-resource-monitor?orgId=1",
    "02_NA_fw_1": "http://10.11.67.29:3000/d/HK5wzuFVk22/natms-fw_resource-monitor?orgId=1",
    "03_NA_total_1": "http://10.11.67.29:3000/d/ZqR0sztVz/na-prd-ccs-neteuweokeu-jonghab-moniteoring-bogoseoyong?orgId=1",
    "04_NA_host_1": "http://10.11.67.29:3000/d/67-wNjK4k/na-bm-and-netapp-resource?orgId=1",
    "05_NA_vm_1": "http://10.11.67.29:3000/d/0azeCrF4k/na-vm-resource?orgId=1",
    "06_NA_database_1": "http://10.11.67.29:3000/d/7DOFRuKVz/na-prd-db-resource-usage-top-20?orgId=1",
    "07_NA_mongo": "http://10.11.67.29:3000/d/1Igbn754k/na_mongodb?orgId=1",
    "08_NA_netapp_info": "http://10.11.67.29:3000/d/LjsjmuF4z/na-prd-netapp-dash-board?orgId=1",
    "09_NA_storage_1": "https://10.7.0.231/clusters/6035/explorer",
    "10_NA_storage_2": "https://10.7.0.231/clusters/82788/explorer",
    "11_NA_cluster_info_1": "http://10.11.67.29:3000/d/DJdDeD5Vz/coc-k8s-summary-dashboard-alert-system-na-1?orgId=1",
    "12_NA_cluster_info_2": "http://10.11.67.29:3000/d/FnMc6vc4k/coc-k8s-summary-dashboard-alert-system-na-2?orgId=1",
    "13_NA_cluster_info_3": "http://10.11.67.29:3000/d/iBqceD5Vk/coc-k8s-summary-dashboard-alert-system-na-3?orgId=1",
    "14_NA_cluster_info_4": "http://10.11.67.29:3000/d/lxRheD5Vz/coc-k8s-summary-dashboard-alert-system-na-4?orgId=1",
    "15_NA_cluster_info_5": "http://10.11.67.29:3000/d/OYNJ6v5Vz/coc-k8s-summary-dashboard-alert-system-na-5?orgId=1"


        }

        filename = f'{screenshots_path}/{bot}_{datetime.now().strftime("%Y%m%d_%H%M")}.png'
        url = urls.get(bot)

        if url: 

            if bot == "09_NA_storage_1" or bot == "10_NA_storage_2":
          
                sleep(25)
                driver.execute_script("document.body.style.zoom=0.80")
                
                sleep(45)
                driver.save_screenshot(filename)    
                driver.close()
                driver.quit()
                print('스토리지 캡')

            else:
                driver.get(url)
                sleep(25)
                driver.set_window_size(1920, 1080)
                driver.maximize_window()
                
                sleep(50)
                driver.execute_script("document.body.style.zoom=0.75")
                sleep(50)
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
        "01_NA_lb(a10)",
        "02_NA_fw_1",
		"03_NA_total_1",
        "04_NA_host_1",
        "05_NA_vm_1",
        "06_NA_database_1",
        "07_NA_mongo",
        "08_NA_netapp_info",
        "09_NA_storage_1",
        "10_NA_storage_2",
		"11_NA_cluster_info_1",
        "12_NA_cluster_info_2",
        "13_NA_cluster_info_3",
        "14_NA_cluster_info_4",
        "15_NA_cluster_info_5",
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
    gc.collect() 
  
    print("---------------------------end----------------------------")