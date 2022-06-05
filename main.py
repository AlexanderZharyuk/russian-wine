import configparser
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_drinks_information(excel_table_name: str) -> defaultdict:
    """Get drinks information from excel table"""
    drinks_info_table = pandas.read_excel(excel_table_name, sheet_name='Лист1', na_values='nan',
                                          keep_default_na=False).values.tolist()

    drinks_information = [tuple(fields) for fields in drinks_info_table]
    drinks = defaultdict(list)

    for drink_type, drink_name, drink_sort, drink_price, drink_image, drink_sale in drinks_information:
        drink_info = {'Категория': drink_type,
                      'Название': drink_name,
                      'Сорт': drink_sort,
                      'Цена': drink_price,
                      'Картинка': drink_image,
                      'Акция': drink_sale}

        drinks[drink_type].append(drink_info)

    return drinks


def get_excel_table_name() -> str:
    """Get excel table name from config"""
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config['EXCEL']['TABLE_NAME']


def render_template() -> None:
    """Render index.html page"""
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )

    excel_filename = get_excel_table_name()
    drinks_info_from_excel = get_drinks_information(excel_filename)

    current_year = datetime.now().year
    company_founding_date = 1920
    company_age = current_year - company_founding_date

    template = env.get_template('template.html')
    rendered_page = template.render(
        company_age=company_age, drinks=drinks_info_from_excel
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    render_template()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
