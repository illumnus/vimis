import os
import sys
import Files_Work
import Patients
import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium_stealth import stealth
import traceback
import time
from selenium.webdriver.common.keys import Keys

# Создаем пустую базу добавляемых пациентов
Patients_Base = Patients.Patients_base()

# Проверяем наличие текстовых файлов, которые сгенерировал 1С в рабочей директории программы
directory = "C:/результат/"  # рабочая директория программы по умолчанию для 1.0 версии программы
File, Laboratory_CODE = Files_Work.get_text_file_paths(directory=directory)
if Laboratory_CODE == "ТМС":
    Laboratory_CODE = 1
elif Laboratory_CODE == "ПЦР":
    Laboratory_CODE = 2
elif Laboratory_CODE == None:
    pass

print(f"Laboratory_CODE: {Laboratory_CODE}")
input()
if File is None:
    print("Не найден файл!")
    time.sleep(5)
    sys.exit()  # если файл не один или его нет - прекратить выполнение программы
current_date = datetime.date.today()  # получаем сегодняшнюю дату
formatted_date = current_date.strftime("%Y-%m-%d")  # формтируем год-месяц-день
print(f"текущая дата: {formatted_date}") #получаем сегодняшнюю дату - для записи
print(File)


with open(File, "r", encoding="UTF-8") as f:
    text = f.read().split("\n")
    for i in range(len(text)):
        text[i] = text[i].split(";")
        if len(text[i]) == 8:  # Если чего-то не хватает, то пропускаем
            Patients_Base.add_volume(
                Number=text[i][0],
                Code=text[i][1],
                mom_FIO=text[i][2],
                child_FIO=text[i][3],
                uniqueNumber=text[i][4],
                date=text[i][5],
                birth_date=text[i][6],
                take_time=text[i][7])  # Добавляем пациентов во хранилище


# Для открытия скрытых рутов
def shadow_root_open(element):
    try:
        root = driver.execute_script('return arguments[0].shadowRoot', element)
        return root
    except Exception as e:
        traceback.print_exc()

#Функция для записи ошибок
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

#Функция для записи успешных
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
# Для скрытности
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


#пробуем попасть на вимис
driver.get('https://vimis.egisz.rosminzdrav.ru/#patients_akineo.nns_list')
time.sleep(10)
#Ждем авторизации
while True:
    if "https://vimis.egisz.rosminzdrav.ru/" not in driver.current_url:
        time.sleep(1)
    else:
        break

time.sleep(1)

#Проходим 10 пациентов - в качестве теста
for i in range(10):
    try:
        #проверяем длину штрихкода
        if len(str(Patients_Base.Code[i])) != 19:
            print(len(str(Patients_Base.Code)))
            error_write(file_name=formatted_date, i=i, message="Штрих-код короче 19 символов")
            continue
        Code = str(Patients_Base.Code[i])[-10:]
        driver.get('https://vimis.egisz.rosminzdrav.ru/#patients_akineo.nns_list')
        time.sleep(10)#10
        shadow_root = []
        shadow_root.append(shadow_root_open(driver.find_element(By.CLASS_NAME, "nf-form-instance")))
        shadow_root.append(shadow_root_open(shadow_root[0].find_element(By.ID, "mainForm")))
        shadow_root.append(shadow_root_open(shadow_root[1].find_element(By.ID, "formManager")))
        shadow_root.append(shadow_root_open(shadow_root[2].find_element(By.CSS_SELECTOR, "nf-form-thread")))
        shadow_root.append(shadow_root_open(shadow_root[3].find_element(By.CSS_SELECTOR, "nf-form-patients_akineo·nns_list")))
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
                    if current_element == str(Patients_Base.Code[i]):
                        print(str(
                            f"Найдено совпадение по штрих-коду:\n" +
                            current_element +
                            f" {Patients_Base.Code[i]}"
                        ))
                        for l in range(len(table_elements_line)):
                            current_element2 = table_elements_line[l].get_attribute('textContent')
                            if str(Patients_Base.Code[i])[-10:] in current_element2:
                                print()
                                print("clicked")
                                time.sleep(10)

    except Exception as e:

        # Get the traceback as a string
        traceback_str = traceback.format_exc()

        # Print the traceback
        print(traceback_str)
        error_write(file_name=formatted_date, i=i, message="Плохое соединение с ВИМИС")
print("End")