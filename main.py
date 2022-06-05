from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas
from collections import defaultdict


def get_drinks_carts_info() -> defaultdict:
    wines_table = pandas.read_excel('wine.xlsx', sheet_name='Лист1',
                                   na_values='nan',
                                   keep_default_na=False).values.tolist()
    table_headers = pandas.read_excel('wine.xlsx', sheet_name='Лист1',
                                      na_values='nan',
                                      keep_default_na=False).keys().tolist()
    counter = 0
    drinks = defaultdict(list)

    for drink_info in wines_table:
        drink_category = drink_info[counter]

        drink = {}
        for table_header in table_headers:
            info_field = drink_info[counter]
            drink[table_header] = info_field
            counter += 1

        drinks[drink_category].append(drink)
        counter = 0

    return drinks


def render_template() -> None:
    drinks_info = get_drinks_carts_info()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
    )

    template = env.get_template('template.html')
    current_year = datetime.now().year
    company_age = current_year - 1920
    rendered_page = template.render(
        company_age=company_age, drinks=drinks_info
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    render_template()
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
