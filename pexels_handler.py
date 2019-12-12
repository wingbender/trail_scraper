"""
Temporary, check the pexels API

DONT RUN THIS IN A LOOP! we have 200 calls an hour and 20_000 monthly
"""
import json
import requests

FLICKR_API_KEY = 'b21cb88140f105550d356495c1f37cc7'
FLICKR_URL = 'https://www.flickr.com/services/rest/'
FLICKR_DEFAULT_PARAMS = {'method': 'flickr.photos.search',
                         'api_key': FLICKR_API_KEY,
                         'sort': 'interestingness-desc',
                         'geo_context': 2,
                         'content_type': 1,
                         'format': 'json',
                         'per_page': 5,
                         'page': 1,
                         'nojsoncallback': 1
                         }

PEXELS_API_KEY = '563492ad6f91700001000001784b26c694dc40b4beaf229d9c0fd2b6'
PEXELS_SEARCH_URL = 'https://api.pexels.com/v1/search'


def get_pexels(search_word=None):
    if not search_word:
        return None
    req_headers = {
        'Authorization': PEXELS_API_KEY
    }
    query_params = {
        'query': search_word,
        'per_page': 5,
        'page': 1
    }
    response = requests.request('GET', PEXELS_SEARCH_URL, params=query_params, headers=req_headers)
    response.raise_for_status()
    photos = json.loads(response.text)
    urls = []
    for photo in photos['photos']:
        urls.append(photo['url'])
    return urls


def get_flickr(search_word = None, search_lat=None, search_lon=None):
    """
    Returns a list of urls for pictures from flickr that corresponds to 'search_word'.
    if 'search word' returns no results, it returns urls of pictures taken around lat-lon (in 5 km radius)
    """
    params = FLICKR_DEFAULT_PARAMS

    if search_word:
        params['text'] = search_word
        params['sort'] = 'interestingness-desc'
        response = requests.request('GET', FLICKR_URL, params=params)
        response.raise_for_status()
        photos = json.loads(response.text)

        if photos['photos']['total'] != '0':
            print(photos['photos']['total'])
            urls = []
            for photo in photos['photos']['photo']:
                urls.append(f'https://farm{photo["farm"]}.staticflickr.com/'
                            f'{photo["server"]}/{photo["id"]}_{photo["secret"]}_z.jpg')
            return urls
    if search_lon and search_lat:

        if 'text' in params.keys():
            params['text']
        if 'sort' in params.keys():
            del params['sort']
        params['lat'] = search_lat
        params['lon'] = search_lon
        params['radius'] = 5
        response = requests.request('GET', FLICKR_URL, params=params)
        response.raise_for_status()
        photos = json.loads(response.text)
        print(photos['photos']['total'])
        if photos['photos']['total'] != '0':
            urls = []
            for photo in photos['photos']['photo']:
                urls.append(f'https://farm{photo["farm"]}.staticflickr.com/'
                            f'{photo["server"]}/{photo["id"]}_{photo["secret"]}_z.jpg')
            return urls
    return None


def main():
    pass


def test():
    # search_word = 'En Karem'

    search_word = None
    lat, lon = 31.455977, 35.383519
    lat = 41.747774
    lon = 2.631495
    pex_urls = get_pexels(search_word)
    # print('\n'.join(pex_urls))

    flickr_urls = get_flickr(search_word=search_word, search_lat=lat, search_lon=lon)

    print('------------------')
    print('\n'.join(flickr_urls))


if __name__ == '__main__':
    test()
    main()
