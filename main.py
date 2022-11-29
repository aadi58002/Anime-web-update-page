#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
import re
import sys
import os

if len(sys.argv) == 1 :
    print("No cmd line argument was passed")
    exit(0)

def localFileParsing(final_links,source_list_file,completed_list,Url_list):
    parsing = False
    for line in source_list_file:
        if line.startswith("# -- End -- #"):
            parsing = False
        if parsing:
            for Url_anime in Url_list:
                if Url_anime in line:
                    completed_list.append(line[line.find("--")+2:].strip())
                    final_links.append(line[line.find("[[")+2:line.find("]")])
        if line.startswith("# -- Start -- #"):
            parsing = True



def onlineWordParsing(final_links,words,completed_list,Url_anime):
    videos_object = requests.get(Url_anime)
    anime_links = bs(videos_object.content,'html.parser').findAll('a')
    anime_links_filtered = []
    for element in anime_links:
        tmp = re.search(r'<a href="(\/category[^"]+)', str(element))
        if tmp :
            test = str(tmp.group(1))
            if not test.endswith("-dub") :
                anime_links_filtered.append(Url_anime + test)
    anime_links_filtered = list(dict.fromkeys(anime_links_filtered))
    for links in anime_links_filtered :
        for word in words :
            if word in links :
                final_links.append(links)
                completed_list.append("new")

def getLatestEp(final_links,show_image_url,show_end_ep):
    for links in final_links :
        test = requests.get(links)
        test_page = bs(test.content,'html.parser').find('div' , class_="main_body")
        tmp_image_url = test_page.find('img')
        tmp = re.search(r'ep_end="(\d+)".*?ep_start="(\d+)"', str(test_page))
        show_image_url.append(tmp_image_url['src'])
        show_end_ep.append(tmp.group(1))

def getLatestCh(final_links,show_image_url,show_end_ep):
    for links in final_links :
        test = requests.get(links)
        test_page = bs(test.content,'html.parser').find('div' , class_="main_body")
        tmp_image_url = test_page.find('img')
        tmp = re.search(r'ep_end="(\d+)".*?ep_start="(\d+)"', str(test_page))
        show_image_url.append(tmp_image_url['src'])
        show_end_ep.append(tmp.group(1))

def writingHtmlBlockToFile(source_list_file,html_push_block):
    with open(source_list_file,"r") as f:
        test = f.read()
        f = test.index('<!-- #Python Code Begin -->') + len('<!-- #Python Code Begin -->')
        l = test.index('    <!-- #Python Code End -->')
        test_final = test[:f+1]
        for link in html_push_block :
            test_final = test_final + link
        test_final = test_final + test[l:]
    final_file = open(source_list_file,"w")
    final_file.write(test_final)
    final_file.close()


final_links = []
anime_completed_list = []
show_image_url = []
# words = ["kawaii","tate","kaguya","date","aharen","seifu","komi","gaikotsu","murabito"]
show_end_ep = []
Url_anime = "https://gogoanime.lu"
html_push_block = []
Url_list = []
Url_list.append(Url_anime)
Url_list.append("https://gogoanime.ar")
Url_list.append("https://gogoanime.fi")

localFileParsing(final_links,open(os.path.join(os.path.dirname(__file__), '../../roam/Entertainment/anime.org'),'r').readlines(),anime_completed_list,Url_list)
# Getting all the latest ep from the final links provided
getLatestEp(final_links,show_image_url,show_end_ep)
for i in range(len(show_image_url)) :
    html_push_block.append("        <div class=\"anime-thumbnail\"><a href=\"" + final_links[i] + "\"><figcaption>Completed till " + anime_completed_list[i] + "</figcaption><img src=\"" + show_image_url[i] + "\"/><figcaption>Latest episode is "+  show_end_ep[i] + "</figcaption></a></div>\n")
writingHtmlBlockToFile(sys.argv[1],html_push_block)

# final_links = []
# manga_completed_list = []
# show_image_url = []
# show_end_ep = []
# Url_manga = "https://comick.fun"
# html_push_block = []

# localFileParsing(final_links,open(os.path.join(os.path.dirname(__file__), '../../roam/Entertainment/manga.org'),'r').readlines(),manga_completed_list,Url_manga)
# print(final_links)
# print(manga_completed_list)
