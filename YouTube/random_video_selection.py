#!/usr/bin/env python
# coding: utf-8

# This is meant to pick a random video id and play it (mediated by selenium).

# In[1]:


import random
import time
import pandas as pd


# In[2]:


from selenium import webdriver


# In[3]:


path = "f:/Jupyter/APIs/YouTube/data/Find a Job in Germany.csv"
while True:
    try:
        df = pd.read_csv(path)
        break
    except FileNotFoundError: 
        path = input("Please enter custom path to your file:")


# In[4]:


rand_id = random.choice(df.id)


# In[5]:


url = f"https://www.youtube.com/watch?v={rand_id}"


# ## Navigate to Site

# In[ ]:


try:
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)
except WebDriverException :
    print("Slight hiccup 😁")
    time.sleep(10)
    pass


# In[ ]:


time.sleep(2400)
driver.quit()


# In[ ]:




