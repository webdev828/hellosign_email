import os
import logging
import random
import sys
import time
import uuid
import glob
import shutil
import warnings
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from configparser import RawConfigParser


warnings.filterwarnings("ignore", category=DeprecationWarning)

WORKING_DIRECTORY = "workflow_{}".format(datetime.now().strftime('%Y_%m_%d'))
DATA_FILE = os.path.join(os.getcwd(), 'list.txt')
TITLE_FILE = os.path.join(os.getcwd(), 'title.txt')
RECORD_HEADER = "name,email_address,pin"
RECORD_FORMATTER = "user,{},"

root = logging.getLogger()
root.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

filehandler = logging.FileHandler(os.path.join(os.getcwd(), '{}.log'.format(WORKING_DIRECTORY)))
filehandler.setLevel(logging.INFO)
filehandler.setFormatter(formatter)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
root.addHandler(handler)
root.addHandler(filehandler)


class Config:
    """
    Configuration class to store all the env vars
    """

    def __init__(self):

        self.configparser = RawConfigParser()
        self.configparser.read('config.properties')
        self.driver = os.getenv('DRIVER_TYPE', 'driver/geckodriver.exe')

        self.domain = self.configparser.get('AppConf', 'domain')
        self.username = self.configparser.get('AppConf', 'username')
        self.password = self.configparser.get('AppConf', 'password')
        self.headless = self.configparser.getboolean('AppConf', 'headless')
        self.limit = self.configparser.getint('AppConf', 'limit')
        self.timeout = self.configparser.getint('AppConf', 'timeout')
        self.template = self.configparser.get('AppConf', 'template')
        self.firstname = self.configparser.get('AppConf', 'firstname')
        self.lastname = self.configparser.get('AppConf', 'lastname')
        self.message = self.configparser.get('AppConf', 'message')


config = Config()


def replace_tags(str1):
    str1 = str1.replace("##date##", datetime.today().strftime('%m/%d/%Y'))
    str1 = str1.replace("##number##", str(random.randint(10000, 1000000)))

    return str1


def write_csv(file_name, header, records):
    with open(os.path.join(WORKING_DIRECTORY, file_name), 'w') as new_file:
        new_file.write(header+'\n')
        for record in records:
            new_file.write(record+'\n')


def generate_csv():

    with open(DATA_FILE) as f:
        records = f.readlines()

        record_counter = 1
        record_file = []
        for record in records:
            if 1 <= record_counter < config.limit:
                record_file.append(RECORD_FORMATTER.format(record.replace('\n', '').strip()))
                record_counter += 1
            elif record_counter == config.limit:
                record_file.append(RECORD_FORMATTER.format(record.replace('\n', '').strip()))
                file_id = uuid.uuid4()
                write_csv('{}.csv'.format(file_id), RECORD_HEADER, record_file)
                logging.info("CSV file {} created with users {}".format("{}.csv".format(file_id), record_file))
                record_file = []
                record_counter = 1

        if len(record_file) != 0:
            file_id = uuid.uuid4()
            write_csv('{}.csv'.format(file_id), RECORD_HEADER, record_file)
            logging.info("CSV file {} created with users {}".format("{}.csv".format(file_id), record_file))


