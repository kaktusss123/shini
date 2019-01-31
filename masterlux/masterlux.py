from json import load
from openpyxl import Workbook
from lxml import html
from requests import get


def parse():
    res = []
    with open('masterlux.json') as f:
        data = load(f)
    for pair in data.items():
        cls = pair[0]
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
            res.append([name, cls, brand, season, size, prices[counter].strip()])
            counter += 1
    return res


def write(rows):
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Класс', 'Бренд', 'Сезонность', 'Размер', 'Цена'])
    for row in rows:
        ws.append(row)

    wb.save('../res/masterlux.xlsx')


if __name__ == '__main__':
    write(parse())
