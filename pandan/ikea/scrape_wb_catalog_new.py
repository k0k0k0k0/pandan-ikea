import math
from datetime import datetime

import tqdm
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep


import glob
import json
import random

def randomUserAgent():
    f = open("user_agent.txt", "r")
    user_agents = [x for x in f]
    f.close()
    return random.choice(user_agents)

def getCatalog(brand, num_articles):
    # вытягиваем из ВБ весь каталог товаров указанного бренда, он отдается json-файлами по 100 позиций в каждом
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--user-agent={randomUserAgent()}")

    driver = webdriver.Firefox(options=options)

    blank_url = f"https://catalog.wb.ru/brands/i/catalog?TestGroup=no_test&TestID=no_test&appType=1&brand={brand}&curr=rub&dest=-1257786&regions=80,83,38,4,64,33,68,70,30,40,86,75,69,1,66,110,22,48,31,71,112,114&sort=popular&spp=99&page="

    blank_file = f"_{brand}_catalog.json"

    # при повторных запусках смотрим, что еще осталось дозагрузить
    nums = set(int(f[:2]) for f in glob.glob("*"+blank_file))
    total = set(range(1, math.ceil(num_articles/100)+1))
    print(f"Осталось загрузить {total-nums}")
    left_to_scan = list(total - nums)
    random.shuffle(left_to_scan)

    try:
        for i in left_to_scan:
            print(f"Пытаемся грузить {i}")
            try:
                driver.get(blank_url+str(i))
                data = json.loads(driver.find_element(By.TAG_NAME, 'body').text) # браузер заворачивает JSON в теги, чтобы показать
                f = open(str("{:02d}".format(i)+blank_file), 'w')  # чтобы цифры выводились двузначными
                json.dump(data, f)
                f.close()
                print("Извлекли", i)
                sleeping = random.randint(600, 1200)
                print(datetime.now(), ", cпим", sleeping)
                sleep(sleeping)
            except:
                return "Ошибка при получении" + str(i)
    except:
        return "Ошибка при загрузке браузера"
    finally:
        driver.quit()
        return "Все загружено"


getCatalog(108439, 9601)
# бренд ikea 108439, 9000 товаров
# бренд икеа 89090, 381 товар