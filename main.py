import os
import sys
import time

import Browser_works
import Files_Work
import Patients
import datetime

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


main_browser = Browser_works.On_vimis_work()
main_browser.Dates = Patients_Base.date
main_browser.Codes = Patients_Base.Code
main_browser.driver.get('https://vimis.egisz.rosminzdrav.ru/#patients_akineo.nns_list')
if Laboratory_CODE == 1:
    main_browser.investigation = "BH"
elif Laboratory_CODE == 2:
    main_browser.investigation = "PCR"
#main_browser.VIMIS_login()

while True:
    print("ожидание перехода на сайт")
    time.sleep(5)
    if "https://vimis.egisz.rosminzdrav.ru/#patients_akineo.nns_list" == main_browser.driver.current_url:
        print("Вы перешли на сайт. Начинаю работу.......")
        break

def cycle(i):
    if len(str(main_browser.Codes[i])) != 19:
        print(f"длина штрихкода {Patients_Base.Code[i]} не равна 19 символам! Пропускаю........")
        return
    main_browser.open_shadow_roots_on_main_list()
    main_browser.all_fields_on()
    main_browser.find_index_of_investigation()
    main_browser.find_patient(i=i)
    result = main_browser.check_if_investigation_exists()
    if result is True:
        main_browser.PLI_click()
        main_browser.PLI_shadow_root_open()
        main_browser.click_on_investigation_CODE()
        main_browser.fill_the_normal(i=i)
        main_browser.submit_the_normal()
        main_browser.exit_the_normal()
        success_write(file_name=formatted_date, i=i)
        print(f"Для {Patients_Base.Code[i]} успешно создана запись")
        return
    elif result is not True:
        print(f"Для {Patients_Base.Code[i]} уже имеется запись от {result}")
        success_write(file_name=formatted_date, i=i)
        return
    elif result == "NotFound":
        print(f"Для {Patients_Base.Code[i]} не найдено направление.")
        error_write(file_name=formatted_date, i=i, message="Не найдено направление")


for i in range(len(Patients_Base.Code)):
    cycle(i=i)

print("End")
