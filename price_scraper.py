import pandas as pd 
import requests
from bs4 import BeautifulSoup
import streamlit as st  # 🎈 data web app development
from info_scraper import *


with st.form(key='my_form'):
	BOOK_NAME =st.text_input(label='Enter some text')
	submit_button = st.form_submit_button(label='Submit')


#liberty
#https://www.libertybooks.com/index.php?route=product/search&search=think%20and%20grow%20rich
libertybooks_list_pages=[f"https://www.libertybooks.com/index.php?route=product/search&search={BOOK_NAME}"]

#get list pages for libertybooks
#libertybooks_list_pages=["https://www.libertybooks.com/index.php?route=product/search&search=think%20and%20grow%20rich"]

#redings
#https://www.readings.com.pk/Pages/searchresult.aspx?Keyword=think%20and%20grow%20rich
readings_list_pages=[f"https://www.readings.com.pk/Pages/searchresult.aspx?Keyword={BOOK_NAME}"]

#get list pages for readings
#readings_list_pages=["https://www.readings.com.pk/Pages/searchresult.aspx?Keyword=think%20and%20grow%20rich"]


#create selectors dictionary for libertybooks.com 
libertybooks_selectors=selectors(
    parentSelector=".box-content>.box-category.box-product>.product-items",
    prodNameSelector=".caption>h4>a",
    prodPriceSelector=".price >.price-old",
    prodDisPricSelector=".price >.price-new",
    productUrlSelector=".box-content>.box-category.box-product>.product-items .caption>h4>a",
    websiteNameSelector="libertybooks.com",
    fixedPriceSelector="p.price"
)

#create selectors dictionary for readings
readings_selectors=selectors(
    parentSelector=".product_detail_page_main #ContentPlaceHolder1_DL_Books .product_detail_page_outer_colum",
    prodNameSelector=".product_detail_page_left_colum_author_name>h5>a",
    prodPriceSelector=".our_price>h6 .linethrough",
    prodDisPricSelector=".our_price>h6 .linethrough+span",
    productUrlSelector=".product_detail_page_left_colum_author_name>h5>a",
    websiteNameSelector="readings.com.pk",
    fixedPriceSelector=".our_price>h6 .linethrough"
)
if submit_button:
    #collect data from libertybooks
    for lb in libertybooks_list_pages:
        scraper(
            lb,
            libertybooks_selectors)

    #collect data from readings
    for rd in readings_list_pages:
        scraper(
            rd,
            readings_selectors)

    df= pd.DataFrame(output_data)
    df.to_csv(f"data.csv")

    col1, col2 = st.columns(2)

    with col1:
        st.title('Readings')
        readings_df=df[df['website_name']=="readings.com.pk"].iloc[0]
        st.header(readings_df["prod_name"])
        st.text(readings_df["prod_price"])
        st.text(readings_df["Product_discount_price"])

    with col2:
        st.title('libertybooks')
        liberty_df=df[df['website_name']=="libertybooks.com"].iloc[0]
        st.header(liberty_df["prod_name"])
        st.text(liberty_df["prod_price"])
        st.text(liberty_df["Product_discount_price"])