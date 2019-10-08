from bs4 import BeautifulSoup
import requests

url = 'http://ethans_fake_twitter_site.surge.sh/'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")
for tweet in content.find('p', attrs={"class": "content"}):
    print(tweet.text.encode('utf-8))



