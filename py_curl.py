#from urllib import request
import requests


headers = {'Content-Type': 'application/json'}

text = 'Hello to you. How is the weather in New York mate? speaker selection via browser was removed from webRTC app'

r = requests.post(url='http://35.161.43.90:8000/predict', json={'text': text})


response_list = r.json()['forecast']

for question in response_list:
    print(question)
    print(' ')
    