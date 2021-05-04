from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    

    # Open browser to NASA Mars News Site
    browser.visit("https://mars.nasa.gov/news/")

    
    html = browser.html
    soup = bs(html, 'html.parser')


    # parse containing class 
    results = soup.find_all(class_='slide')[0]

    # get the latest tittle and body
    news_title = results.find(class_='content_title').text
    news_p = results.find(class_='article_teaser_body').text
    

### Mars Featured Image
    time.sleep(1)


# Connect to JPL 
    browser.visit("https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html")

# Click through to find full image
    browser.links.find_by_partial_text('FULL IMAGE').click()

# Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = bs(html, "html.parser")

# Featured image from img  & src (2nd img)
    featured_img_url = image_soup.find_all('img')[1]["src"]

    final_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space" +featured_img_url
    
    time.sleep(1)

    ### Mars Facts

    
    # Open browser to NASA Mars News Site
    mars_facts = pd.read_html("https://space-facts.com/mars/")
    # get table with desired values
    mars_facts = mars_facts[0]
    mars_facts.columns=['Mars Properties', 'Measurements']
    mars_facts.set_index('Mars Properties', inplace=True)
    mars_facts= mars_facts.reset_index().to_html(index = False)

   
    time.sleep(1)

    ### Mars Hemispheres

    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres

    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    # Parse HTML with Beautiful Soup
    soup = bs(browser.html, 'html.parser')

    # Create List to hold images & Url
    hems_image_url = []

    #locate element that holds results
    results = soup.find_all('div', class_='item')  


    for result in results:

        # Get title
        title_hemis = result.find('h3').text

        first_url = "https://astrogeology.usgs.gov" + result.find('a', class_='itemLink')['href']
        
        #visit first_url
        browser.visit(first_url)
        soup = bs(browser.html, 'html.parser')
        
        final_url = "https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')['src']
        hems_image_url.append({'title': title_hemis, 'hemisphere_image_urls':final_url})
        
        
    results_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": final_image_url,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hems_image_url
        }


    return results_dict

