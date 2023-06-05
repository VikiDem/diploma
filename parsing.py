import time

import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

Options = Options()
# Options.headless = True # Фоновый режим
Options.add_experimental_option('excludeSwitches', ['enable-logging']) # Убирает мерзкое сообщение об ошибке


service = ChromeService(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome(options=Options, service=service)    # Фоновый режим

action = ActionChains(driver)

# Вход на сайт компании
def log_in_to(login, password):
    driver.get('https://spark-interfax.ru/#/dashboard')

    login_input = driver.find_element('name', 'username')
    login_input.send_keys(login)
    time.sleep(.1)


    password_input = driver.find_element('name', 'password')
    password_input.send_keys(password)
    time.sleep(.1)

    log_in_button = driver.find_element('class name', 'login-form__btn')   # Кнопка поиска
    log_in_button.click()
    time.sleep(1.1)


# Найти в компанию в поиске и перейти на ее страницу
def open_company_page(company_name='7731481013'):
    counter = 0
    try:
        driver.get('https://spark-interfax.ru/')
        continue_button = driver.find_element('class name','js-login-continue-button')   # Кнопка поиска
        continue_button.click()
        time.sleep(1.1)

        my_company = company_name + '\n'
        driver.find_element('tag name', 'input').send_keys(my_company)
        time.sleep(1.5)  # Вставка id

        my_company_name = driver.find_elements('class name', 'sp-summary__header')
        my_company_name[0].click()  # Нажатие на первую найденую компанию

        print('---------------')
        print(f'Компания "{company_name}" найдена')
        print('---------------')
        return 1
    except:
        print('---------------')
        print(f'Компания "{company_name}" не найдена')
        print('---------------')

# Получение списка патентов
def save_data_of_section(name):
    result = []
    try:
        patents = driver.find_elements('xpath', f"//div[contains(text(), '{name}')]")
        for patent in patents:
            result.append(patent.text)
    except:
        pass
    return result

# Переход на страницу конкретного раздела Интелектуальной собственности
def open_page_section_of_intellectual_property(name):
    sections = driver.find_elements('xpath', f"//tr[td[text()='{name}']]")
    patents = []
    for i in range(len(sections)):
        buttons = driver.find_elements('xpath', f"//tr[td[text()='{name}']]")
        buttons[i].find_element('tag name', 'button').click()
        time.sleep(0.5)
        patents += save_data_of_section('Изобретение')
        patents += save_data_of_section('Полезная модель')
        patents += save_data_of_section('Программа для ЭВМ')
        patents += save_data_of_section('База данных')

        driver.back()
        time.sleep(0.3)
    #print(patents)
    return patents


# Интелектуальная собственность: патент(Государственная поддержка: форма поддержки и год)
def patents_intellectual_property():
    counter = 0
    patents = []
    try:
        intellectual_property = driver.find_element('xpath', "//span[text()='Интеллектуальная собственность']")

        ActionChains(driver) \
            .scroll_to_element(intellectual_property) \
            .perform()    # Скролинг

        intellectual_property.click()    # Переход на страницу Интелектуальной собственности
        time.sleep(1.5)
        try:
            patents += open_page_section_of_intellectual_property('Изобретения и полезные модели')
        except:
            counter += 1
        try:
            patents += open_page_section_of_intellectual_property('Программы для ЭВМ, базы данных')
        except:
            counter += 1

        if counter == 2:
            patents += save_data_of_section('Изобретение')
            patents += save_data_of_section('Полезная модель')
            patents += save_data_of_section('Программа для ЭВМ')
            patents += save_data_of_section('База данных')

        # print(patents)
        return(patents)

    except:
        print('Раздел "Интеллектуальная собственность" у компании отсутствует')

# Первый тип страницы Гос поддержки
def state_support_type_1():
    result = dict()
    time.sleep(1.5)
    elements = driver.find_elements('css selector', 'tr[class]')   # Списик всех строк поддержек
    for element in elements:
        all_dates = []
        support_category = element.find_element('class name', 'btn__text').text   # Название категории
        try:
            dates = element.find_elements('class name', 'text_color_secondary')   # Все года поддержек
            for date in dates:
                all_dates.append(date.text)
        except:
            pass
        result[support_category] = all_dates
    # print(result)
    return result   # Возвращает словать {Категория: [годы]}

# Второй тип страницы Гос поддержки
def state_support_type_2():
    result = dict()
    elements = driver.find_elements('class name', 'subsidies-section__inner')   # Список всех поддержек
    for element in elements:
        # Название категории поддержки
        support_category_cell = element.find_element('xpath', "//tr[td[text()='Форма и вид поддержки']]")
        support_category = support_category_cell.find_element('class name', 'white-space-normal').text

        # Дата принятия решения по поддержке
        date_cell = element.find_element('xpath', "//tr[td[text()='Принятие решения']]")
        date = date_cell.find_element('class name', 'sp-properties-form__value').text
        if support_category in result.keys():   # Проверка наличия категории в словаре
            result[support_category].append(date)
        else:
            result[support_category] = [date]

    # print(result)
    return result    # Возвращает словать {Категория: [даты]}

# Третий тип страницы Гос поддержки
def state_support_type_3():
    result = dict()
    dates = []
    support_category = driver.find_element('xpath', '//th[text()]').text
    elements = driver.find_elements('xpath', '//tr[td[div]]')
    for element in elements:
        date = element.find_elements('class name', 'new-table__content-td-wrap')
        dates.append(date[2].text)
    result[support_category] = dates
    # print(result)
    return result

# Государственная поддержка
def state_support():
    counter = 0
    try:
        intellectual_property = driver.find_element('xpath', "//span[text()='Государственная поддержка']")

        ActionChains(driver) \
            .scroll_to_element(intellectual_property) \
            .perform()    # Скролинг

        intellectual_property.click()    # Переход на страницу Гос поддержки
        try:
            test_1 = state_support_type_1()
        except:
            test_1 = ''
            counter += 1
        try :
            test_2 = state_support_type_2()
        except:
            test_2 = ''
            counter += 1
        try:
            test_3 = state_support_type_3()
        except:
            test_3 = ''
            counter += 1

        if test_1:
            result = test_1
        elif test_2:
            result = test_2
        elif test_3:
            result = test_3
        else:
            result = {'Ошибка': []}

        #print(result)
        time.sleep(1.5)
        return result
    except:
        print('Раздел "Государственная поддержка" у компании отсутствует')
        return dict()


# Бухгалтерская отчетность - выводит если есть (код 1120)
def bugalteo_reporting():
    try:
        intellectual_property = driver.find_element('xpath', "//span[text()='Бухгалтерская отчетность']")

        ActionChains(driver) \
            .scroll_to_element(intellectual_property) \
            .perform()    # Скролинг

        intellectual_property.click()
        time.sleep(1.0)
        td1120 = driver.find_elements('xpath', '//td[text() = 1120]')
        if len(td1120) > 0:
            return 'Да'
        else:
            return 'Нет'

    except:
        print('Раздел "Бухгалтерская отчетность" у компании отсутствует')
        return ''


def parsing(company_names_array, login, password):
    result = []
    log_in_to(login, password)
    f = open('errors.txt', 'w', encoding='UTF-8')
    f.close()
    error_file  = open('errors.txt', 'a')
    for company in company_names_array[:10]:
        try:
            if open_company_page(company):
                time.sleep(3.5)

                original_window = driver.current_window_handle  # Старая вкладка
                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)  # Переключение на новую вкладку
                        break

                patents = patents_intellectual_property()
                time.sleep(0.3)
                support = state_support()
                time.sleep(0.3)
                bugalteo1120 = bugalteo_reporting()
                print(f'{company}:')
                print(patents)
                print(support)
                print(bugalteo1120)

                result.append([company, patents, support, bugalteo1120])

                driver.close()  # Закрытие новой вкладки
                driver.switch_to.window(original_window)  # Переключение на старую вкладку
            else:
                error_file.write(f'{company}\n')
                print(f"Компания {company} не найдена")
        except:
            print(f'{company} - Ошибка Т_Т')
    error_file.close()
    time.sleep(3.1)
    return(result)



if __name__ == '__main__':
    test_data = pd.read_excel('test1.xlsx')
    company_names_array = np.array(test_data['Наименование'].tolist())
    my_company = '7731481013'  # id НИИИТ
    parsing(company_names_array, 'none', 'none')
