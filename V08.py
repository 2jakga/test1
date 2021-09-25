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

def get_ma7(ticker):
    """7일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=7)
    ma7 = df['close'].rolling(7).mean().iloc[-1]
    return ma7

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
print("autotrade start - V8 210925 ")


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


# 시장가 매수 함수 
def buy(coin): 
    money = get_balance("KRW") 
    if money < 20000 : 
        res = upbit.buy_market_order(coin, money) 
    elif money < 50000: 
        res = upbit.buy_market_order(coin, money*0.4) 
    elif money < 100000 : 
        res = upbit.buy_market_order(coin, money*0.3) 
    else : 
        res = upbit.buy_market_order(coin, money*0.2) 
    return 

# 시장가 매도 함수 
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = get_current_price(coin)
    total = amount * cur_price 
    if total < 20000 : 
        res = upbit.sell_market_order(coin, amount) 
    elif total < 50000: 
        res = upbit.sell_market_order(coin, amount*0.4) 
    elif total < 100000: 
        res = upbit.sell_market_order(coin, amount*0.3) 
    else : 
        res = upbit.sell_market_order(coin, amount*0.4) 
    return


while(True):                    
    for i in range(len(coinlist)):
        now = datetime.datetime.now()
        start_time = get_start_time(coinlist[i])
        end_time = start_time + datetime.timedelta(days=1)
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")  #3분봉 기준

        if start_time < now < end_time - datetime.timedelta(seconds=60):
            
            target_price1 = get_target_price(coinlist[i], 0.2)
            target_price2 = get_target_price(coinlist[i], 0.3)
            ma15 = get_ma15(coinlist[i])
            # ma7 = get_ma7(coinlist[i])
            current_price = get_current_price(coinlist[i])

            if upbit.get_avg_buy_price(coinlist[i])*0.96 > current_price and upbit.get_balance(coinlist[i]) > 0.00008:
                    upbit.sell_market_order(coinlist[i], upbit.get_balance(coinlist[i]))    #-3.5% 손실 시 손절 
                    print("-3.5% 손절 완료")
            
            else :
            
                if data is not None:                    
                    now_rsi = rsi(data, 14).iloc[-1]
                    print([i],coinlist[i]) 
                    print("CASE1:",target_price1 < current_price)
                    print("CASE2:",target_price1 < current_price and ma15 < current_price)
                    print()

                    if target_price1 < current_price :
                    
                        if  ma15 < current_price :  #안전한 상승장                               
                            print("CASE2 : Safety")
                            print([i], coinlist[i],"  RSI :", now_rsi) 
                            # print("현재시간: ", datetime.datetime.now()) 
                            print()


                            if upbit.get_avg_buy_price(coinlist[i])*1.03 < current_price and upbit.get_balance(coinlist[i]) > 0.00008:
                                upbit.sell_market_order(coinlist[i], upbit.get_balance(coinlist[i]))     
                                print("3% 익절 완료")  

                            if now_rsi <= 40 : 
                                RSI28[i] = True
                                print(coinlist[i],"RSI 28 Check")
                                                
                            if now_rsi >= 43 and RSI28[i] == True :
                                print(coinlist[i],"BUY")
                                buy(coinlist[i])                        
                                RSI28[i] = False                                                                               
                            
                            if now_rsi >= 70 and RSI70[i] == False and upbit.get_avg_buy_price(coinlist[i]) < current_price: 
                                print(coinlist[i],"RSI 70 Check")
                                print(coinlist[i],"SELL")
                                sell(coinlist[i])            
                                RSI70[i] = True

                            if now_rsi <= 60 : 
                                RSI70[i] = False

                        else : #이제막 상승장  - 보수적인 매매                            
                            print("CASE1 : first")
                            print([i], coinlist[i],"  RSI :", now_rsi) 
                            # print("현재시간: ", datetime.datetime.now()) 
                            print()


                            if upbit.get_avg_buy_price(coinlist[i])*1.025 < current_price and upbit.get_balance(coinlist[i]) > 0.00008:
                                upbit.sell_market_order(coinlist[i], upbit.get_balance(coinlist[i]))   
                                print("2.5% 익절 완료") 

                            if now_rsi <= 28 : 
                                RSI28[i] = True
                                print(coinlist[i],"RSI 28 Check")
                                                
                            if now_rsi >= 33 and RSI28[i] == True :
                                print(coinlist[i],"BUY")
                                buy(coinlist[i])                        
                                RSI28[i] = False                                                                               
                            
                            if now_rsi >= 65 and RSI70[i] == False and upbit.get_avg_buy_price(coinlist[i]) < current_price: 
                                print(coinlist[i],"RSI 70 Check")
                                print(coinlist[i],"SELL")
                                sell(coinlist[i])            
                                RSI70[i] = True
                            
                            if now_rsi <= 60 : 
                                RSI70[i] = False 
                            
        else :
            upbit.sell_market_order(coinlist[i], upbit.get_balance(coinlist[i]))    

        time.sleep(0.2)




