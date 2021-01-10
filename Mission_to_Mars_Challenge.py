#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/Users/death/.wdm/drivers/chromedriver/win32/87.0.4280.88/chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# With the following line, `browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)`, we are accomplishing two things.
# 
# One is that we're searching for elements with a specific combination of tag (`ul` and `li`) and attribute (`item_list` and `slide`, respectively). For example, `ul.item_list` would be found in HTML as `<ul class=”item_list”>`.
# 
# Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# In[3]:


# Setup the HTML parser
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# Notice how we've assigned `slide_elem` as the variable to look for the `<ul />` tag and its descendent (the other tags within the `<ul />` element), the `<li />` tags? This is our parent element. This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. The `.` is used for selecting classes, such as `item_list`, so the code `'ul.item_list li.slide'` pinpoints the `<li />` tag with the class of `slide` and the `<ul />` tag with a class of `item_list`. 
# 
# CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using `select_one`, the first matching element returned will be a `<li />` element with a class of `slide` and all nested elements within it.

# ## Scrape the Article's Title
# 
# Chain `.find` on our `slide_elem` variable, as it holds information we want to find the data we are looking for - which is the content title that in a `<div />` with a class of `'content_title'`

# In[4]:


slide_elem.find("div", class_='content_title')


# ## Use `.get_text()` to return only the text
# 
# We found the title in the mix of HTML in the output above. Now we just need the text only by chaining the `.get_text()` method on our `.find()` method

# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# The first code to find the Article's title is different than just the text because Earlier, we identified the parent element and created a variable to hold it. With this new code, we’re searching within that element for the title. We’re also stripping the additional HTML attributes and tags with the use of `.get_text()`.

# # Scrape the Summary Text

# The Summary text is in the class `'article_teaser_body'`, but when we ctrl-f this class we get more than one result.
# 
# Since we only want the first article we only need the most recent one:
# 
# There are two methods used to find tags and attributes with BeautifulSoup:
# 
# - `.find()` is used when we want only the first class and attribute we've specified.
# - `.find_all()` is used when we want to retrieve all of the tags and attributes.
# 
# For example, if we were to use `.find_all()` instead of `.find()` when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one.

# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# # Scrape the Featured Image

# To get to the full-sized image on the NASA website (specifically this link: https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars), we need to click into 3 different pages:
# 
# 1. Click the FULL IMAGE button
# 2. Click the 'More Info' button
# 3. Click on the image to go to the full-size version
# 
# First we need to setup the URL:

# In[27]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# ### Using `id` as a unique identifier
# 
# In checking the HTML for the 'full image' button, there is alot of classes that can be found in other tags. But we can use `id` as its a compeltely unique identfier which can only be used one time through the entire page.
# 

# In[28]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# # Clicking a button - finding the 'more info' button
# ### Searching HTML Elements by Text 
# 
# With no unique classes or IDs for the 'more info' button can be found by searching for HTML elements by text to find it. 
# 
# We can use the `is_element_present_by_text()` method to search for an element that has the provided text. This will return a Boolean to let us know if the element is present(True) or not (False)
# 
# the `more_info_elem` is where we actualy find the link for us to click it, by employing the `browser.links.find_by_partial_text()` method to take the string `'more info'` to find the link associated with the 'more info' text
# 
# Lastly use the `.click()` function to click

# In[29]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[30]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# # Pull the most recent image
# 
# Inspecting the image we can see it is contained in a `<figure />` and `<a />` tags, and the actual link is contained in the `src`

# In[12]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# What we've done here is tell BeautifulSoup to look inside the `<figure class=”lede” />` tag for an `<a />` tag, and then look within that `<a />` tag for an `<img />` tag. Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."
# 
# We then need to take this part of the link and add it to the base URL

# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# The curly brackets hold a variable that will be inserted into the f-string when it's executed
# 
# We're using an f-string for this print statement because it's a cleaner way to create print statements; they're also evaluated at run-time. This means that it, and the variable it holds, doesn't exist until the code is executed and the values are not constant. This works well for our scraping app because the data we're scraping is live and will be updated frequently.

# # Scraping Mars Data
# ## Scraping Tables in HTML with Pandas' `.read_html()` function

# In[14]:


df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# `df = pd.read_html('http://space-facts.com/mars/')[0]` With this line, we're creating a new DataFrame from the HTML table. The Pandas function `read_html()` specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
# 
# `df.columns=['description', 'value']` Here, we assign columns to the new DataFrame for additional clarity.
# 
# `df.set_index('description', inplace=True)` By using the `.set_index()` function, we're turning the Description column into the DataFrame's index. `inplace=True` means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.

# ### Add the DataFrame to a web application with Pandas' `.to_html()` function
# 

# In[15]:


df.to_html()


# ### Mars Weather

# In[ ]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[ ]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[ ]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# In[39]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[40]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')

title_items= html_soup.find('div', class_='collapsible results')

titles = title_items.find_all('h3')

for title in titles:
    # Convert title to text and click link by title
    hemisphere_title = title.text
    title_elem = browser.links.find_by_partial_text(hemisphere_title)
    title_elem.click()
    
    # Parse the resulting html with soup and get link to image
    html = browser.html
    img_soup = soup(html, 'html.parser')
    hemisphere_url= img_soup.select_one('ul li a').get("href")
        
    hemisphere = {'image_url':hemisphere_url, 'title':hemisphere_title}
    hemisphere_image_urls.append(hemisphere)
    browser.visit(url)


# In[ ]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[16]:


browser.quit()

