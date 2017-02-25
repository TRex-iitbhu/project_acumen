import requests

id_ = input('bot id :')
reading = input('reading :')

url = 'http://localhost:8000/LDR/'+id_+'/'+reading+'/'

requests.post(url)
