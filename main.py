import configparser
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_drinks(excel_table_name: str) -> defaultdict:
    """Get drinks information from excel table"""
    products = pandas.read_excel(excel_table_name, sheet_name='Лист1', na_values='nan',
                                          keep_default_na=False).to_dict(orient='records')

    grouped_products = defaultdict(list)

    for product in products:
        grouped_products[product['Категория']].append(product)

    return grouped_products


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
    drinks = get_drinks(excel_filename)

    current_year = datetime.now().year
    company_founding_date = 1920
    company_age = current_year - company_founding_date

    template = env.get_template('template.html')
    rendered_page = template.render(
        company_age=company_age, drinks=drinks
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    render_template()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
