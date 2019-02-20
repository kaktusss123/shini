from json import load
from openpyxl import Workbook
from lxml import html
from requests import get

REQ_URL = 'http://agropiese.md/s_c/s_c.aspx?md=1&d='


def parse():
    res = []
    with open('./source/agropiese/agropiese.json', encoding='UTF-8') as f:
        data = load(f)
    for pair in data.items():
        print(pair[0])
        cls = pair[0]
        page = html.fromstring(get(pair[1]).text)
        ids = page.xpath('//tbody/tr/@class')
        for id in ids:
            product = html.fromstring(get(REQ_URL + id).text)
            trs = product.xpath('//tr')
            d = {}
            for tr in trs:
                if tr.xpath('./td/text()') and tr.xpath('./td/strong/text()'):
                    d.update(dict(zip(tr.xpath('./td/text()'), tr.xpath('./td/strong/text()'))))
            try:
                name = d['Описание:']
                brand = d['Бренд :']
                try:
                    season = d['Сезон :']
                except:
                    season = '-'
                price = d['Цена со скидкой:']
                res.append([name, cls, brand, season, price])
            except Exception as e:
                print(e, id, d)
    return res


def write(rows):
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Класс', 'Бренд', 'Сезонность', 'Цена'])
    for row in rows:
        ws.append(row)

    wb.save('./res/agropiese.xlsx')


if __name__ == '__main__':
    write(parse())
