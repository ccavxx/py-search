#!/usr/bin/env python2
from bs4 import BeautifulSoup as bsfrom requests.packages.urllib3 import connectionpoolimport requestsimport timeimport logging
# EDIT START
cookies = {'ALIPAYJSESSIONID': ''}api = ''key = ''
# EDIT END
url = 'https://lab.alipay.com/consume/record/items.htm'logging.basicConfig(filename='/tmp/alipay.log', level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y%m%d %H:%M:%S')connectionpool.log.setLevel(logging.WARNING)

def getPaymentID(soup):    PaymentID = [] for i in soup.select('.consumeBizNo'):        PaymentID.append(i.string.strip()) return PaymentID

def getTime(soup):    Time = []    timeFormat = '%Y-%m-%d %H:%M:%S' for i in soup.select('.time'):        Time.append(int(time.mktime(time.strptime(i.string, timeFormat)))) return Time

def getName(soup):    Name = [] for i in soup.select('.emoji-li'): for ii in i.stripped_strings:            Name.append(ii) return Name

def getAmount(soup):    Amount = [] for i in soup.select('.amount.income'):        Amount.append(i.string) return Amount

def postData(PaymentID, Time, Name, Amount):    data = { 'key': key, 'ddh': PaymentID, 'time': Time, 'name': Name, 'money': Amount    } try:        requests.post(api, data=data, timeout=5) except:        logging.warning('Timeout, retrying')        postData(PaymentID, Time, Name, Amount)    logging.info('%s--%s--%s--%s' % (PaymentID, Time, Name, Amount))
if __name__ == '__main__':    posted = [] while True: if len(posted) > 1000:            posted = [] try:            req = requests.get(url, cookies=cookies) except:            logging.warning('Connect to alipay failed!') continue if req.url.startswith('https://auth.alipay.com/'):            logging.critical('Authentication failed!') import sys            sys.exit(0)        html = req.text        soup = bs(html, 'lxml') for i in soup.select('.amount.outlay'):            i.parent.decompose() for i in soup.select('.subTransCodeValue'):            i.decompose()        PaymentID = getPaymentID(soup)        Time = getTime(soup)        Name = getName(soup)        Amount = getAmount(soup)        length = len(PaymentID) for i in range(length): if not Name[i].startswith(u'\u4ed8\u6b3e-'): continue if PaymentID[i] not in posted:                postData(                        PaymentID[i],                        Time[i],                        Name[i].split('-')[1],                        Amount[i],                    )                posted.append(PaymentID[i])        time.sleep(5)