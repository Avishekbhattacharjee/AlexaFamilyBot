from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from telethon import events
from urllib.parse import quote_plus
from urllib.error import HTTPError
from time import sleep
import asyncio
import os
import random
from haruka import GOOGLE_CHROME_BIN, CHROME_DRIVER
from haruka.events import register
import os
import time
import asyncio
import random
import asyncio
import shutil
from bs4 import BeautifulSoup
import re
from time import sleep
from html import unescape
from re import findall
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote_plus
from urllib.error import HTTPError
from telethon import events

CARBONLANG = "en"

@register(pattern="^/carbon (.*)")
async def carbon_api(e):
    """ A Wrapper for carbon.now.sh """
    jj = "`Processing..`"
    gg = await e.reply(jj)
    CARBON = 'https://carbon.now.sh/?bg=rgba(239%2C40%2C44%2C1)&t=one-light&wt=none&l=application%2Ftypescript&ds=true&dsyoff=20px&dsblur=68px&wc=true&wa=true&pv=56px&ph=56px&ln=false&fl=1&fm=Hack&fs=14px&lh=143%25&si=false&es=2x&wm=false&code={code}'
    global CARBONLANG
    code = e.pattern_match.group(1)
    await gg.edit("`Processing..\n25%`")
    os.chdir("./")
    if os.path.isfile("./carbon.png"):
       os.remove("./carbon.png")
    url = CARBON.format(code=code, lang=CARBONLANG)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    prefs = {'download.default_directory': './'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER,
                              options=chrome_options)
    driver.get(url)
    await gg.edit("`Processing..\n50%`")
    download_path = './'
    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_path
        }
    }
    command_result = driver.execute("send_command", params)
    driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
    await gg.edit("`Processing..\n75%`")
    while not os.path.isfile("./carbon.png"):
          await asyncio.sleep(1)
    await gg.edit("`Processing..\n100%`")
    file = './carbon.png'
    await e.edit("`Uploading..`")
    await e.client.send_file(
        e.chat_id,
        file,
        caption="Made using [Carbon](https://carbon.now.sh/about/),\
        \na project by [Dawn Labs](https://dawnlabs.io/)",
        force_document=True)
    os.remove('./carbon.png')
    driver.quit()

__help__ = """
 - /carbon <text>: Beautifies your text and enwraps inside a terminal image [ENGLISH ONLY]
"""

__mod_name__ = "Carbon"
