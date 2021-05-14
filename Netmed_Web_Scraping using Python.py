# Importing required libraries
import pandas as pd
import requests
import bs4
# import io
# import urllib
# import urllib.request
# import urllib.parse
import csv
from bs4 import BeautifulSoup
import re
# import os
# from PIL import Image

""" 
WE ARE GOING TO SCRAPE NETMED DATA BY USING TWO STEPS, STEPS ARE MENTIONED BELOW:
1. IN STEP ONE, WE WILL EXTRACT ALL THE LINKS FROM THE NETMED WEBSITE (FOR EACH PRODUCT)
2. IN STEP TWO, WE WILL DOWNLOAD/EXTRACT/SCRAPE THE REQUIRED DATA BY USING SCRAPED LINKS IN STEP 1 
"""

#step 1:
netmed = requests.get('https://www.netmeds.com/medicine/manufacturers')
netmed = netmed.text
data = bs4.BeautifulSoup(netmed, "lxml")
read1 = data.select('.alpha-drug-list')
#print(read1)
'''Lets extract all the Manufacturer's url'''
co_url=[]
for i in range(len(read1)):
        x=read1[i].find_all('li')
        for j in range (len(x)):
            y=x[j].find_all('a')
            for k in range(len(y)):
                z=y[k].get('href')
                co_url.append(z)
                #print(z)
#print(co_url)
'''Now we have all the manufacturer url's. So, lets extract all products url using manufacturer url's'''
all_url = []
for i in range(len(co_url)):
    netmed = requests.get(co_url[i])
    netmed = netmed.text
    data = bs4.BeautifulSoup(netmed, "html.parser")
    read1 = data.select('.panel-body')
    for i in range (len(read1)):
        x=read1[i].find_all('li')
        for j in range (len(x)):
            y=x[j].find_all('a')
            for k in range(len(y)):
                z=y[k].get('href')
                all_url.append(z)
#print(all_url)
#print(len(all_url))
'''Let's create a DataFrame and then CSV file'''
df=pd.DataFrame(all_url, columns=['Links'])
df.to_csv('Netmed_links.csv', index=False, header=False)#, encoding='utf-8'

#STEP TWO
final_list=[]
i=0
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def appendrow(list_of_elem):
    # Open file in append mode
    with open('data.csv','a+', encoding='utf-8') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


appendrow(['Quantity_and_Packform', 'Manufacturer', 'Medname', 'Discount Price', 'Sales Price', 'Composition', 'Image'])

with open("Netmed_links.csv", 'r') as f1:
    csvreader = csv.reader(f1)
    count = 0
    for row1 in csvreader:
        # if count >= 20000:
        #     break
        count += 1
        temp_list = []
        row = list(row1)
        url = row[0]
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')

        # To find Quantity and Packform
        qnp = str(soup.find("span", attrs={'class': 'drug-varient'}))
        Quantity_and_packform = cleanhtml(qnp)
        temp_list.append(Quantity_and_packform)
        # print(qnp)

        # To find the manufacturer
        manu = str(soup.find("span", attrs={"class": 'drug-manu'}))
        Manufacturer = cleanhtml(manu)[3:]
        temp_list.append(Manufacturer)

        # To find the name of the medicine
        name = str(soup.find("h1", attrs={"class": 'black-txt'}))
        Medname = cleanhtml(name)
        temp_list.append(Medname)

        # To find the discount price
        inter_dp = str(soup.find("span", attrs={"class": 'final-price'}))
        Discount_Price = cleanhtml(inter_dp)
        temp_list.append(Discount_Price)

        # To find sales price
        inter_sp = str(soup.find("span", attrs={"class": 'price'}))
        Actual_Price = cleanhtml(inter_sp)
        temp_list.append(Actual_Price)

        comp = str(soup.find("div", attrs={"class": 'drug-manu'}))
        Composition = cleanhtml(comp)
        comp_list = Composition.split(' + ')
        temp_list.append(comp_list)

        try:
            img = soup.find("figure", attrs={"class": "figure largeimage"})
            Image = img.get('src')
            temp_list.append(Image)

        except:
            temp_list.append("None")

        final_list.append(temp_list)
        appendrow(temp_list)

print("finished")