import csv,time,sys,signal
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import random
from tkinter import *
import pygame
import openai
from gtts import gTTS
import subprocess
from collections import deque
import asyncio
import json
import requests


class wechatlive():

    def __init__(self):
        self.barrageList = {}
        self.cookie_string = input("请输入你的cookie: ")
        #self.cookie_string = 'promotewebsessionid=; sessionid=BgAAzr%2F%2FPx3Y80AxrWDWBpOOVnKoe%2Bg%2BrbeazJB8ndc1Lw01DiiiAO%2Fet56H%2BJAGTt5LHg57nCKCzQT9rByYJ639Hw%3D%3D; wxuin=1728252584'
    def Connect(self):#连接
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("window-size=10,10")
        #chrome_options.add_argument("--headless")  # 隐藏UI界面
        # chromedriver的绝对路径（需下载和chrome版本一致http://chromedriver.storage.googleapis.com/index.html）
        driver_path = r'C:\Users\Administrator\Downloads\chromedriver_win32 (1)\chromedriver.exe'
        # 初始化一个driver，并且指定chromedriver的路径
        driver = webdriver.Chrome(executable_path=driver_path,options = chrome_options)
        driver.get("https://channels.weixin.qq.com/platform/login")
         # 设置等待条件：找到登录页
        input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="finder-page"]'))
        )
        print("加载cookie")
        for i in range(10, 0, -1):
            time.sleep(0.5)
            percent_complete = (10 - i) * 10
            print(f"{percent_complete}%")
        cookie_list = self.cookie_string.split(";")
        for cookie in cookie_list:
            cookies = []
            name, value = cookie.split("=",maxsplit=1)
            cookies = ({
                'name': name.lstrip(),
                'value': value
            })
            cookie_dict = {
                'domain': 'channels.weixin.qq.com',
                'name': cookies.get('name'),
                'value': cookies.get('value'),
                #"expires": cookie.get('value'),
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'SameSite':None,
                'Secure': True}
            driver.add_cookie(cookie_dict)
        driver.get('https://channels.weixin.qq.com/platform/live/liveBuild')
        # 设置等待条件：找到直播页面
        input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="vue-recycle-scroller__item-wrapper"]'))
        )
        last_data_id = None
        last_barrage = None
        while True:  # 无限循环，伪监听
            time.sleep(1)  # 等待1秒加载
            chat_room_list = driver.find_element(By.XPATH, '//*[@class="vue-recycle-scroller__item-wrapper"]')
            chat_msgs = chat_room_list.find_elements(By.XPATH, '//*[@class="vue-recycle-scroller__item-view"]')

            new_chat_msgs = []
            
            if last_data_id:
                for chat_msg in chat_msgs:
                    if chat_msg.find_element(By.XPATH, './/div[@data-index]').get_attribute('data-index') == last_data_id:
                        new_chat_msgs = chat_msgs[chat_msgs.index(chat_msg) + 1:]
                        break
            else:
                new_chat_msgs = chat_msgs
                
            for chat_msg in new_chat_msgs:
                try:
                    content = {} # 初始化弹幕内容字典
                    # 尝试是否为消息弹幕
                    try:
                        #content["username"] = chat_msg.find_element(By.CLASS_NAME, "message-username-desc").text
                        content["msg"] = chat_msg.find_element(By.CLASS_NAME, "message-content").text
                    except:
                        pass
                    last_barrage = content
                except:
                    continue

            if new_chat_msgs:  
                last_data_id = new_chat_msgs[-1].find_element(By.XPATH, './/div[@data-index]').get_attribute('data-index')
                text= last_barrage['msg']
                openai.api_key = ""
                url = "https://api.openai.com/v1/engines/davinci-codex/completions"
                messages =  [ {"role": "system", "content": "你是虚拟主播小雨酱，你会对用户的输入做出可爱的回应，并对你回复的观众施加可爱魔法，回答字数不要超过100字"},{"role": "user", "content": text}]

                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                answer = str(response['choices'][0]['message']['content'])
                print(answer)
                #self.putvoice(answer)
    #def putvoice(answer):
    # 设置要合成的文本
                #生成TTS语音
                command = f'edge-tts --voice zh-CN-XiaoyiNeural --text "{answer}" --write-media output.mp3'  # 将 AI 生成的文本传递给 edge-tts 命令
                subprocess.run(command, shell=True)  # 执行命令行指令
                # 初始化 Pygame
                pygame.mixer.init()
                # 加载语音文件
                pygame.mixer.music.load("output.mp3")
                # 播放语音
                pygame.mixer.music.play()
                # 等待语音播放结束
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                # 退出临时语音文件
                pygame.mixer.quit()
            


def QuitAndSave(signum, frame):#监听退出信号
    print ('catched singal: %d' % signum)
    sys.exit(0)

if __name__ == '__main__':#执行层
    #信号监听
    signal.signal(signal.SIGTERM, QuitAndSave)
    signal.signal(signal.SIGINT, QuitAndSave)
    weobj = wechatlive()
    weobj.Connect()
