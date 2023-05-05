import pandas as pd
import cufflinks as cf
import numpy as np
import requests
from datetime import date, datetime
import mysql.connector
import sys

today = date.today()
#Connection to the database
mydb = mysql.connector.connect(user='root', password='root', host='mysql', port="3306", database='STOCKS')
print("DB connection success")
cursor = mydb.cursor(buffered=True)

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
    #def get_stock_ratios(ticker):
     #   url = f"https://financialmodelingprep.com/api/v3/ratios/{ticker}?limit=1&apikey={api_key}"
      #  response = requests.get(url)
       # data = response.json()
        #df = pd.DataFrame(data)
        #df = df.T
    #  current_ratio = ratio_df.loc['currentRatio']
    # quick_ratio = ratio_df.loc['quickRatio']
        #return df
class PortValue:
    def __init__(self):
        self.portfolio = {}
        user = self

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

    ''' def get_input(self):
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
                
                
    '''


    def execute(self):
        time = datetime.now()
        quote = EquityValue.get_stock_quote(self.ticker)
        ratio = EquityValue.get_stock_ratios(self.ticker)
        wallet_balance = cursor.execute("SELECT Wallet_Balance FROM User WHERE User = "+self.user)
        if not quote:
            return
        price = quote[0]['price']
        print(ratio)

        if self.transaction_type == "buy":
            cost = price * self.quantity
            print(f"Bought {self.quantity} shares of {self.ticker} at ${price:.2f} each, for a total cost of ${cost:.2f} at {time}")
            self.port_value.update_portfolio(self.ticker, self.quantity)
            cursor.execute("UPDATE User SET share_holdings = "+self.ticker+" WHERE User = "+self.user)
            mydb.commit()
            cursor.execute("UPDATE User SET buy_price = "+(price)+" WHERE User = "+self.user)
            mydb.commit()
            cursor.execute("UPDATE User SET Wallet_Balance = "+(wallet_balance - price)+"WHERE User = "+self.user)
            cursor.execute()
            mydb.close()
        elif self.transaction_type == "sell":
            if self.ticker in self.port_value.portfolio and self.port_value.portfolio[self.ticker] >= self.quantity:
                cost = price * self.quantity
                print(f"Sold {self.quantity} shares of {self.ticker} at ${price:.2f} each, for a total revenue of ${cost:.2f} at {time}")
                self.port_value.update_portfolio(self.ticker, -self.quantity)
                cursor.execute("DELETE User SET share_holdings = "+self.ticker+" WHERE User = "+self.user)
                mydb.commit()
                cursor.execute("DELETE User SET buy_price = "+(price)+" WHERE User = "+self.user)
                mydb.commit()
                cursor.execute("UPDATE User SET Wallet_Balance = "+(wallet_balance + price)+"WHERE User = "+self.user)
                cursor.execute()
                mydb.close()
            else:
                print(f"Error: Not enough quantity of {self.ticker} to sell")
        else:
            print("Invalid transaction type")
            return

        self.port_value.get_portfolio_value()
        self.port_value.portfolio.items()

class MoneyTransfer:
    def MoneyTransfer (User1,User2,TransferAmount):
        # Takes the amount in Users Wallets
        User1Wallet = cursor.execute("SELECT wallet_balance FROM user_info WHERE user = '"+User1+"';")
        User2Wallet = cursor.execute("SELECT wallet_balance FROM user_info WHERE user = '"+User2+"';")

        # Updates the value in User1 Wallet (sender)
        cursor.execute("UPDATE user_info SET wallet_balance = "+(User1Wallet-TransferAmount)+"WHERE user = '"+User1+"';")

        # Updates value in User2 Wallet (receiver)
        cursor.execute("UPDATE user_info SET wallet_balance = "+(User2Wallet-TransferAmount)+"WHERE user = '"+User2+"';")
        mydb.close()

def main():
    #port_value = PortValue()
    #transaction = Stock_Transaction(port_value)
    #transaction.execute()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'MoneyTransfer':
            MoneyTransfer.MoneyTransfer(sys.argv[2],sys.argv[3], sys.argv[3])
        elif sys.argv[1] == 'StockInformation':
            EquityValue.get_stock_quote(sys.argv[2])
        elif sys.argv[1] == 'StockTransaction':
            Stock_Transaction.execute(sys.argv[2])
        else:
            print("Error no arg passed")
    

    mydb.close()

if __name__ == "__main__":
    main()
