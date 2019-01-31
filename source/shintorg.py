from openpyxl import Workbook
from lxml import html
from requests import get

BASE_URL = 'http://shintorg.md/catalog/shiny?page='


def parse():
    res = []
    for i in range(1, 9):
        page = html.fromstring(get(BASE_URL + str(i)).text)
        items = page.xpath('//div[@class="pc-item product"]')
        for item in items:
            name = item.xpath('.//a/img/@alt')[0]
            size = '-'
            for word in name.split():
                if '/' in word and 'r' in word.lower():
                    size = word
                    break
            cls = item.xpath('.//div[@class="shin-tip"]/img/@title')[0]
            brand = item.xpath('.//div[@class="type"]/text()')[0].strip().split()[-1]
            price = item.xpath('.//div[@class="price pull-left"]/text()')[0]
            res.append([name, brand, cls, size, price])
    return res


def write(rows):
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Бренд', 'Сезонность', 'Размер', 'Цена'])
    for row in rows:
        ws.append(row)

    wb.save('../res/shintorg.xlsx')


if __name__ == '__main__':
    write(parse())
