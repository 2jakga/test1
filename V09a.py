import time
import pyupbit
import datetime
import pandas

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

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

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

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

def rsi(ohlc: pandas.DataFrame, period: int = 14):
     delta = ohlc["close"].diff() 
     ups, downs = delta.copy(), delta.copy()
     ups[ups < 0] = 0 
     downs[downs > 0] = 0 
     
     AU = ups.ewm(com = period-1, min_periods = period).mean() 
     AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
     RS = AU/AD 
     
     return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

access = "m0uV5VEpMw9uNrvDlxUXvahxvYYG2O3KGNW3vRsJ"
secret = "iRmSf6ovpVTpSzPnyxDLYEMcvKYmbsPo9QE8gQuw"
upbit = pyupbit.Upbit(access, secret)
print("autotrade start - V7 210919 ")


print("보유 현금 :",get_balance("KRW"))

# keyin = input("Start (Y/N) : ")
# y=keyin
# print(keyin)
# if keyin == "Y" or "y":
#   print("loading....")


krwlist = pyupbit.get_tickers(fiat="KRW") #KRW 전체 종목 리스트 
# coinlist = ["KRW-ELF", "KRW-BTC", "KRW-BCHA", "KRW-EOS", "KRW-XRP", "KRW-EOS", "KRW-ARK"]
# coinlist = ["KRW-ARK", "KRW-AERGO", "KRW-LOOM", "KRW-ATOM", "KRW-BCHA", "KRW-MTL", "KRW-LSK"]  #9/19 기준 주간 TOP4 + 일간 TOP3
coinlist = krwlist
print(coinlist)  #전체 리스트
# print(len(coinlist)) #전체 수량


RSI28 = []
RSI70 = []
RSI33 = []
RSI33C = []

for i in range(len(coinlist)):
  RSI28.append(False)  
  RSI70.append(False)
  RSI33.append(False)
  RSI33C.append(0)




# 시장가 매수 함수 1
def buy1(coin): 
    money = get_balance("KRW") 
    if money < 100000 : 
        res = upbit.buy_market_order(coin, money)         
    else : 
        res = upbit.buy_market_order(coin, 100000) 
    return 

# 시장가 매수 함수 2
def buy2(coin): 
    money = get_balance("KRW") 
    if money < 50000 : 
        res = upbit.buy_market_order(coin, money)         
    else : 
        res = upbit.buy_market_order(coin, 50000) 
    return 

# 시장가 매도 함수2 
def sell1(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = get_current_price(coin)
    total = amount * cur_price 
    if total < 50000 : 
        res = upbit.sell_market_order(coin, amount) 
    else : 
        res = upbit.sell_market_order(coin, amount*0.5) 
    return


while(True):                    
    for i in range(len(coinlist)):
        now = datetime.datetime.now()
        start_time = get_start_time(coinlist[i])
        end_time = start_time + datetime.timedelta(days=1)
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")  #3분봉 기준

        if start_time < now < end_time - datetime.timedelta(seconds=60):
            
            target_price1 = get_target_price(coinlist[i], 0.1)            
            ma15 = get_ma15(coinlist[i])
            # ma7 = get_ma7(coinlist[i])
            current_price = get_current_price(coinlist[i]) 

            if data is not None:                    
                now_rsi = rsi(data, 14).iloc[-1]
                
                if target_price1 < current_price :
                
                    if  ma15 < current_price :  #안전한 상승장                               
                        print([i], coinlist[i],"  RSI :", now_rsi) 
                        if now_rsi < 35 and RSI70[i] == False : 
                            buy1(coinlist[i]) 
                            print([i],coinlist[i],"buy")
                            print()                                      
                            RSI70[i] = True     
                   
                        if now_rsi <= 28 and upbit.get_avg_buy_price(coinlist[i])*0.98 > current_price :   
                            RSI70[i] = False
                            buy2(coinlist[i])
                            print([i],coinlist[i],"water+") 
                        
                        
                        if upbit.get_avg_buy_price(coinlist[i])*0.95 > current_price :   
                            sell1(coinlist[i]) #-5% 손절
                            print([i],coinlist[i],"Die")                    
                                                              
        else :
            upbit.sell_market_order(coinlist[i], upbit.get_balance(coinlist[i]))    

        time.sleep(0.1)




