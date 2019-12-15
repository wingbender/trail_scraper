# Trail Scraper

Web scraper to extract trails from www.wikiloc.com and find nearby images from www.Flickr.com using their API.

## Getting Started

This python program will help you extract all the trails from your favorite category on wikiloc.com
into an MySQL database. Simply download the files and run wikiloc_scraper.py with command line arguments.

### Prerequisites

You'll need python 3.6 with "requests", "BeautifulSoup", "re" and "pymysql" to run these functions.


## Using the program
1) Run the create_db.py file in order to create locally a MySQL database.

    a. See trail_DB.pdf for the database diagram.
    
    b. The credentials.py file can be edited for each user access to its server.


2) Run wikiloc_scraper.py with the following command line arguments:

    [-h] : show help message
    
    [-c category to scrape int]: category to scrape by number
    
    [-C category to scrape string]: category to scrape by name
    
    [-r trails range]: range of trails to scrape e.g.: '14-76'
    
    [-f]: extracts the max number of trails from a category
    
    [-FF]: scrape the entire site. if this flag is passed all others will be ignored
    
    [-p]: Enter the number of photos to extract from Flickr API. Default is 5



For example: 
  wikiloc_scraper.py -c 1 -r 5-50 -p 5
  Will extract trails 5 through 50 from the 1th category (mountain biking) and 5 nearby photos from Flickr


## Authors

* **Sagiv Yaari** - *Initial work* - [wingbender](https://github.com/wingbender)
* **Roi Weinberger** - *Initial work* - [RoiWR](https://github.com/roiwr)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* count dracula (Roi)
* dad (Sagiv)
* Thank you tal for the cereals (Both)
