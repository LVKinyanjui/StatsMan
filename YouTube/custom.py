#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re


# In[2]:


def extract_key_from_json(json_data, target_key):
    result = []

    def search_nested(json_obj, key):
        if isinstance(json_obj, dict):
            for k, v in json_obj.items():
                if k == key:
                    result.append(v)
                elif isinstance(v, (dict, list)):
                    search_nested(v, key)
        elif isinstance(json_obj, list):
            for item in json_obj:
                search_nested(item, key)

    search_nested(json_data, target_key)
    return result


# In[3]:


def clean_string(input_string):
    # Define the regular expression pattern to match unwanted characters
    pattern = r'[^a-zA-Z_,\s]'
    
    # Use re.sub() to replace unwanted characters with an empty string
    cleaned_string = re.sub(pattern, '', input_string)
    
    return cleaned_string


# In[ ]:




