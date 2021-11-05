import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')
# used to test API was working
# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)


def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter sales data fromt he last market.")
    print("Data should be six numbers, seperated by commas.")
    print("Example: 10,20,30,40,50,60\n")
    while True:
        data_str = input("Enter your data here: \n")
        # Splits the input by the comma
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False
    return True


# def update_sale_worksheet(data):
#     """
#     Update sales worksheet with new row from the input provided by the user
#     """
#     print("Updating sales worksheet.....\n")
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully\n")


# def update_surplus_worksheet(surplus_data):
#     """
#     Update surplus worksheet with new row from the input provided by the user
#     """
#     print("Updating surplus worksheet.....\n")
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(surplus_data)
#     print("Surplus worksheet updated successfully\n")

# The above was refactored into the below function

def update_worksheet(data, worksheet):
    """
    Review a list of integers and update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet.....\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully....\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data.....\n")
    stock = SHEET.worksheet('stock').get_all_values()
    # a special way to print a list of lists....
    # # pprint(stock)
    # ^ remember to import pprint at the top of the file ^
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns form the sales worksheet, collecting
    the last 5 entries for each sandwich and retruns the data
    as a list of lists.
    """
    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        # last_5_entries = column[-5:] long hand of the below
        columns.append(column[-5:])
    
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each itm type, and add 10%
    """
    print("calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("welcome to the Love sandwiches Data automation")
main()
