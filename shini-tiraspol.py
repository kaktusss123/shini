from lxml import html
from json import load
from openpyxl import Workbook
from requests import get
from pprint import pprint


def light():
    res = []

    # Summer
    page = html.fromstring(get('http://shini-tiraspol.ru/catalog/letnie-shiny?page=all').text)
    cells = page.xpath('//div[@class="one_section_product_cells"]')
    for cell in cells:
        name = cell.xpath('.//div[@class="name_product"]/a/text()')[0]
        brand = cell.xpath('.//strong/text()')[0]
        size = name.split()[0]
        season = 'летние'
        price = cell.xpath('.//div[@class="new_price"]/text()')[1]
        res.append([name, brand, size, season, price])

    # Winter
    page = html.fromstring(get('http://shini-tiraspol.ru/catalog/zimnie-shiny?page=all').text)
    cells = page.xpath('//div[@class="one_section_product_cells"]')
    for cell in cells:
        name = cell.xpath('.//div[@class="name_product"]/a/text()')[0]
        brand = cell.xpath('.//strong/text()')[0]
        size = name.split()[0]
        season = 'зимние'
        price = cell.xpath('.//div[@class="new_price"]/text()')[1]
        res.append([name, brand, size, season, price])

    # All seasons
    page = html.fromstring(get('http://shini-tiraspol.ru/catalog/vsesezonnye-shiny?page=all').text)
    cells = page.xpath('//div[@class="one_section_product_cells"]')
    for cell in cells:
        name = cell.xpath('.//div[@class="name_product"]/a/text()')[0]
        brand = cell.xpath('.//strong/text()')[0]
        size = name.split()[0]
        season = 'всесезонные'
        price = cell.xpath('.//div[@class="new_price"]/text()')[1]
        res.append([name, brand, size, season, price])

    return res


def parse():
    res = []
    with open('shini-tiraspol.json') as f:
        data = load(f)
    for cls in data:
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
        print(cls, 'completed\n')

    wb = Workbook()
    ws = wb.create_sheet('Шины', 0)
    ws.append(['Наименование', 'Класс', 'Бренд', 'Размер', 'Сезонность', 'Цена'])
    for row in res:
        ws.append(row)
    wb.save('./res/shini-tiraspol.xlsx')


if __name__ == '__main__':
    # light()
    parse()
