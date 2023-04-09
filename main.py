import httpx
import itertools
import os
from datetime import datetime
request = '%20'.join([''.join([l for l in letter if l.isalnum()]) for letter in input(
    'Enter your search request: ').split()])
print(request)
page_num = itertools.count(1)
url = f"https://api.pexels.com/v1/search/?page={next(page_num)}&per_page=10&query={request}"
print(url)
headers = {
    'Authorization': 'DTjupNdHYTzWLml43pfzssxY1irC0VPrKXGzrQyHYS4av62lxd0zJ7Yb'}
link_list = []


def link_gettin(url):
    with httpx.Client() as client:
        content = client.get(url, headers=headers)
        while True:
            if not content.status_code == 200:
                print(content.status_code)
                break
            if "next_page" not in content.json().keys():
                link_list.extend([pics.get('src').get('original')
                                  for pics in content.json().get('photos')])
                break
            link_list.extend([pics.get('src').get('original')
                             for pics in content.json().get('photos')])
            print('Moving to the next page...')
            url = f"https://api.pexels.com/v1/search/?page={next(page_num)}&per_page=80&query={request}"
            content = client.get(url, headers=headers)


def link_writin(link_list):
    print('Going to download pics now..')
    with open(f'{request}_photos.txt', 'w') as f:
        for line in link_list:
            f.write(line + '\n')


def pic_downloadin(links):
    title = f'{request}_{datetime.now().strftime("%d:%H:%M")}'
    os.mkdir(title)
    os.chdir(title)
    with httpx.Client() as client:
        for link in links:
            print(link.split('-')[-2])
            with open(f"{link.split('/')[-1].split('.')[0]}.jpg", 'bw') as f:
                f.write(client.get(link).content)

    print(f'Photos are stored in {os.path.abspath(os.getcwd())}')


link_gettin(url)
link_writin(link_list)
pic_downloadin(link_list)
