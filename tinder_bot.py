from selenium import webdriver
from time import sleep
import random as rand 

from secrets import phonenmbr

class TinderBot():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(chrome_options=options)

    def login_phone(self):
        self.driver.get('https://tinder.com')

        sleep(12)
        phone_btn = self.driver.find_element_by_xpath("//*[contains(text(), 'Log in with phone number')]")
        phone_btn.click()

        sleep(2)
        phno_in = self.driver.find_element_by_xpath('//*[@name="phone_number"]') 
        phno_in.send_keys(phonenmbr)

        sleep(2)
        phno_send = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[1]/button')
        phno_send.click()

        sms_code = input("Enter the Code received by SMS:\n")
        sms_code = str(sms_code)

        for idx, val in enumerate(list(sms_code)):
            xpath = '//*[@id="modal-manager"]/div/div/div[1]/div[3]/input[%s]' %(idx+1)
            code_in = self.driver.find_element_by_xpath(xpath)
            code_in.send_keys(val)
        
        code_send = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[1]/button')
        code_send.click()

        sleep(2)

        popup_1 = self.driver.find_element_by_xpath("//*[contains(text(), 'Allow')]")
        popup_1.click()

        popup_2 = self.driver.find_element_by_xpath("//*[contains(text(), 'Enable')]")
        popup_2.click()

    def like(self):
        like_btn = self.driver.find_element_by_xpath('//*[@aria-label="Like"]')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//*[@aria-label="Nope"]')
        dislike_btn.click()
    
    def info(self):
        try:
            info = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/button')
            info.click()
        except Exception:
            info = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[2]/div[6]/button')
            info.click()

    def distance(self):
        self.info()
        distance = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]').text

        if 'kilometers' in distance:
            distance = int(distance.replace(' kilometers away', ''))
            return distance

        else: 
            distance = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[2]').text
            if 'kilometers' in distance:
                distance = int(distance.replace(' kilometers away', ''))
                return distance
            else: 
                distance = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[3]/div[2]').text
                if 'kilometers' in distance:
                    distance = int(distance.replace(' kilometers away', ''))
                    return distance
                else:
                    return 1000000

    def nearby(self):
        distance = self.distance()
        
        if distance < 100:
            return True
        else:
            return False

    def loading(self):
        try:
            loading = self.driver.find_element_by_xpath('//*[@aria-label="loading"]')
        except Exception:
            return
        
        if loading:
            print("no more people in vicinity. Stop autoswipping.")

    def auto_swipe(self):
        like_count = 0
        dislike_count = 0

        while True:
            sleep(rand.randint(1,10))
            print("Number of likes: ", like_count)
            print("Number of dislikes: ", dislike_count)
            try:
                if self.nearby():
                    self.like()
                    like_count += 1
                else: 
                    self.dislike()
                    dislike_count +=1

            except Exception:
                try:
                    self.close_popup()
                except Exception:
                    self.close_match()
                    try: 
                        self.loading()
                        break
                    except Exception:
                        print("Something unexpected happend. Stop autoswipping.")
                        break

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

# bot = TinderBot()
# bot.login()
