CREATE DATABASE IF NOT EXISTS `STOCKS`;
GO
USE `STOCKS`;
GO
ALTER TABLE `stock_info` (
  -- `stock_name` varchar(100) NOT NULL,
  -- `recent_price` varchar(50) NOT NULL,
  -- `purchase_price` varchar(50) NOT NULL,
  -- `10_day_price` varchar(50) NOT NULL,
  -- `monthly_price` varchar(50) NOT NULL,
  -- `quantity` varchar(50) NOT NULL,
  -- `purchase_date` varchar(50) NOT NULL,
  -- `sell_date` varchar(50) NOT NULL,
  `todays_date` date
);
GO