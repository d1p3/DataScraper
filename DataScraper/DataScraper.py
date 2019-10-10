from bs4 import BeautifulSoup
import requests
import json 
import re

headers = {'User-Agent': 'Mozilla/5.0'}

#---Simple read--------
#domains = content.find_all("div",class_="grid-card-image-container")
#print(domains)

#----------Getting recepie links------------
page_count = 0
links = []
while page_count < 1:
    url = "https://www.allrecipes.com/?page=%d" % (page_count)
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    for domain in content.findAll('div', attrs={"class": "grid-card-image-container"}):
        for a in domain.find_all('a',href=True):
            links.append(a['href'])
    page_count+=1
print(links[1])
#-------------Writing recipie link-file----------------------
#with open('receipeLinks.json','w') as outfile:
#    json.dump(links,outfile)

#-------------Scraping Data For Each Receipe----------------
details = []
receipeDirections = []
prepTime = []

calories = float(0.0)
fat = float(0.0)
carbohydrate = float(0.0)
protein = float(0.0)
cholesterol = float(0.0)
sodium = float(0.0)
#for link in links:
response = requests.get(links[1], timeout=5)
content = BeautifulSoup(response.content, "html.parser")
for receipe in content.find_all('section', attrs={"class": "ar_recipe_index"}):
    #Extracting Directions
    for directions in receipe.find_all('ol'):
        for direction in directions.find_all('li', class_ = 'step'):
            try:
                receipeDirections.append(direction.get_text().strip())
            except AttributeError:
                receipeDirections.append("****Instructions not found******")
    #Extracting Preparation-Time
    for pTime in receipe.find_all('ul', class_ = 'prepTime'):
        for p in pTime.find_all('li'):
            try:
                string = p.get_text().strip()
                if(string == ""):
                    continue
                prepTime.append(list(map(int,re.findall(r'\d+', string))))
            except AttributeError:
                receipeDirections.append(int(0))
    #Extracting Nutrients
    try:
        calories = list(map(float,re.findall(r'\d+.\d+|\d+', receipe.find('span', itemprop = 'calories').get_text().strip())))
    except AttributeError:
        calories = 0
    try:
        fat = list(map(float,re.findall(r'\d+.\d+|\d+', receipe.find('span', itemprop = 'fatContent').get_text().strip())))
    except AttributeError:
        fat = 0
    try:
        carbohydrate = list(map(float,re.findall(r'\d+.\d+|\d+', receipe.find('span', itemprop = 'carbohydrateContent').get_text().strip())))
    except AttributeError:
        carbohydrate = 0
    try:
        protein = list(map(float,re.findall(r'\d+.\d+|\d+', receipe.find('span', itemprop = 'proteinContent').get_text().strip())))
    except AttributeError:
        protein = 0
    try:
        cholesterol = list(map(float,re.findall(r'\d+.\d+|\d+', receipe.find('span', itemprop = 'cholesterolContent').get_text().strip())))
    except AttributeError:
        cholesterol = 0
    try:
        sodium = list(map(float,re.findall(r'\d+.\d+|\d+', receipe.find('span', itemprop = 'sodiumContent').get_text().strip())))
    except AttributeError:
        sodium = 0

print(receipeDirections)
print(prepTime)
print(calories,fat,carbohydrate,protein,cholesterol,sodium)
            #try:
            #    print(data.get_text())
            #except AttributeError:
            #    print("Data Not Found")
       
    


#-------------Writing to file----------------------
#with open('twitterData.json','w') as outfile:
#    json.dump(tweetArr,outfile)

