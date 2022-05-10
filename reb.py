#!/bin/python
from xml.etree import ElementTree as xml
from requests import get, post
from base64 import b64encode as b64
from time import sleep
import requests

ip = input("what's your ip range?, Press enter to use default, ip: 192.168.")
ip = "192.168.8.1" if ip == '' else "192.168." + ip.replace(" ","")


tokenheaders = {
       'Connection': 'close',
       'Host': ip,
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
       'X-Requested-With': 'XMLHttpRequest',
       '__RequestVerificationToken': '',
       'Accept': '*/*',
       'Accept-Language': 'en',
       'Accept-Encoding': 'gzip, deflate',
       'Referer': f'http://{ip}/html/index.html'
}

print('[info]  Trying to get a token....')

while 1:
   try:
      token = get('http://'+ip+'/api/webserver/token', headers=tokenheaders)
      if token.status_code == 200:
         print('[info]  Successfully obtained a token')
         break
      else:
         print("[error] Couldn't obtain a token something went wrong, Error code:", token.status_code, token.text)
         print("[info]  Trying one more time")
         sleep(2)

   except requests.exceptions.ConnectionError:
      print('[error] Connection unreachable is this true? trying again....')
      sleep(2)

token = xml.fromstring(token.text)
token = token[0].text


loginheaders = {
       'Connection': 'close',
       'Host': ip,
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
       'X-Requested-With': 'XMLHttpRequest',
       '__RequestVerificationToken': token,
       'Accept': '*/*',
       'Accept-Language': 'en',
       'Accept-Encoding': 'gzip, deflate',
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       'Referer': f'http://{ip}/html/home.html'
}

user  = input("what's your username?  (press enter for default) user: ")
user  = 'admin' if user.replace(' ','') == '' else user
passw = input("what's your password?  (press enter to use default) password: ")
passw = "admin" if passw.replace(' ','') == '' else passw
ENCpas= b64(passw.encode('ascii'))

print(f"\n[info]  Trying to sign in using {user} {passw}")

while 1:
   try:
      data = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><Username>{user}</Username><Password>{ENCpas.decode()}</Password></request>"""
      login = post('http://'+ip+'/api/user/login', headers=loginheaders, data=data)
      if login.status_code == 200 and "<response>OK</response>" in login.text:
         print('[info]  Successfully signed in!')
         break
      elif "100008" in login.text:
         print(f"[error] Couldn't signin username: {user} is wrong, Error code:", login.status_code, login.text)
         print("\n\n Please restart this script with correct username")
         exit(1)
      elif "108006" in login.text:
         print(f"[error] Couldn't signin password: {passw} is wrong, Error code:", login.status_code, login.text)
         print("\n\n Please restart this script with correct password")
         exit(1)
      elif "108007" in login.text:
         print(f"[error] Couldn't signin Maximum tries reached try in 5 mins, Error code:", login.status_code, login.text)
         print("\n\n Please restart this script in 5 mins")
         exit(1)
      elif "125001" in login.text:
         print(f"[error] Couldn't signin token expired?, Error code:", login.status_code, login.text)
         print("\n\n Please restart this script")
         exit(1)
      else:
         print("[error] Couldn't signin something went wrong, Error code:", login.status_code, login.text)
         print("[info]  Trying one more time")
         sleep(2)
   except requests.exceptions.ConnectionError:
      print('[error] Connection unreachable is this true? trying again....')
      sleep(2)

rebootheaders = {
       'Connection': 'close',
       'Host': ip,
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
       'X-Requested-With': 'XMLHttpRequest',
       '__RequestVerificationToken': token,
       'Accept': '*/*',
       'Accept-Language': 'en',
       'Accept-Encoding': 'gzip, deflate',
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       'Referer': f'http://{ip}/html/reboot.html'
}

print(f"\n[info]  Attempting to request a restart....")


while 1:
   try:
      data = """<?xml version=\"1.0\" encoding=\"UTF-8\"?><request><Control>1</Control></request>"""
      reboot = post('http://'+ip+'/api/device/control', headers=rebootheaders, data=data)
      if reboot.status_code == 200 and "<response>OK</response>" in reboot.text:
         print('[info]  Successfully requested a reboot!')
         print('[info]  Your router should restart shortly!')
         exit(0)
      elif "100003" in reboot.text or  "100002" in reboot.text:
         print(f"[error] Request refused token expired?, Error code:", reboot.status_code, reboot.text)
         print("\n\n Please restart this script")
         exit(1)
      else:
         print("[error] Request refused something went wrong, Error code:", reboot.status_code, reboot.text)
         print("[info]  Trying one more time")
         sleep(2)

   except requests.exceptions.ConnectionError:
      print('[error] Connection unreachable is this true? trying again....')
      sleep(2)

