import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, Comment
import re
import os

def process(word):
    word = list(word)
    for i in range(len(word)):
        if word[i]=='/' or word[i]=='\\' or word[i]==':':
            word[i] = ' '
    return ''.join(word)

def write(text):
    #print("I have input ",text )
    file_text = text.encode('utf-8')
    return_string = ""
    for char in file_text:
        if char>=32 and char <=127:
            return_string += chr(char)
    #print("returning ",return_string)
    return return_string
    file_decoded_text = str(file_text.decode('utf-8'))

def crawl(each_link):
    driver.get(each_link)

    page_html = driver.page_source
    soup = BeautifulSoup(page_html,'html.parser')

    data = soup.find("div", class_="mw-parser-output")

    word = str(soup.find('h1', {'class': 'firstHeading'}).text)
    word = process(word)

    fileName= os.getcwd() + "\\data\\" + str(word) + ".txt"
    fileContent = ""
    file = open(fileName, 'w+')

    for i in data:

        string_i = str(i)
        if string_i[0:2]=='<h' and i.find("span").text!='' and i.find("span").text!='See also':
            fileContent = fileContent.strip()
            file.write(str(write(fileContent)))
            fileContent = ""

            file.close()

            word = str(i.find("span").text)
            word = process(word)

            fileName = os.getcwd() + "\\data\\" + str(word) +  ".txt"
            fileContent = ""
            file = open(fileName, 'w+')

            child = i.find_all('p')
            for each_child in child:
                try:
                    fileContent += str(each_child.text) + " "
                except:
                    fileContent += str(write(each_child.text)) + " "
        elif string_i[0:3]=='<p>':
            try:
                fileContent += str(i.text) + " "
            except:
                fileContent +=  str(write(i.text)) + " "
        elif string_i[0:3]=='<pr':
            try:
                fileContent += str(i.text) + " "
            except:
                fileContent += str(write(i.text)) + " "
        elif string_i[0:3]=='<ta' and i.has_attr('class') and i['class'][0] in ["wikitable", "noprint", "metadata", "topicon", "notice", "notice-todo"]:
            pass
        elif string_i[0:3]=='<ta':
            try:
                fileContent += str(i.text) + " "
            except:
                fileContent += str(write(i.text)) + " "
        elif string_i[0:2]=='<d':
            try:
                fileContent += str(i.text) + " "
            except:
                fileContent += str(write(i.text)) + " "
        elif string_i[0:2]=='<u':
            #print(i)
            #print(i.text)
            list_li = i.find_all('li')
            for li in list_li:
                try:
                    fileContent += str(li.text) + " "
                    #print("in try")
                except:
                    fileContent += str(write(li.text)) + " "
                    #print("in except")

    fileContent = fileContent.strip()
    file.write(str(write(fileContent)))
    file.close()

def get_links():
    driver.get("https://en.wikibooks.org/wiki/Java_Programming")

    page_html = driver.page_source
    soup = BeautifulSoup(page_html,'html.parser')
    data = soup.find("div", class_="mw-parser-output")

    #'''
    list_h3 = data.find_all('h3')
    list_ul = data.find_all('ul')

    for h3 in list_h3:
        if h3.find('a') is not None:
            links_of_interest.append(baseurl + h3.find('a')['href'])

    for ul in list_ul:
        li_list = ul.find_all('li')
        for li in li_list:
            a_list = li.find_all('a')
            if len(a_list)==2 and a_list[-1]['href'] is not None:
                links_of_interest.append(baseurl + a_list[-1]['href'])
    #'''

    #links_of_interest = ['https://en.wikibooks.org/wiki/Java_Programming/3D_Programming']

    for each_link in links_of_interest:
        crawl(each_link)

if __name__== "__main__":
    driver = webdriver.Chrome()
    baseurl = 'https://en.wikibooks.org'
    links_of_interest = []
    get_links()
