# Trail Scraper

Web scraper to extract trails from www.wikiloc.com

## Getting Started

This python program will help you extract all the trails from your favorite category on wikiloc.com
simply download the files and run wikiloc_scraper.py with command line arguments described below

### Prerequisites

You'll need python 3.6 with "requests", "BeautifulSoup" and "re" to run this functions.


## Using the program
after downloading, run wikiloc_scraper.py with the following command line arguments:

[-h] : show help message
[-c category to scrape int]: category to scrape by number
[-C category to scrape string]: category to scrape by name
[-r trails range]: range of trails to scrape e.g.: '14-76'
[-FF]: scrape the entire site. if this flag is passed all others will be ignored


for example: 
  wikiloc_scraper.py -c 4 -r 5-50
  will extract trails 5 through 50 from the 4th category (Hiking trails)

## Authors

* **Sagiv Yaari** - *Initial work* - [wingbender](https://github.com/wingbender)
* **Roi Weinberger** - *Initial work* - [RoiWR](https://github.com/roiwr)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


* count dracula (Roi)
* dad (Sagiv)
* Thank you tal for the cereals (Both)
