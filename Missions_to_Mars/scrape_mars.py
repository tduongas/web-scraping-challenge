from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def latest_mars_news():
    browser = init_browser()

    # mars news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    # results are returned as an iterable list
    result = soup.find('li', class_="slide")

    # Identify and return news title
    content_title = result.find('div', class_="content_title")
    news_title = content_title.a.text
    
    paragraph = result.find('div', class_="article_teaser_body").text
    
    # Store news title and paragraph into a dictionary
    nasa_mars_news = {'title': news_title.strip('\n'), 'paragraph': paragraph}

    print(nasa_mars_news)

    # Close the browser after scraping
    browser.quit()

    # Return results
    return nasa_mars_news

def featured_image():
    browser = init_browser()

    # mars news
    domain_name = "https://www.jpl.nasa.gov"
    url = domain_name + "/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    image_description_container = soup.find('div', class_="image_and_description_container")
    latest_image = image_description_container.find('img', class_="thumb")
    featured_image_url = domain_name + latest_image['src']
    print(f"featured_image_url = {featured_image_url}")

    image_url = {'img_url':featured_image_url}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return image_url

def current_mars_weather():
    browser = init_browser()

    # mars news
    domain_name = "https://twitter.com"
    url = domain_name + "/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    mars_weather = soup.find('span', text = re.compile("InSight sol"))
    print(f"Mars weather = {mars_weather.text}")

    weather = {'text':mars_weather.text}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return weather

def mars_facts():
     # url to visit
    url = 'http://space-facts.com/mars/'

    # use pandas to extract table from the page
    facts_table = pd.read_html(url)

    # create df with columns' headers
    df_mars_facts = facts_table[0]
    df_mars_facts.columns = ['Parameter','Value']
    df_mars_facts.set_index(['Parameter','Value'], inplace = True)

    # convert to html table
    mars_table = df_mars_facts.to_html()
    mars_table = mars_table.replace("\n", "")
    print(mars_table)

    mars_facts = {"html": mars_table}

    return mars_facts

def mars_hemispheres():
    browser = init_browser()

    hemisphere_base_url = "https://astrogeology.usgs.gov"

    # mars news
    url = hemisphere_base_url + "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(5)

    #using bs to write it into html
    html = browser.html
    soup = bs(html,"html.parser")

    div = soup.find('div', class_='results')
    div = div.find_all('div', class_='description')
    
    # Initialise list of dictionaries to store title and img_url
    hemisphere_image_urls = []

    # Loop through div results
    for div_result in div:
        # Error handling
        try:
            # Identify and return news title
            title = div_result.find('h3').text
            
            anchor_tag = div_result.find('a', class_="itemLink product-item")
            image_url = hemisphere_base_url + anchor_tag["href"]
            
            browser.visit(image_url)        
            sub_soup = bs(browser.html, 'html.parser')
            
            download_div = sub_soup.find('div', class_="downloads")
            img_anchor_tag = download_div.find('a')
            full_res_image_url = img_anchor_tag["href"]
                                    
            # Store news title and image url into a dictionary
            hemisphere_image_urls.append({'title': title, 'image_url': full_res_image_url})

        except AttributeError as e:
            print(e) 

    print(hemisphere_image_urls)        

    # Close the browser after scraping
    browser.quit()
    
    # Return results
    return hemisphere_image_urls
