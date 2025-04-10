"""
Garrett Safsten, Jack Mair, Tanner Crookston, Ryan Baldwin
Description: 
"""
import sqlalchemy as sq # Does same as psycopg2 except it helps when working with pandas.
from sqlalchemy import create_engine, text
import pandas as pd
import psycopg2 # We can work with sql.
import matplotlib.pyplot as plot

productCategoriesDict = {
        'Camera': 'Technology',
        'Laptop': 'Technology',
        'Gloves': 'Apparel',
        'Smartphone': 'Technology',
        'Watch': 'Accessories',
        'Backpack': 'Accessories',
        'Water Bottle': 'Household Items',
        'T-shirt': 'Apparel',
        'Notebook': 'Stationery',
        'Sneakers': 'Apparel',
        'Dress': 'Apparel',
        'Scarf': 'Apparel',
        'Pen': 'Stationery',
        'Jeans': 'Apparel',
        'Desk Lamp': 'Household Items',
        'Umbrella': 'Accessories',
        'Sunglasses': 'Accessories',
        'Hat': 'Apparel',
        'Headphones': 'Technology',
        'Charger': 'Technology'}


while True :
    try:
        options = int(input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: "))
        if options == 1:
            file_path = "Retail_Sales_Data.xlsx"

            df = pd.read_excel(file_path) # df stands for dataframe

            username = 'postgres'
            password = '123456'
            host = 'localhost'
            port = '5432'
            database = 'is303'

            engine =  create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}') # This connects python to postgres sql 
            dfSeparatedNames = df["name"].str.split("_", expand = True)
            df["first_name"] = dfSeparatedNames[0]  # First part
            df["last_name"] = dfSeparatedNames[1]   # Second part
            print(df.head())          
            
            df.to_sql('sale', con=engine, if_exists='replace', index=True)
            print("You've imported the excel file into your postgres database.")

        elif options == 2:
            continue
        else:
            print("Exiting Program. Goodbye.")
            break
    
    except ValueError:
        print("Please enter a whole integer (ex. '1')")
