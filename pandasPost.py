"""
Garrett Safsten, Jack Mair, Tanner Crookston, Ryan Baldwin
Description: This code reads an excel file of data and puts it into a database in pgadmin. The user can input data and then select data that the user would like to
summarize with a pop-up chart. The user can continue to add data or summarize data until another valiue except 1 or 2 is entered.
"""
# Imported libraries
import sqlalchemy as sq # Does same as psycopg2 except it helps when working with pandas.
from sqlalchemy import create_engine, text
import pandas as pd
import psycopg2 # We can work with sql.
import matplotlib.pyplot as plot

# Dictionary with the correct key and value which is used to replace all the incorrect values in the category column.
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


while True : # This loop encompasses all the code and will keep running until user exits the code. 
        options = (input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: ")) # The menu that user can choose from and type their selection.
        # This if statement allows the user to choose 1, 2, or any other number to exit.
        if options == '1': 
            file_path = "Retail_Sales_Data.xlsx"

            df = pd.read_excel(file_path) # df stands for dataframe
            #Necessary info to access the table in postgres.
            username = 'postgres'
            password = '123456'
            host = 'localhost'
            port = '5432'
            database = 'is303'
            # This line of code connects python to postgres.
            engine =  create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}') # This connects python to postgres sql 
            dfSeparatedNames = df["name"].str.split("_", expand = True)
            df["first_name"] = dfSeparatedNames[0]  # First part
            df["last_name"] = dfSeparatedNames[1]   # Second part
            del df["name"]
            df.insert(1, 'first_name', df.pop('first_name'))  # Move first_name to column B
            df.insert(2, 'last_name', df.pop('last_name')) # Move last_name to column C          

            
            df["category"] = df["product"].map(productCategoriesDict) # Replaces each value in the category column with the correct value according to the product key in the dictionary.

            
            df.to_sql('sale', con=engine, if_exists='replace', index=True) # This sends everything we are doing from python to postgres.
            print("You've imported the excel file into your postgres database.") # Notifying the user of the completed action.
            continue

        elif options == '2':
            # 1. Print intro message
            print("The following are all the categories that have been sold:")

            # 2a. Read the entire 'sale' table into a DataFrame
            dfImported = pd.read_sql_query("SELECT * FROM sale;", engine)

            # 2b/c. Get unique categories and print them with numbers using enumerate()
            unique_categories = dfImported["category"].unique()
            category_dict = {}  # Will map number to category name

            for i, category in enumerate(unique_categories, start=1):
                print(f"{i}: {category}")
                category_dict[i] = category

            # 3. Ask the user for a category selection
            user_input = int(input("Please enter the number of the category you want to see summarized: "))

            # Translate input number to category name
            if user_input not in category_dict:
                print("Invalid selection. Please run the program again.")
            else:
                selected_category = category_dict[user_input]

                # 4a. Filter the DataFrame for the selected category
                dfCategory = dfImported.query("category == @selected_category")

                # 4b/c. Calculate required stats
                total_sales = dfCategory["total_price"].sum()
                average_sale = dfCategory["total_price"].mean()
                total_units_sold = dfCategory["quantity_sold"].sum()

                # Print summary
                print("\nSummary Statistics:")
                print(f"Total Sales: ${total_sales:,.2f}")
                print(f"Average Sale Amount: ${average_sale:,.2f}")
                print(f"Total Units Sold: {int(total_units_sold)}")

                # 5. Group by product and sum total_price
                product_sales = dfCategory.groupby("product")["total_price"].sum().reset_index()

                # Plot bar chart
                plot.figure(figsize=(10, 6))
                plot.bar(product_sales["product"], product_sales["total_price"])
                plot.title(f"Total Sales by Product in Category: {selected_category}")
                plot.xlabel("Product")
                plot.ylabel("Total Sales")
                plot.xticks(rotation=45)
                plot.tight_layout()
                plot.show()
                continue

        else: # Ends the program and exits the loop
            print("Exiting Program. Goodbye.")
            break 
    
   
