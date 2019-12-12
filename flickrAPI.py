""" Flickr API - implementation for Wikiloc Scraper
Given coordinates (latitude and longitude) extracted from the initial trail coordinates of a trail in wikiloc.com,
this API returns a list of image urls within a radius of that location from Flickr.com
authors: Roi Weinberger & Sagiv Yaari. Date: December 2019 """

import json
import requests


class FLICKR():
    def __init__(self, method='photos.search', geo_context=2,):
        self.api_key = 'b21cb88140f105550d356495c1f37cc7'
        self.flickr_url = 'https://www.flickr.com/services/rest/'
        self.params = {'method': 'flickr.photos.search',
                       'api_key': self.api_key,
                       'sort': 'interestingness-desc',
                       'geo_context': 2,
                       'content_type': 1,
                       'format': 'json',
                       'page': 1,
                       'nojsoncallback': 1
                       }

    def __get_urls_from_json(self, data):
        if data['photos']['total'] == '0':
            print(f"No photos were found on Flickr in {self.params['radius']} from the trail location")
            return ''
        else:
            urls = []
            for photo in data['photos']['photo']:
                url_str = f'https://farm{photo["farm"]}.staticflickr.com/'\
                          f'{photo["server"]}/{photo["id"]}_{photo["secret"]}_z.jpg'
                urls.append(url_str)
            return urls

    def get_photos_url(self, lat, lon, radius=5, no_of_photos=5):
        self.params['lat'] = lat
        self.params['lon'] = lon
        self.params['radius'] = radius
        self.params['per_page'] = no_of_photos
        response = requests.request('GET', self.flickr_url, params=self.params)
        response.raise_for_status()
        data = json.loads(response.text)
        return self.__get_urls_from_json(data)


def test():
    lat, lon = 31.455977, 35.383519  # Ein - Gedi coordinates
    f = FLICKR()
    flickr_urls = f.get_photos_url(lat, lon)
    print('------------------')
    print('\n'.join(flickr_urls))


def main():
    test()


if __name__ == "__main__":
    main()