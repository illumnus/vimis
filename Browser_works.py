import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from chromedriver_py import binary_path  # this will get you the path variable
import traceback


class On_vimis_work:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        svc = webdriver.ChromeService(executable_path=binary_path)
        self.driver = webdriver.Chrome(options=options, service=svc)
        self.by_list = [By.ID, By.CSS_SELECTOR, By.CLASS_NAME]
        self.shadow_root = []
        self.Codes = []
        self.Dates = []
        self.investigation = None
        self.investigation_index = None

    def shadow_root_open(self, element):
        try:
            root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            return root
        except Exception as e:
            traceback.print_exc()

    def VIMIS_login(self):
        self.driver.get('https://vimis.egisz.rosminzdrav.ru/#patients_akineo.nns_list')
        for i in range(2):
            try:
                self.driver.find_element(By.ID, "details-button").click()
                time.sleep(1)
                self.driver.find_element(By.ID, "proceed-link").click()
                break
            except:
                time.sleep(2)
        for i in range(2):
            try:
                self.driver.find_element(By.ID, "login").send_keys("89899557610")
                self.driver.find_element(By.ID, "password").send_keys("Qn:e~SS1l4")
                self.driver.find_element(By.CLASS_NAME, "plain-button_wide").click()
                break
            except:
                time.sleep(1)
        for i in range(2):
            try:
                abstract_request_information = self.driver.find_element(By.CLASS_NAME,
                                                                        "abstract-request-information__text")
                if "2 цифры номера" in abstract_request_information.text:
                    self.driver.find_element(By.CLASS_NAME, "input__field").send_keys("87")
                break
            except:
                time.sleep(1)
        for i in range(2):
            try:
                self.driver.find_element(By.CLASS_NAME, "plain-button-inline").click()
                return
            except:
                time.sleep(1)

    def open_shadow_roots_on_main_list(self):
        for i in range(15):
            try:
                self.shadow_root = []
                self.shadow_root.append(
                    self.shadow_root_open(self.driver.find_element(By.CLASS_NAME, "nf-form-instance")))
                self.shadow_root.append(self.shadow_root_open(self.shadow_root[0].find_element(By.ID, "mainForm")))
                self.shadow_root.append(self.shadow_root_open(self.shadow_root[1].find_element(By.ID, "formManager")))
                self.shadow_root.append(
                    self.shadow_root_open(self.shadow_root[2].find_element(By.CSS_SELECTOR, "nf-form-thread")))
                self.shadow_root.append(self.shadow_root_open(
                    self.shadow_root[3].find_element(By.CSS_SELECTOR, "nf-form-patients_akineo·nns_list")))
                self.shadow_root.append(
                    self.shadow_root_open(self.shadow_root[4].find_element(By.CSS_SELECTOR, "nf-react-component")))
                return
            except:
                time.sleep(1)
                print(f"Попытка открытия формы №{i}. Без результата.")

    def all_fields_on(self):
        for i in range(15):
            try:
                time.sleep(1)
                root = self.shadow_root[5]
                root_panel = root.find_element(By.CLASS_NAME, "root-options-panel")
                root_filter_icons = root_panel.find_element(By.CLASS_NAME, "root-filter-icons")
                root_filter_icons.click()
                time.sleep(1)
                root_table = root.find_element(By.CLASS_NAME, "root-table")
                tco_top_wrapper = root_table.find_element(By.CLASS_NAME, "tco-top")
                switch = tco_top_wrapper.find_element(By.CLASS_NAME, "root-switch")
                switch_state = switch.find_element(By.CLASS_NAME, "ant-switch")
                #print(f"switch_state{switch_state.get_attribute('aria-checked')}")
                if switch_state.get_attribute("aria-checked") == "false":
                    switch.click()
                return
            except:
                time.sleep(1)

    def find_index_of_investigation(self):
        for i in range(15):
            try:
                root = self.shadow_root[5]
                table_head = root.find_element(By.CLASS_NAME, "ant-table-thead")
                table_head_elements = table_head.find_elements(By.CSS_SELECTOR, "th")
                for i in range(len(table_head_elements)):
                    if table_head_elements[i].find_element(By.CSS_SELECTOR, "p").text == "Дата результата МГИ":
                        if self.investigation == "PCR":
                            self.investigation_index = i
                    elif table_head_elements[i].find_element(By.CSS_SELECTOR, "p").text == "Дата результата ТМС":
                        if self.investigation == "BH":
                            self.investigation_index = i
                return
            except:
                time.sleep(1)

    def check_if_investigation_exists(self):
        time.sleep(5)
        root = self.shadow_root[5]
        for i in range(15):
            try:
                table = root.find_element(By.CLASS_NAME, "ant-table-tbody")
                line = table.find_element(By.CLASS_NAME, "ant-table-row-level-0")
                rows = line.find_elements(By.CLASS_NAME, "ant-table-cell")
                if rows[self.investigation_index].text == "":
                    return True
                else:
                    return rows[self.investigation_index].text
            except:
                try:
                    root.find_element(By.CLASS_NAME, "empty-data-table")
                    return "NotFound"
                except:
                    time.sleep(1)

    def find_patient(self, i):
        for j in range(15):
            try:
                element = self.shadow_root[5]
                #print(i)
                input_field = element.find_element(By.ID, "neoScreeningTopFilterNew_extNumber")
                for t in range(35):
                    input_field.send_keys(Keys.BACKSPACE)
                input_field.send_keys(self.Codes[i])
                element.find_element(By.CLASS_NAME, "ant-btn-primary").click()
                return
            except:
                time.sleep(1)

    def PLI_click(self):
        for i in range(15):
            try:
                root = self.shadow_root[5]
                table = root.find_element(By.CLASS_NAME, "ant-table-tbody")
                lines = table.find_elements(By.CLASS_NAME, "ant-table-row-level-0")
                if len(lines) == 1:
                    rows = lines[0].find_elements(By.CLASS_NAME, "ant-table-cell")
                    rows[0].find_element(By.CLASS_NAME, "triangle-down-m-solid").click()
                    time.sleep(1)
                    table = root.find_element(By.CLASS_NAME, "ant-dropdown-menu-vertical")
                    table_elements = table.find_elements(By.CSS_SELECTOR, "li")
                    table_elements[1].click()
                    return
            except:
                time.sleep(1)

    def PLI_shadow_root_open(self):
        for i in range(15):
            try:
                self.shadow_root.append(
                    self.shadow_root_open(self.shadow_root[2].find_element(By.CLASS_NAME, "iron-selected")))
                self.shadow_root.append(
                    self.shadow_root_open(self.shadow_root[7].find_element(By.CLASS_NAME, "iron-selected")))
                self.shadow_root.append(
                    self.shadow_root_open(self.shadow_root[8].find_element(By.CSS_SELECTOR, "react-external-forms")))
                return
            except Exception as e:
                print(e)
                time.sleep(1)

    def click_on_investigation_CODE(self):
        for i in range(15):
            try:
                root = self.shadow_root[9]
                root.find_element(By.ID, "neonatal-screening_labProfileCode").click()
                table = root.find_element(By.CLASS_NAME, "rc-virtual-list-holder-inner")
                table_elements = table.find_elements(By.CLASS_NAME, "ant-select-item")
                time.sleep(1)
                if self.investigation == "PCR":
                    table_elements[2].click()
                elif self.investigation == "BH":
                    table_elements[1].click()
                return
            except:
                time.sleep(1)

    def fill_the_normal(self, i):
        stages = [False for i in range(5)]
        for j in range(15):
            print(stages)
            try:
                root = self.shadow_root[9]
                if stages[0] is False:
                    root.find_element(By.CLASS_NAME, "justify-content-center").click()
                    stages[0] = True
                if stages[1] is False:
                    sticky_filter = root.find_element(By.CLASS_NAME, "sticky-filter")
                    sticky_filter.find_element(By.CLASS_NAME, "ant-select-selection-search-input").click()
                    table = sticky_filter.find_element(By.CLASS_NAME, "rc-virtual-list-holder-inner")
                    table_elements = table.find_elements(By.CLASS_NAME, "ant-select-item")
                    table_elements[0].click()
                    stages[1] = True
                if stages[2] is False:
                    table = sticky_filter.find_element(By.CLASS_NAME, "x6")
                    interpreter = table.find_element(By.CLASS_NAME, "ant-select-selection-search-input")
                    interpreter.send_keys("Нормальный (в пределах референсного диапазона)")
                    interpreter.send_keys(Keys.ENTER)
                    stages[2] = True
                if stages[3] is False:
                    data_input = sticky_filter.find_element(By.CLASS_NAME, "ant-picker-input")
                    data_input.find_element(By.CSS_SELECTOR, "input").send_keys(self.Dates[i])
                    time_table = sticky_filter.find_element(By.CLASS_NAME, "ant-picker-panel-container")
                    time_table.find_element(By.CLASS_NAME, "ant-btn-primary").click()
                    stages[3] = True
                if stages[4] is False:
                    button = sticky_filter.find_element(By.CLASS_NAME, "btn-wrap")
                    button.find_element(By.CSS_SELECTOR, "button").click()
                    stages[4] = True
                print("fill_the_normal success")
                return
            except Exception as e:
                print(e)
                time.sleep(1)

    def submit_the_normal(self):
        for i in range(15):
            try:
                root = self.shadow_root[9]
                sticky_bottom = root.find_element(By.CLASS_NAME, "sticky-bottom")
                buttons = sticky_bottom.find_elements(By.CLASS_NAME, "ant-form-item-control")
                time.sleep(3)
                buttons[1].click()
                print("submit_the_normal success")
                return
            except:
                time.sleep(1)

    def exit_the_normal(self):
        for i in range(20):
            try:
                shadow_root_exit = []
                time.sleep(6)
                shadow_root_exit.append(
                    self.shadow_root_open(self.driver.find_element(By.CLASS_NAME, "nf-form-instance")))
                shadow_root_exit.append(self.shadow_root_open(shadow_root_exit[0].find_element(By.ID, "mainForm")))
                shadow_root_exit.append(
                    self.shadow_root_open(shadow_root_exit[1].find_element(By.ID, "formManager")))
                shadow_root_exit.append(
                    self.shadow_root_open(shadow_root_exit[2].find_element(By.CLASS_NAME, "iron-selected")))
                shadow_root_exit.append(
                    self.shadow_root_open(shadow_root_exit[3].find_element(By.CLASS_NAME, "nf-form-instance")))
                shadow_root_exit.append(
                    self.shadow_root_open(shadow_root_exit[4].find_element(By.CSS_SELECTOR, "react-external-forms")))
                sticky_bottom = shadow_root_exit[5].find_element(By.CLASS_NAME, "sticky-bottom")
                buttons = sticky_bottom.find_elements(By.CLASS_NAME, "btn-wrap")
                buttons[1].click()
                print("exit_the_normal success")
                return
            except:
                time.sleep(1)


if __name__ == "__main__":
    simple = On_vimis_work()
    simple.VIMIS_login()
    simple.open_shadow_roots_on_main_list()
    simple.all_fields_on()
    simple.find_index_of_investigation()

    result = simple.check_if_investigation_exists()
    if result is True:
        pass
    elif result is False:
        pass
    elif result == "NotFound":
        pass
    input()
