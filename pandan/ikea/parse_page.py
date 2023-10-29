import json
import pprint
import random

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep


def randomUserAgent():
    f = open("user_agent.txt", "r")
    user_agents = [x for x in f]
    f.close()
    return random.choice(user_agents)


def parsePage(item_id):
    # шаг 3
    # идем в карточку товара по id
    # вытаскиваем:
    # -название
    # -описание
    # -параметры
    try:
        print(f"Пытаемся сканировать {item_id}...", end="")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--user-agent={randomUserAgent()}")
        driver = webdriver.Firefox(options=chrome_options)

        item_data = {}
        driver.get(f"https://www.wildberries.ru/catalog/{item_id}/detail.aspx")
        sleep(3)

        # читаем заголовок и описание
        item_data["title"] = driver.title
        item_data["description"] = driver.find_element(By.CLASS_NAME, "collapsable__text").text

        # нужно нажать селениумом на ссылку "развернуть характеристики", чтобы соскрейпить полный список параметров
        expand_button = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div[3]/div/div[3]/section/div[3]/div[1]/div/div[2]/div[2]/button')
        expand_button.click()

        # читаем параметры товара
        item_data["params"] = {}
        all_params = driver.find_elements(By.CLASS_NAME, "product-params__table")

        # читаем первый блок с параметрами товара и пишем в массив
        params1 = all_params[0].text.split("\n")
        item_data["params"][params1[0]] = {}
        for i in range(1, len(params1), 2):
            item_data["params"][params1[0]][params1[i]] = params1[i + 1]

        # читаем следующие блоки внизу, начиная с третьего (второй — повторение первого)
        for k in range(2, len(all_params)):
            caption = all_params[k].find_element(By.CLASS_NAME, "product-params__caption").text
            item_data["params"][caption] = {}
            data_rows = all_params[k].find_elements(By.CLASS_NAME, "product-params__row")
            # if "\t" not in data_rows[0].text: # это просто значение к заголовку (состав: полиэстер)
            #     item_data["params"][caption][caption] = data_rows[0].text
            for row in data_rows:
                key = row.find_element(By.TAG_NAME, "th").text
                value = row.find_element(By.TAG_NAME, "td").text
                item_data["params"][caption][key] = value
        print("успешно!")
        return item_data

    except:
        print(f"Не удалось просканировать {item_id} :( ", end="")
        return None
    finally:
        driver.quit()


def updateJson(item_id, brand, new_dict):
    # пишем результат парсинга страницы в общий словарь под ключом id
    if not new_dict:
        print(f"Нет данных для {item_id}")
    else:
        f = open(f"all_{brand}_products.json", "r")
        json_dump = json.load(f)
        f.close()

        json_dump[item_id].update(new_dict)

        f = open(f"all_{brand}_products.json", "w")
        json.dump(json_dump, f)
        f.close()
    return None


def resumeParsingPages(brand):
    fi = open(f"all_{brand}_products.json", "r")
    scan_file = json.load(fi)
    fi.close()
    # pprint.pp(scan_file)

    for item, value in scan_file.items():
        if "description" not in value:  # если страницу этого товара еще не сканировали
            print(f"{item} еще не сканировали, поэтому ", end="")
            updateJson(item, brand, parsePage(item))  # сканируем и обогащаем данные в json
        else:
            continue


resumeParsingPages(89090)