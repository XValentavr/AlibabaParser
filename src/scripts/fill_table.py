import csv
from collections import defaultdict

from clients.database.database_client import database_client
from handlers.endpoint_handlers.amazon_endpoint_handler import amazon_endpoint_handler
from helpers.enums.alibaba.search_types import SearchTypes
from cruds.amazon_cruds import AmazonCRUDS
from cruds.alibaba_cruds import AlibabaCRUDS


def read_amazon_links_from_table():
    columns = defaultdict(list)

    with open("wolia.csv", encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k, v in row.items():
                columns[k].append(v)

    return columns['LINK']


def fill_table(number: int, amazon: str, links: list, average: str):
    with open('table_data.txt', 'a') as file:
        alibaba_product_links_to_str = '\n'.join(links)
        extra_line = str(
            number) + ', ' + amazon + '\nALIBABA_LINKS:\n' + alibaba_product_links_to_str + '\nAVERAGE: ' + str(
            average) + '\n\n'
        file.write(extra_line)


if __name__ == "__main__":
    for number, am_link in enumerate(read_amazon_links_from_table()):
        alibaba_products_link_list = []
        print('am_lin2k', am_link)
        if am_link and 'http' in am_link:
            amazon_endpoint_handler.parse_data(
                search_type_amazon=SearchTypes.API,
                search_type_alibaba=SearchTypes.API,
                photo=am_link,
            )
            most_similar = database_client.send_most_similar_products()
            if most_similar:
                for data in most_similar:
                    average = data.get('average')
                    link = data.get('alibabaSourceLink')
                    if link:
                        alibaba_products_link_list.append(link)
                fill_table(number=number, amazon=am_link, links=alibaba_products_link_list, average=average)  # noqa
                AmazonCRUDS().remove_amazon_product_all()
                AlibabaCRUDS().remove_alibaba_product_all()
