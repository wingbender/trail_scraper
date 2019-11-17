import requests


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
        page = requests.get(page_url, headers=get_headers())
        page.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return -1
    except Exception as err:
        print(f'Non HTTP error occurred: {err}')
        return -1
    if page.status_code == 200:
        return page
    else:
        return -1


def test():
    pass


if __name__ == '__main__':
    test()
