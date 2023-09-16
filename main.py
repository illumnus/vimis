import os
import sys
import traceback

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver

import Files_Work
import Patients
import datetime
import time

# Создаем пустую базу добавляемых пациентов
Patients_Base = Patients.Patients_base()

# Проверяем наличие текстовых файлов, которые сгенерировал 1С в рабочей директории программы
directory = "C:/результат/"  # рабочая директория программы по умолчанию для 1.0 версии программы
File, Laboratory_CODE = Files_Work.get_text_file_paths(directory=directory)
unsuccess = None
if Laboratory_CODE == "ТМС_ВИМИС":
    unsuccess = Files_Work.get_unsuccess(Laboratory_CODE)
    Laboratory_CODE = 1
elif Laboratory_CODE == "ПЦР_ВИМИС":
    unsuccess = Files_Work.get_unsuccess(Laboratory_CODE)
    Laboratory_CODE = 2
if Laboratory_CODE == "ТМС":
    Laboratory_CODE = 1
elif Laboratory_CODE == "ПЦР":
    Laboratory_CODE = 2
elif Laboratory_CODE == None:
    pass

print(f"Лабораторный код: {Laboratory_CODE}\nЕсли 1 - ТМС\n2- ПЦР")

if File is None:
    print("Не найден файл!")
    sys.exit()  # если файл не один или его нет - прекратить выполнение программы
current_date = datetime.date.today()  # получаем сегодняшнюю дату
formatted_date = current_date.strftime("%Y-%m-%d")  # формтируем год-месяц-день
print(f"текущая дата: {formatted_date}")  # получаем сегодняшнюю дату - для записи
print(File)

Patients_VIMIS = Patients.Patients_base()
if unsuccess is not None:
    for i in range(len(unsuccess)):
        Patients_VIMIS.add_volume(Number=None,
                                  Code=unsuccess[i][0],
                                  mom_FIO=None,
                                  child_FIO=None,
                                  uniqueNumber=None,
                                  date=None,
                                  birth_date=None,
                                  take_time=None)
with open(File, "r", encoding="UTF-8") as f:
    text = f.read().split("\n")
    for i in range(len(text)):
        text[i] = text[i].split(";")
        if len(text[i]) == 9:  # Если чего-то не хватает, то пропускаем
            if unsuccess is not None:
                try:
                    if int(text[i][1]) in Patients_VIMIS.Code:
                        print(f"in unsuccess: {text[i][1]}")
                        pass
                    else:
                        print(f"not in unsuccess: {text[i][1]}")
                        continue
                except:
                    pass
            Patients_Base.add_volume(
                Number=text[i][0],
                Code=text[i][1],
                date=text[i][2],
                mom_FIO=text[i][3],
                child_FIO=text[i][4],
                uniqueNumber=text[i][5],
                birth_date=text[i][7],
                take_time=text[i][8])  # Добавляем пациентов во хранилище

# Для открытия скрытых рутов
def shadow_root_open(element):
    try:
        root = driver.execute_script('return arguments[0].shadowRoot', element)
        return root
    except Exception as e:
        traceback.print_exc()


# Функция для записи ошибок
def error_write(file_name, i, message):
    try:
        os.mkdir(directory + "Errors")
    except:
        pass
    try:
        with open(f"{directory}/Errors/{file_name}.txt", "r") as f:
            text = f.read()
    except:
        text = ""
    with open(f"{directory}/Errors/{file_name}.txt", "w") as f:
        f.write(text)
        f.write("\n")
        f.write(str(Patients_Base.Number[i]))
        f.write(";")
        f.write(str(Patients_Base.Code[i]))
        f.write(";")
        f.write(str(Patients_Base.date[i]))
        f.write(";")
        f.write(message)


