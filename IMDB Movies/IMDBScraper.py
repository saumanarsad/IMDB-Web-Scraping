#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor


# In[2]:


# Step 1: Retrieve HTML content
url = 'https://www.imdb.com/chart/top'
response = requests.get(url)
html_content = response.content


# In[3]:


# Step 2: Parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')
movies_table = soup.find('tbody', {'class': 'lister-list'})
movies = movies_table.find_all('tr')


# In[4]:


# Create empty lists to store data
titles = []
years = []
ratings = []
directors = []

# Extract data from HTML content
for movie in movies:
    title_column = movie.find('td', {'class': 'titleColumn'})
    title = title_column.a.text
    titles.append(title)
    year = title_column.span.text.strip('()')
    years.append(year)
    rating = movie.find('td', {'class': 'ratingColumn'}).strong.text
    ratings.append(float(rating))
    director = title_column.a['title'].split(',')[0].strip('Directed by ')
    directors.append(director)


# In[7]:


# Step 3: Clean and preprocess data
data = {'Title': titles, 'Year': years, 'Rating': ratings, 'Director': directors}
movies_df = pd.DataFrame(data)
movies_df['Year'] = pd.to_datetime(movies_df['Year'])
director_counts = movies_df.groupby('Director')['Title'].count()
avg_rating_by_director = movies_df.groupby('Director')['Rating'].mean().sort_values(ascending=False)[:10]


# In[12]:


# Step 4: Create visualizations
plt.figure(figsize=(10,6))
plt.bar(avg_rating_by_director.index, avg_rating_by_director.values)
plt.title('Top 10 Directors by Average Rating and Number of Movies Directed', fontsize=16)
plt.xlabel('Director', fontsize=14)
plt.ylabel('Average Rating', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
for i, v in enumerate(avg_rating_by_director.values):
    plt.text(i-0.2, v+0.1, str(int(director_counts[avg_rating_by_director.index[i]])), fontsize=12)
plt.show()


# In[ ]:





# In[ ]:




