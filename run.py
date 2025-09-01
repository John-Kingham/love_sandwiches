# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """Get valid sales figures from user.

    Returns:
        List[int]: Validated sales data.
    """
    while True:
        print_instructions()
        sales_data = input("Enter your data here:\n").split(",")
        if data_is_valid(sales_data):
            break
    return [int(data) for data in sales_data]


def print_instructions():
    """
    Show data entry instructions to user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")


def data_is_valid(values):
    """Validate that user entered 6 integers.

    Args:
        values (List[str]): Values entered by user.

    Returns:
        bool: True if user entered 6 integers, else False.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            msg = f"Exactly 6 values required, you provided {len(values)}"
            raise ValueError(msg)
        return True
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False


def update_worksheet(name, data):
    """Add a row of data to a worksheet.

    Args:
        name (str): Name of the worksheet.
        data (List[int]): A row of data.
    """
    print(f"Updating {name} worksheet...\n")
    SHEET.worksheet(name).append_row(data)
    print(f"{name} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus stock.
    The surplus is defined as sales minus stock:
        - Positive surplus indicates waste.
        - Negative surplus indicates extra sandwiches had to be made.

    Args:
        sales_row (List[int]): Sales data for each sandwich type.
    """
    print("Calculating surplus data...\n")
    stock_row = SHEET.worksheet("stock").get_all_values()[-1]
    stock_row = [int(data) for data in stock_row]
    surplus_row = []

    for stock, sales in zip(stock_row, sales_row):
        surplus_row.append(stock - sales)
    return surplus_row


def get_last_5_sales_entries():
    """
    Get the last 5 sales entries for each sandwich type.

    Return:
        List[List[int]]: Each inner list contains the last 5 entries for a
        sandwich type.
    """
    print("Getting recent sales for stock calculation...\n")
    sales = SHEET.worksheet("sales")
    last_5_entries = []
    num_sandwich_types = 6

    for i in range(num_sandwich_types):
        # note: col_values() is 1-based rather than 0-based
        last_5_rows_str = sales.col_values(i + 1)[-5:]
        last_5_entries.append([int(data) for data in last_5_rows_str])
    return last_5_entries


def calculate_stock_data():
    """Calculate the amount of stock required for the next market.

    Returns:
        List[int]: The required stock amount for each sandwich type.
    """
    print("Calculating required stock levels...\n")
    sales_data = get_last_5_sales_entries()
    stock_data = []
    margin_of_safety = 1.1

    for column in sales_data:
        avg_sales = sum(column) / len(column)
        stock_data.append(round(avg_sales * margin_of_safety))
    return stock_data


def main():
    """
    Run the Love Sandwiches program.
    """
    print("LOVE SANDWICHES DATA AUTOMATION\n")

    sales_data = get_sales_data()
    update_worksheet("sales", sales_data)
    update_worksheet("surplus", calculate_surplus_data(sales_data))
    update_worksheet("stock", calculate_stock_data())

    print("Love Sandwiches database updated successfully.\n")


if __name__ == "__main__":
    main()
