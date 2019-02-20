from lxml import html
from openpyxl import Workbook
from requests import get


def parse():
    URL = 'http://avtolyalya.com/catalog/shiny?page=all'
    res = []
    items = html.fromstring(get(URL).text).xpath('//div[@class="prodposit"]')
    for item in items:
        name = item.xpath('./h3/a/text()')[0]
        price = item.xpath('.//span[@class="newcen"]/text()')[0]
        res.append([name, price])
    return res


def write(rows):
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Цена'])
    for row in rows:
        ws.append(row)

    wb.save('./res/avtolyalya.xlsx')


if __name__ == '__main__':
    write(parse())
