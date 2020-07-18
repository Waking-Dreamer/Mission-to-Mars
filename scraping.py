# ## Scraping Articles

# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Path to chromedriver
!which chromedriver

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)
# **executable_path is unpacking the dictionary we’ve stored the path in.

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
slide_elem = news_soup.select_one('ul.item_list li.slide')

# Assigned slide_elem as the variable to look for the <ul /> tag and its descendent (the other tags within the
# <ul /> element), the <li /> tags. This is the parent element, it holds all of the other elements within it,
# we reference it when we want to filter search results even further. The . is used for selecting classes, such as
# item_list, so the code 'ul.item_list li.slide' pinpoints the <li /> tag with the class of slide and the
# <ul /> tag with a class of item_list. CSS works from right to left, such as returning the last item on the list
# instead of the first. Because of this, when using select_one, the first matching element returned will be
# a <li /> element with a class of slide and all nested elements within it.

# Chain .find onto slide_elem variable to find specific info.
slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ## Scraping Images

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

# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel
# tell BeautifulSoup to look inside the <figure class=”lede” /> tag for an <a /> tag, and then look within 
# that <a /> tag for an <img /> tag.
# Pull the link of the image by pointing BeautifulSoup to where the image will be, instead of grabbing the URL
# directly. This way, when NASA updates its image page, the code will still pull the most recent image.

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# ## Mars Facts

# Scrape HTML table and store in new df
# The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
# By specifying an index of 0, we’re telling Pandas to pull only the first table it encounters.
df = pd.read_html('http://space-facts.com/mars/')[0]

# Assign columns to the new DataFrame for additional clarity
df.columns=['Description', 'Mars']

# Turn the Description column into the DataFrame’s index. inplace=True means that the updated index will remain 
# in place, without having to reassign the DataFrame to a new variable.
df.set_index('Description', inplace=True)
df

# Convert stored df back into HTML format so it can be added to a website
df.to_html()

# End the automated browsing session
browser.quit()