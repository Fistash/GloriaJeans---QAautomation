# Тест-кейс №3. Проверка соответствия: наличие товара и возможность его добавить в корзину/избранные

import pytest
import base_function as bf
from selenium.webdriver.common.by import By

STOCK_VALUE = []
BUTTON_CART_VALUE = []
URL = 'https://www.gloria-jeans.ru'
main_category = bf.MAIN_CATEGORY
prices = bf.PRICES


@pytest.fixture
def stock():
    global driver
    driver = bf.get_driver(URL=URL)                                         # Запуск браузера
    bf.turn_off_region(driver=driver)                                       # Выбор региона (закрыть)
    bf.select_category(driver=driver, main_category=main_category[0])       # Переход в категорию (Женщины)
    bf.sort_by_price(driver=driver, price=prices[6])                        # Сортировка по ценовой категории (4000 - 4999)
    qty_of_items = len(bf.get_all_items(driver=driver))                     # Подсчет количества товаров на странице
    base_uri = bf.get_base_uri(driver=driver)                               # Ссылка на текущую страницу (всех товаров определенное категории)
    # Получение информации о наличии товара и возможности добавить его в корзину/избранные
    for i in range(qty_of_items):
        href = driver.find_elements(By.XPATH, f'//div[@data-qa="product-block"]//div[@class="listing-item__img-wrapper"]//a')[i].get_attribute('href')
        driver.get(href)
        driver.find_element(By.XPATH, '//div[@class="block-size js-block-size-sku"]//div').click()
        STOCK_VALUE.append(bf.get_stock_info(driver=driver))
        BUTTON_CART_VALUE.append(bf.get_attr_of_button_cart(driver=driver))
        driver.get(base_uri)


# Если товар есть в наличии, то возвращает - 1, иначе - 0
def stock_value(i):
    if int(STOCK_VALUE[i]) > 0:
        return 1
    else:
        return 0


# Проверка соответствия наличия товара и возможности его добавить в корзину/избранные
def test_case_match(stock):
    for i in range(len(STOCK_VALUE)):
        assert stock_value(i) == BUTTON_CART_VALUE[i], 'Несоответствие наличия товара и возможности добавления в корзину'
    driver.quit()
