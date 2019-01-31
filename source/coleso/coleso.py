from json import load
from requests import get
from lxml import html
from openpyxl import Workbook

seasons = {'image/stk/all.png': 'всесезонные', 'image/stk/s1.png': 'летние', 'image/stk/w2.png': 'зимние'}


def parse():
    res = []
    with open('coleso.json') as f:
        data = load(f)
    for data_cls in data.items():
        cls = data_cls[0]
        print(cls)
        for i in range(data_cls[1]['pages']):
            page = html.fromstring(get(data_cls[1]['url'] + str(i)).text)
            items = page.xpath('//div[@class="row"]/div[@class="product-layout product-list col-xs-12"]')
            for item in items:
                try:
                    try:
                        season = seasons[item.xpath('.//div[@class="stk"]/img/@src')[0]]
                    except:
                        season = '-'
                    name = item.xpath('.//div[@class="caption"]/h4/a/text()')[0].strip()
                    price = item.xpath('.//p[@class="price"]/text()')[0].strip()
                    if not price:
                        price = item.xpath('.//p[@class="price"]/span[@class="price-new"]/text()')[0].strip()
                    res.append([name, cls, season, price])
                except Exception as e:
                    print('Error on ' + str(e))
    print(res)
    return res


def write(rows):
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Класс', 'Сезонность', 'Цена'])
    for row in rows:
        ws.append(row)

    wb.save('../../res/coleso.xlsx')


if __name__ == '__main__':
    write(parse())