# Функция для записи успешных
def success_write(file_name, i):
    try:
        os.mkdir(directory + "Success")
    except:
        pass
    try:
        with open(f"{directory}/Success/{file_name}.txt", "r") as f:
            text = f.read()
    except:
        text = ""
    with open(f"{directory}/Success/{file_name}.txt", "w") as f:
        f.write(text)
        f.write(str(Patients_Base.Number[i]))
        f.write(";")
        f.write(str(Patients_Base.Code[i]))
        f.write(";")
        f.write("\n")
    if Laboratory_CODE == 1:
        search = "ТМС"
    elif Laboratory_CODE == 2:
        search = "ПЦР"
    try:
        with open(f"{directory}/{search}_успешные.txt", "r") as f:
            uspeshnie = f.read()
    except:
        uspeshnie = ""
    with open(f"{directory}/{search}_успешные.txt", "w") as f:
        f.write(uspeshnie)
        f.write(str(Patients_Base.Number[i]))
        f.write(";")
        f.write(str(Patients_Base.Code[i]))
        f.write(";")
        f.write("\n")


# Инициализируем брауер
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

# пробуем попасть на вимис
driver.get('https://vimis.egisz.rosminzdrav.ru/#patients_akineo.nns_list')
time.sleep(10)
# Ждем авторизации
while True:
    if "https://vimis.egisz.rosminzdrav.ru/" not in driver.current_url:
        time.sleep(1)
    else:
        break

time.sleep(1)

