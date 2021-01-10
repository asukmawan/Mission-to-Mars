# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Path to chromedriver (macOS users only)
# !which chromedriver

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/Users/death/.wdm/drivers/chromedriver/win32/87.0.4280.88/chromedriver'}
browser = Browser('chrome', **executable_path)

### Scrape New Title and Paragraph
# Convert to function by adding 'browser' argument to our function to use the browser variable we defined outside the function.
# change output variables 'news_title' and 'news_p' into the return statement so we can access the resulting variables outside the function
# Add error handling with a try/except clause to handle AttributeErrors - which come up when the webpage format has changed and scraping code doesn't match with the new HTML elements
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    # By adding try: just before scraping, we're telling Python to look for these elements. If there's an error, Python will continue to run the remainder of the code. If it runs into an AttributeError, however, instead of returning the title and paragraph, Python will return nothing instead.
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text() 
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    return news_title, news_p


# ## JPL Space Images Featured Image
# Convert code to a function for Featured Image
# 1. Define the function
# 2. Remove prints and return them instead
# 3. Add error handling: AttributeError

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# ## Mars Facts
# Convert code to function for Mars Facts
# 1. Define the function: mars_facts
# 2. Remove print statements or wanted outputs into return: df.to_html()
# 3. Error Handling with try/except: BaseException
    # A BaseException is a little bit of a catchall when it comes to error handling. 
    # It is raised when any of the built-in exceptions are encountered and it won't handle any user-defined exceptions. 
    # We're using it here because we're using Pandas' read_html() function to pull data, instead of scraping with BeautifulSoup and Splinter. 
    # The data is returned a little differently and can result in errors other than AttributeErrors, which is what we've been addressing so far.
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

browser.quit()