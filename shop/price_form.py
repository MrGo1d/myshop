import requests
import urllib
import patoolib
import os
import xlrd
import xlwt
import pandas as pd
import shutil


def directory_cleaning(path: str = None) -> None:
    """ Function checks if there is a "Price" folder for unpacking the price, if not - it creates it"""
    if path == None:
        path = os.getcwd()
    if 'Price' not in os.listdir():
        os.mkdir("Price")
        print('"Price" folder was create!')
    else:
        os.chdir(path + '/Price')
        if len(os.listdir()) == 0:
            os.chdir(path)
        else:
            for file in os.listdir():
                print(f'{file} was removed!')
                os.remove(file)
            os.chdir(path)


def file_download(url: str = None) -> str:
    ''' func for price downloads'''
    if url is None:
        url = "https://microinform.by/downloads/m_price.rar"
    outfilename = url[-(url[::-1].index('/')):]
    urllib.request.urlretrieve(url, outfilename)
    print(f'Preparation for loading from {url}.')
    return outfilename


def rar_unpacking(path=''):
    ''' func for unpacking files from price.rar'''
    if path == '':
        path = "m_price.rar"
    patoolib.extract_archive("m_price.rar", outdir="Price")
    return f'File "{path}" succefully unpacked!'


def price_conversion(file_path: str = None, percent: int = None) -> dict:
    '''function converts data from download price and add allowance '''
    if percent is None:
        percent = 0
    if file_path is None:
        os.chdir(os.getcwd() + '/Price')
        file_name = os.listdir()[0]
    else:
        file_name = file_path
    rb = xlrd.open_workbook(file_name, formatting_info=True, encoding_override='cp1251')
    sheet = rb.sheet_by_index(0)
    flag = False
    data_dict = {}
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        if row[0] == 'D-LINK (сетевое оборудование)':
            flag = True
        elif row[0] == 'ENERGIZER':
            break
        if flag:
            if file_path is None:
                del row[2]
                del row[5]
            if row[2] != '' and percent > 0:
                row[2] += float('{:.2f}'.format(row[2] * percent / 100))
            data_dict[row[0]] = row[1:]
    print('Price formation finished.')
    return data_dict


def price_create(data_dict: dict) -> None:
    '''function create excele file - price for downloads'''
    thin_border = xlwt.easyxf('border: left thin, right thin, top thin, bottom thin')
    thick_border = xlwt.easyxf('border: left thick, right thick, top thick, bottom thick')

    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.colour_index = 0
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Price')
    ws.write(0, 0, '"Horns and hooves" LLC', style0)
    ws.write(1, 0, '200000, г. Минск, пр-т Машерова, 1', style0)
    ws.write(2, 0, 'р/с №BY00XXXX000000000000000000000001 в ЗАО «Альфа-Банк»', style0)
    ws.write(3, 0, 'Республика Беларусь, 220013, г. Минск, ул. Сурганова, 43-47.', style0)
    ws.write(4, 0, 'тел. факс: +375 (17) 200-00-00', style0)
    ws.write(5, 0, 'e-mail: info@myshop.by', style0)
    ws.write(7, 0, 'Сетевое оборудование ведущих мировых производителей', style0)
    ws.write(9, 0, '   * - менее 5; ** - менее 10; *** - более 10')

    ws.write(10, 0, 'Код товара', thick_border)
    ws.col(0).width = 5000
    ws.write(10, 1, 'Наименование (характеристики)', thick_border)
    ws.col(1).width = 15000
    ws.write(10, 2, 'Цена с НДС', thick_border)
    ws.col(2).width = 3000
    ws.write(10, 3, 'Склад', thick_border)
    ws.col(3).width = 2000
    ws.write(10, 4, 'Резерв', thick_border)
    ws.col(4).width = 2000
    ws.write(10, 5, 'Описание', thick_border)
    ws.col(5).width = 10000

    for en, key in enumerate(data_dict):
        ws.write(11 + en, 0, key, thin_border)
        length = len(data_dict[key])
        for i in range(length):
            ws.write(11 + en, i + 1, data_dict[key][i], thin_border)
    try:
        wb.save('../price.xls')
        print('"price.xls" created.')
        shutil.copyfile(r'/home/mr_go1d/Projects/Mele/myshop/Price/price.xls',
                        r'/home/mr_go1d/Projects/Mele/myshop/shop/static/price.xls')
    except PermissionError('Close the price.xls file!'):
        pass
