from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    #Connect to NASA Mars News Site for scrapping
    browser.visit('https://mars.nasa.gov/news/')

    time.sleep(1)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for news titles
    title_results = soup.find_all('div', class_='content_title')

    # Search for paragraph text under news titles
    p_results = soup.find_all('div', class_='article_teaser_body')

    # Extract first title and paragraph, and assign to variables
    news_title = title_results[0].text
    news_p = p_results[0].text

    print(news_title)
    print(news_p)
    
       
        
    # Open browser to JPL Featured Image
    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')

    time.sleep(1)

    # Click through to find full image
    featured_img = browser.links.find_by_partial_text('FULL IMAGE')

    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for image source
    results = soup.find_all("div", class_="fancybox-inner")

    featured_img = soup.find_all('img')[1]["src"]

    final_img = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space' + featured_img
    final_img

    time.sleep(1)
    
    # Mars Facts
    
    # --- Use Pandas to scrape Mars Space Facts ---
    mars_facts = pd.read_html('https://space-facts.com/mars/')

    
    # Take first table for Mars facts
    mars_facts = tables[0]

    # Rename columns and set index
    mars_facts.columns=['description', 'value']
    mars_facts
    
   
    # --- Visit USGS Astrogeology Site ---
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    
    time.sleep(1)
    
    # Open browser to USGS Astrogeology site
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    
    # Parse HTML with Beautiful Soup
    soup = bs(browser.html, 'html.parser')

    # Create List to hold all the images & URLs collected
    hems_image_url = []

    #locate element that holds results for all hemis
    results = soup.find_all('div', class_='item')

    for result in results:
    # get tittle for hemis
    title_hemis = result.find('h3').text
    
    #to get the URL  - https://astrogeology.usgs.gov (29 char)+ href for full img (/search/map/Mars/Viking/cerberus_enhanced) 
    # = URL for the larger img page
    first_url = 'https://astrogeology.usgs.gov' + result.find('a', class_='itemLink')['href']
    
    #connect to first URL and parse
    browser.visit(first_url)
    soup = bs(browser.html, 'html.parser')
    
     # Open full image and get URL or src
    final_url = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
    
    # Append list
    hems_image_url.append({'title': title_hemis, 'img_url':final_url})
    
    ##Go back
    browser.back()
    
    hems_image_url
    
    
    
    # Store data in a dictionary
     results_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": final_image_url,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hems_image_url
        }

    # Return results
    return results_dict
