import numpy as np
import pandas as pd
import pickle
import streamlit as st
import json
import math

result = None

with open(
        r"C:\Users\Mohammed Naser\Desktop\MHP\model\mumbai_home_prices_model.pickle", 
        'rb') as f:
    __model = pickle.load(f)

with open(r"C:\Users\Mohammed Naser\Desktop\MHP\model\columns.json", 'r') as obj:
    __data_columns = json.load(obj)["data_columns"]
    __locations = __data_columns[2:]


def get_estimated_price(location,area,bedrooms):
    try:
        loc_index = __data_columns.index(location)
    except ValueError as e:
        loc_index = -1

    lis = np.zeros(len(__data_columns))
    lis[0] = area
    lis[1] = bedrooms

    if loc_index >= 0:
        lis[loc_index] = 1

    price = round(__model.predict([lis])[0], 2)
    strp = ' lakhs'

    if math.log10(price) >= 2:
        price = price / 100
        price = round(price, 2)
        strp = " crores"

    return str(price) + strp


def main():
    global result
    html_temp = """
           <div>
           <h2>House Price Prediction </h2>
           </div>
           """
    st.markdown(html_temp, unsafe_allow_html=True)
    area = st.text_input("Area (in sqft)")
    bedrooms = st.text_input("Number of Bedrooms")
    location = st.selectbox("Location", __locations)

    if st.button("Predict"):
        result = get_estimated_price(location,area,bedrooms)

    st.success(f"Price => {result}")


if __name__ == "__main__":
    main()