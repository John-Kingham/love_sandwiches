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
    """Get valid sales figures from user

    Returns:
        List[int]: Validated sales data
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")
        sales_data = input("Enter your data here: ").split(",")
        if data_is_valid(sales_data):
            print("Data valid")
            break
    return [int(data) for data in sales_data]


def data_is_valid(values):
    """Validate that user entered 6 integers.

    Args:
        values (List[str]): Values entered by user

    Returns:
        bool: True if user entered 6 integers, else False
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


def update_sales_worksheet(data):
    """Update sales spreadsheet with data from user

    Args:
        data (List[int]): Sandwich sales data from user
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales data updated successfully.\n")


def update_surplus_data(data):
    """Update surplus worksheet with calculated surplus values.

    Args:
        data (List[int]): A row of surplus amounts.
    """
    print("Updating surplus worksheet...\n")
    surplus_sheet = SHEET.worksheet("surplus")
    surplus_sheet.append_row(data)
    print("Surplus data updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus stock.
    The surplus is defined as sales minus stock:
        - Positive surplus indicates waste
        - Negative surplus indicates extra sandwiches had to be made

    Args:
        sales_row (List[int]): Sales data for each sandwich type.
    """
    print("Calculating surplus data...\n")
    stock_row = SHEET.worksheet("stock").get_all_values()[-1]
    stock_row = [int(data) for data in stock_row]
    surplus_row = []
    for stock, sales in zip(stock_row, sales_row):
        surplus_row.append(stock - sales)
    print(surplus_row)
    return surplus_row


def main():
    """
    Run the Love Sandwiches program
    """
    print("Welcome to LOVE SANDWICHES DATA AUTOMATION.\n")
    sales_data = get_sales_data()
    update_sales_worksheet(sales_data)
    surplus_data = calculate_surplus_data(sales_data)
    update_surplus_data(surplus_data)


if __name__ == "__main__":
    main()
