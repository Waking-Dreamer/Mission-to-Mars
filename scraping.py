# Scraping Articles

# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    # headless=True means scraping will be done behind the scenes and no webpage will open to visually watch
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # Set news title and paragraph variables, function will return two values. Tells Python to use mars_news function to pull this data.
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemisphere_images(browser),
        "last_modified": dt.datetime.now()
    }
    print(data)

    # Stop webdriver and return data
    browser.quit()
    return data

# Set the executable path and initialize the chrome browser in splinter
#executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#browser = Browser('chrome', **executable_path)
# **executable_path is unpacking the dictionary we’ve stored the path in.

# Declare and define fucntion
def mars_news(browser):
    #Scrape Mars News

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Searching for elements with a specific combination of tag (ul and li) and attribute (item_list and slide).
    # Tell browser to wait one second before searching for components. The optional delay is useful because 
    #sometimes dynamic pages take a little while to load, especially if they are image-heavy.

    # Set up the HTML Parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    #Add try/except for error handling
    try:
        # Assigned slide_elem as the variable to look for the <ul /> tag and its descendent (the other tags within the
        # <ul /> element), the <li /> tags. This is the parent element, it holds all of the other elements within it,
        # we reference it when we want to filter search results even further. The . is used for selecting classes, such as
        # item_list, so the code 'ul.item_list li.slide' pinpoints the <li /> tag with the class of slide and the
        # <ul /> tag with a class of item_list. CSS works from right to left, such as returning the last item on the list
        # instead of the first. Because of this, when using select_one, the first matching element returned will be
        # a <li /> element with a class of slide and all nested elements within it.
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# Scraping Images

# Declare and define function
def featured_image(browser):

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button by searching for text and click it
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # tell BeautifulSoup to look inside the <figure class=”lede” /> tag for an <a /> tag, and then look within 
        # that <a /> tag for an <img /> tag.
        # Pull the link of the image by pointing BeautifulSoup to where the image will be, instead of grabbing the URL
        # directly. This way, when NASA updates its image page, the code will still pull the most recent image.

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# Mars Facts
def mars_facts():

    try: 
        # Scrape HTML table and store in new df
        # The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
        # By specifying an index of 0, we’re telling Pandas to pull only the first table it encounters.
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns to the new DataFrame for additional clarity
    df.columns=['Description', 'Mars']

    # Turn the Description column into the DataFrame’s index. inplace=True means that the updated index will remain 
    # in place, without having to reassign the DataFrame to a new variable.
    df.set_index('Description', inplace=True)

    # Convert stored df back into HTML format so it can be added to a website
    return df.to_html(classes="table table -striped")

# CHALLENGE 
# Reviewed speed run for assistance with function creation

# Store Mars Hemisphere Image links
def mars_hemisphere_images(browser):

    #create list
    hemisphere_image_urls = []

    #Assign mars image website to url variable
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #visit site
    browser.visit(url)

    #retrieve list of hemisphere links
    #links = browser.find_by_css('a.product-item h3', wait_time=1)

    #loop through links 
    for index in range (4):
        
        #find element link and click
        browser.find_by_css('a.product-item h3')[index].click()
        # Call scrape_hemisphere_images function and store results
        hemisphere_data = scrape_hemisphere_images(browser.html)
        #add image and title to list
        hemisphere_image_urls.append(hemisphere_data)
        
        #navigate back for next image link
        browser.back()

    return hemisphere_image_urls

#scrape hemisphere images
def scrape_hemisphere_images(html_text):
    
    #parse html text
    hemispheres_soup = BeautifulSoup(html_text, "html.parser")

    #Try to scrape image and title
    try:
        hemisphere_title = hemispheres_soup.find("h2", class_="title").get_text()
        image_link = hemispheres_soup.find("a", text="Sample").get("href")
    #return nothing if error occcurs
    except AttributeError:
        hemisphere_title = None
        image_link = None

    #create dictionary with stored image and title
    hemispheres = {
        "title": hemisphere_title,
        "image_url": image_link
    }
    
    return hemispheres

# Tell Flask to run
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())