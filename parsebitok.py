import json


with open("tests.json", "r") as read_file:
    data = json.load(read_file)

list_messages = data["messages"]
count = 0
for i in list_messages:
    if i.get("from") == "ITLocker":
        prev_id = list_messages[count - 1]["text"]
        print(prev_id[1])
    count += 1