import json
import re

with open("tests/result.json", "r", encoding="utf8") as read_file:
    data = json.load(read_file)

bitloks = {'bito4ki': []}
n_bitloks = {'bito4ki': []}

def parse_itlocker():
    list_messages = data["messages"]
    count = 0
    for massage in list_messages:
        if massage.get("from") == "ITLocker":
            prev_massage = list_messages[count - 1]["text"]

            try:
                if len(prev_massage) > 1:
                    zion_number = re.sub(r'\s', '', prev_massage[1])

                split_massage = re.split(r'\+', massage["text"])
                password, recovery_key = split_massage[0], split_massage[1]
                dict = {'zion': zion_number,
                        'password': password,
                        'recovery': recovery_key}
                update_dictionary(dict)
            except IndexError:
                print('Not Found! Zion:', zion_number)

        count += 1

def delete_considences():
    return 0;
#    for i in range(len(bitloks['bito4ki'])):
#        for j in range(1, len(bitloks['bito4ki']) - 1):
#            if bitloks['bito4ki'][i].get('zion') != bitloks['bito4ki'][j].get('zion'):
#                n_bitloks['bito4ki'].append({
#                    'zion': bitloks['bito4ki'][i].get('zion'),
#                    'password': bitloks['bito4ki'][i].get('password'),
#                    'recovery': bitloks['bito4ki'][i].get('recovery')})

def update_dictionary(dict):
    bitloks['bito4ki'].append(dict)

parse_itlocker()
delete_considences()
#print(bitloks)

with open("tests/result-1.json", "w") as outfile:
    json.dump(bitloks, outfile)
