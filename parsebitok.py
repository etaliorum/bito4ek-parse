import json
import re

with open("tests/result.json", "r", encoding="utf8") as read_file:
    data = json.load(read_file)

bit_locks = {'bito4ki': []}


def parse_ITLocker():
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
                gen_dict = {'zion': zion_number,
                            'password': password,
                            'recovery': recovery_key}

                if check_coincidences(gen_dict) == 0:
                    update_dictionary(gen_dict)

            except IndexError:
                print('Not Found! Zion:', zion_number)

        count += 1


def check_coincidences(l_dict):
    status = 0
    list_blocks = bit_locks['bito4ki']
    for dict_l in list_blocks:
        if dict_l.get('zion') == l_dict.get('zion'):
            status += 1
    return status


def update_dictionary(l_dict):
    bit_locks['bito4ki'].append(l_dict)


parse_ITLocker()
print(len(bit_locks['bito4ki']))

with open("tests/result-1.json", "w") as outfile:
    json.dump(bit_locks, outfile)
