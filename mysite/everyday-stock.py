from bs4 import BeautifulSoup
import urllib.request as req
import datetime

nd_url="https://finance.yahoo.com/quote/%5EIXIC?p=%5EIXIC"
kp_url='https://finance.yahoo.com/quote/%5EKS11?p=^KS11&.tsrc=fin-srch'
kd_url='https://finance.yahoo.com/quote/%5EKQ11?p=^KQ11&.tsrc=fin-srch'

res_nd=req.urlopen(nd_url)
res_kp=req.urlopen(kp_url)
res_kd= req.urlopen(kd_url)

soup_nd = BeautifulSoup(res_nd, "lxml")
soup_kp= BeautifulSoup(res_kp, "lxml")
soup_kd= BeautifulSoup(res_kd, "lxml")

nasdaq= soup_nd.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)").string
nasdaq_diff= soup_nd.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(500\).Pstart\(10px\).Fz\(24px\).C\(\$positiveColor\)").string

kospi= soup_kp.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)").string
kospi_diff= soup_kp.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(500\).Pstart\(10px\).Fz\(24px\).C\(\$negativeColor\)").string

kosdaq = soup_kd.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)").string
kosdaq_diff= soup_kd.select_one("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(500\).Pstart\(10px\).Fz\(24px\).C\(\$positiveColor\)").string
all=kospi+" " +kospi_diff+ " "+ kosdaq+" "+kosdaq_diff+" " + nasdaq+" " + nasdaq_diff+ " " +datetime.datetime.now().strftime("%H:%M")
t= datetime.datetime.now()
fname="/srv/django/price.txt"
with open(fname, "w", encoding="utf-8") as f:
    f.write(all)