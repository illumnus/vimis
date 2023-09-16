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
        self.PCR_index = None
        self.BH_index = None

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
                self.driver.find_element(By.CLASS_NAME, "anomaly__button").click()
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
                        self.PCR_index = i
                    elif table_head_elements[i].find_element(By.CSS_SELECTOR, "p").text == "Дата результата ТМС":
                        self.BH_index = i
                print(f"self.PCR_index: {self.PCR_index}, self.BH_index: {self.BH_index}")
                return
            except:
                time.sleep(1)

    def check_if_investigation_exists(self):
        root = self.shadow_root[5]
        for i in range(15):
            try:
                table = root.find_element(By.CLASS_NAME, "ant-table-tbody")
                lines = table.find_elements(By.CLASS_NAME, "ant-table-row-level-0")
                for j in range(len(lines)):
                    rows = lines[j].find_elements(By.CLASS_NAME, "ant-table-cell")
                    text = ""
                    for k in range(len(rows)):
                        text = text + f"{k}:{rows[k].text}\t"
                    print(text)
            except:
                try:
                    root.find_element(By.CLASS_NAME, "empty-data-table")
                    return False
                except:
                    time.sleep(1)

    def find_patient(self, i):
        element = self.shadow_root[5]
        print(i)
        input_field = element.find_element(By.ID, "neoScreeningTopFilterNew_extNumber")
        for t in range(25):
            input_field.send_keys(Keys.BACKSPACE)
            break
        input_field.send_keys(self.Codes[i])
        self.driver.find_element(By.CLASS_NAME, "ant-btn-primary").click()


if __name__ == "__main__":
    simple = On_vimis_work()
    simple.VIMIS_login()
    simple.open_shadow_roots_on_main_list()
    simple.all_fields_on()
    simple.find_index_of_investigation()
    simple.check_if_investigation_exists()
    input()
