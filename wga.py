from selenium import webdriver
from bs4 import BeautifulSoup
import wga_Parameters as Parameters
from collections import OrderedDict
from urllib import request
import pandas as pd
import csv

def browser_open():
    driver = webdriver.Firefox(executable_path=Parameters.Firefox_Driver_PATH)
    return driver

def browser_open_url(browser, url) :
    browser.get(url)
    return browser

def get_html_page(browser):
    res = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res, 'lxml')
    return soup


def search_for_keyword(browser,keyword):
    frame = browser.find_elements_by_tag_name('frame')
    browser.switch_to.frame(frame[1])
    title = browser.find_element_by_xpath("//*/input[@name='title']")

    title.send_keys(keyword)

    submit = browser.find_element_by_xpath("//*/input[@type='SUBMIT']")
    submit.click()
    print('Search is done!')
    return browser

def extract_metadatas_page(browser,page):

    soup = get_html_page(browser)
    items = soup.find('table', {'border': '1' , 'cellpadding' : '5' , 'width': "97%"}).find_all('tr')

    image_URL   = ''
    artist      = ''
    location    = ''
    title       = ''
    date        = ''
    image_URL   = ''
    material    = ''
    file_name   = ''
    item_frames = []
    item_metadata = {

        'Photo Archive' : 'https://www.wga.hu/',
        'File Name'     : file_name,
        'Title'         : title,
        'Artist'        : artist,
        'Date'          : date,
        'Location'      : location,
        'Image URL'     : image_URL,
    }
    page_metadata = []

    i = 1
    for item in items:
        if (item.find('b') is not None):
            if (item.find('a') is not None):
                image_URL = Parameters.base_url + item.find('td').findChild('a').get('href')

            item_frame_datas = item.find('b').findParent('td')

            s_list = item_frame_datas.text.replace('\n' , ';')
            s_list = s_list.split(';')
            artist      = s_list[1]
            title       = s_list[2]
            date        = s_list[3]
            material    = s_list[4]
            location    = s_list[5]
            file_name   = 'page_' + str(page) + '_item_' + str(i) + '_' + image_URL.split('/')[-1]

            print('Item ' + str(i))
            print(image_URL)
            print(file_name)
            if not Parameters.Images_are_already_downloaded:
                download_image(image_URL,file_name)
            print('...............')

            item_metadata = {
                'Photo Archive'     : 'https://www.wga.hu/',
                'Iconography'       : Parameters.Iconography,
                'Branch'            : 'ArtHist',
                'File Name'         : file_name,
                'Title'             : title,
                'Artist'            : artist,
                'Earliest Date'     : date,
                'Current Location'  : location,
                'Genre'             : 'Painting',
				'Material'			: material,
                'Details URL'       : '',
                'Image Credits'     : image_URL,
            }

            keyorder = Parameters.Header
            item_metadata = OrderedDict(sorted(item_metadata.items(), key=lambda i: keyorder.index(i[0])))
            page_metadata.append(item_metadata)
            i += 1

    print('______________________')
    return page_metadata

def go_to_next_page(browser):

    page_box = browser.find_elements_by_xpath('//*/table/tbody/tr/td/p/a')
    if page_box is not None:
        n = len(page_box)
        if n !=0:
            s = page_box [n-1].text
            if "Next Page" in s:
                page_box[n-1].click()
                return True
        else:
            return False

def download_image(url,file_name):
    #time.sleep(1)
    path = Parameters.Images_PATH + file_name
    request.urlretrieve(url, path)

def save_metadata_to_CSV(dic):

    df = pd.DataFrame(dic)
    df.to_csv(Parameters.CSV_File_PATH)

def create_csv_file(file_path):
    keyorder = Parameters.Header
    with open(file_path, "w", encoding="utf-8") as f:
        wr = csv.DictWriter(f, dialect="excel", fieldnames=keyorder)
        wr.writeheader()

def append_metadata_to_CSV(row):
    keyorder = Parameters.Header
    with open(Parameters.CSV_File_PATH, "a", encoding="utf-8") as fp:
        wr = csv.DictWriter(fp,dialect="excel",fieldnames=keyorder)
        wr.writerow(row)

def browser_quit(browser):
    browser.quit()