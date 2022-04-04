# Тест-кейс №2. Сортировка товаров по возрастанию цены

import pytest
import base_function as bf

URL = 'https://www.gloria-jeans.ru'
main_category = bf.MAIN_CATEGORY
main_sort_params = bf.MAIN_SORT_PARAMS
sub_sort_params = bf.SUB_SORT_PARAMS
prices = bf.PRICES
data_price = []

@pytest.fixture
def sort_by_price():
    global driver
    driver = bf.get_driver(URL=URL)                                         # Запуск браузера
    bf.turn_off_region(driver=driver)                                       # Выбор региона (закрыть)
    bf.select_category(driver=driver, main_category=main_category[0])       # Переход в категорию (Женщины)
    bf.sub_sort(driver=driver, sub_sort_param=sub_sort_params[3])           # Сортировка (по возрастанию цены)
    all_items = bf.get_all_items(driver=driver)                             # Запись всех товаров на странице в массив
    for i in range(len(all_items)):                                         # Запись цены каждого товара в массив
        data_price.append(float(all_items[i].get_attribute('innerText').split(' ')[0]))


def test_case_sort(sort_by_price):
    k = 0
    for i in range(len(data_price)):
        k += 1
        for j in range(len(data_price) - k):
            assert data_price[i] <= data_price[k + j], f'Ошибка элемента {i}'
    driver.quit()
