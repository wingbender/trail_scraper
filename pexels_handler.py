"""
Temporary, check the pexels API

DONT RUN THIS IN A LOOP! we have 200 calls an hour and 20_000 monthly
"""
import json
import requests

# flickr = 'https://www.flickr.com/services/api/flickr.photos.search.html'

PEXELS_API_KEY = '563492ad6f91700001000001784b26c694dc40b4beaf229d9c0fd2b6'
ADOBE_API_KEY = 'dbfa43a664b64f30abe53ccb6c7e6ba5'
ADOBE_PRODUCT_NAME = 'Trail thumbnails API'

pexels_search_url = 'https://api.pexels.com/v1/search'
adobe_search_url = 'https://stock.adobe.io/Rest/Media/1/Search/Files'


def get_pex(search_word=None):
    req_headers = {
        'Authorization': '%s' % PEXELS_API_KEY
    }
    query_params = {'query': search_word}
    response = requests.request('GET', pexels_search_url, params=query_params, headers=req_headers)
    return json.loads(response.text)


def get_adobe(search_word=None):
    req_headers = {'x-api-key': ADOBE_API_KEY, 'x-product': ADOBE_PRODUCT_NAME}
    search_parameters = {'words': search_word}
    response = requests.request(method='GET', url=adobe_search_url, headers=req_headers, params=search_parameters)
    return json.loads(response.text)

def main():
    pass


def test():
    search_word = 'Pozuelo de Alarcón'
    print(get_pex(search_word))
    # print(get_adobe(search_word))


if __name__ == '__main__':
    test()
    main()
