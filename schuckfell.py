#!/usr/bin/python3
# Made with ♥
import os
import time
import socket
import datetime
from selenium import webdriver


class SchuckFell:
    def __init__(self):
        self.chromedriver = webdriver.Chrome(f'{os.getcwd()}/chromedriver')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.gateway = f'{".".join(s.getsockname()[0].split(".")[:-1])}.1'  # Not the greatest - harcode last octet to 1
        print(self.gateway)
        s.close()

    def go(self, duration_minutes):
        start_time = time.time()
        print(start_time + (duration_minutes * 60))
        print(start_time)
        while start_time + (duration_minutes * 60) + time.time():
            self.chromedriver.get(f'http://{self.gateway}')
            username_field = self.chromedriver.find_element_by_id('UserName')
            username_field.clear()
            username_field.send_keys('admin')  # yup default gateway credentials
            password_field = self.chromedriver.find_element_by_id('Password')
            password_field.clear()
            password_field.send_keys('password')
            login_apply_button = self.chromedriver.find_element_by_css_selector('#mainpage > div > div:nth-child(3) > input')
            login_apply_button.click()
            print(f'{datetime.datetime.now()} :: Logged in!')
            time.sleep(5)
            self.chromedriver.get(f'http://{self.gateway}/?util_restart')
            time.sleep(5)
            restart_button = self.chromedriver.find_element_by_css_selector('#mainpage > div > div:nth-child(2) > input')
            restart_button.click()
            confirm_popup = self.chromedriver.switch_to_alert()
            print(f'{datetime.datetime.now()} :: {confirm_popup.text}')
            confirm_popup.accept()
            time.sleep(20)  # wait for 20 seconds for modem to power off
            # add ping here with requests module with timeout to verify that down instead of all these arbitrary sleeps
            time.sleep(120)
            self.chromedriver.delete_all_cookies()  # delete cookies so we can ensure we get login form instead of dealing with cookie expiration
        self.chromedriver.quit()


SchuckFell().go(30)
