import mysql.connector
from datetime import date

today = date.today()
mydb = mysql.connector.connect(
    host = "localhost",
    user = "user",
    password = "pass"
)

cursor = mydb.cursor()

def Sale (shareName,targetWithdraw, User):
    sharePrice = cursor.execute("SELECT Recent_Price FROM Stock WHERE Share_name="+shareName)
    sharePortion = targetWithdraw / sharePrice

    wallet_value = cursor.execute("SELECT Wallet_value FROM User WHERE User_id = "+User)
    # Sets the share number to updated value
    cursor.execute("UPDATE User SET Num_Shares = "+sharePortion+" WHERE shareName="+shareName+"AND User_id = "+User)
    # Sets the wallet amount 
    cursor.execute("UPDATE User SET Wallet_value = "+(wallet_value+targetWithdraw)+"WHERE User_id = "+User)

    # Updates sell date
    cursor.execute("UPDATE Stock SET Sell_Date ="+today+" WHERE Share_Name = "+shareName)

def MoneyTransfer (User1,User2,TransferAmount):
    # Takes the amount in Users Wallets
    User1Wallet = cursor.execute("SELECT Wallet_value FROM User WHERE User_id = "+User1)
    User2Wallet = cursor.execute("SELECT Wallet_value FROM User WHERE User_id = "+User2)

    # Updates the value in User1 Wallet (sender)
    cursor.execute("UPDATE User SET Wallet_value = "+(User1Wallet-TransferAmount)+"WHERE User_id = "+User1)

    # Updates value in User2 Wallet (receiver)
    cursor.execute("UPDATE User SET Wallet_value = "+(User2Wallet-TransferAmount)+"WHERE User_id = "+User2)

    
