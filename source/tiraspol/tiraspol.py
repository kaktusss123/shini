from json import load

from lxml import html
from openpyxl import Workbook
from requests import get


def parse():
    res = []
    with open('./source/tiraspol/tiraspol.json', encoding='UTF-8') as f:
        data = load(f)
    for cls in data:
        print(cls)
        for season in data[cls]:
            page = html.fromstring(get(data[cls][season]).text)
            cells = page.xpath('//div[@class="one_section_product_cells"]')
            for cell in cells:
                name = cell.xpath('.//div[@class="name_product"]/a/text()')[0]
                brand = cell.xpath('.//strong/text()')[0]
                size = name.split()[0]
                price = cell.xpath('.//div[@class="new_price"]/text()')[1]
                res.append([name, cls, brand, size, season, price])
            print(season, 'completed')
    return res


def write(res):
    wb = Workbook()
    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Класс', 'Бренд', 'Размер', 'Сезонность', 'Цена'])
    for row in res:
        ws.append(row)
    wb.save('./res/shini-tiraspol.xlsx')


if __name__ == '__main__':
    # light()
    parse()
