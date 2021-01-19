import json

with open("tests/result.json", "r", encoding="utf8") as read_file:
    data = json.load(read_file)

bitloks = {}

def parse_itlocker():
    list_messages = data["messages"]
    count = 0
    for i in list_messages:
        try:
            if i.get("from") == "ITLocker":
                zion_number = list_messages[count - 1]["text"]
                password, recovery_key = list_messages[count]["text"].split("+")
                update_dictionary(zion_number[1].replace(' ',''), password, recovery_key)
            count += 1
        except Exception:
            print("Text Not found")

def update_dictionary(zion, passwod, recovery_key):
    bitloks["Zion"] = zion
    bitloks["Password"] = passwod
    bitloks["Recovery"] = recovery_key

parse_itlocker()

with open("tests/result-1.json", "w") as outfile:
    json.dump(bitloks, outfile)
