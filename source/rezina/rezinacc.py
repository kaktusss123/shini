from json import loads, load

from lxml import html
from openpyxl import Workbook
from requests import get


def parse():
    res = []
    with open('rezina.json') as f:
        data = load(f)

    for cls in data:
        for i in range(1, data[cls]['pages']):
            page = html.fromstring(get(data[cls]['url'].format(i)).text)
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

                    res.append([js['name'], cls, js['brand'], model, size,
                                item.xpath('.//div[@class="hover-block"]//span[@class="value"]/text()')[1],
                                js['price']])
                except Exception as e:
                    print(e)
    return res


def write(res):
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Класс', 'Бренд', 'Модель', 'Размер', 'Сезонность', 'Цена'])
    for row in res:
        ws.append(row)

    wb.save('../../res/rezina.cc.xlsx')


if __name__ == '__main__':
    write(parse())
