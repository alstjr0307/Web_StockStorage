
#!/usr/bin/python3

import yfinance as yf
import datetime

tickers = [ '^KS11', '^KQ11','^IXIC']
datas=[]
for ticker in tickers:
    ticker_yahoo = yf.Ticker(ticker)
    datam = ticker_yahoo.history()
    last_quote = (datam.tail(1)['Close'].iloc[0])
    lasst_quote = (datam.tail(2)['Close'].iloc[0])
    gap = (last_quote-lasst_quote)*100/lasst_quote 
    datas.append(round(last_quote,2))
    tmp = round(gap,2)
    if tmp>=0:
        datas.append('+'+str(round(gap,2))+'%')
    else:
        datas.append('-'+str(round(gap,2))+'%')
kospi, kospi_diff, kosdaq, kosdaq_diff, nasdaq, nasdaq_diff = str(datas[0]),str(datas[1]),str(datas[2]),str(datas[3]),str(datas[4]),str(datas[5])
fname="/srv/django/price.txt"   
print(datas)
all = kospi+" " +kospi_diff+ " "+ kosdaq+" "+kosdaq_diff+" " + nasdaq+" " + nasdaq_diff+ " " +datetime.datetime.now().strftime("%H:%M")
with open(fname, "w", encoding="utf-8") as  f:
    f.write(all)