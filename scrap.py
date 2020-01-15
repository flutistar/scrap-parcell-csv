from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
import os
import xlsxwriter 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


def getList(urls):
    # options = Options()
    
    # print(f'user-agent={userAgent}')
    chrome_options = webdriver.ChromeOptions()
    currentPath = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver.exe'
    driver = webdriver.Chrome(options=chrome_options, executable_path= currentPath)
    print('SSSSTTTTTAAAAARRRRRTTTTTT')
    for url in urls:
        print('==================================================')
        try:
            # url = "https://ge.ch/terextraitfoncier/rapport.aspx?commune=46&parcelle=5751"
            driver.get(url)
            time.sleep(4)
            if len(driver.find_elements_by_xpath("//div[@id='captchaContainer']")):
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox']/div[@class='recaptcha-checkbox-border']"))).click()
                driver.switch_to_default_content()
                WebDriverWait(driver, 150).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"span.recaptcha-checkbox.goog-inline-block.recaptcha-checkbox-unchecked.rc-anchor-checkbox.recaptcha-checkbox-checked")))
                time.sleep(70)
            else:
                print('no capthcha')
            table_rows1 = driver.find_elements_by_xpath("//form[@id='reportForm']/table[2]/tbody/tr")
            if len(table_rows1):
                commune = driver.find_element_by_xpath("//form[@id='reportForm']/table[2]/tbody/tr[1]/td[2]").text
                immeuble = driver.find_element_by_xpath("//form[@id='reportForm']/table[2]/tbody/tr[2]/td[2]/b").text
                type_val = driver.find_element_by_xpath("//form[@id='reportForm']/table[2]/tbody/tr[2]/td[3]/b").text
                surface = driver.find_element_by_xpath("//form[@id='reportForm']/table[2]/tbody/tr[2]/td[4]/b").text
                print(commune, immeuble, type_val, surface)
            table_rows2 = driver.find_elements_by_xpath("//form[@id='reportForm']/table[4]/tbody/tr")
            if len(table_rows2):
                for row in table_rows2:
                    dst_flag = 0
                    adrs_flag = 0
                    cells = row.find_elements_by_tag_name("td")
                    for cell in cells:
                        if cell.text == 'Destination:':
                            dst_flag = 1
                            continue
                        elif cell.text == 'Adresse(s):':
                            adrs_flag = 1
                            continue
                        if dst_flag == 1:
                            print(cell.text)
                            dst_flag = 0
                        if adrs_flag == 1:
                            print(cell.text)
                            adrs_flag = 0
            table_rows3 = driver.find_elements_by_xpath("//form[@id='reportForm']/table[6]/tbody/tr")
            if len(table_rows3):
                for row in table_rows3:
                    cells = row.find_elements_by_tag_name("td")
                    for cell in cells:
                        if cell.text.strip() != '':
                            print(cell.text.strip())
        except Exception as ex:
            pass
            print("passed: ", ex, "    ", url)
    driver.quit()
