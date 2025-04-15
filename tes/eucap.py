import os
import sys
import signal
import time
import requests
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options

from concurrent.futures import ThreadPoolExecutor
import threading

# 이미지 폴더 지정
screenshots_path = 'ScreenShots'

# 이미지 폴더 존재 유무 체크 (필요 시 생성)
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

# 스레드별로 구분되는 네임스페이스 제공
thread_local = threading.local()

# 웹페이지 로그인 제공
def login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath):
    # Grafana 로그인 페이지로 이동
    driver.get(url)
    sleep(100)
    driver.switch_to.default_content()
    driver.switch_to.parent_frame()

    try:
        driver.implicitly_wait(3)        
        # 고급 버튼 클릭
        driver.find_element('xpath', '//*[@id="details-button"]').click()
        sleep(1)

        # 이동 버튼 클릭
        driver.find_element('xpath', '//*[@id="proceed-link"]').click()
        sleep(10)

    except Exception as e:
        print(e)

    finally:
        print("Step 1, login")
        driver.implicitly_wait(3)           
        # UserID 입력
        username = driver.find_element('xpath', userid_xpath)                                            
        username.clear()
        username.send_keys(userid)
        sleep(3)

        print("Step 2, login")
        # Password 입력
        password = driver.find_element('xpath', passwd_xpath)
        password.clear()
        password.send_keys(passwd)
        sleep(3)

        print("Step 3, login")
        # Login 버튼 클릭
        driver.find_element('xpath', login_xpath).click()

        sleep(3)

# 웹드라이버 클래스와 로그인 함수를 사용한, 스레드별 웹페이지 띄우기
# 결과: 로그인 된 화면
def create_driver(bot):
    the_driver = getattr(thread_local, 'the_driver', None)
    if the_driver is None:

        # 웹드라이버 생성
        try:
            the_driver = Driver()
            setattr(thread_local, 'the_driver', the_driver)
        except Exception as e:
            print(e)
            pass

        # Special Initialization to login:
        try:
            driver = the_driver.driver
        except Exception as e:
            print(e)
            pass

        print("Step 1, create_driver")
        print(bot)
        sleep(30)
        if bot == "lb(a10)":
            # Login Info
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input' 
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button' 
            # Login        
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)
        elif bot == "fw_1":
            # Login Info
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button' 
            # Login        
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)
        elif bot == "total_1":
            # Login Info
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button' 
            # Login        
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)
        elif bot == "host_1":
            # Login Info
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'  
            # Login                
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)

        elif bot == "vm_1":
            # Login Info
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button' 
            # Login                
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)

        
        elif bot == "database_1":
            # Login Info
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button' 
            # Login                
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)

        elif bot == "mongo":
            # Login Info
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'  
            # Login                
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)

        # Grafana Dashboard 미완성
        elif bot == "netapp_info":
            # Login Info
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
            # Login                
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)
           
        elif bot == "storage_1":
            # Login Info            
            url = "https://10.7.0.231/"
            userid = 'spark'
            passwd = 'tmvkzm1!'
            userid_xpath='//*[@id="nwf-login-form"]/dl/dd[1]/input'
            passwd_xpath='//*[@id="nwf-login-form"]/dl/dd[2]/input'
            login_xpath='//*[@id="nwf-login-form"]/button'     
            # Login                    
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath) 
            # Login                
            
        elif bot == "cluster_info_1":
            # Login Info              
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
            # Login                    
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)   
        elif bot == "cluster_info_2":
            # Login Info              
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
            # Login                    
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)   
        elif bot == "cluster_info_3":
            # Login Info              
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
            # Login                    
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)   
        elif bot == "cluster_info_4":
            # Login Info              
            url = "http://10.11.67.29:3000/login"
            userid = 'readonly'
            passwd = 'readonly!23'
            userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
            passwd_xpath='//*[@id="current-password"]'
            login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
            # Login                    
            login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)   
        # elif bot == "zabbix_dash":
        #     # Login Info              
        #     url = "http://10.11.67.29:3000/login"
        #     userid = 'readonly'
        #     passwd = 'readonly!23'
        #     userid_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input'
        #     passwd_xpath='//*[@id="current-password"]'
        #     login_xpath='//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
        #     # Login                
        #     login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath)            

    return driver

