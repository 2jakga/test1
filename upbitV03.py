import time
import pyupbit
import datetime
import schedule
#from fbprophet import Prophet

keyin = input("Start (Y/N) : ")
y=keyin
print(keyin)
if keyin == "Y" or "y":
  print("loading....")

access = "m0uV5VEpMw9uNrvDlxUXvahxvYYG2O3KGNW3vRsJ"
secret = "iRmSf6ovpVTpSzPnyxDLYEMcvKYmbsPo9QE8gQuw"

itemname = "KRW-OMG"
Kvalue = 0.2

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


upbit = pyupbit.Upbit(access, secret)
print("autotrade start - V4 210912 ")
a=1
b=1
c=1



while True:
    try:
        
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        schedule.run_pending()
        target_price = get_target_price("KRW-OMG", 0.3)
        current_price = get_current_price("KRW-OMG")
        krw = get_balance("KRW")
        
        print(target_price, current_price)        
        print("현재시간",now,"수익률:",(1-upbit.get_avg_buy_price('KRW-OMG')/current_price)*100,"%")
                    
        if start_time < now < end_time - datetime.timedelta(seconds=60): #09:00~17:59
            if target_price < current_price : #예상가격이 현재가격보다 낮으면 매수 (상승신호 간주)
                if krw > 5000:                 
                     if a<2:                
                        upbit.buy_market_order("KRW-OMG", krw*0.6*0.9995) #보유금의 60% 매수 (수수로 감안)
                        print(a,"매수 평균단가:",upbit.get_avg_buy_price('KRW-OMG')) 
                        a=a+1

        
        if upbit.get_avg_buy_price('KRW-OMG')*1.05 < current_price :
            btc = get_balance("OMG")
            print(btc)
            if btc > 0.00008:
             upbit.sell_market_order("KRW-OMG", btc)
             a=0
             print("익절") 
              
            
        if upbit.get_avg_buy_price('KRW-OMG')*0.95 > current_price : # -5% 1차 추매 
            if krw > 5000:
                if c<2: 
                    upbit.buy_market_order("KRW-OMG", krw*0.4*0.9995) 
                    print("1차 추가 매수")
                    c=c+1
                    
        if upbit.get_avg_buy_price('KRW-OMG')*0.9 > current_price : #  -10% 2차 추매
            if krw > 5000:
                if b<2: 
                    upbit.buy_market_order("KRW-OMG", krw*0.9995) 
                    print("2차 추가 매수")
                    b=b+1            

        if upbit.get_avg_buy_price('KRW-OMG')*0.87 > current_price : # -13%되면 손절 
            if btc > 0.00008:
             upbit.sell_market_order("KRW-OMG", btc)
             print("익절")              
                 
        time.sleep(1)
    except Exception as e:
        
        print(e)
        
        time.sleep(1)
