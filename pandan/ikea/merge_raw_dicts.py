# This Python file uses the following encoding: utf-8
import glob
import json
import tqdm


def mergeRawDicts(brand):  # сливаем все вытянутые из ВБ кусочки в единый словарь
    blank_file = f"_{brand}_catalog.json"
    products = []
    for i in tqdm.tqdm(range(1, len(glob.glob("*"+blank_file))+1)):
        f = open(str("{:02d}".format(i)) + blank_file, "r", encoding="utf-8")
        data = json.load(f)
        for product in data["data"]["products"]:
            products.append(product)

    print("Успешно обработано записей", len(products))

    with open(f"all_{brand}_products_raw.json", 'w') as output:
        json.dump(products, output)


def restructureRawDict(brand):  # упрощаем структуру словаря, выбрасываем ненужные параметры
    with open(f"all_{brand}_products_raw.json", 'r') as raw_file:
        data = json.load(raw_file)
        raw_file.close()

    products = {}
    for product in tqdm.tqdm(data):
        item = {"name": product["name"], "brand": product["brand"], "price": product["salePriceU"],
                "rating": product["reviewRating"]}
        products.update({product["id"]: item})

    print("Успешно объединено записей", len(products))

    with open(f"all_{brand}_products.json", 'w') as output:
        json.dump(products, output)


mergeRawDicts(89090)
restructureRawDict(89090)
