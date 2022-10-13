#from urllib import request
import requests
import sys


headers = {'Content-Type': 'application/json'}

text = 'Hello to you. How is the weather in New York mate? speaker selection via browser was removed from webRTC app'


r = requests.post(url='http://13.210.49.59:8000/predict', json={'text': text}, timeout=3.0)
response_list = r.json()['forecast']



for question in response_list:
    print(question)
    print(' ')
    