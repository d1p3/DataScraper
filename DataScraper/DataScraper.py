from bs4 import BeautifulSoup
import requests
import json 
from selenium import webdriver


headers = {'User-Agent': 'Mozilla/5.0'}

#---Simple read--------
#domains = content.find_all("div",class_="grid-card-image-container")
#print(domains)

#----------Getting recepie links------------
page_count=0
links = []
while page_count<2:
    url = "https://www.allrecipes.com/?page=%d" %(page_count)
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    for domain in content.findAll('div', attrs={"class": "grid-card-image-container"}):
        for a in domain.find_all('a',href=True):
            links.append(a['href'])
    page_count+=1

#-------------Writing recipie link-file----------------------
with open('receipeLinks.json','w') as outfile:
    json.dump(links,outfile)


#-------------Scraping Data----------------
#tweetArr = []
#for tweet in content.findAll('article', attrs={"class": "fixed-recipe-card"}):
#    #print(tweet.text.encode('utf-8'))
#    tweetObject = {
#        "ImageLink": tweet.find('img', attrs={"class": "author"}).text,
#        "date": tweet.find('a', attrs={"data-name": "dateTime"}).text,
#        "tweet": tweet.find('p', attrs={"class": "content"}).text,
#        "likes": tweet.find('p', attrs={"class": "likes"}).text,
#        "shares": tweet.find('p', attrs={"class": "shares"}).text
#    }
#    tweetArr.append(tweetObject)

#-------------Writing to file----------------------
#with open('twitterData.json','w') as outfile:
#    json.dump(tweetArr,outfile)

