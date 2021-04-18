import requests
import json

URL ='https://sm.ms/api/v2/upload'
TOKEN = 'mEFip38PSWJICQDTnUYVzu9RSpOjPgbn'
APITYPE	= 'imgur'


def uploadImage(filePath):
    headers = {'Authorization': TOKEN}
    files = {'smfile': open(filePath, 'rb')}
    res = requests.post(URL, files=files, headers=headers, verify=False)
    print(json.loads(res.content.decode()))
    data = json.loads(res.content.decode())
    return data['data']['url']


if __name__ == '__main__':
    uploadImage(r'..\image\test1.png')

