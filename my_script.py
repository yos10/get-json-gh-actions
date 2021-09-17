import requests
import json

def get_json_data(url):
    response = requests.get(url)
    json_data = response.json()
    return json_data

def list_to_dict(list):
    new_dict = {}
    for item in list:
        prefecture = item['name_jp']
        npatients = item['npatients']
        new_dict.setdefault(prefecture, npatients)
    return new_dict

def calc_new_cases(dict1, dict2):
    new_cases_dict = {}
    for key in dict1:
        if key in dict2:
            new_cases_dict[key] = abs(int(dict1[key]) - int(dict2[key]))
    return new_cases_dict

def save_as_json(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    url = 'https://opendata.corona.go.jp/api/Covid19JapanAll'
    json_data = get_json_data(url)
    latest_date_item_list = json_data['itemList'][0:47]
    previous_date_item_list = json_data['itemList'][47:94]
    latest_date_npatients_dict = list_to_dict(latest_date_item_list)
    previous_date_npatients_dict = list_to_dict(previous_date_item_list)
    new_cases_dict = calc_new_cases(latest_date_npatients_dict, previous_date_npatients_dict)
    save_as_json('total-cases.json', json_data['itemList'])
    save_as_json('new-cases.json', new_cases_dict)

main()
