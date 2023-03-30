import requests

api_key = "76aca232cf48b7732e7d62cf2fd91072"

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

class PortValue:
    def __init__(self):
        self.portfolio = {}

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

            

class Stock_Transaction:
    def __init__(self, port_value):
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
            print(f"{self.ticker} is currently trading at {price:.2f}")
            buy_stock = input("Would you like to purchase this stock? (y/n): ")
            if buy_stock.lower() == "y":
                self.transaction_type = "buy"
                self.quantity = int(input("Enter quantity: "))
                return True
            else:
                return False

    def execute(self):
        quote = EquityValue.get_stock_quote(self.ticker)
        if not quote:
            return

        price = quote[0]['price']

        if self.transaction_type == "buy":
            cost = price * self.quantity
            print(f"Bought {self.quantity} shares of {self.ticker} at ${price:.2f} each, for a total cost of ${cost:.2f}")
            self.port_value.update_portfolio(self.ticker, self.quantity)
        elif self.transaction_type == "sell":
            revenue = price * self.quantity
            print(f"Sold {self.quantity} shares of {self.ticker} at ${price:.2f} each, for a total revenue of ${revenue:.2f}")
            self.port_value.update_portfolio(self.ticker, -self.quantity)
        else:
            print("Invalid transaction type")
            return

        self.port_value.get_portfolio_value()

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


