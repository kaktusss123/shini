from lxml import html
from json import loads
from openpyxl import Workbook
from requests import get
from pprint import pprint


def light():
    res = []

    for i in range(1, 859):
        page = html.fromstring(get('https://rezina.cc/shiny?page={}&view=partial'.format(i)).text)
        items = page.xpath('//li[@class="tile-item"]')
        print('Page: {}'.format(i))

        for item in items:
            try:
                js = loads(item.xpath('.//a[@class="category-name-title title"]/@data-ga')[0])

                size = ''
                for word in js['name'].split():
                    if '/' in word and 'R' in word:
                        size = word

                # Следующее за брендом слово
                model = js['name'].split()[js['name'].lower().split().index(js['brand'].lower().split()[-1]) + 1]

                res.append([js['name'], 'легковые', js['brand'], model, size,
                            item.xpath('.//div[@class="hover-block"]//span[@class="value"]/text()')[1], js['price']])
            except Exception as e:
                print(e)
    return res


def heavy():
    res = []

    for i in range(1, 114):
        page = html.fromstring(get('https://rezina.cc/gruzovye-shiny?page=2&view=partial'.format(i)).text)
        items = page.xpath('//li[@class="tile-item"]')
        print('Page: {}'.format(i))

        for item in items:
            try:
                js = loads(item.xpath('.//a[@class="category-name-title title"]/@data-ga')[0])

                size = ''
                for word in js['name'].split():
                    if '/' in word and 'R' in word:
                        size = word

                # Следующее за брендом слово
                model = js['name'].split()[js['name'].lower().split().index(js['brand'].lower().split()[-1]) + 1]

                res.append([js['name'], 'грузовые', js['brand'], model, size,
                            item.xpath('.//div[@class="hover-block"]//span[@class="value"]/text()')[1], js['price']])
            except Exception as e:
                print(e)
    return res


def write():
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    rows = [['Наименование', 'Класс', 'Бренд', 'Модель', 'Размер', 'Сезонность', 'Цена']]
    rows += light()
    rows += heavy()
    for row in rows:
        ws.append(row)

    wb.save('./res/rezina.cc.xlsx')


if __name__ == '__main__':
    write()
