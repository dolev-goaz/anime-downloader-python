import sys
import re
import os
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from threading import Thread
import shutil
from downloadEpisode import Downloader

QUALITY_REGEX = re.compile('DOWNLOAD \(([\d]+)P - MP4\)')


def download(href, filename, filepath, hook):
	downloader = Downloader(href, filename, filepath, hook)
	downloader.start()

# returns the href to the highest quality download
def get_best_download_href(driver):
    download_buttons = driver.find_elements_by_class_name('dowload')
    downloads = [download_button.find_element_by_css_selector("*") for download_button in download_buttons if 'MP4' in download_button.text]

    return get_highest_quality_href(downloads)

def get_highest_quality_href(downloads):
        max = (0, None)
        for download in downloads:
                result = QUALITY_REGEX.search(download.text)
                if result:
                        quality = int(result.group(1))
                        if quality > max[0]:
                                max = (quality, download)
        return (max[1].get_attribute('href'), max[0]) #href, quality

#closes selenium tab
def close_tab(driver, index):
    cur_index = driver.window_handles.index(driver.current_window_handle)

    driver.switch_to.window(driver.window_handles[index])
    driver.close()

    cur_index = min(cur_index, len(driver.window_handles))
    driver.switch_to.window(driver.window_handles[cur_index])

#start downloading hrefs
def download_episodes(directory_name, download_hrefs, hook=None):
        threads = []
        if os.path.exists(directory_name):
                shutil.rmtree(directory_name)
        os.mkdir(directory_name)

        for href in download_hrefs:
                t = Thread(target=download, args=(href[0], href[1], f'{directory_name}\{href[1]}', hook))
                t.start()
                threads.append(t)
        for thread in threads:
                thread.join()

def get_episode_hrefs(parsed_anime_name, url = 'https://animekisa.tv'):
        episodes = []
        data = requests.get(f'{url}/{parsed_anime_name}')
        soup = BeautifulSoup(data.text, 'html.parser')
        episodes = soup.find('div', {'class': 'infoepbox'})
        hrefs = [ episode['href'] for episode in episodes.find_all('a', href=True) ]
        return hrefs

def get_all_download_hrefs(hrefs, url = 'https://animekisa.tv'):
        DRIVER_PATH = r'C:\Program Files (x86)\chromedriver.exe'
        
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(DRIVER_PATH, chrome_options=chrome_options)

        #clicks on download episode- redirects to download page
        for href in hrefs:
                driver.get(f'{url}/{href}')
                time.sleep(1)
                download_button = driver.find_element_by_class_name('server_button_l')
                download_button.click()
        #close the non-download tab
        close_tab(driver, 0)

        download_hrefs = []
        # loop through each open tab and download
        length = len(hrefs)
        for i in range(length):
                driver.switch_to.window(driver.window_handles[i])
                href = get_best_download_href(driver)
                href_download = href[0]
                quality = href[1]
                download_hrefs.append((href_download, f'EP {i + 1}({quality}P).mp4'))
                print(f'EP {i + 1}({quality}P).mp4: {href_download}')
                
        driver.quit()
        return download_hrefs


def start_download(anime_name, url = 'https://animekisa.tv', hook = None):
        parsed_anime_name = re.sub('[^A-Za-z0-9 ]+', '', anime_name.strip().lower()).replace(' ', '-')

        hrefs = get_episode_hrefs(parsed_anime_name, url)
        
        download_hrefs = get_all_download_hrefs(hrefs, url)
        
        download_episodes(parsed_anime_name, download_hrefs, hook)
