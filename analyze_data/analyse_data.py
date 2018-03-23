import json

data = json.load(open('data.txt', encoding='utf8'))

print(data['offers']["0"])
