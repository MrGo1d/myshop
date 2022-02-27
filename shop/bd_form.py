import requests
from bs4 import BeautifulSoup
from shop.price_form import price_conversion
import json
import os


def get_desc_spec_img(url: str) -> list:
    """The function saves the specification and link to the product photo."""
    response = requests.get(url)
    if response.status_code == 404:
        return []
    else:
        print(f'Connecting with {url} done.')
    soup = BeautifulSoup(response.text, 'lxml')
    quotes_specifications = soup.find_all(class_="sub-content-block table")
    quotes_images = soup.find_all('a', href=True)
    specifications = ''
    images_list = []
    temp_list = []
    total = []

    for quote in quotes_specifications:
        specifications = quote.text
        specifications = specifications.replace('\r', '')
        specifications = specifications.replace('\t', '')
        specifications = specifications.replace('\xa0', ' ')

    for quote in quotes_images:
        if ".jpg" in str(quote) :
            temp_list.append(str(quote))

    for elem in temp_list:
        elem = elem.split('<')
        for i in elem:
            if '.jpg' in i and 'prod_fotos' in i and 'min_' not in i:
                i = 'https://dlink.ru' + i[i.index('/up'):i.index('.jpg')+4]
                images_list.append(i)
                break
        if len(images_list) == 0:
            continue
        else:
            break

    total.append(specifications)
    total.append(images_list)

    return total


def add_data(bd_dict: dict) -> dict:
    """function parse official site and add to bd_dict specification
     and link to equipments photo """
    for key in bd_dict:
        link = bd_dict[key][4]
        if link.startswith('http'):
            for data_block in get_desc_spec_img(link):
                bd_dict[key].append(data_block)
    return bd_dict


def dict_convert(bd_dictionary: dict) -> dict:
    '''This function converts dict to:
    {'category_1': {'equipment_1': ['description_1'],
                    'equipment_2': ['description_2']},
     'category_2': {'equipment_3': ['description_3'],
                    'equipment_4': ['description_4']}
    ...
    }'''
    new_dict = {}
    for key, value in bd_dictionary.items():
        if value.count('') == 5:
            tmp_key = key
            new_dict[tmp_key] = {}
            continue
        new_dict[tmp_key].update({key: value})
    print('Dictionary convert done')
    return new_dict


def save_base(base):
    """Save base as base.txt"""
    with open('../base.txt', 'w', encoding='utf-8') as fh:
        json.dump(base, fh, indent='    ', ensure_ascii=False)
    print('File base.txt created!', os.getcwd())
