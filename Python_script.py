#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[2]:


def find_parquet_files(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the links on the page
        links = soup.find_all('a', href=True)

        # Filter links that end with '.parquet'
        parquet_files = [link['href'] for link in links if link['href'].endswith('.parquet')]

        return parquet_files
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []


# In[3]:


def download_yellow_tripdata_files(file_urls):
    # Filter URLs that contain "yellow_tripdata"
    yellow_tripdata_urls = [url for url in file_urls if "yellow_tripdata" in url]

    # Download each file
    for url in yellow_tripdata_urls:
        # Extract the file name from the URL
        file_name = url.split('/')[-1]

        # Send a GET request to download the file
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the file locally
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download {file_name}. Status code: {response.status_code}")


# In[4]:


# Example usage
url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
parquet_files = find_parquet_files(url)
print("Parquet files found:", parquet_files)


# In[5]:


download_yellow_tripdata_files(parquet_files)

