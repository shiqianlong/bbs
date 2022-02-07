# -*- coding: utf-8 -*-
# FileName  : cmsapi_test.py
# Author    : shiqianlong
import requests

headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0NDIyMjY2MCwianRpIjoiZWUxZTBjNjgtZGFhZi00ODQ5LThiNWMtMDkzZGM0NGIxNTgzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im85VlVMekRZZzd5ZmRvUVlvQVNvZnMiLCJuYmYiOjE2NDQyMjI2NjAsImV4cCI6MTY0NDIyMzU2MH0.fbMYEf88DHsyGwtKDIWnxH3wqyNeJezjOSpl-xr9ZWU'
}
res = requests.get('http://127.0.0.1:5000/cmsapi', headers=headers)
print(res.text)
# {
#   "code": 200,
#   "data": {
#     "identity": "o9VULzDYg7yfdoQYoASofs" #这个就是user.id
#   },
#   "message": "success"
# }
