from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import  time



def instagram_login(username,password):
    firefox_binary_path = "firefox/firefox.exe"
    geckodriver_path = "geckodriver.exe"

    firefox_options=Options()
    firefox_options.binary_location = firefox_binary_path

    service = Service(executable_path=geckodriver_path,log_path=None)
    driver = webdriver.Firefox(service=service, options=firefox_options)



    try:
        driver.get("https:/www.instagram.com/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(10)
        driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(5)
        driver.find_element(By.XPATH, "//span[contains(text(),'Request')]").click()
        time.sleep(5)
        if driver.find_element(By.XPATH, "//div[@style= 'opacity: 1;']"):
            driver.find_element(By.XPATH, "//div[@style= 'opacity: 1;']").click()
            time.sleep(5)
            if driver.find_element(By.XPATH, "//ul//li//div[contains(text(), 'Kabul Et')]"):
                driver.find_element(By.XPATH, "//ul//li//div[contains(text(), 'Kabul Et')]").click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[@role='textbox'][@aria-label ='Mesaj Gönder']").send_keys("Merhaba")
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[contains(text(),'Send')]").click()
    except Exception as e:
        print(f"Hata Oluştu : {e}")

    finally:
        print("Bitti")
        #driver.quit()

if __name__ == "__main__":
    username = ""
    password = ""
    instagram_login(username,password)
