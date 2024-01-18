import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys


def third_website():
    html_text = requests.get('https://karriere.akad.de/').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs_info = soup.find_all('div', class_='joboffer_container')
    job_title = []
    links = []
    for i in jobs_info:
        job_title.append(i.find('a').text)
        links.append(i.find('a',href=True)['href'])
    loc_info = soup.find_all('div', class_='joboffer_informations joboffer_box')
    location = []
    for i in loc_info:
        location.append(i.text)
    additional_info = []
    for link in links:
        html = requests.get(link).text
        s = BeautifulSoup(html, 'lxml')
        try:
            dept_info = s.find_all('ul', class_='scheme-additional-data')
            #dept = dept_info.split(',')
            complete_info = ''
            # for dept in dept_info:
            #     complete_info = complete_info + (dept.text) + " "
            #     if('map-marker' in dept):
            # if(complete_info == ''):
            #     complete_info = 'No additional info'
            # additional_info.append(complete_info)
        except:
            print("No additional info")
    # for i in range(len(job_title)):
    #     print(job_title[i])
    #     print(location[i])
    #     print(additional_info[i])
    #     print()

def second_website():
    html_text = requests.get('https://www.berlin-international.de/hochschule/stellenangebote/').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs_info = soup.find('div', class_='col-lg-12 col-md-12 col-sm-12 col-xs-12 del-padding page-content link-effect')
    jobs = jobs_info.find_all('li')
    job_title = []
    for i in jobs:
        job_title.append(i.text)

def get_info(driver,job_title,location,job_type,hiring_institute,job_level):
    wait = WebDriverWait(driver, 10)
    div_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"title")))
    for ele in div_elements:
        ele_html = ele.get_attribute("outerHTML")
        soup = BeautifulSoup(ele_html, 'lxml')
        job_title.append(soup.find('div', class_='title').text)

    span_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "meta")))
    for ele in span_elements:
        ele_html = ele.get_attribute("outerHTML")
        soup = BeautifulSoup(ele_html, 'lxml')
        elements = soup.find_all('span')
        job_level.append(elements[0].text)
        location.append(elements[1].text)
        job_type.append(elements[2].text)
        hiring_institute.append(elements[3].text)
    return(job_title,location,job_type,hiring_institute,job_level)
def first_website():
    url = 'https://karriere.crf-education.com/stellenangebote/'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    div_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"title")))
    job_title = []
    for ele in div_elements:
        ele_html = ele.get_attribute("outerHTML")
        soup = BeautifulSoup(ele_html, 'lxml')
        job_title.append(soup.find('div', class_='title').text)

    location = []
    hiring_institute = []
    job_type = []
    job_level = []
    span_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "meta")))
    for ele in span_elements:
        ele_html = ele.get_attribute("outerHTML")
        soup = BeautifulSoup(ele_html, 'lxml')
        elements = soup.find_all('span')
        job_level.append(elements[0].text)
        location.append(elements[1].text)
        job_type.append(elements[2].text)
        hiring_institute.append(elements[3].text)

    # while True:
    #     try:
    #         driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
    #             EC.element_to_be_clickable((By.CLASS_NAME, "next"))))
    #         driver.find_element(By.CLASS_NAME, "next").click()
    #         print("Navigating to Next Page")
    #         #get_info(driver,job_title,location,job_type,hiring_institute,job_level)
    #     except (TimeoutException, WebDriverException) as e:
    #         print("Last page reached")
    #         break
    print(job_title)
    driver.quit()


if __name__ == '__main__':
    #second_website()
    #third_website()
    first_website()

