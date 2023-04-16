import httpx
import itertools
import os
from datetime import datetime
from tqdm import tqdm
import asyncio
from math import ceil


async def main():
    # get the user's search request and format it for the API query
    request = '%20'.join([l for l in input(
        'Enter your search request: ').split() if l.isalnum() or l == " "])
    # set the initial page number to 1 and display the search query
    page_num = itertools.count(1)
    print(f'Looking for pictures by "{request}" keyword...')
    url = f"https://api.pexels.com/v1/search/?page=1&per_page=80&query={request}"
    headers = {
        'Authorization': 'DTjupNdHYTzWLml43pfzssxY1irC0VPrKXGzrQyHYS4av62lxd0zJ7Yb'}
    # create an empty list to store image URLs
    link_list = []

    async def link_gettin():
        # construct the API request URL with the current page number
        url = f"https://api.pexels.com/v1/search/?page={next(page_num)}&per_page=80&query={request}"
        # send an asynchronous request to the API and parse the JSON response
        content = await client.get(url, headers=headers)
        content_json = content.json()
        # extract the list of photos from the response and add their URLs to the link_list
        page_photos_list = content_json.get('photos')
        for pics in page_photos_list:
            # getting urls of pics in original size
            link_list.append(pics.get('src').get('original'))

    # def link_writin(link_list): # write the list of image URLs to a text file
    #     print('Going to download pics now..')
    #     with open(f'{request}_photos.txt', 'w') as f:
    #         for line in link_list:
    #             f.write(line + '\n')

    def pic_downloadin(list_with_links):
        # create a folder to store the downloaded images
        title = f'{request}_{datetime.now().strftime("%B_%d_%H_%M")}'
        os.mkdir(title)
        os.chdir(title)
        # download each image using the httpx library and display progress with tqdm
        with httpx.Client() as client:
            for link in tqdm(list_with_links, desc='Downloading pictures...'):
                with open(f"{link.split('/')[-1].split('.')[0]}.jpg", 'bw') as f:
                    f.write(client.get(link).content)
        print(f'Pictures are stored in: {os.path.abspath(os.getcwd())}')

    # create an asynchronous httpx client and send a request to the API
    async with httpx.AsyncClient() as client:
        content = await client.get(url, headers=headers)
        content_json = content.json()
        page_count = ceil(int(content_json.get('total_results'))/80)
        await asyncio.gather(*[link_gettin() for _ in range(1, page_count+1)])
        # display the total number of images found and raise an error if none were found
        print(f'{len(link_list)} pictures found in total...')
        assert len(
            link_list) > 0, f'No pictures were found by your request..'
        pic_downloadin(link_list)

if __name__ == '__main__':
    asyncio.run(main())
