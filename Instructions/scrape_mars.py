import pickle
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import time
import pandas as pd
executable_path = {
    'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)
from pymongo import MongoClient
client = MongoClient()

def mars_headline():
    url = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    resp = requests.get(url).json()
    first_item = resp.get('items')[0]
    return {"item_title": first_item.get('title'), 
            "item_desc": first_item.get('description')
           }

def mars_news():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(2)
    browser.click_link_by_partial_text("more info")
    #get html code once at page
    image_html = browser.html

    #parse
    soup = BeautifulSoup(image_html, "html.parser")

    #find path and make full path
    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path
    return{"featured_image_url": featured_image_url}


def mars_weather():
    browser.visit('https://twitter.com/marswxreport?lang=en')

    soup = BeautifulSoup(browser.html, "html.parser")
    get_mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return {"mars_weather": get_mars_weather}

def mars_facts():

    # * Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url = 'http://space-facts.com/mars/'


    # * Use Pandas to convert the data to a HTML table string.
    tables = pd.read_html(url)
    new_table = tables[0]
    new_table.columns = ["Description", "Value"]
    formatted =  new_table.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    return {"html_table_facts": formatted}

def mars_hemispheres():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemis in hemispheres:
        title = hemis.find("h3").text
        end_link = hemis.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

    return {"hemisphere_image_urls": mars_hemisphere}


def scrape_master():
    print('scraping stuff')
    headlines_dict = mars_headline()
    news_dict = mars_news()
    facts_dict = mars_facts()
    weather_dict = mars_weather()
    hemispheres_dict = mars_hemispheres()
    merged_dict = {**headlines_dict, **news_dict, **weather_dict, **facts_dict, **hemispheres_dict}
    print('done merging')
    # merged dict will be the new data in mongodb
    return merged_dict