#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
import re
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


# Api referneces
# https://api.comick.fun/comic/little-girl-x-scoop-x-evil-eye
# https://api.comick.fun/comic/39649/chapter




# if len(sys.argv) <= 1:
#     print("Less than required cmd line argument was passed")
#     exit(0)


def localFileParsing(anime_links, anime_name, anime_file, my_completed_list, Url_anime):
    parsing = False
    for line in anime_file:
        if line.startswith("# -- End -- #"):
            parsing = False
        if parsing:
            if Url_anime in line:
                my_completed_list.append(line[line.find("--") + 2 :].strip())
                anime_link = line[line.find("[[") + 2 : line.find("]")]
                anime_links.append(anime_link)
                anime_name.append(anime_link.replace(Url_anime + "/category/", ""))
        if line.startswith("# -- Start -- #"):
            parsing = True


def getLatestEp(anime_links, show_end_ep, show_start_ep):
    for links in anime_links:
        test = requests.get(links)
        test_page = bs(test.content, "html.parser").find("div", class_="main_body")
        tmp = re.search(r'ep_end="(\d+)".*?ep_start="(\d+)"', str(test_page))
        show_end_ep.append(int(tmp.group(1)))
        show_start_ep.append(int(tmp.group(2)) + 1)


def linksToEpConverter(
    anime_links, show_end_ep, show_start_ep, ep_list_links, Url_anime
):
    for i in range(len(anime_links)):
        for j in range(show_start_ep[i], show_end_ep[i] + 1):
            ep_list_links.append(
                anime_links[i].replace("/category", "") + "-episode-" + str(j)
            )
            ep_list_names.append(anime_name[i] + "-episode-" + str(j))


driver_path = "/bin/chromedriver"
brave_path = "/bin/brave"
anime_links = []
anime_name = []
my_completed_list = []
show_end_ep = []
show_start_ep = []
Url_anime = "https://gogoanime.lu"
ep_list_links = []
ep_list_names = []
ep_download_links = []
page_load_timeout = 5


localFileParsing(
    anime_links,
    anime_name,
    open(
        os.path.join(os.path.dirname(__file__), "../../roam/Entertainment/anime.org"),
        "r",
    ).readlines(),
    my_completed_list,
    Url_anime,
)
getLatestEp(anime_links, show_end_ep, show_start_ep)
linksToEpConverter(anime_links, show_end_ep, show_start_ep, ep_list_links, Url_anime)

option = webdriver.ChromeOptions()
option.binary_location = brave_path
option.add_argument("--incognito")
option.add_argument("--headless")

driverService = Service(driver_path)
for link in ep_list_links:
    driver = webdriver.Chrome(service=driverService, options=option)
    try:
        driver.set_page_load_timeout(page_load_timeout)
        driver.get(link)
    except TimeoutException as e:
        pass
    for a in driver.find_elements(By.XPATH, ".//a"):
        if "goload" in str(a.get_attribute("href")):
            print(str(a.get_attribute("href")))
            ep_download_links.append(str(a.get_attribute("href")))
    driver.quit()
