# Тест-кейс №1. Добавление товаров в корзину

import pytest
import base_function as bf
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
URL = 'https://www.gloria-jeans.ru'
main_category = bf.MAIN_CATEGORY
prices = bf.PRICES
CHECK = []


@pytest.fixture
def add_to_cart():
    global driver
    driver = bf.get_driver(URL=URL)                                     # Запуск браузера
    bf.turn_off_region(driver=driver)                                   # Выбор региона (закрыть)
    bf.select_category(driver=driver, main_category=main_category[0])   # Переход в категорию (Женщины)
    bf.sort_by_price(driver=driver, price=prices[6])                    # Сортировка по ценовой категории (0 - 499)
    qty_of_items = len(bf.get_all_items(driver=driver))                 # Подсчет количества товаров на странице
    base_uri = bf.get_base_uri(driver=driver)
    for i in range(qty_of_items):
        item = bf.get_all_items_href(driver=driver)
        driver.get(item[i].get_attribute('href'))
        driver.find_element(By.XPATH, '//div[@class="block-size js-block-size-sku"]//div').click()  # Выбор первого параметра товара
        element_button_cart = bf.get_attr_of_button_cart(driver=driver)                             # Проверка button (избранные или корзина)
        if element_button_cart == 1:                                    # Условие выполянется, если button = добавить в корзину
            try:
                driver.find_element(By.XPATH, '//div[@class="button-wrapper"]//button[@type="button"]').click()
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="pop-up-basket__header margin-bottom-16"]')))
                element_expected_modal_window = driver.find_element(By.XPATH, '//div[@class="pop-up-basket__header margin-bottom-16"]').get_attribute(
                    'innerText')
                if element_expected_modal_window == 'Товар добавлен в корзину':
                    driver.get('https://www.gloria-jeans.ru/cart')
                    bf.clear_cart(driver=driver)
                    CHECK.append(True)
                else:
                    CHECK.append(False)
            except BaseException as text:
                print(f'Ошибка в блоке add_to_cart: {str(text)}')
                CHECK.append(False)
        driver.get(base_uri)


def test_case_add_to_cart(add_to_cart):
    for i in range(len(CHECK)):
        assert CHECK[i], f'Товар {i} не удалось добавить в корзину'
    driver.quit()
