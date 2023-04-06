import pandas as pd
import cufflinks as cf
import numpy as np
import yfinance as yf
import requests
from datetime import datetime

api_key = "76aca232cf48b7732e7d62cf2fd91072"
cf.set_config_file(theme='pearl', world_readable=False)
cf.go_offline()
class EquityValue:
    @staticmethod
    def get_stock_quote(ticker):
        url = f"https://financialmodelingprep.com/api/v3/quote-short/{ticker}?apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
    def get_stock_ratios(ticker):
        url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?limit=1&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data)
        df = df.T
    #  current_ratio = ratio_df.loc['currentRatio']
    # quick_ratio = ratio_df.loc['quickRatio']
        return df
class PortValue:
    def __init__(self):
        self.portfolio = {}
        user = "brandon"

    def get_portfolio_value(self):
        total_value = 0
        for ticker, quantity in self.portfolio.items():
             quote = EquityValue.get_stock_quote(ticker)
             if quote:
                price = quote[0]['price']
                total_value += price * quantity
        print("Total Portfolio Value:", total_value)

    def update_portfolio(self, ticker, quantity):
        if ticker in self.portfolio:
            self.portfolio[ticker] += quantity
        else:
            self.portfolio[ticker] = quantity
        print(self.portfolio)

class Stock_Transaction:
    def __init__(self, port_value):
        self.user = None
        self.ticker = None
        self.quantity = None
        self.transaction_type = None
        self.port_value = port_value

    def get_input(self):
        self.ticker = input("Enter ticker symbol: ")
        quote = EquityValue.get_stock_quote(self.ticker)
        if not quote:
            print(f"No quote data for ticker {self.ticker}")
            return False
        else:
            price = quote[0]['price']
            print(f"{self.ticker.upper()} is currently trading at {price:.2f}")

            transaction_input = input("Would you like to buy or sell this stock? (buy/sell): ")
            if transaction_input.lower() == "buy":
                self.transaction_type = "buy"
                self.quantity = int(input("Enter quantity: "))
                return True
            elif transaction_input.lower() == "sell":
                if self.ticker in self.port_value.portfolio and self.port_value.portfolio[self.ticker] >= self.quantity:
                    self.transaction_type = "sell"
                    self.quantity = int(input("Enter quantity"))
                return True
            else:
                print("thank you")


    def execute(self):
        time = datetime.now()
        quote = EquityValue.get_stock_quote(self.ticker)
        ratio = EquityValue.get_stock_ratios(self.ticker)


        if not quote:
            return
        price = quote[0]['price']
        print(ratio)

        if self.transaction_type == "buy":
            cost = price * self.quantity
            print(f"Bought {self.quantity} shares of {self.ticker} at ${price:.2f} each, for a total cost of ${cost:.2f} at {time}")
            self.port_value.update_portfolio(self.ticker, self.quantity)
        elif self.transaction_type == "sell":
            if self.ticker in self.port_value.portfolio and self.port_value.portfolio[self.ticker] >= self.quantity:
                cost = price * self.quantity
                print(f"Sold {self.quantity} shares of {self.ticker} at ${price:.2f} each, for a total revenue of ${cost:.2f} at {time}")
                self.port_value.update_portfolio(self.ticker, -self.quantity)
            else:
                print(f"Error: Not enough quantity of {self.ticker} to sell")
        else:
            print("Invalid transaction type")
            return

        self.port_value.get_portfolio_value()
        self.port_value.portfolio.items()


def main():
    port_value = PortValue()
    transaction = Stock_Transaction(port_value)
    while True:
        if transaction.get_input():
            transaction.execute()
        else:
            break

if __name__ == "__main__":
    main()