def process_csv(file_name, title):

    options = Options()
    options.headless = config.headless
    browser = webdriver.Firefox(options=options, executable_path=config.driver)

    browser.get(config.domain)

    time.sleep(5)

    WebDriverWait(browser, config.timeout).until(
        EC.presence_of_element_located((By.NAME, 'logIn.emailAddress'))
    )

    browser.find_element_by_name('logIn.emailAddress').send_keys(config.username)

    browser.find_element_by_class_name('l-nowrap').click()

    WebDriverWait(browser, config.timeout).until(
        EC.presence_of_element_located((By.NAME, 'logIn.password'))
    )

    browser.find_element_by_name('logIn.password').send_keys(config.password)

    browser.find_element_by_class_name('l-nowrap').click()

    WebDriverWait(browser, config.timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'dig-Button-content'))
    )

    WebDriverWait(browser, config.timeout).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'dig-Button-content'))
    )

    browser.find_elements_by_class_name('dig-Button-content')[1].click()

    time.sleep(4)

    WebDriverWait(browser, config.timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'src-hellospa-components-prep-and-'
                                                       'send-file-uploader-styles__buttonsContainer--ULZm_'))
    )

    browser.find_element_by_class_name('src-hellospa-components-prep-and-send-file'
                                       '-uploader-styles__buttonsContainer--ULZm_').click()

    WebDriverWait(browser, config.timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'src-hellospa-components-prep-and-send'
                                                       '-template-picker-styles__templateItem--1yJXu'))
    )

    templates = browser.find_elements_by_class_name('src-hellospa-components-prep-and-send'
                                                    '-template-picker-styles__templateItem--1yJXu')

    time.sleep(4)

    template_name = ''
    for template in templates:

        if template.text.strip() == config.template:
            template_name = template.text.strip()
            template.click()
            break

    if template_name == '':
        raise Exception("Template not found")

    buttons = browser.find_elements_by_css_selector('button')

    time.sleep(5)

    for button in buttons:
        if button.text.strip() == 'Next':
            button.click()
            break

    time.sleep(3)

    browser.find_element_by_css_selector("input[type=file]").send_keys(file_name)

    buttons = browser.find_elements_by_css_selector('button')

    time.sleep(5)

    for button in buttons:
        if button.text.strip() == 'Next':
            button.click()
            break

    time.sleep(3)

    try:
        browser.find_element_by_id('document.firstname').send_keys(config.firstname)
    except:
        pass

    try:
        browser.find_element_by_id('document.lastname').send_keys(config.lastname)
    except:
        pass

    try:
        browser.find_element_by_id('document.message').send_keys(replace_tags(config.message))
    except:
        pass

    try:
        browser.find_element_by_id('document.title').clear()
        browser.find_element_by_id('document.title').send_keys(replace_tags(title))
    except:
        pass

    browser.find_element_by_class_name('src-hellospa-components-stepper-stepper__longText--3cdGt').click()

    WebDriverWait(browser, config.timeout).until(
        EC.presence_of_element_located((By.ID, 'bulk'))
    )

    time.sleep(10)

    browser.quit()


def create_workflow_dir():
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, WORKING_DIRECTORY)
    if os.path.exists(os.path.join(current_directory, 'prev_run')):
        shutil.rmtree(os.path.join(current_directory, 'prev_run'))
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
        os.makedirs(os.path.join(final_directory, 'processed'))
        os.makedirs(os.path.join(final_directory, 'errors'))
    else:
        shutil.move(final_directory, os.path.join(current_directory, 'prev_run'))
        os.makedirs(final_directory)
        os.makedirs(os.path.join(final_directory, 'processed'))
        os.makedirs(os.path.join(final_directory, 'errors'))


def move_file(file_path, destination):
    shutil.move(file_path, destination)


def start_workflow():

    # Initial step creating directories

    create_workflow_dir()

    # Check if input files are present

    if os.path.isfile(DATA_FILE) is not True:
        raise Exception("Data file not found. Please add a list.txt with emails to root folder.")

    if os.path.isfile(TITLE_FILE) is not True:
        raise Exception("File with titles not found. Please add title.txt with titles to root folder.")

    # Read DATA file and build CSVs
    generate_csv()

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, WORKING_DIRECTORY)

    # Start processing CSV
    file_list = glob.glob("{}/*.csv".format(final_directory))

    # Read titles

    titles = open(TITLE_FILE).readlines()
    title_index = 0

    for indv_file in file_list:

        try:
            if title_index == len(titles):
                title_index = 0

            process_csv(indv_file, titles[title_index])
            move_file(indv_file, os.path.join(final_directory, 'processed'))
            logging.info("CSV file {} processed and moved to processed".format(indv_file))

            title_index += 1

        except Exception as e:
            move_file(indv_file, os.path.join(final_directory, 'errors'))
            logging.error(e)
            logging.info("CSV file {} processed and moved to err0r".format(indv_file))


if __name__ == "__main__":
    start_workflow()
