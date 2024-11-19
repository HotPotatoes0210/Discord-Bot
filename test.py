import requests

url = 'https://api.simsimi.vn/v1/simtalk'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {'text': 'mày biết tao là ai không', 'lc': 'vn', 'key': ''}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    response_json = response.json()
    message = response_json.get('message', 'No message found')
    print("Message:", message)
else:
    print("Failed to get response. Status code:", response.status_code)
    print("Response:", response.text)