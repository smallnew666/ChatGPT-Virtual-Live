ChatGPT-Virtual-Live
====================

项目简介
----

ChatGPT-Virtual-Live 是一个基于 Python 的虚拟主播直播助手，可以通过 blivedm 接口和监听程序获取 B 站、抖音弹幕信息，并将弹幕信息传输给 ChatGPT 进行语义理解和回复，最后将 vtuber 的说话画面推送给直播软件。项目的目标是为虚拟主播提供更加智能、丰富的直播体验，提升观众的互动感和沉浸感。

该项目基于开源项目 blivedm 和 DouyinBarrageGrab，感谢开源社区的贡献和支持。

功能特性
----

*   支持获取 B 站直播间、抖音直播间的弹幕信息
    
*   支持将弹幕信息传输给 ChatGPT 进行语义理解和回复
    
*   支持通过 Edge TTS 合成语音，并将语音推送给虚拟主播
    
*   支持推送虚拟主播的说话画面给直播软件
    

系统架构
----

系统主要分为以下几个模块：

*   弹幕获取模块：通过 blivedm 和 DouyinBarrageGrab 获取直播间弹幕信息，并将信息传输给语义理解模块。
    
*   语义理解模块：通过 ChatGPT 对弹幕信息进行语义理解和回复，将回复信息传输给语音合成模块。
    
*   语音合成模块：通过 Edge TTS 将回复信息合成语音，并将语音推送给虚拟主播vtuber。
    
*   画面推送模块：通过obs将虚拟主播的说话画面推送至直播软件。
    

使用方法
----

1.  下载代码并安装依赖：
    
    ```
    git clone https://github.com/smallnew666/ChatGPT-Virtual-Live.git 
    cd ChatGPT-Virtual-Live 
    pip install -r requirements.txt
    ```
2.  配置参数：
    
    在 `config.py` 文件中配置以下参数：
    

*   `BILI_ROOM_ID`：B 站直播间的房间号
    
*   `CHATGPT_ENDPOINT`：ChatGPT 服务器的 API 地址
    
    

4.  运行程序：
    
    ```
    python bilibili.py
    ```
注意事项
----

*   本项目仅供学习和研究使用，不得用于商业用途。
    
*   请遵守 B 站、抖音等平台的使用规范，不得用于违法或有害活动。


获取更详细教程，欢迎加入知识星球，里面包括免费api key分享，chatgpt教程等相关知识
----

![2023-04-17 17 58](https://user-images.githubusercontent.com/24582880/233049472-8a731396-933a-4401-a773-f0ed58cc7b13.jpg)

