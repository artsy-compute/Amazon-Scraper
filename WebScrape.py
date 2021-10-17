# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:08:22 2021

@author: formi
"""

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import matplotlib.pyplot as plt

def get_url(search_term):
    template = 'https://amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')
    
    #add search term to url
    url = template.format(search_term)
    
    #add page query placeholder
    url += '&page={}'
    
    return url

def extract_record(item, min_ratings, min_stars, sponsored):
    #sponsored
    isSponsored = item.find('span', {'class': 'a-color-base'}).text
    
    #title
    titleTag = item.h2.a
    title = titleTag.text.strip()
    
    try:
        #price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    
    try:
        #rating and review count
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    
    tempReviewCount = review_count
    if(review_count.find(',') != -1):
        tempReviewCount = review_count[0:review_count.index(',')] + review_count[review_count.index(',')+1]
    
    if(rating != ''):
        if(float(rating[0:3]) < min_stars or float(tempReviewCount) < min_ratings):
            return
    
    if(min_ratings != 0 and review_count == ''):
        return
    if(min_stars != 0 and rating == ''):
        return
    
    if(sponsored == 'n' and isSponsored == 'Sponsored'):
        return
    result = (title, price, rating, review_count)
    
    return result

def main(search_term, min_ratings, min_stars, pages, name_csv, sponsored):
    driver = webdriver.Chrome()
    records = []
    url = get_url(search_term)
    
    for page in range(1, pages+1):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in results:
            record = extract_record(item, min_ratings, min_stars, sponsored)
            if record:
                gonnaAdd = True
                for i in range(len(records)):
                    if(records[i][0] == record[0] and records[i][1] == record[1] and records[i][2] == record[2] and records[i][3] == record[3]):
                        gonnaAdd = False
                if(gonnaAdd):
                    records.append(record)
    driver.close()
    
    with open(name_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Price', 'Rating', 'Review Count'])
        writer.writerows(records)
    
    totalPrice = 0
    prices = []
    for i in range(len(records)):
        currPrice = records[i][1][1:]
        while(currPrice.find(',') != -1):
            currPrice = currPrice[0:currPrice.index(',')] + currPrice[currPrice.index(',')+1:]
        totalPrice += float(currPrice)
        prices.append(float(currPrice))
    
    avgPrice = totalPrice/len(records)
    
    titles = []
    for i in range(len(records)):
        titles.append(i)
    
    plt.bar(titles, prices)
    plt.title('Prices of Listings')
    plt.xlabel('Item')
    plt.ylabel('Price (in USD)')
    plt.show()
    

def firstPrint():
    print('Howdy! This program finds the average price on Amazon of up to the first twenty pages of listings matching your search term.')
    print('It also produces a bar chart showing the price of each individual listing, as well as a .csv file with the title, price, rating, and review count of each listing.\n')
    print('You may choose your minimum number of ratings, minimum star rating, whether to include sponsored listings, and the number of pages to look through.\n')
    beginOrNot = input('Would you like to begin? (y/n) ')
    
    if(beginOrNot=='y'):
        prompt()
    else:
        print('Goodbye.')
        
def prompt():
    search_term = input('What is your search query? ')
    min_ratings = int(input('How many ratings must the listing have to be included? '))
    min_stars = float(input('How many stars must the listing have to be included? (supports floating values) '))
    pages = int(input('How many pages to search through? '))
    sponsored = input('Include sponsored listings? (y/n) ')
    name_csv = input('What should the name of the output file be? (ex: phones.csv) ')
    
    main(search_term, min_ratings, min_stars, pages, name_csv, sponsored)
    
    continueOrNot = input('Would you like to try another search? (y/n) ')
    if(continueOrNot=='y'):
        prompt()
    else:
        print('Goodbye.')

firstPrint()