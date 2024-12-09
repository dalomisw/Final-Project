"""
This program works as a currency exchange rate tracker and lookup tool. 
Any currency can be inputted using the openexchangerates.org API. There is a base currency
of USD that is used for the exchange rates. The program can also predict the trend of the 
exchange rate and convert between two currencies using USD.
This program can also plot predictions based on historical data.
Wikoria Dalomis
"""
import requests
import matplotlib.pyplot as plt
import datetime
import numpy

APP_ID = "8a6ffee0a3ae4e5f9bb46fc324709a7c"

def main():
    """
    The main function that runs the program.
    """
    print("Welcome to the Currency Exchange Rate Tracker!")
    while True:
        option = main_menu()
        if option == "1":
            convert_usd_to_currency_from_user()
        elif option == "2":
            convert_between_currencies_from_user()
        elif option == "3":
            user_run_predictions()
        elif option == "4":
            break
        else:
            print("Invalid option. Please try again.")

def get_available_currencies():
    """
    Gets a list of all available currency codes.
    """
    response = requests.get("https://openexchangerates.org/api/currencies.json")
    response.raise_for_status()
    return list(response.json().keys())

def get_current_rates():
    """
    Gets the latest exchange rates.
    """
    response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={APP_ID}")
    response.raise_for_status()
    return response.json()

def get_historical_rates(date):
    """
    Gets the historical exchange rates for a specific date.
    """
    response = requests.get(f"https://openexchangerates.org/api/historical/{date}.json?app_id={APP_ID}")
    response.raise_for_status()
    return response.json()['rates']


def convert_usd_to_currency(amount, type_of_currency):
    """
    Takes the USD value and converts it into any other currency.
    """
    response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={APP_ID}")
    response.raise_for_status()
    currency_rates = response.json()['rates']
    return amount * currency_rates[type_of_currency]


def predict_trend(exchange_rates):
    """
    Predict the currency trends using linear regression.
    """
    if not exchange_rates:
        raise ValueError("No exchange rates provided.")
    x = list(range(1, len(exchange_rates) + 1))
    y = exchange_rates  # Directly use the list of floats
    slope, intercept = numpy.polyfit(x, y, 1)
    trend = "upward" if slope > 0 else "downward" if slope < 0 else "stable"
    return slope, intercept, trend

def select_currency(prompt):
    """
    Have user select the currency they want to convert (validated).
    """
    currencies = get_available_currencies()
    while True:
        print(prompt)
        for i, currency in enumerate(currencies):
            print(f"{i+1}. {currency}")
        selection = input("Enter the number corresponding to the currency: ")
        if selection.isdigit() and 1 <= int(selection) <= len(currencies):
            return currencies[int(selection) - 1]
        else:
            print("Invalid selection. Please try again.")


def plot_predictions(historic_data, slope, intercept, currency):
    """
    Plots the historical exchange rates and the predicted trend line.
    """
    if isinstance(historic_data, dict):
        y = list(historic_data.values())
    elif isinstance(historic_data, list):
        y = historic_data
    else:
        raise TypeError("historic_data must be a list or a dictionary")

    x = list(range(len(y)))
    predicted_y = [slope * xi + intercept for xi in x]

    plt.plot(x, y, label='Historical Data')
    plt.plot(x, predicted_y, label='Predicted Trend', linestyle='--')
    plt.xlabel('Days')
    plt.ylabel('Exchange Rate')
    plt.title(f'Exchange Rate Trend for {currency}')
    plt.legend()
    plt.show()

def convert_between_currencies(amount, original_currency, new_currency):
    """
    Converts the amount of one selected currency into another one using the USD currency as a bridge.
    """
    get_current_rates()
    response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={APP_ID}")
    response.raise_for_status()
    currency_rates = response.json()['rates']
    usd_amount = amount / currency_rates[original_currency]
    new_amount = usd_amount * currency_rates[new_currency]
    return new_amount

def main_menu():
    """
    Displays the main menu and returns the user's choice.
    """
    print("\nMain Menu:")
    print("1. Convert USD to another currency")
    print("2. Convert between two currencies")
    print("3. Predict exchange rate trend")
    print("4. Exit")
    return input("Please choose an option (1-4): ")

def get_int_from_user(prompt, min_value, max_value):
    """
    Gets an integer from the user with validation.
    """
    while True:
        try:
            user_input = int(input(prompt))
            if min_value <= user_input <= max_value:
                return user_input
            else:
                print("Invalid input. Please enter a value within the specified range.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def convert_usd_to_currency_from_user():
    """
    Gets the amount and currency from the user then performs the conversion and displays the results.
    """
    amount = get_positive_number_from_user("Enter the amount in USD: ")
    currency = select_currency("Select the currency to convert to:")
    converted_amount = convert_usd_to_currency(amount, currency)
    print(f"{amount} USD is equal to {converted_amount} {currency}.")

def get_positive_number_from_user(prompt):
    """
    Gets a positive number from the user with validation.
    """
    while True:
        try:
            user_input = float(input(prompt))
            if user_input > 0:
                return user_input
            else:
                print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def convert_between_currencies_from_user():
    """
    Gets the amount and currencies from the user then performs the conversion and displays the results.
    """
    amount = get_positive_number_from_user("Enter the amount to convert: ")
    original_currency = select_currency("Select the original currency: ")
    new_currency = select_currency("Select the new currency: ")
    converted_amount = convert_between_currencies(amount, original_currency, new_currency)
    print(f"{amount} {original_currency} is equal to {converted_amount} {new_currency}.")


def user_run_predictions():
    """
    The user enters the name of a currency and how many days should be analyzed, and then it 
    displays information about the highest value and lowest value it has had in that period
    along with performing a linear regression to compute the future values. 
    """
    currency = select_currency("Select the currency to analyze: ")
    number_of_days = get_int_from_user("Enter the number of days to analyze: ", 1, 365)
    exchange_rates = get_exchange_rate_for_many_days(currency, number_of_days)
    slope, intercept, trend = predict_trend(exchange_rates)
    plot_predictions(exchange_rates, slope, intercept, currency)
    
def get_exchange_rate_for_many_days(currency, number_of_days):
    """
    Gets the historic exchange rate for the previous several days. 
    """

    rates = []
    today = datetime.date.today()
    for i in range(number_of_days):
        date = today - datetime.timedelta(days=i+1)
        formatted_date = date.strftime("%Y-%m-%d")
        rates.append(get_historical_rates(formatted_date)[currency])
    return rates


if __name__ == "__main__":
    main()

