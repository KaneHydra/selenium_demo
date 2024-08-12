# -*- coding=utf-8 -*-
import tkinter as tk
from tkinter import ttk
import csv

# Read the CSV file and store the data in a dictionary
currency_data = {}
with open(
    "./data/currency-price_2024-08-12_10-05.csv", newline="", encoding="utf-8"
) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        currency_data[row["外幣"]] = row

# Currency shorthand codes
currency_shorthand = {
    "新臺幣": "TWD",
    "美元": "USD",
    "澳幣": "AUD",
    "加拿大幣": "CAD",
    "港幣": "HKD",
    "瑞士法郎": "CHF",
    "日圓": "JPY",
    "歐元": "EUR",
    "紐西蘭幣": "NZD",
    "新加坡幣": "SGD",
    "南非幣": "ZAR",
    "瑞典克朗": "SEK",
    "泰銖": "THB",
    "人民幣": "CNY",
    "印度幣": "INR",
    "丹麥幣": "DKK",
    "土耳其里拉": "TRY",
    "墨西哥披索": "MXN",
    "越南幣": "VND",
    "菲律賓披索": "PHP",
    "馬來西亞幣": "MYR",
    "韓圜": "KRW",
    "印尼盾": "IDR",
}


# Function to perform the conversion
def convert_from_source_currency():
    currency = currency_var.get()
    action = action_var.get()
    try:
        amount = float(source_amount_entry.get())
    except ValueError:
        amount = 0
    if currency in currency_data:
        rate = 0
        if action == "Buy":
            rate = float(currency_data[currency]["即期買入"])
        elif action == "Sell":
            rate = float(currency_data[currency]["即期賣出"])
        result = amount * rate
        result_var.set(f"{result:.2f}")
        # result_label.config(text=f"Result: {result:.2f} TWD")
    else:
        result_var.set("Currency not found")
        # result_label.config(text="Currency not found")


# Function to perform the conversion
def convert_from_result_currency():
    currency = currency_var.get()
    action = action_var.get()
    try:
        amount = float(result_amount_entry.get())
    except ValueError:
        amount = 0
    if currency in currency_data:
        rate = 0
        if action == "Buy":
            rate = float(currency_data[currency]["即期買入"])
        elif action == "Sell":
            rate = float(currency_data[currency]["即期賣出"])
        source = amount / rate
        source_var.set(f"{source:.2f}")
        # result_label.config(text=f"Result: {result:.2f} TWD")
    else:
        source_var.set("Currency not found")
        # source_label.config(text="Currency not found")


# Function to update the result unit label
def update_result_unit(event=None):
    currency = currency_var.get()
    result_unit_var.set(currency_shorthand.get(currency, ""))


# Create the main window
root = tk.Tk()
root.title("Currency Converter")

# Create and place the widgets
source_var = tk.StringVar(value="0")
tk.Label(root, text="Source amount:").grid(row=0, column=0, padx=10, pady=10)
source_amount_entry = tk.Entry(root, textvariable=source_var)
source_amount_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Label(root, text="TWD").grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Action:").grid(row=1, column=0, padx=10, pady=10)
action_var = tk.StringVar(value="Buy")
action_menu = ttk.Combobox(root, textvariable=action_var, values=["Buy", "Sell"])
action_menu.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Currency:").grid(row=2, column=0, padx=10, pady=10)
currency_var = tk.StringVar(value="美元")
currency_menu = ttk.Combobox(
    root, textvariable=currency_var, values=list(currency_data.keys())
)
currency_menu.grid(row=2, column=1, padx=10, pady=10)
currency_menu.bind("<<ComboboxSelected>>", update_result_unit)

# Create and place the widgets
result_var = tk.StringVar(value="0")
tk.Label(root, text="Result amount:").grid(row=3, column=0, padx=10, pady=10)
result_amount_entry = tk.Entry(root, textvariable=result_var)
result_amount_entry.grid(row=3, column=1, padx=10, pady=10)
result_unit_var = tk.StringVar(value="USD")
tk.Label(root, textvariable=result_unit_var).grid(row=3, column=2, padx=10, pady=10)

convert_from_source_button = tk.Button(
    root, text="Convert\nFrom\nSource", command=convert_from_source_currency
)
convert_from_source_button.grid(row=4, column=1, padx=10, pady=10)

convert_from_result_button = tk.Button(
    root, text="Convert\nFrom\nResult", command=convert_from_result_currency
)
convert_from_result_button.grid(row=4, column=2, padx=10, pady=10)

# Run the application
root.mainloop()
