import json

'''
#Save data using this
with open("data_file.json", "w") as write_file:
    json.dump(data, write_file, indent=4)
'''

with open("data.json", "r") as read_file:
    data = json.load(read_file)

print(type(data))
print(data)
