from json import load
from openpyxl import Workbook
from lxml import html
from requests import get


def parse():
    res = []
    # TODO не забыть убрать точку
    with open('./source/masterlux/masterlux.json') as f:
        data = load(f)
    for pair in data.items():
        cls = pair[0]
        print(cls)
        page = html.fromstring(get(pair[1]).text)
        items = page.xpath('//div[@class="product-form"]')
        prices = page.xpath('//button[@title="В корзину"]/text()')
        counter = 0
        for item in items:
            product = item.xpath('./p/text()')
            name = product[0]
            brand = name.split()[0]
            size = '{}/{}R{}'.format(product[3].split()[-1], product[4].split()[-1], product[5].split()[-1])
            season = product[2].split()[-1]
            price = item.xpath('./div/button/text()')[0]
            res.append([name, cls, brand, season, size, price])
            counter += 1
    return res


def write(rows):
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Класс', 'Бренд', 'Сезонность', 'Размер', 'Цена'])
    for row in rows:
        ws.append([str(x) for x in row])

    wb.save('./res/masterlux.xlsx')


if __name__ == '__main__':
    write(parse())
