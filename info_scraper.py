import pandas as pd 
import requests
from bs4 import BeautifulSoup

#final output for csv
output_data={
    "prod_name":[],
    "prod_price":[],
    "Product_discount_price":[],
    "product_url":[],
    "website_name":[],
}

#request headers
request_header={
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

#function to create dictionary of selectors
def selectors(
    parentSelector,
    prodNameSelector,
    prodPriceSelector,
    prodDisPricSelector,
    productUrlSelector,
    websiteNameSelector,
    fixedPriceSelector
    ): 
    return {
    "parentSelector":parentSelector,
    "prodNameSelector":prodNameSelector,
    "prodPriceSelector":prodPriceSelector,
    "prodDisPricSelector":prodDisPricSelector,
    "productUrlSelector":productUrlSelector,
    "websiteNameSelector":websiteNameSelector,
    "fixedPriceSelector":fixedPriceSelector
    }

#scraper function to collect data from each list page
def scraper(geturl,selectors):
    requesturl=requests.session()
    get_response = requesturl.get(
    url=geturl,
    headers=request_header
    )
    sop= BeautifulSoup(get_response.text, "html.parser")
    all_divs=sop.select(selectors.get('parentSelector'))
    for div in all_divs:
        try:
            output_data.get("prod_name").append(
                div.select_one(selectors.get('prodNameSelector')).text.strip())
        except:
            output_data.get("prod_name").append(None)
        
        #check  discount prices 
        if div.select_one(selectors.get('prodDisPricSelector'))==None:
            
            output_data.get("prod_price").append(
                div.select_one(selectors.get('fixedPriceSelector')).text.strip())
            
            output_data.get("Product_discount_price").append(None)
           
        else:
            
            output_data.get("prod_price").append(
                div.select_one(selectors.get('prodPriceSelector')).text.strip())
            
            output_data.get("Product_discount_price").append(
                div.select_one(selectors.get('prodDisPricSelector')).text.strip())
        
        try:
            output_data.get("product_url").append(
                div.select_one(selectors.get('productUrlSelector')).get('href'))
        except:
            output_data.get("product_url").append(None)
        try:
            output_data.get("website_name").append(selectors.get('websiteNameSelector'))
        except:
            output_data.get("website_name").append(None)

