from lxml import html
from json import load
from openpyxl import Workbook
from requests import get
from pprint import pprint

seasons = ['летняя', 'зимняя']


def parse():
    res = []
    for i in range(1, 15):
        print('Страница {}/{}'.format(i, 15))
        page = html.fromstring(get('https://tiravto.com/catalogs/tires?page={}'.format(i)).text)
        cells = page.xpath('//div[@class="catalogItem"]')
        for cell in cells:
            name = cell.xpath('.//h3/text()')[0]
            brand = cell.xpath('.//span[@class="text-center productStock"]/text()')[0].strip()

            size = ''
            for word in range(len(name.split())):
                if '/' in name.split()[word]:
                    size = ' '.join([name.split()[word], name.split()[word + 1]])
                    break

            season = '-'
            for s in seasons:
                if s in name:
                    season = s

            price = cell.xpath('.//h4/text()')[0].strip()
            presense = cell.xpath('.//div[@class="catalogButton"]/b/text()')[0]
            res.append([str(name), brand, size, season, price, str(presense)])
    return res


def write(res):
    wb = Workbook()

    ws = wb.create_sheet('Шины', 0)
    rows = [['Наименование', 'Бренд', 'Размер', 'Сезонность', 'Цена', 'Наличие']]
    rows += res
    for row in rows:
        ws.append([str(x) for x in row])

    wb.save('./res/tiravto.xlsx')


if __name__ == '__main__':
    write(parse())
