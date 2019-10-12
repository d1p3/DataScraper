from bs4 import BeautifulSoup
import requests
import json 
import re
headers = {'User-Agent': 'Mozilla/5.0'}
#----------Getting recepie links------------
def GetPageLink():
    page_count = 0
    links = []
    while page_count < 3:
        url = "https://www.allrecipes.com/?page=%d" % (page_count)
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")

        for domain in content.findAll('div', attrs={"class": "grid-card-image-container"}):
            for a in domain.find_all('a',href=True):
                if((re.search("video",a['href'], re.IGNORECASE)!=None)):
                   continue
                else:
                    links.append(a['href'])
        page_count+=1
    print("Writing Link File..")
    writeToFile("linkDoc",links)
    print("Done")
    Scrape(links[0:3])
    #print(len(links))
def writeToFile(name,list):
#-------------Writing recipie link-file----------------------
    with open(name+'.json','a') as outfile:
        json.dump(list,outfile)
#-------------Reading recipie link-file----------------------
def readFile(name):    
    with open(name,'r') as outfile:
        for link in outfile:
            print(linl+'\n')

#-------------Scraping Data For Each Receipe----------------
def Scrape(links):
    #Once
    a=1
    while a:
        print("Scraping Data....")
        a=0
    for link in links:
        details = []
        receipeDirections = []
        prepTime = []
        ingredientsList = []
        calories = float(0.0)
        fat = float(0.0)
        carbohydrate = float(0.0)
        protein = float(0.0)
        cholesterol = float(0.0)
        sodium = float(0.0)
        title = ""

    
        try:
            response = requests.get(link, timeout=5)
        except:
            continue
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
                for p in pTime.find_all('time'):
                    string = p.get_text().strip()
                    if(string != ""):
                        try:
                            prepTime.append(list(map(int,re.findall(r'\d+.\d+|\d+', string))))
                        except AttributeError:
                            receipeDirections.append(int(0))
            #Extracting Ingredients
            for ingredients in receipe.find_all('ul', class_ = "list-ingredients-1"):
                for ingredient in ingredients.find_all('li', class_ = 'checkList__line'):
                    try:
                        ingredientsList.append(ingredient.get_text().strip())
                    except AttributeError:
                        ingredientsList.append("N/A")
            for ingredients in receipe.find_all('ul', class_ = "list-ingredients-2"):
                for ingredient in ingredients.find_all('li', class_ = 'checkList__line'):
                    try:
                        ingredientsList.append(ingredient.get_text().strip())
                    except AttributeError:
                        ingredientsList.append("N/A")
            del ingredientsList[-1]
            
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

            #title extraction
            try:
                title = receipe.find('h1', class_ = 'recipe-summary__h1').get_text().strip()
            except AttributeError:
                receipeDirections.append("****No Title******")
        if(len(prepTime)>=3):
            receipeObject = {
                "receipeTitle": title,
                "receipeDirections": receipeDirections,
                "preparationTime": prepTime[0],
                "cookTime": prepTime[1],
                "totalTime": prepTime[2],
                "calories": calories,
                "fat": fat,
                "carbohydrate": carbohydrate,
                "protein": protein,
                "cholesterol": cholesterol,
                "sodium": sodium,
                "ingredients": ingredientsList,
                }
        else:
            receipeObject = {
            "receipeTitle": title,
            "receipeDirections": receipeDirections,
            "preparationTime": int(0),
            "cookTime": int(0),
            "totalTime": int(0),
            "calories": calories,
            "fat": fat,
            "carbohydrate": carbohydrate,
            "protein": protein,
            "cholesterol": cholesterol,
            "sodium": sodium,
            "ingredients": ingredientsList,
            }
        writeToFile('receipeData',receipeObject)

GetPageLink()
