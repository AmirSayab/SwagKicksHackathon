import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def display_data(df):
    # Clear any existing rows from the Treeview widget
    treeview.delete(*treeview.get_children())

    # Display the data in the Treeview widget
    for _, row in df.iterrows():
        treeview.insert("", "end", values=(row["Sneaker Name"], row["Price"], row["Attributes"], row["Published Date"]))

def scrape_data():
    url = entry_url.get()

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Web scraping code to extract data from the website using Beautiful Soup
        data = []
        for product_item in soup.find_all('div', class_='tiles_container m--t--1'):
            # Find the product name inside the product item
            product_name_tag = product_item.find('a', class_='tile__title tc--b')
            product_name = product_name_tag.text.strip() if product_name_tag else "N/A"

            # Find the product price inside the product item
            product_price_tag = product_item.find('span', class_='p--t--1 fw--bold')
            product_price = product_price_tag.text.strip() if product_price_tag else "N/A"

            # Find the product attributes (size and brand) inside the product item
            product_attributes = product_item.find('div', class_='d--fl m--t--1').text.strip() if product_item.find('div', class_='d--fl m--t--1') else "N/A"

            # Find the product published date inside the product item
            product_published_date_tag = product_item.find('div', class_='timestamp')
            product_published_date = product_published_date_tag.text.strip() if product_published_date_tag else "N/A"

            # Add the extracted data to the list
            data.append({
                'Sneaker Name': product_name,
                'Price': product_price,
                'Attributes': product_attributes,
                'Published Date': product_published_date
            })

        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(data)

        # Display the data in the table
        display_data(df)

        # Save the data to a CSV file (append to existing file)
        output_file = "sneakers_data.csv"
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Sneaker Name", "Price", "Attributes", "Published Date"])
            if file.tell() == 0:  # Check if the file is empty (write header only once)
                writer.writeheader()
            writer.writerows(data)

        messagebox.showinfo("Success", "Data has been scraped and exported to CSV successfully!")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    # Create the main application window
    app = tk.Tk()
    app.title("Sneakers Fashion Website Scraper")

    # Create GUI elements
    label_url = tk.Label(app, text="Enter website URL:")
    label_url.pack()

    entry_url = tk.Entry(app, width=50)
    entry_url.pack()

    btn_scrape = tk.Button(app, text="Scrape Data", command=scrape_data)
    btn_scrape.pack()

    # Create Treeview widget to display the data
    treeview = ttk.Treeview(app, columns=["Sneaker Name", "Price", "Attributes", "Published Date"], show="headings")

    # Define column headings
    treeview.heading("Sneaker Name", text="Sneaker Name")
    treeview.heading("Price", text="Price")
    treeview.heading("Attributes", text="Attributes")
    treeview.heading("Published Date", text="Published Date")

    # Set column widths
    treeview.column("Sneaker Name", width=200)
    treeview.column("Price", width=100)
    treeview.column("Attributes", width=200)
    treeview.column("Published Date", width=150)

    treeview.pack()

    # Start the main loop
    app.mainloop()
