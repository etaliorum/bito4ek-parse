import json
import re

bit_locks = {'bito4ki': []}


def position_dict(l_list):
    for item in range(len(l_list)):
        if type(l_list[item]) == dict:
            return item


def get_atr_texts(list_messages):
    list_m = []
    for massage in list_messages:
        if isinstance(massage['text'], list):
            if massage['text'][position_dict(massage['text'])].get('text') == '/zion':
                list_m.append(massage['text'])
    return list_m


def update_dictionary(l_dict):
    bit_locks['bito4ki'].append(l_dict)


def parse_without_ITLocker():
    with open("tests/result-without-itlocker.json", "r", encoding="utf8") as read_file:
        data = json.load(read_file)
    lists_texts = get_atr_texts(data["messages"])

    for item in lists_texts:
        for string_l in item:
            if type(string_l) != dict:
                zion = re.findall(r'[lL]\-\d{3}|\b\d{3}\b', string_l)
                password = re.findall(r'\d{7}', string_l)
                recovery_key = re.findall(r'\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}-\d{6}', string_l)

                zion = ''.join(zion)
                password = ''.join(password)
                recovery_key = ''.join(recovery_key)

                gen_dict = {'zion': zion,
                            'password': password,
                            'recovery': recovery_key}
                update_dictionary(gen_dict)


def parse_ITLocker():
    with open("tests/result.json", "r", encoding="utf8") as read_file:
        data = json.load(read_file)

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


if __name__ == "__main__":
    parse_ITLocker()
    parse_without_ITLocker()

    with open("tests/result-2-2.json", "w") as outfile:
        json.dump(bit_locks, outfile, indent=2, ensure_ascii=False)
