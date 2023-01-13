from seleniumwire import webdriver
import time


options = {
'proxy': {
    'http': 'http://owlshopchecker:pallushort@geo.iproyal.com:12323',
    'https': 'http://owlshopchecker:pallushort@geo.iproyal.com:12323',
    'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
    }
}

'''
options = {
'proxy': {
    'http': 'http://fnjiaucp-rotate:745b5cvkac1z@p.webshare.io:80',
    'https': 'http://fnjiaucp-rotate:745b5cvkac1z@p.webshare.io:80',
    'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
    }
}
'''
driver = webdriver.Firefox(seleniumwire_options=options, executable_path="driver/geckodriver.exe")
driver.get("https://www.whatismyip.com")

time.sleep(666)