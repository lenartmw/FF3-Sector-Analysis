# FF3-Sector-Analysis
The project demonstrates how the Fama French Three Factor model alphas of three selected sectors change throughout the business cycle

# Sectors #

The three sectors include:
* Technology Select Sector SPDR Fund (XLK)
* Health Care Select Sector SPDR Fund (XLV)
* Financial Select Sector SPDR Fund (XLF)

# Data #
The prices and daily returns of the funds were obtained and calculated as follows:
```ruby
import datetime
import yfinance as yf

tickers = ['XLK', 'XLV', 'XLF']
start_date = datetime.date(1999, 1, 1)
end_date = datetime.date(2024, 6, 1)
df = yf.download(tickers, start=start_date, end=end_date, interval='1mo')
df1 = df['Adj Close'].dropna()
df2 = df1.pct_change()
df2 = df2.dropna()

df2.to_csv('sectorsdata.csv', index=False)
```

The Fama French Three Factors data was downloaded from [the Kenneth R. French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html). <br>
The business cycles' dates were sourced from [NBER](https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions).

[1]: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html            "the Kenneth R. French Data Library"
[2]: https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions            "NBER"

