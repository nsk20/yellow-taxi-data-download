import os
import subprocess
import requests
from bs4 import BeautifulSoup

def find_parquet_files(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        parquet_files = [link['href'] for link in links if link['href'].endswith('.parquet')]
        return parquet_files
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

def download_yellow_tripdata_files(file_urls, download_dir):
    yellow_tripdata_urls = [url for url in file_urls if "yellow_tripdata_2024" in url]
    for url in yellow_tripdata_urls:
        file_name = url.split('/')[-1]
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(download_dir, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download {file_name}. Status code: {response.status_code}")

def git_add_commit_push(repo_path, commit_message):
    os.chdir(repo_path)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

# Example usage
url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
parquet_files = find_parquet_files(url)
print("Parquet files found:", parquet_files)

download_dir = "parquet_files"
os.makedirs(download_dir, exist_ok=True)
download_yellow_tripdata_files(parquet_files, download_dir)

repo_path = "/path/to/your/repo"  # Update this path
commit_message = "Add downloaded Parquet files to new folder"
git_add_commit_push(repo_path, commit_message)
