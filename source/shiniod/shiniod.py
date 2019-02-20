from json import load

from lxml import html
from openpyxl import Workbook
from requests import get


def parse():
    URL = 'https://www.shiniod.ua/katalog-shin?specs={}viewmode=list&pagesize=72&pagenumber={}'
    with open('./source/shiniod/shiniod.json', encoding='UTF-8') as f:
        data = load(f)
    res = []
    for pair in data.items():
        print(pair[0])
        PAGES = int(html.fromstring(get(URL.format(pair[1], 1)).text).xpath('//li[@class="last-page"]/a/text()')[0])
        for i in range(1, (PAGES + 1)):
            print('Page: ' + str(i))
            items = html.fromstring(get(URL + str(i)).text).xpath('//div[@class="product-item"]')
            for item in items:
                name = item.xpath('.//div[@class="product-title down-space-sm"]/a/text()')[0].strip()
                season = pair[0]
                price = item.xpath('.//span[@class="price actual-price"]/text()')[0]
                res.append([name, season, price])
    return res


def write(res):
    wb = Workbook()
    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Сезонность', 'Цена'])
    for row in res:
        ws.append(row)
    wb.save('./res/shiniod.xlsx')


if __name__ == '__main__':
    write(parse())
