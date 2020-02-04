# Web Crawler for the Web Gallery of Art (http://www.wga.hu/) photo archive
# Author(s): Mehrdad Tabrizi, Aug. 2018
# Attention: In order to use this code, you have to have the firefox/chrome driver. You need also their path in your Hard drive.
# This crawler uses Firefox driver (geckodriver.exe)

import wga
import wga_Parameters as Parameters
import time

def Main():
    page_items = []
    current_page = 1
    browser = wga.browser_open()
    browser = wga.browser_open_url(browser, Parameters.search_URL)
    browser = wga.search_for_keyword(browser, Parameters.KEYWORD)
    PAGE_EXISTS = True
    wga.create_csv_file(Parameters.CSV_File_PATH)

    while (PAGE_EXISTS):
        print('Working on Page ' + str(current_page))
        time.sleep(1)
        page_items = []
        page_items.extend(wga.extract_metadatas_page(browser,current_page))
        for item in page_items:
            wga.append_metadata_to_CSV(item)
        PAGE_EXISTS = wga.go_to_next_page(browser)
        current_page +=1
        print('__________________________________')

    wga.browser_quit(browser)


if __name__ == '__main__':
    Main()