CREATE DATABASE IF NOT EXISTS 'STOCKS';
USE 'STOCKS';
GO
CREATE TABLE 'user_info' (
  'user' varchar(100) NOT NULL,
  'password' varchar(50) NOT NULL,
  'wallet_balance' varchar(50) NOT NULL,
  'share_holdings' varchar(50) NOT NULL,
  'buy_price' varchar(50) NOT NULL
);