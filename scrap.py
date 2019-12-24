#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author  : Ting
Contact : ting.lik.2@gmail.com
Version : 1
Purpose : Scrap from supermarket websites
'''
import requests
from bs4 import BeautifulSoup
from market_list import market_list
from collections import defaultdict
import pprint

def main():
    location = "10494"
    store = "Whole Foods"

    URL = market_list[store] + location
    soup = BeautifulSoup(requests.get(URL).text, 'html.parser')

    link_results = soup.find_all(class_="w-sales-tile")
    item_sale_location = defaultdict(dict)

    for each_result in link_results: 
        result_dict = {}
        result_dict["brand"] = each_result.find(class_="w-sales-tile__brand").text
        print("Item brand: ", result_dict["brand"])
        result_dict["item"] = each_result.find(class_="w-sales-tile__product").text
        print("Item name: ", result_dict["item"])
        result_dict["price"] = each_result.find(class_="w-sales-tile__sale-price").text
        print("Item price: ", result_dict["price"])
        result_dict["sales_dates"] = each_result.find(class_="w-sm-txt").text 
        print("Item Sales Dates: ", result_dict["sales_dates"])
        result_dict["image_link"] = each_result.find(class_="w-sales-tile__image")["src"]
        print("Image link: ", result_dict["image_link"])
        item_sale_location[store][location] = {result_dict["item"]: result_dict}

    pprint.pprint(item_sale_location)


if __name__ == '__main__':
	main()



