
import yfinance as yf
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta
import json
today = date.today().strftime('%Y-%m-%d')
yesterday = (date.today()-timedelta(1)).strftime('%Y-%m-%d')
last_month = (date.today()-timedelta(30)).strftime('%Y-%m-%d')
three_month = (date.today() - timedelta(90)).strftime('%Y-%m-%d')
last_year = (date.today() - relativedelta(years=1)).strftime('%Y-%m-%d')


tickers = [ 'QQQ', 'QLD','TQQQ','TQQQ','UPRO','UDOW','URTY','FNGU','SOXL','TECL','CURE','PILL','LABU','FAS','BNKU','DPST','WANT','NRGU','RETL','DEFN','DUSL','NAIL','DRN','TPOR','UTSL','BULZ','VTI','SPY']
data={}

for ticker in tickers:
    imsi={}
    ticker_yahoo = yf.Ticker(ticker)
    datam = ticker_yahoo.history(start=last_year, end=today )
    
    now = (datam.tail(1)['Close'].iloc[0])
    week = (datam.tail(6)['Close'].iloc[0])
    month = (datam.tail(22)['Close'].iloc[0])
    three_month = (datam.tail(66)['Close'].iloc[0])
    year = (datam.head(1)['Close'].iloc[0])
    imsi['week'] = round((now-week)*100/week,2)
    imsi['month'] = round((now-month)*100/month,2)
    imsi['three_month'] = round((now-three_month)*100/three_month,2)
    data[ticker] =imsi
fname="C:/Users/alswp/webprog/django/nasdaq_performances.json "  
with open(fname, "w", encoding="utf-8") as  f:
    f.write(json.dumps(data,indent=4))