from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
MAIN_CATEGORY = ('LadyLink',
                 'GuysLink',
                 'Teenagers_Link',
                 'Kids_Link'
                 )

MAIN_SORT_PARAMS = ('productLabelType',
                    'height',
                    'productColors',
                    'productSizeGroupsFacet',
                    'price'
                    )
SUB_SORT_PARAMS = (
    'rating-desc',
    'priority',
    'price-desc',
    'price-asc',
    'discount-desc'
)
PRICES = (
    [0, 499],
    [500, 999],
    [1000, 1499],
    [1500, 1999],
    [2000, 2999],
    [3000, 3999],
    [4000, 4999]
)


# Запуск бразуера. Инициализация драйвера
def get_driver(URL):
    sleep(3)
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("window-size=1280,1080")
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('log-level=3')
    driver = webdriver.Remote(command_executor='http://selenium:4444/wd/hub', options=options)
    driver.implicitly_wait(3)
    driver.get(URL)
    return driver


# Отключение выбора региона
def turn_off_region(driver):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of(driver.find_element(By.XPATH, "//div[@data-qa='closeAutodetectRegion']")))
        element_region = driver.find_element(By.XPATH, "//div[@data-qa='closeAutodetectRegion']")
        element_region.click()
    except BaseException as text:
        if str(text)[9:24] == 'no such element':
            print(f'No region button')


# Переход на страницу выбранной категории
def select_category(driver, main_category):
    element_lady_category = driver.find_element(By.XPATH, f'//div[@data-for="{main_category}"]')
    element_lady_category.click()


# Сброс параметров сортировки
def reset_price_params(driver, reset_param):
    element_params = driver.find_element(By.XPATH, f'//div[@data-qa="{reset_param}"]//div[@data-reset-params]')
    element_params.click()


# Сортировка по ценовой категории
def sort_by_price(driver, price):
    driver.find_element(By.XPATH, '//div[@data-qa="price"]').click()                                     # Выбор тип сортировки
    driver.find_element(By.XPATH, f'//label[@data-qa="facet_{price[0]}₽-{price[1]}₽"]').click()        # Выбор значения цены
    driver.find_element(By.XPATH, '//p[@data-qa="apply_price"]').click()                                 # Применение выбранного зачения


# Выбор параметра общей сортировки
def sub_sort(driver, sub_sort_param):
    driver.find_element(By.XPATH, '//div[@class="check-dropdown-list__button-text"][1]').click()
    driver.find_element(By.XPATH, f'//input[@data-sort-code="{sub_sort_param}"]/parent::a').click()


# Информация о наличии товара (на странице любой категории)
def get_stock_info(driver):
    element_size = driver.find_element(By.XPATH, '//div[@data-stock]')
    text = element_size.get_attribute('outerHTML')
    split = text.split(' ')
    f = list(filter(lambda a: 'data-stock' in a, split))
    data_stock = f[0].split('"')[1]
    return data_stock


# Параметры кнопки добавления в корзину/избранные (в карточке товара)
def get_attr_of_button_cart(driver):
    element_button_to_cart = driver.find_element(By.XPATH, '//div[@class="button-wrapper"]//button[@type="button"]')
    attr_of_button_to_cart = element_button_to_cart.get_attribute('innerText')
    element_sub_banner = driver.find_element(By.XPATH, '//div[@class="product-info-container"]//div[@class="shield-wrapper js-shield-container"]')
    attr_of_sub_banner = element_sub_banner.get_attribute('innerText')
    if attr_of_button_to_cart == 'ДОБАВИТЬ В КОРЗИНУ' and attr_of_sub_banner != 'СКОРО':
        return 1
    elif attr_of_button_to_cart == 'ДОБАВИТЬ В ИЗБРАННОЕ' or attr_of_sub_banner == 'СКОРО':
        return 0
    else:
        return 2


# Ссылка на текущую страницу
def get_base_uri(driver):
    base_uri = driver.find_element(By.XPATH, '//head').get_attribute('baseURI')
    return base_uri


# Функция возвращает список товаров (ввиде вэб-элементов)
def get_all_items(driver):
    return driver.find_elements(By.XPATH, '//div[@data-qa="product-block"]//div[@class="listing-item__info"]')


# Функция возвращает список ссылок на каждый товар (в виде вэб-элементов)
def get_all_items_href(driver):
    return driver.find_elements(By.XPATH, f'//div[@data-qa="product-block"]//div[@class="listing-item__img-wrapper"]//a')


# Очистка корзины
def clear_cart(driver):
    driver.find_element(By.XPATH, '//div[@class="basket-block__clear"]').click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="press-button press-button--red-style js-clear-basket"]')))
    driver.find_element(By.XPATH, '//button[@class="press-button press-button--red-style js-clear-basket"]').click()
