import requests

result=requests.post("http://127.0.0.1:9911/translate",json={"q":"你好啊我的朋友","source":"zh","target":"en"})
print(result.json())