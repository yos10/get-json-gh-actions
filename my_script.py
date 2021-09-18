import requests
import json

def get_json_data(url):
    response = requests.get(url)
    json_data = response.json()
    return json_data

def extract_patients_by_prefecture(list):
    new_dict = {}
    for l in list:
        prefecture = l['name_jp']
        npatients = l['npatients']
        new_dict.setdefault(prefecture, npatients)
    return new_dict

def calc_new_cases(dict1, dict2):
    new_cases_list = []
    for prefecture in dict1:
        if prefecture in dict2:
            d = {
                prefecture : abs(int(dict1[prefecture]) - int(dict2[prefecture]))
            }
            new_cases_list.append(d)
    return new_cases_list

def save_as_json(file_name, data, indent=True):
    if indent:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

def main():
    url = 'https://opendata.corona.go.jp/api/Covid19JapanAll'
    json_data = get_json_data(url)

    latest_date_item_list = json_data['itemList'][0:47]
    previous_date_item_list = json_data['itemList'][47:94]
    latest_date_npatients_dict = extract_patients_by_prefecture(latest_date_item_list)
    previous_date_npatients_dict = extract_patients_by_prefecture(previous_date_item_list)

    new_cases_list = calc_new_cases(latest_date_npatients_dict, previous_date_npatients_dict)

    save_as_json('total-cases.json', json_data['itemList'], indent=False)
    save_as_json('new-cases.json', new_cases_list)

main()