for i in range(len(Patients_Base.Code)):
    try:
        # проверяем длину штрихкода
        if len(str(Patients_Base.Code[i])) != 19:
            print(len(str(Patients_Base.Code)))
            error_write(file_name=formatted_date, i=i, message="Штрих-код короче 19 символов")
            continue
        Code = str(Patients_Base.Code[i])[-10:]
        driver.get('https://vimis.egisz.rosminzdrav.ru/#patients_akineo.nns_list')
        time.sleep(10)
        shadow_root = []
        shadow_root.append(shadow_root_open(driver.find_element(By.CLASS_NAME, "nf-form-instance")))
        shadow_root.append(shadow_root_open(shadow_root[0].find_element(By.ID, "mainForm")))
        shadow_root.append(shadow_root_open(shadow_root[1].find_element(By.ID, "formManager")))
        shadow_root.append(shadow_root_open(shadow_root[2].find_element(By.CSS_SELECTOR, "nf-form-thread")))
        shadow_root.append(
            shadow_root_open(shadow_root[3].find_element(By.CSS_SELECTOR, "nf-form-patients_akineo·nns_list")))
        shadow_root.append(shadow_root_open(shadow_root[4].find_element(By.CSS_SELECTOR, "nf-react-component")))
        element = shadow_root[5]
        print(Code)
        input_field = element.find_element(By.ID, "neoScreeningTopFilterNew_medBirthCertificateNumber")
        for t in range(25):
            input_field.send_keys(Keys.BACKSPACE)
        input_field.send_keys(Code)
        element.find_element(By.CLASS_NAME, "ant-btn-primary").click()
        time.sleep(5)
        table = element.find_element(By.CSS_SELECTOR, "table")
        table_elements = table.find_elements(By.CSS_SELECTOR, "tr")

        if len(table_elements) < 2:
            error_write(file_name=formatted_date, i=i, message="По данному штрих-коду не найдены елементы")
            continue

        if len(table_elements) >= 2:
            for j in range(1, len(table_elements)):
                table_elements_line = table_elements[j].find_elements(By.CSS_SELECTOR, "td")
                for k in range(len(table_elements_line)):
                    current_element = table_elements_line[k].get_attribute('textContent')
                    PLI = None
                    if current_element == str(Patients_Base.Code[i]):
                        print(str(
                            f"Найдено совпадение по штрих-коду:\n" +
                            current_element +
                            f" {Patients_Base.Code[i]}"
                        ))
                        PLI = True
                    MSR = str(Patients_Base.uniqueNumber[i])[:2] + " " + str(Patients_Base.uniqueNumber[i])[2:]
                    print(MSR)
                    if current_element == MSR:
                        print(str(
                            f"Найдено совпадение по МСР:\n" +
                            current_element +
                            f" {Patients_Base.Code[i]}"
                        ))
                        PLI = True
                    if PLI is True:

                        table_elements[j].find_element(By.CLASS_NAME, "triangle-down-m-solid").click()
                        time.sleep(2)
                        table = element.find_element(By.CLASS_NAME, "ant-dropdown-menu-vertical")
                        table_elements = table.find_elements(By.CSS_SELECTOR, "li")
                        table_elements[1].click()  # Нажимаем на ПЛИ
                        time.sleep(3)
                        shadow_root.append(
                            shadow_root_open(shadow_root[2].find_element(By.CLASS_NAME, "iron-selected")))
                        shadow_root.append(
                            shadow_root_open(shadow_root[6].find_element(By.CLASS_NAME, "iron-selected")))
                        shadow_root.append(
                            shadow_root_open(shadow_root[7].find_element(By.CSS_SELECTOR, "react-external-forms")))
                        shadow_root[8].find_element(By.ID, "neonatal-screening_labProfileCode").click()
                        table = shadow_root[8].find_element(By.CLASS_NAME, "rc-virtual-list-holder-inner")
                        table_elements = table.find_elements(By.CLASS_NAME, "ant-select-item")
                        print(f"Выберется {Laboratory_CODE + 1} код лабораторного профиля")
                        time.sleep(1)
                        table_elements[Laboratory_CODE].click()
                        time.sleep(0.4)
                        shadow_root[8].find_element(By.CLASS_NAME, "justify-content-center").click()
                        time.sleep(2)

                        sticky_filter = shadow_root[8].find_element(By.CLASS_NAME, "sticky-filter")
                        sticky_filter.find_element(By.CLASS_NAME, "ant-select-selection-search-input").click()
                        table = sticky_filter.find_element(By.CLASS_NAME, "rc-virtual-list-holder-inner")
                        table_elements = table.find_elements(By.CLASS_NAME, "ant-select-item")
                        table_elements[0].click()
                        table = sticky_filter.find_element(By.CLASS_NAME, "x6")
                        interpreter = table.find_element(By.CLASS_NAME, "ant-select-selection-search-input")
                        interpreter.send_keys("Нормальный (в пределах референсного диапазона)")
                        interpreter.send_keys(Keys.ENTER)
                        data_input = sticky_filter.find_element(By.CLASS_NAME, "ant-picker-input")
                        data_input.find_element(By.CSS_SELECTOR, "input").send_keys(Patients_Base.date[i])
                        time.sleep(1)
                        time_table = sticky_filter.find_element(By.CLASS_NAME, "ant-picker-panel-container")
                        time_table.find_element(By.CLASS_NAME, "ant-btn-primary").click()
                        button = sticky_filter.find_element(By.CLASS_NAME, "btn-wrap")
                        button.find_element(By.CSS_SELECTOR, "button").click()
                        sticky_bottom = shadow_root[8].find_element(By.CLASS_NAME, "sticky-bottom")
                        buttons = sticky_bottom.find_elements(By.CLASS_NAME, "ant-form-item-control")
                        time.sleep(3)
                        buttons[1].click()
                        shadow_root_exit = []
                        time.sleep(6)
                        shadow_root_exit.append(
                            shadow_root_open(driver.find_element(By.CLASS_NAME, "nf-form-instance")))
                        shadow_root_exit.append(shadow_root_open(shadow_root_exit[0].find_element(By.ID, "mainForm")))
                        shadow_root_exit.append(
                            shadow_root_open(shadow_root_exit[1].find_element(By.ID, "formManager")))
                        shadow_root_exit.append(
                            shadow_root_open(shadow_root_exit[2].find_element(By.CLASS_NAME, "iron-selected")))
                        shadow_root_exit.append(
                            shadow_root_open(shadow_root_exit[3].find_element(By.CLASS_NAME, "nf-form-instance")))
                        shadow_root_exit.append(
                            shadow_root_open(shadow_root_exit[4].find_element(By.CSS_SELECTOR, "react-external-forms")))
                        sticky_bottom = shadow_root_exit[5].find_element(By.CLASS_NAME, "sticky-bottom")
                        buttons = sticky_bottom.find_elements(By.CLASS_NAME, "btn-wrap")
                        buttons[1].click()

                        success_write(file_name=formatted_date, i=i)
                        continue
                    else:
                        error_write(file_name=formatted_date, i=i, message="Не найдено направление")

    except:
        # Get the traceback as a string
        traceback_str = traceback.format_exc()

        # Print the traceback
        print(traceback_str)
        error_write(file_name=formatted_date, i=i, message="Плохое соединение с ВИМИС")
print("End")