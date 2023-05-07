import csv
from collections import defaultdict
from os.path import join, dirname, abspath

path = join(dirname(dirname(dirname(abspath(__file__)))))


def get_amazon_links():
    """
    Get amazon links from amazon products file
    :return: None
    """
    columns = defaultdict(list)

    with open(path + "/products.csv", encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k, v in row.items():
                columns[k].append(v)
    with open(path + "/urls.txt", "w") as file:
        for index, url in enumerate(columns["Product Url"]):
            file.write(url + "\n")
            if index > 1000:
                break


if __name__ == "__main__":
    get_amazon_links()
