#!/usr/bin/env python
# coding: utf-8

# In[10]:


import time
import subprocess
import pyautogui


# In[4]:


from custom import get_elements


# In[3]:


subprocess.Popen('c:/Users/USER/AppData/Local/Programs/deemix-gui/deemix-gui.exe')


# In[15]:


def download_deemix():
    get_elements(['deemix_unopen.jpg', 'deemix_unopen.jpg'])
    get_elements(['deemix_search.jpg'])
    pyautogui.moveRel(xOffset=100, yOffset=0)
    pyautogui.click()
    pyautogui.typewrite('Mariah Carey')
    pyautogui.press('enter')


# In[ ]:




