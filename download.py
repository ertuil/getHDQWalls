import os
import re
import time
import requests
from bs4 import BeautifulSoup

# Basic Configurations and these options can be decided by yourself
save_path = "imgs/" # Where to save these images?
resolution = "3840x2160" # It could be '3840*2160', '1920*1080', '1024*768' etc.
catagory = "nature" # It could be 'nature', 'games', 'superheroes', 'girls', 'movies', 'cars', 'artist' etc.
sleep = 2

basic_url = "https://hdqwalls.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}
urlQueue = []
maxPage = 1

# Utilities 
def makeDestDir():
    ''' mkdir in save_path '''
    try:
        os.mkdir(save_path)
    except:
        pass


# Functions
def downloadPic(name, route):
    url = basic_url + route
    name = save_path + name + ".jpg"
    print("Downloading {}".format(url),end='\t')

    try:
        image_data = requests.get(url, headers=headers).content
        with open(name, "wb+") as f:
            f.write(image_data)
            print("Success.")
    except Exception as e:
        print("Failed: " + str(e)+".")
        pass

def getPicUrl():
    url,name = urlQueue.pop()
    url = basic_url + url
    r = str(requests.get(url, headers=headers).text)
    soup = BeautifulSoup(r,features="html.parser")
    a = soup.find('span', id="c_download_btn")
    try:
        downloadPic(name, a.span.a.attrs['href'])
    except KeyError:
        pass

def getPicList(index: int):
    url = "https://hdqwalls.com/category/"+catagory+"-wallpapers/"+resolution+"/page/" + str(index)
    r = str(requests.get(url, headers=headers).text)
    soup = BeautifulSoup(r,features="html.parser")
    a = soup.find_all('a', class_="caption")
    for url in a:
        print("Add url: {}".format(url.attrs['href']))
        urlQueue.append( (url.attrs['href'],url.string))

def getMaxPages():
    url = "https://hdqwalls.com/category/"+catagory+"-wallpapers/"+resolution+"/page/1"
    r = str(requests.get(url, headers=headers).text)
    soup = BeautifulSoup(r,features="html.parser")
    a = soup.find_all('li', class_="active",text= re.compile("^Page"))
    if len(a) <= 0:
        print("Error: Cannot find max page.")
        exit(1)
    maxPage = re.search(r"\d*$" , a[0].string, flags=0)

# Main Function
def main():
    makeDestDir()
    getMaxPages()
    page = 1
    while page <= maxPage:
        getPicList(page)
        while len(urlQueue) > 0:
            getPicUrl()
            time.sleep(sleep)
        page += 1
    
if __name__ == "__main__":
    main()