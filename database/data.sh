sleep 90s

/opt/mssql-toola/bin/sqlcmd -S localhost -U SA -P "my-secret-pw" -i setup.sql

/opt/mssql-tools/bin/bcp heroes.dbo.HeroValue in "/usr/work/stocks.csv" -c -t',' -S localhost -U SA -P "my-secret-pw" -d stocks
