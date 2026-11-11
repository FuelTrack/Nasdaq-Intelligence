#!/usr/bin/env python3
"""Collect daily close prices and public headline links. Standard library only."""
import json, os, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

SYMBOLS = ['QQQ','AAPL','MSFT','NVDA','AMZN','GOOGL','META','TSLA','AVGO','AMD','NFLX','COST']
PATH = 'data/market.json'
HEADERS = {'User-Agent':'Mozilla/5.0 NasdaqIntelligence/1.0 (public research dashboard)','Accept':'application/json, application/xml, text/xml, */*'}

def fetch(url):
    request=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(request,timeout=15) as response:
        return response.read()

def prices(symbol):
    url='https://query1.finance.yahoo.com/v8/finance/chart/'+urllib.parse.quote(symbol)+'?range=3mo&interval=1d'
    payload=json.loads(fetch(url))
    result=payload['chart']['result'][0]
    timestamps=result['timestamp']
    quotes=result['indicators']['quote'][0]['close']
    history=[{'date':datetime.fromtimestamp(t,timezone.utc).strftime('%Y-%m-%d'),'close':round(float(p),4)} for t,p in zip(timestamps,quotes) if p is not None]
    if not history: raise ValueError('No daily closes')
    last=history[-1]['close']
    prior=history[-2]['close'] if len(history)>1 else None
    return {'close':last,'date':history[-1]['date'],'change_pct':round((last/prior-1)*100,2) if prior else None,'history':history[-60:]}

def news():
    query=urllib.parse.quote('NASDAQ stocks OR technology stocks OR Federal Reserve when:2d')
    xml=fetch('https://news.google.com/rss/search?q='+query+'&hl=en-US&gl=US&ceid=US:en')
    root=ET.fromstring(xml)
    items=[]
    for item in root.findall('./channel/item')[:20]:
        link=item.findtext('link') or ''
        if not link.startswith('https://'): continue
        published=item.findtext('pubDate') or ''
        try: published=parsedate_to_datetime(published).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
        except (ValueError,TypeError): pass
        items.append({'title':item.findtext('title') or 'Untitled','url':link,'source':item.findtext('source') or 'Google News','published':published})
    return items

def main():
    os.makedirs('data',exist_ok=True)
    try:
        with open(PATH,encoding='utf-8') as f: old=json.load(f)
    except (OSError,ValueError): old={}
    snapshot={'updated':datetime.now(timezone.utc).isoformat(),'prices':{},'news':[],'errors':[]}
    for symbol in SYMBOLS:
        try: snapshot['prices'][symbol]=prices(symbol)
        except Exception as exc:
            snapshot['errors'].append(symbol+': '+str(exc)[:120])
            if symbol in old.get('prices',{}): snapshot['prices'][symbol]=old['prices'][symbol]
        time.sleep(.35)
    try: snapshot['news']=news()
    except Exception as exc:
        snapshot['errors'].append('news: '+str(exc)[:120])
        snapshot['news']=old.get('news',[])
    with open(PATH,'w',encoding='utf-8') as f: json.dump(snapshot,f,indent=2,ensure_ascii=False)
    print('Updated',len(snapshot['prices']),'prices and',len(snapshot['news']),'headlines;',len(snapshot['errors']),'errors')

if __name__=='__main__': main()
