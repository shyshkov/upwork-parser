import time

from selenium.webdriver.common.by import By
from webdriver.browser import ChromeDriver

if __name__ == "__main__":
    b = ChromeDriver()
    b.driver.get("https://www.upwork.com/nx/find-work/")
    b.login_upwork()
    time.sleep(5)
    b.parse_jobs()

    time.sleep(999)







# import undetected_chromedriver as uc

# if __name__ == '__main__':
    
#     driver.get('https://nowsecure.nl')
#     driver.get("https://www.upwork.com/nx/find-work/")
#     time.sleep(5)
#     element = driver.find_element(By.XPATH, "//input[@id='login_username']")
#     time.sleep(2)
#     element.send_keys('Funnymanzona@gmail.com')
#     driver.find_element(By.XPATH, "//button[@id='login_password_continue']").click()
#     time.sleep(5)
#     element = driver.find_element(By.XPATH, "//input[@id='login_password']")
#     time.sleep(2)
#     element.send_keys("QwertY!2345")
#     driver.find_element(By.XPATH, '//button[@button-role="continue"]').click()
#     time.sleep(99999)
    
    