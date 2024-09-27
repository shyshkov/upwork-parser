import json
import os
import time
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc


class ChromeDriver:
    def __init__(self):
        self.driver = uc.Chrome(headless=False,use_subprocess=False)

    # def create_browser(self, local=False, load_cookie: bool = False):
    #     if self.driver:
    #         print("Create New FinderPrint")
    #         self.driver.quit()

    #     chrome_options = self.__set_option()

    #     if not local:
    #         self.__set_setting(chrome_options)

    #     else:
    #         self.__set_local(chrome_options)

        # if load_cookie:
        #     self.__load_cookies()
        
    # def __set_option(self) -> Options:
    #     '''
    #     Enabling standard browser options
    #     '''
    #     chrome_options = Options()
    #     chrome_options.add_argument("--lang=ru")
    #     # chrome_options.add_argument("--disable-web-security")
    #     chrome_options.add_argument("--no-sandbox")
    #     chrome_options.add_argument("--allow-running-insecure-content")
    #     chrome_options.add_argument("--disable-dev-shm-usage")
    #     chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
    #     chrome_options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    #     chrome_options.add_argument('--accept-language=ru')
    #     chrome_options.add_argument('--accept-encoding=gzip, deflate, br, zstd')
    #     chrome_options.add_argument('--referer=https://www.upwork.com/nx/create-profile/experience')
    #     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    #     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #     chrome_options.add_experimental_option('useAutomationExtension', False)
    #     return chrome_options
        
    # def __set_setting(self, chrome_options):
    #     '''
    #     Use for selenoid
    #     '''
    #     chrome_options.browser_version = '126.0'
    #     chrome_options.set_capability('selenoid:options', {
    #         "enableVNC": True,
    #         "enableVideo": False
    #     })

    #     self.driver = webdriver.Remote(
    #         command_executor='http://162.55.5.228:58387/wd/hub',
    #         options=chrome_options
    #     )

    #     return self
    
    # def __set_local(self, chrome_options):
    #     '''
    #     Use for local webdriver
    #     '''
    #     path = './chromedriver.exe'
    #     self.driver = webdriver.Chrome(service=Service(executable_path=path), options=chrome_options)

    #     return self

    # def __load_cookies(self, file_path='cookies.json'):
    #     '''
    #     Enables cookies for the Expedia.
    #     '''
    #     if os.path.exists(file_path):
    #         self.driver.get('https://www.expedia.com/login')
    #         with open(file_path, 'r') as file:
    #             cookies = json.load(file)
    #             for cookie in cookies:
    #                 self.driver.add_cookie(cookie)
    #         self.driver.refresh()

    #     return self

    # def save_cookies(self, file_path='cookies.json'):
    #     '''
    #     Save cookies
    #     '''
    #     cookies = self.driver.get_cookies()
    #     with open(file_path, 'w') as file:
    #         json.dump(cookies, file)

    #     return self
    
    def check_load_element(self, by: By, name_element: str, element: WebElement = None, time_wait: int = 10) -> Optional[WebElement]:
        '''
        Find one element to webdriver
        '''
        if element:
            search = element
        else:
            search = self.driver

        try:
            element = WebDriverWait(search, time_wait).until(
                EC.presence_of_element_located((by, name_element))
            )
            return element
        
        except:
            return None
        
    def check_load_elements(self, by: By, name_element: str, element: WebElement = None, time_wait: int = 10) -> Optional[List[WebElement]]:
        '''
        Find many elements to webdriver
        '''
        if element:
            search = element
        else:
            search = self.driver

        try:
            elements = WebDriverWait(search, time_wait).until(
                EC.presence_of_all_elements_located((by, name_element))
            )
            return elements
        
        except:
            return None

    def login_upwork(self):
        login_elem = self.check_load_element(By.XPATH, "//input[@id='login_username']")
        if login_elem:
            login_elem.send_keys('Funnymanzona@gmail.com')

        continue_button = self.check_load_element(By.XPATH, "//button[@id='login_password_continue']")
        if continue_button:
            continue_button.click()
        time.sleep(2)
        password_element = self.check_load_element(By.XPATH, "//input[@id='login_password']")
        if password_element:
            password_element.send_keys('QwertY!2345')

        login_button = self.check_load_element(By.XPATH, '//button[@button-role="continue"]')
        if login_button:
            login_button.click()

    def parse_jobs(self):
        os.makedirs('./jobs/', exist_ok=True) 
        page = 1
        find_param = 'devops'
        while True:
            self.driver.get(f"https://www.upwork.com/nx/search/jobs/?nbs=1&q={find_param}&page={page}&per_page=50")
            article = self.check_load_elements(By.XPATH, '//article')    
            for index, job in enumerate(article):
                try:
                    title = self.check_load_element(By.XPATH, ".//a", element=job)
                    self.driver.execute_script("arguments[0].click();", title)

                    job_window = self.check_load_element(By.XPATH, "//div[@data-ev-sublocation='jobdetails']")
                    if not job_window:
                        continue

                    title_job = self.check_load_element(By.XPATH, ".//h4", element=job_window, time_wait=2)
                    location = self.check_load_element(By.XPATH, ".//div[@data-test='LocationLabel']", element=job_window, time_wait=2)
                    description = self.check_load_element(By.XPATH, ".//div[@data-test='Description']", element=job_window, time_wait=2)
                    feature = self.check_load_element(By.XPATH, ".//section[@data-test='Features']", element=job_window, time_wait=2)
                    activity = self.check_load_element(By.XPATH, ".//section[@data-test='ClientActivity']", element=job_window, time_wait=2)
                    rating = self.check_load_element(By.XPATH, '//div[@data-testid="buyer-rating"]//div[@class="air3-rating-value-text"]', element=job_window) 
                    tags = self.check_load_elements(By.XPATH, ".//span[@slot='reference']", element=job_window, time_wait=3)

                    client_loc = self.check_load_element(By.XPATH, '//li[@data-qa="client-location"]', time_wait=2)
                    count_posted_jobs = self.check_load_element(By.XPATH, '//li[@data-qa="client-job-posting-stats"]', time_wait=2)
                    total_spent = self.check_load_element(By.XPATH, '//strong[@data-qa="client-spend"]', time_wait=2)
                    hourly_rate = self.check_load_element(By.XPATH, '//strong[@data-qa="client-hourly-rate"]', time_wait=2)
                    posted_job = self.check_load_element(By.XPATH, '//div[@data-test="PostedOn"]', time_wait=2)
                    time_parse = int(time.time())

                    close_button = self.check_load_element(By.XPATH, "//button[@data-test='slider-close-desktop']")

                    tag_list = []
                    if tags:
                        for tag in tags:
                            tag_list.append(tag.text)

                    json_saved = {
                        'link': title.get_attribute('href'),
                        'posting_job': posted_job.text if posted_job else None,
                        'title_job': title_job.text if title_job else None,
                        'location': location.text if location else None,
                        'description': description.text if description else None,
                        'feature': feature.text if feature else None,
                        'activity': activity.text if activity else None,
                        'tags': tag_list,
                        'client': {
                            'location': client_loc.text if client_loc else None,
                            'count_posted_jobs': count_posted_jobs.text if count_posted_jobs else None,
                            'total_spent': total_spent.text if total_spent else None,
                            'hourly_rate': hourly_rate.text if hourly_rate else None,
                            'rating': rating.text if rating else None
                        },
                        'time_parsing': time_parse
                    }
                    

                    if close_button:
                        self.driver.execute_script("arguments[0].click();", close_button)
                    
                    time.sleep(2)

                    print(json_saved)
                    with open(f"./jobs/page_{page}_job_{index}.json", 'w', encoding='utf8') as file:
                        json.dump(json_saved, file, ensure_ascii=False, indent=4)
                
                except Exception as e:
                    print(f"ERROR: {e}")

                    close_button = self.check_load_element(By.XPATH, "//button[@data-test='slider-close-desktop']")
                    if close_button:
                        close_button.click()

            page += 1
            
            #     title = self.check_load_element(By.XPATH, ".//a", element=job)
            #     job_infos = self.check_load_element(By.XPATH, ".//ul[@data-test='JobInfoClient']", element=job)
            #     job_info = self.check_load_element(By.XPATH, ".//ul[@data-test='JobInfo']", element=job)
            #     description = self.check_load_element(By.XPATH, ".//div[contains(@data-test, 'JobDescription')]", element=job)
            #     attribute = self.check_load_element(By.XPATH, ".//div[contains(@data-test, 'JobAttrs')]", element=job)
                
            #     json_saved = {
            #         'title': title.text,
            #         'job_infos': job_infos.text.split('\n') if job_infos else None,
            #         'job_info': job_info.text.split('\n') if job_info else None,
            #         'description': description.text if description else None,
            #         'attribute': attribute.text.split('\n') if attribute else None,
            #     }
            #     print(json_saved)
            #     with open(f"./jobs/job_{index}_page{page}.json", 'w', encoding='utf8') as file:
            #         json.dump(json_saved, file, ensure_ascii=False, indent=4)


            # return