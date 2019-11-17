""" Functions to request and download trail page in the website wikiloc.com
    -- Roi Weinberger & Sagiv Yaari -- Nov 2019 - ITC data science project

    The function get_page() is called by get_trail() in the file trail_scraper.py """

import requests
PAGE_TIMEOUT = 5


def get_headers():
    """
    generate headers to use when accessing a url
    # TODO implement random header generator (Not required at this time)
    :return:
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/77.0.3865.120 Safari/537.36'}
    return headers


def get_page(page_url):
    """
    returns an HTML string from page URL
    # TODO: add logging
    :param page_url:
    :return: string HTML string
    """
    try:
        page = requests.get(page_url, headers=get_headers(), timeout=PAGE_TIMEOUT)
        page.raise_for_status()
    except Exception:
        raise requests.HTTPError(Exception)
    if page.status_code == 200:
        return page
    else:
        return -1


def test():
    pass


if __name__ == '__main__':
    test()
