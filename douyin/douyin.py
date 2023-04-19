# -*- coding: utf-8 -*-
import asyncio
import random
from tkinter import *
import pygame
import openai
from gtts import gTTS
import subprocess
from collections import deque
import asyncio
import websockets
import json
import requests

async def get_data():
    async with websockets.connect('ws://127.0.0.1:8888',ping_interval =None) as websocket:
        while True:
        # 接收消息
            message = await websocket.recv()
            message =  json.loads(message,strict=False)
            if(message['Type']==1):
                msg =  json.loads(message['Data'],strict=False)
                #print(msg['Content'])
                text= msg['Content']
                openai.api_key = ""
                url = "https://api.openai.com/v1/engines/davinci-codex/completions"
                messages =  [ {"role": "system", "content": "你是虚拟主播初音酱，你会对用户的输入做出可爱的回应，并对你回复的观众施加可爱魔法，回答字数不要超过100字"},{"role": "user", "content": text}]

                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                answer = str(response['choices'][0]['message']['content'])
                print(answer)
                putvoice(answer)
                
            if(message['Type']==3):
                msg =  json.loads(message['Data'],strict=False)
                nickname = msg['User']['Nickname']
                answer = "欢迎"+nickname+"来到直播间"
                print(answer)
                #await putvoice(answer)
            if(message['Type']==5):
                msg =  json.loads(message['Data'],strict=False)
                nickname = msg['User']['Nickname']
                answer = "感谢"+nickname+"送到礼物"
                putvoice(answer)
        await asyncio.Future()  # run forever
def putvoice(answer):
# 设置要合成的文本
        text = answer
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
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(get_data())


	
