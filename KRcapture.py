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
        sleep(30)
        self.driver.maximize_window()

    def __del__(self):
        self.driver.quit() # clean up driver when we are cleaned up


thread_local = threading.local()

# 웹페이지 로그인 제공


def login(driver, url, userid, userid_xpath, passwd, passwd_xpath, login_xpath):
    try:
        # Grafana 로그인 페이지로 이동
        driver.get(url)
        sleep(30) 
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

        
        sleep(30)         
    
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
    "01_KR_network": {
        "url": "http://10.7.19.118:3000/login",
        "userid": "monitor",
        "passwd": "P@ssw0rd",
        "userid_xpath": '//*[@id="login-view"]/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="login-view"]/div/form/div[2]/div[2]/div/div/input',
        "login_xpath": '//*[@id="login-view"]/div/form/button'
    },
    "02_KR_network_2": {
        "url": "https://hubble-apne2-prd.platform.hcloud.io/grafana/login/generic_oauth",
        "userid": "cocop",
        "passwd": "cocop",
        "userid_xpath": '//*[@id="username"]',
        "passwd_xpath": '//*[@id="password"]',
        "login_xpath": '//*[@id="kc-form-login"]/button'
    },
    "03_KR_lb_a10": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "04_KR_lb_f5": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "05_KR_total_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "06_KR_total_2": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "07_KR_host_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "08_KR_host_1_new": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "09_KR_host_2": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "10_KR_vm_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "11_KR_vm_2": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "12_KR_database_1": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "13_KR_database_2": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "14_KR_netapp_nvme": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "15_KR_netapp_old_new_prd_bigdata": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "16_KR_netapp_stg": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "17_KR_storage_new_1": {
        "url": "https://10.7.0.231/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/dl/dd[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/dl/dd[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/button'
    },
    "18_KR_storage_new_2": {
        "url": "https://10.7.0.231/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/dl/dd[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/dl/dd[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/button'
    },
    "19_KR_storage_old_1": {
        "url": "https://10.7.0.231/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/dl/dd[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/dl/dd[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/button'
    },
    "20_KR_netapp_prd_2center": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "21_KR_netapp_manila_prd_2center": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "22_KR_netapp_stg_2center": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "23_KR_storage_2center_fas_03r02": {
        "url": "https://172.16.9.211/sysmgr/v4/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/div[1]/input', 
        "passwd_xpath": '//*[@id="nwf-login-form"]/div[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/div[3]/nwf-loading-button/button'
    },
    "24_KR_storage_2center_aff_03r02": {
        "url": "https://172.16.9.216/sysmgr/v4/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/div[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/div[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/div[3]/nwf-loading-button/button'
    },
    "25_KR_storage_2center_fas_03r03": {
        "url": "https://172.16.9.221/sysmgr/v4/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/div[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/div[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/div[3]/nwf-loading-button/button'
    },
    "26_KR_storage_2center_aff_03r03": {
        "url": "https://172.16.9.226/sysmgr/v4/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/div[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/div[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/div[3]/nwf-loading-button/button'
    },
    "27_KR_storage_2center_fas_03r04": {
        "url": "https://172.16.9.231/sysmgr/v4/",
        "userid": "spark",
        "passwd": "tmvkzm1!",
        "userid_xpath": '//*[@id="nwf-login-form"]/div[1]/input',
        "passwd_xpath": '//*[@id="nwf-login-form"]/div[2]/input',
        "login_xpath": '//*[@id="nwf-login-form"]/div[3]/nwf-loading-button/button'
    },
    "28_KR_k8s_cluster_1center_ccskr_rancher_prd": {
        "url": "https://hubble-apne2-prd.platform.hcloud.io/grafana/login/generic_oauth",
        "userid": "cocop",
        "passwd": "cocop",
        "userid_xpath": '//*[@id="username"]',
        "passwd_xpath": '//*[@id="password"]',
        "login_xpath": '//*[@id="kc-form-login"]/button'
    },
    "29_KR_k8s_cluster_1center_ccskr_devworks_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "30_KR_k8s_cluster_1center_ccskr_dkc2hpkr_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "31_KR_k8s_cluster_1center_ccskr_dkc2kpgkr_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "32_KR_k8s_cluster_1center_ccskr_dkc2kplkr_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "33_KR_k8s_cluster_1center_ccskr_svchub_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "34_KR_k8s_cluster_1center_ccskr_svchubcore_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "35_KR_k8s_cluster_1center_ccskr_svchubutil_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "36_KR_k8s_cluster_1center_kr_vdsp_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "37_KR_k8s_cluster_1center_ccskr_vtwin_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "38_KR_k8s_cluster_1center_ccskr_vtwin2_prd": {
        "url": "http://10.11.67.29:3000/login",
        "userid": "readonly",
        "passwd": "readonly!23",
        "userid_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/div[1]/div[2]/div/div/input',
        "passwd_xpath": '//*[@id="current-password"]',
        "login_xpath": '//*[@id="reactRoot"]/div/main/div[3]/div/div[2]/div/div/form/button'
    },
    "39_KR_k8s_cluster_2center_ccskr2_rancher_prd": {
        "url": "https://hubble-apne2-prd.platform.hcloud.io/grafana/login/generic_oauth",
        "userid": "cocop",
        "passwd": "cocop",
        "userid_xpath": '//*[@id="username"]',
        "passwd_xpath": '//*[@id="password"]',
        "login_xpath": '//*[@id="kc-form-login"]/button'
    },
    "40_KR_k8s_cluster_2center_ccs_prd": {
        "url": "https://hubble-apne2-prd.platform.hcloud.io/grafana/login/generic_oauth",
        "userid": "cocop",
        "passwd": "cocop",
        "userid_xpath": '//*[@id="username"]',
        "passwd_xpath": '//*[@id="password"]',
        "login_xpath": '//*[@id="kc-form-login"]/button'
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
    "01_KR_network": "http://10.7.19.118:3000/d/Ax-HFsa4z/yiwang-ccs-bordermoniteoring-keulraudeuunyeongsenteo?orgId=1&from=now-2d&to=now",
    "02_KR_network_2": "https://hubble-apne2-prd.platform.hcloud.io/grafana/d/RbJ9FxXnk/inteones-caryang-data-sms-hoeseon?orgId=13&from=now-2d&to=now",
    "03_KR_lb_a10": "http://10.11.67.29:3000/d/tdbzxsNnz1/kr-a10-3030-old-a10?orgId=1&from=now-2d&to=now",
    "04_KR_lb_f5": "http://10.11.67.29:3000/d/ixuLyos7k/kr-lb-f5?from=now-2d&to=now&orgId=1",
    "05_KR_total_1": "http://10.11.67.29:3000/d/-zbrCFr7g/kr-1senteo-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1&from=now-2d&to=now",
    "06_KR_total_2": "http://10.11.67.29:3000/d/9zxCEzp4k/kr-2senteo-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1",
    "07_KR_host_1": "http://10.11.67.29:3000/d/vGUN6GW4z/kr-1senteo-prd-old-bm-resources?orgId=1&from=now-30m&to=now",
    "08_KR_host_1_new": "http://10.11.67.29:3000/d/yo86eMWVz/kr-1senteo-prd-new-bm-resources?orgId=1&from=now-30m&to=now",
    "09_KR_host_2": "http://10.11.67.29:3000/d/U_asi7W4z/kr-2senteo-prd-bm-resources?orgId=1&from=now-30m&to=now",
    "10_KR_vm_1": "http://10.11.67.29:3000/d/yVNMjMZVk/kr-1senteo-prd-vm-resources?orgId=1&from=now-30m&to=now",
    "11_KR_vm_2": "http://10.11.67.29:3000/d/Jxvrz7Z4k/kr-2senteo-prd-vm-resources?orgId=1&from=now-30m&to=now",
    "12_KR_database_1": "http://10.11.67.29:3000/d/JU5R-_m4k/kr-1senteo-prd-db-resource-usage-top-20?orgId=1&from=now-6h&to=now",
    "13_KR_database_2": "http://10.11.67.29:3000/d/bxdzB_iVz/kr-2senteo-prd-db-resource-usage-top-20?orgId=1&from=now-6h&to=now",
    "14_KR_netapp_nvme": "http://10.11.67.29:3000/d/MWXLP7K4z1/kr-1center-netapp-nvme-dash-board?orgId=1",
    "15_KR_netapp_old_new_prd_bigdata": "http://10.11.67.29:3000/d/jhvYINK4z2/kr-1centor-old-prd-and-new-prd-big-data?orgId=1",
    "16_KR_netapp_stg": "http://10.11.67.29:3000/d/gHJ-NHK4k3/kr-1centor-stg-netapp-dash-board?orgId=1",
    "17_KR_storage_new_1": "https://10.7.0.231/clusters/53770/explorer",
    "18_KR_storage_new_2": "https://10.7.0.231/clusters/133326/explorer",
    "19_KR_storage_old_1": "https://10.7.0.231/clusters/15462/explorer",
    "20_KR_netapp_prd_2center": "http://10.11.67.29:3000/d/ytGbd1UVk/kr2-prd_netapp?orgId=1&refresh=1d",
    "21_KR_netapp_manila_prd_2center": "http://10.11.67.29:3000/d/IFrv6NWIk/kr-2center-netapp-prd-manila?orgId=1&refresh=1d",
    "22_KR_netapp_stg_2center": "http://10.11.67.29:3000/d/LIdYdJU4z/kr2_stg_netapp?orgId=1",
    "23_KR_storage_2center_fas_03r02": "https://172.16.9.211/sysmgr/v4/",
    "24_KR_storage_2center_aff_03r02": "https://172.16.9.216/sysmgr/v4/",
    "25_KR_storage_2center_fas_03r03": "https://172.16.9.221/sysmgr/v4/",
    "26_KR_storage_2center_aff_03r03": "https://172.16.9.226/sysmgr/v4/",
    "27_KR_storage_2center_fas_03r04": "https://172.16.9.231/sysmgr/v4/",
    "28_KR_k8s_cluster_1center_ccskr_rancher_prd": "https://hubble-apne2-prd.platform.hcloud.io/grafana/d/coBoVkG4z/kr-apne1-rancher-local?orgId=27",
    "29_KR_k8s_cluster_1center_ccskr_devworks_prd": "http://10.11.67.29:3000/d/1HihRd54k/coc-k8s-summary-dashboard-alert-system-kr1-kr_devworks_prd_cluster?orgId=1",
    "30_KR_k8s_cluster_1center_ccskr_dkc2hpkr_prd": "http://10.11.67.29:3000/d/oOYkgdc4z/coc-k8s-summary-dashboard-alert-system-kr1-dkc2-hpkr?orgId=1",
    "31_KR_k8s_cluster_1center_ccskr_dkc2kpgkr_prd": "http://10.11.67.29:3000/d/95RgRd54z/coc-k8s-summary-dashboard-alert-system-kr1-dkc2-kpg?orgId=1",
    "32_KR_k8s_cluster_1center_ccskr_dkc2kplkr_prd": "http://10.11.67.29:3000/d/q20rev5Vz/coc-k8s-summary-dashboard-alert-system-kr1-dkc2-kpl?orgId=1",
    "33_KR_k8s_cluster_1center_ccskr_svchub_prd": "http://10.11.67.29:3000/d/X0-SRdc4z/coc-k8s-summary-dashboard-alert-system-kr1-kr_svchub_prd_cluster?orgId=1",
    "34_KR_k8s_cluster_1center_ccskr_svchubcore_prd": "http://10.11.67.29:3000/d/Zx4vgdcVz/coc-k8s-summary-dashboard-alert-system-kr1-kr_svchubcore_prd_cluster?orgId=1",
    "35_KR_k8s_cluster_1center_ccskr_svchubutil_prd": "http://10.11.67.29:3000/d/KeocRd5Vz/coc-k8s-summary-dashboard-alert-system-kr1-kr_svchubutil_prd_cluster?orgId=1",
    "36_KR_k8s_cluster_1center_kr_vdsp_prd": "http://10.11.67.29:3000/d/Njzv9SZIk/coc-k8s-summary-dashboard-alert-system-krbig-vdsp-prd?orgId=1",
    "37_KR_k8s_cluster_1center_ccskr_vtwin_prd": "http://10.11.67.29:3000/d/Ig7ngd5Vk/coc-k8s-summary-dashboard-alert-system-kr1-kr_vtwin_prd_cluster?orgId=1",
    "38_KR_k8s_cluster_1center_ccskr_vtwin2_prd": "http://10.11.67.29:3000/d/8IhZgdcVz/coc-k8s-summary-dashboard-alert-system-kr1-kr_vtwin2_prd_cluster?orgId=1",
    "39_KR_k8s_cluster_2center_ccskr2_rancher_prd":'https://hubble-apne2-prd.platform.hcloud.io/grafana/d/GgRmDQ-4z/kr_apne2_rancher_cluster-prd?orgId=27',
    "40_KR_k8s_cluster_2center_ccs_prd":'https://hubble-apne2-prd.platform.hcloud.io/grafana/d/rBwSwVJVk/ccs_prd_cluster?orgId=27',
        }

        filename = f'{screenshots_path}/{bot}_{datetime.now().strftime("%Y%m%d_%H%M")}.png'
        url = urls.get(bot)

        if url: 

            if bot == "23_KR_storage_2center_fas_03r02" or bot == "24_KR_storage_2center_aff_03r02" or bot == "25_KR_storage_2center_fas_03r03" or bot == "26_KR_storage_2center_aff_03r03" or bot == "27_KR_storage_2center_fas_03r04":
                #driver.find_element('xpath','/html/body/app-root/ui-view/ui-view/topnav/div/ui-view/mainbody/nwf-mainbody/div/main/dashboard/div/div[2]/div[1]/div/cluster-capacity/div/div[2]/ngb-popover-window/div[2]/nwf-dismiss-button/button').click()          
                sleep(30)
                #driver.find_element('xpath','/html/body/app-root/ui-view/ui-view/topnav/div/ui-view/mainbody/nwf-mainbody/div/main/dashboard/div/div[3]/div/div/cluster-performance/perf-interval-selection/div/ngb-tabset/ul/li[3]/a').click()
                #sleep(15)
                driver.execute_script("document.body.style.zoom=0.80")
                sleep(30)
                
                driver.save_screenshot(filename)    
                driver.close()
                driver.quit()
                print('그냥캡')
                    

            else:
                    driver.get(url)
                    sleep(30)
                    sleep(15)
                    driver.set_window_size(1920, 1080)
                    driver.maximize_window()
                    sleep(30)
                    
                    driver.execute_script("document.body.style.zoom=0.80")
                    sleep(15)
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

    number_threads = 10
    

    bots = [
    "01_KR_network",
    "02_KR_network_2",
    "03_KR_lb_a10",
    "04_KR_lb_f5",
    "05_KR_total_1",
    "06_KR_total_2",
    "07_KR_host_1",
    "08_KR_host_1_new",
    "09_KR_host_2",
    "10_KR_vm_1",
    "11_KR_vm_2",
    "12_KR_database_1",
    "13_KR_database_2",
     "14_KR_netapp_nvme",
     "15_KR_netapp_old_new_prd_bigdata",
     "16_KR_netapp_stg",
    "17_KR_storage_new_1",
    "18_KR_storage_new_2",
    "19_KR_storage_old_1",
    "20_KR_netapp_prd_2center",
    "21_KR_netapp_manila_prd_2center",
     "22_KR_netapp_stg_2center",
    "23_KR_storage_2center_fas_03r02",
    "24_KR_storage_2center_aff_03r02",
    "25_KR_storage_2center_fas_03r03",
    "26_KR_storage_2center_aff_03r03",
    "27_KR_storage_2center_fas_03r04",
    "28_KR_k8s_cluster_1center_ccskr_rancher_prd",
    "29_KR_k8s_cluster_1center_ccskr_devworks_prd",
    "30_KR_k8s_cluster_1center_ccskr_dkc2hpkr_prd",
    "31_KR_k8s_cluster_1center_ccskr_dkc2kpgkr_prd",
    "32_KR_k8s_cluster_1center_ccskr_dkc2kplkr_prd",
    "33_KR_k8s_cluster_1center_ccskr_svchub_prd",
    "34_KR_k8s_cluster_1center_ccskr_svchubcore_prd",
    "35_KR_k8s_cluster_1center_ccskr_svchubutil_prd",
    "36_KR_k8s_cluster_1center_kr_vdsp_prd",
    "37_KR_k8s_cluster_1center_ccskr_vtwin_prd",
    "38_KR_k8s_cluster_1center_ccskr_vtwin2_prd",
    "39_KR_k8s_cluster_2center_ccskr2_rancher_prd",
    "40_KR_k8s_cluster_2center_ccs_prd"
    ]   

    
    with ThreadPoolExecutor(max_workers=number_threads) as pool:
        try:
            pool.map(capture_screen, bots)
        except KeyboardInterrupt:
            print('Caught keyboardinterrupt')
            pass

if __name__ == "__main__":##main되는 직접호출을위해
    try:
        main_capture()
    except KeyboardInterrupt:
        print('Caught keyboardinterrupt')
        pass

    
    import gc
    gc.collect() 
    
    print("---------------------------end----------------------------")