# Amazon-Scraper
A web scraper for Amazon developed in Python using the Selenium and BeautifulSoup packages for TAMU Datathon 2021. It finds the average price of up to the first twenty pages of listings matching a user-specified search term, produces a bar chart with the price distribution of those listings, and outputs the title, price, rating, and review count of each listing to a .csv file. The user is able to exclude listings based on number of reviews, overall rating, and whether the listing is sponsored.

# Dependencies
[selenium](https://pypi.org/project/selenium/)

[beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

# Usage
To use the program, the user first needs to compile and execute WebScrape.py. The program will then begin to request input from the user; the user simply needs to enter their response to each of the input requests, one by one. The user should avoid entering floating values for the minimum number of ratings and the number of pages to look through.

## Example Input and Output
The following image shows a set of example responses to the input requests:

![](https://i.imgur.com/dm8Tcqe.png)

Which produced the following output, at the time it was executed:

![](https://i.imgur.com/JVsY2mL.png)


# Demo
Should the user still be confused after reading the above instructions, the following demo video may be of use:

[![Amazon Scraper](https://img.youtube.com/vi/Zu_i5F4LV-A/0.jpg)](https://www.youtube.com/watch?v=Zu_i5F4LV-A)