def take_screenshot(bot):
    print("Step 1, take_screenshot")
    # 웹드라이버 생성
    try:
        driver = create_driver(bot)
    except KeyboardInterrupt:
        print('Caught keyboardinterrupt')
        pass
    print("Step 2, take_screenshot")   

    try:
        while True:
            try:
                print(f"Capturing the screens started at {datetime.now()}")
                print(f"It captures every 5 mins")
                print("Step 3, take_screenshot")

                start_time = time.time()

                # 최종(대시보드) 페이지 및 저장파일 이름 설정
                if bot == "total_1":
                    url = 'http://10.11.67.29:3000/d/MtWXiuFVz/eu-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1'
                    filename = screenshots_path + '/EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "lb(a10)":
                    url = 'http://10.11.67.29:3000/d/BfKKMwcVz/eutms-a10-resource-monitor?orgId=1'
                    filename = screenshots_path + '/LB(A10)_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "fw_1":
                    url = 'http://10.11.67.29:3000/d/HK5wzuFVk2/eutms-fw_resource-monitor?orgId=1'
                    filename = screenshots_path + '/FW_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'                    
                elif bot == "host_1":
                    url = 'http://10.11.67.29:3000/d/ZdXDq9F4k/eu-bm-and-netapp-resource?orgId=1&'
                    filename = screenshots_path + '/HOST_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "vm_1":        
                    url = 'http://10.11.67.29:3000/d/_us9CrK4z/eu-vm-resource?orgId=1'
                    filename = screenshots_path + '/VM_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "database_1":
                    url = "http://10.11.67.29:3000/d/t4xORuFVz/eu-prd-db-resource-usage-top-20?orgId=1"
                    filename = screenshots_path + '/DB_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "mongo":
                    url = "http://10.11.67.29:3000/d/y0-T77cVk/eu_mongodb?orgId=1"
                    filename = screenshots_path + '/mongo_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "netapp_info":
                    url = "http://10.11.67.29:3000/d/bhPMpo54k/eu-netapp-dash-board?orgId=1"
                    filename = screenshots_path + '/NETAPP_INFO_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "storage_1":
                    url = 'https://10.7.0.231/clusters/69010/explorer'
                    filename = screenshots_path + '/NPS1_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "cluster_info_1":
                    url = 'http://10.11.67.29:3000/d/k4uJRdc4z/coc-k8s-summary-dashboard-alert-system-eu-1?orgId=1'
                    filename = screenshots_path + '/ccs_k8s_EU_1_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "cluster_info_2":
                    url = 'http://10.11.67.29:3000/d/BBEbgOc4k/coc-k8s-summary-dashboard-alert-system-eu-2?orgId=1'
                    filename = screenshots_path + '/ccs_k8s_EU_2_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "cluster_info_3":
                    url = 'http://10.11.67.29:3000/d/6yD-Rdc4k/coc-k8s-summary-dashboard-alert-system-eu-3?orgId=1'
                    filename = screenshots_path + '/ccs_k8s_EU_3_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                elif bot == "cluster_info_4":
                    url = 'http://10.11.67.29:3000/d/niGBgO5Vz/coc-k8s-summary-dashboard-alert-system-eu-4?orgId=1'
                    filename = screenshots_path + '/ccs_k8s_EU_4_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'
                # elif bot == "zabbix_dash":
                #     url = 'http://10.11.67.29:3000/d/JVrr775Vk/eu-zabbix-dash-board?orgId=1&refresh=5m'
                #     filename = screenshots_path + '/zabbix_EU_1center_PRD_' + datetime.now().strftime('%Y%m%d_%H%M') + '.png'



                # end_time = time.time()
                # elapsed_time = end_time - start_time
                # # print(elapsed_time)   
                # with open('elapsed_time_{}.txt'.format(bot), 'w') as t:
                #     t.write('Total elapsed time of {}: {:.2f} sec'.format(bot, elapsed_time)) 
            
                try:
                    if bot=="lb(a10)":
                        driver.get(url)                 
                        sleep(180)                 
                        driver.set_window_size(1920,1080)
                        driver.maximize_window()
                        sleep(2)
                        driver.execute_script("document.body.style.zoom=0.58")
                        sleep(2)
                        sleep(180)     
                    elif bot=="total_1":
                        driver.get(url)                 
                        sleep(180)                 
                        driver.set_window_size(1920,1080)
                        driver.maximize_window()
                        sleep(2)
                        driver.execute_script("document.body.style.zoom=0.67")
                        sleep(2)

                    elif bot == "storage_1":
                # Login Info
                        sleep(50)
                        driver.get(url)                        
                        sleep(180)
                        driver.find_element('xpath','//*[@id="mainViewContainer"]/main/div/div/div[3]/div/performance-explorer/nwf-grid-params-controller/div[2]/div/div[2]/span').click()
                        sleep(50)                   
                        driver.set_window_size(1920,1080)
                        sleep(50)
                        driver.maximize_window()
                        sleep(50)
                        # driver.execute_script("document.body.style.transform='scale(0.75)
                        sleep(30)                           
 
                    elif bot=="database_1" :
    
                        driver.get(url)                 
                        sleep(180)                 
                        driver.set_window_size(1920,1080)
                        driver.maximize_window()
                        driver.execute_script("document.body.style.zoom=0.67")
                        sleep(2)
         
                    else:
                        driver.get(url)                 
                        sleep(180)                 
                        driver.set_window_size(1920,1080)
                        sleep(10)
                        driver.maximize_window()
                        sleep(10)
                        driver.execute_script("document.body.style.zoom=0.80")
                        sleep(2)
                except Exception as e:
                    print(e)
                    print("shit...")

                # 화면 캡처 수행
                try:
                    driver.save_screenshot(filename)
                except KeyboardInterrupt:
                    print('Caught keyboardinterrupt')
                    pass                
                        
                print("Step 4, take_screenshot")

            # 예외 처리
            except (KeyboardInterrupt, SystemExit):
                print("\nkeyboardinterrupt caught")
                print("\n... Program Stopped Manually!")
                exiting.set()
            break

    # 예외 처리
    except (KeyboardInterrupt, SystemExit):
        print("\nkeyboardinterrupt caught")
        print("\n... Program Stopped Manually!")
        exiting.set()

def process_screencapture():

    number_threads = 20
    
    # total2의 경우 LB가 포함되어 있음
    bots = [
        'lb(a10)',
        "fw_1",
        "total_1",
        "host_1",
        "vm_1",
        "database_1",
        "mongo",
        "netapp_info",
        "storage_1",
		"cluster_info_1",
        "cluster_info_2",
        "cluster_info_3",
        "cluster_info_4",
        # "zabbix_dash",
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

    # 스레드 네임스페이스 삭제
    # Quit the selenium drivers:
    del thread_local

    # 메모리 캐시 삭제
    import gc
    gc.collect() # a little extra insurance
