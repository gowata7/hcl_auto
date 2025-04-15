import os
import time
from datetime import datetime
from time import sleep
from selenium import webdriver
from threading import Event
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ThreadPoolExecutor
import threading
from selenium.webdriver.common.action_chains import ActionChains

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

        
        sleep(5)     
    
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
    "common_jenifer": {
        "url": "http://10.11.65.167:7900/dashboard/realtimeAdmin",
        "userid":'ccsadmin',
        "passwd":'ccsadmin!00',
        "userid_xpath":'//*[@id="app"]/div/div[2]/div[1]/form/div[1]/div/input',
        "passwd_xpath":'//*[@id="app"]/div/div[2]/div[1]/form/div[2]/div/input',
        "login_xpath":'//*[@id="app"]/div/div[2]/div[1]/div[3]/div',
        
    },

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
        login_data = login_info.get("common_jenifer")
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
     
        aa="http://10.11.65.167:7900/dashboard/realtimeAdmin"
        
        urls = {
            "TMS_MAIN_":aa,
            "TMS_Gen1_":aa,
            "TMS_Gen2_":aa,
            "TMS_ETC_":aa,
            "TMS_SBS_VOICE_":aa,

        }

        filename = f'{screenshots_path}/Jennifer_{bot}_{datetime.now().strftime("%Y%m%d_%H%M")}.png'
        url = urls.get(bot)

        if url: 
                    driver.get(url)
                    sleep(15)
                    sleep(10)
                    tree_icon_xpath = '//*[@id="vue_app"]/div/div[1]/div[1]/div[1]/div/div/div'
                    element = driver.find_element('xpath', tree_icon_xpath)
                    action = ActionChains(driver)
                    action.move_to_element(element).click().perform()
                    
                    sleep(3)
                    if bot ==  "TMS_MAIN_":
                        dashboard_xpath='//*[@id="vue_app"]/div/div[1]/div[4]/div[2]/div[2]/div[1]/img'
                    elif bot == "TMS_Gen1_":
                        dashboard_xpath = '//*[@id="vue_app"]/div/div[1]/div[4]/div[2]/div[2]/div[2]/img'
                    elif bot == "TMS_Gen2_":
                        dashboard_xpath = '//*[@id="vue_app"]/div/div[1]/div[4]/div[2]/div[2]/div[5]/img'
                    elif bot == "TMS_ETC_":
                        dashboard_xpath = '//*[@id="vue_app"]/div/div[1]/div[4]/div[2]/div[2]/div[11]/img'
                    else:
                        dashboard_xpath = '//*[@id="vue_app"]/div/div[1]/div[4]/div[2]/div[2]/div[17]/img'

                    element = driver.find_element('xpath', dashboard_xpath)
                    action = ActionChains(driver)
                    action.move_to_element(element).click().perform()
                    sleep(3)
                    
                    tree_icon_xpath = '//*[@id="vue_app"]/div/div[1]/div[1]/div[1]/div/div/div'
                    element = driver.find_element('xpath', tree_icon_xpath)
                    action = ActionChains(driver)
                    action.move_to_element(element).click().perform()

                    sleep(50) 

                    driver.save_screenshot(filename)
                    sleep(15)
                    driver.close()
                    driver.quit()
        else: 
            print("fucking error")
            
        


       
        print("----"+bot+"캡처함수종료-----")
    # 예외 처리
    except Exception as e:
        print(f"Error occurred: {e}")
        print("\n... erro!!!!!!!!!!!!")
        return


def main_capture():

    number_threads = 10
    

    bots = [
    "TMS_MAIN_",
    "TMS_Gen1_",
    "TMS_Gen2_",
    "TMS_ETC_",
    "TMS_SBS_VOICE_",   
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

    # 메모리 캐시 삭제
    import gc
    gc.collect() # a little extra insurance
    
    print("---------------------------end----------------------------")