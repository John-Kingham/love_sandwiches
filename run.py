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

sales = SHEET.worksheet("sales")
data = sales.get_all_values()


def get_sales_data():
    """Get valid sales figures from user

    Returns:
        List[str]: Validated sales data
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data valid")
            break
    return sales_data


def validate_data(values):
    """Validate that the user has entered 6 integers.

    Args:
        values (List[str]): Values entered by the user

    Returns:
        bool: True if user entered 6 integers, otherwise False
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            msg = f"Exactly 6 values required, you provided {len(values)}"
            raise ValueError(msg)
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True


data = get_sales_data()
