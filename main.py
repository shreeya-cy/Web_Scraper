import argparse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


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

    while True:
        try:
            driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "next"))))
            driver.find_element(By.CLASS_NAME, "next").click()
            print("Navigating to Next Page")
        except (TimeoutException, WebDriverException) as e:
            print("Last page reached")
            break

    driver.quit()
    column = ['Job Title', 'Job Level', 'Location', 'Job Type', 'Hiring Institute']
    data = pd.DataFrame(list(zip(job_title, job_level, location, job_type, hiring_institute)), columns=column)
    data.to_csv('./CRF.csv', index=False, encoding='utf-8')


def second_website():
    html_text = requests.get('https://www.berlin-international.de/hochschule/stellenangebote/').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs_info = soup.find('div', class_='col-lg-12 col-md-12 col-sm-12 col-xs-12 del-padding page-content link-effect')
    jobs = jobs_info.find_all('li')
    job_title = []
    for i in jobs:
        job_title.append(i.text)
    column = ['Job Title and Description']
    data = pd.DataFrame(job_title, columns=column)
    data.to_csv('./Berlin International.csv', index=False, encoding='utf-8')


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
            for dept in dept_info:
                complete_text = ''
                for i in dept:
                    complete_text = complete_text + " " + i.text
                    additional_info.append(complete_text)
        except:
            additional_info.append("No additional info")

    column = ['Job Title','Location', 'Additional Info']
    data = pd.DataFrame(list(zip(job_title, location, additional_info)), columns=column)
    data.to_csv('./AKAD.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    second_website()
    third_website()
    first_website()


