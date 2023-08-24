#!/usr/bin/env python
# coding: utf-8

# In[1]:


import openai


# In[2]:


import pandas as pd
import numpy as np
from tqdm import tqdm
import os


# In[3]:


import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans


# In[4]:


API_KEY = os.getenv("OPENAI_API_KEY")


# ## Load

# In[5]:


filename = input("Enter file (csv with text column): ")
## Text df
df = pd.read_csv(f"./data/{filename}.csv")

# Embeddings
embeddings = np.load(f"./data/{filename}.npy")


# ## Cluster

# In[6]:


def plot_elbow(matrix):
    """
    Features to fit Kmeans on
        Could be embeddings.
    """
    wcss = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(matrix)
        wcss.append(kmeans.inertia_)

    # Plot the elbow plot
    plt.plot(range(1, 11), wcss)
    plt.title('Elbow Plot')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    plt.show()


# In[7]:


plot_elbow(embeddings)


# ### Colating Datasets

# In[8]:


def label_clusters(matrix, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, init="k-means++",
                    random_state=1)
    kmeans.fit(matrix)
    labels = kmeans.labels_

    df = pd.DataFrame()
    df['Cluster'] = labels
    return df


# In[9]:


df['Cluster'] = label_clusters(embeddings, n_clusters=8)


# In[10]:


df.rename(columns={'text': 'combined'}, inplace=True)


# ## Sample and Completion

# In[19]:


# Reading a review which belong to each group.
rev_per_cluster = int(input("Integer samples per cluster: "))
try:
    n_clusters = int(input("Integer Number of clusters (From analysing elbow plot pop-up): "))
except ValueError:
    n_clusters = 1
my_prompt = input("Ask a question about your data: ")


# In[20]:


def sample(df, rev_per_cluster, replace=False):
    reviews = "\n".join(
    df[df.Cluster == i]
    .combined.str.replace("Title: ", "")
    .str.replace("\n\nContent: ", ":  ")
    .sample(rev_per_cluster, random_state=42, replace=replace)
    .values
    )
    return reviews


# In[24]:


responses = []
for i in tqdm(range(n_clusters)):
    print(f"Cluster {i} Theme:", end=" ")
    
    try:
        reviews = sample(df, rev_per_cluster)
    except ValueError:
        reviews = sample(df, rev_per_cluster, replace=True)
        
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f'{my_prompt}:\n"""\n{reviews}\n"""\n\nTheme:',
    temperature=0,
    max_tokens=64,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )
    
    filtered_response = response["choices"][0]["text"].replace("\n", "")
    responses.append(filtered_response)
    
    print(filtered_response)

#     sample_cluster_rows = df[df.Cluster == i].sample(rev_per_cluster, random_state=42)
#     for j in range(rev_per_cluster):
#         print(sample_cluster_rows.Score.values[j], end=", ")
#         print(sample_cluster_rows.Summary.values[j], end=":   ")
#         print(sample_cluster_rows.Text.str[:70].values[j])

#     print("-" * 100)


# ## Save

# In[25]:


with open(f"./data/{filename}_summary.txt", "w", encoding='utf-8') as f:
    f.write(my_prompt + '\n\n')
    for response in responses:
        f.write("-" * 100 + '\n\n')
        f.write(response + '\n')


# In[ ]:




