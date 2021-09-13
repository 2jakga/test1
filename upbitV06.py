import time
import pyupbit
import datetime

access = "m0uV5VEpMw9uNrvDlxUXvahxvYYG2O3KGNW3vRsJ"
secret = "iRmSf6ovpVTpSzPnyxDLYEMcvKYmbsPo9QE8gQuw"

coinname = 'KRW-OMG'
coin = 'OMG'


def get_target_price1(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_target_price2(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_target_price3(ticker, k):
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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start - V6 210913 ")
print("현재가 : " , get_current_price(coinname))
print("현재가 : " , get_target_price1(coinname, 0.2))
print("현재가 : " , get_target_price2(coinname, 0.5))
print("현재가 : " , get_target_price3(coinname, 0.7))

if get_current_price(coinname) > get_target_price1(coinname, 0.2):
    print("매수 가능")
else :
    print("매수 조건 불만족")


# keyin = input("Start (Y/N) : ")
# y=keyin
# print(keyin)
# if keyin == "Y" or "y":
#   print("loading....")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(coinname)
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=60):
            target_price1 = get_target_price1(coinname, 0.2) #1차 매수 기준
            target_price2 = get_target_price2(coinname, 0.5) #2차 매수 기준
            target_price3 = get_target_price3(coinname, 0.7) #3차 매수 기준
            ma15 = get_ma15(coinname)
            current_price = get_current_price(coinname)
            buy1 = 1
            buy2 = 1
            buy3 = 1
            buy4 = 1
            btc = get_balance(coin)
            
            #초기 구매
            if target_price1 < current_price < target_price2 and ma15 < current_price :
                krw = get_balance("KRW")                
                if krw > 5000:
                    if buy1 < 2:
                        krw1 = krw*0.4*0.9995
                        upbit.buy_market_order(coinname, krw1) #40% 매수                        
                        buy1 = buy1 +1  #1회 수행
                        print("1차 매수 완료")

            if target_price2 < current_price < target_price3 and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    if buy2 < 2:
                        krw2 = (krw-krw1)*(krw*0.3/(krw-krw1))*0.9995
                        upbit.buy_market_order(coinname, krw2) #30% 매수
                        buy2 = buy2 +1  #1회 수행
                        print("2차 매수 완료")

            if target_price3 < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    if buy3 < 2:
                        upbit.buy_market_order(coinname, krw*0.995) #30% 매수
                        buy3 = buy3 +1  #1회 수행
                        print("3차 매수 완료")

            #익절 후 구매
            if upbit.get_avg_buy_price(coinname)*1.05 < current_price and btc > 0.00008:
                 profit_sell = current_price
                 upbit.sell_market_order(coinname, btc)    #5% 수익 시 익절 
                 print("5% 수익 실현 후 익절 완료")
                 buy1 = 1
                 buy2 = 1
                 buy3 = 1
                 buy4 = 1
                 if profit_sell*0.97 > current_price and target_price1 < current_price < target_price2 and ma15 < current_price :
                    krw = get_balance("KRW")                
                    if krw > 5000:
                        if buy1 < 2:
                            krw1 = krw*0.4*0.9995
                            upbit.buy_market_order(coinname, krw1) #40% 매수                        
                            buy1 = buy1 +1  #1회 수행
                            print("1차 재 매수 완료")


                 if profit_sell*0.97 > current_price and target_price2 < current_price < target_price3 and ma15 < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        if buy2 < 2:
                            krw2 = (krw-krw1)*(krw*0.3/(krw-krw1))*0.9995
                            upbit.buy_market_order(coinname, krw2) #30% 매수
                            buy2 = buy2 +1  #1회 수행
                            print("2차 재 매수 완료")

                 if profit_sell*0.97 > current_price and target_price3 < current_price and ma15 < current_price:
                     krw = get_balance("KRW")
                     if krw > 5000:
                         if buy3 < 2:
                            upbit.buy_market_order(coinname, krw*0.995) #30% 매수
                            buy3 = buy3 +1  #1회 수행
                            print("3차 재 매수 완료")

            #손절 후 구매
            if upbit.get_avg_buy_price(coinname)*0.95 < current_price and btc > 0.00008:
                 loss_sell = current_price
                 upbit.sell_market_order(coinname, btc)    #-5% 손실 시 손절 
                 print("-5% 손절 완료")
                 buy1 = 1
                 buy2 = 1
                 buy3 = 1
                 buy4 = 1
                 if loss_sell*1.03 < current_price and target_price1 < current_price < target_price2 and ma15 < current_price :
                    krw = get_balance("KRW")                
                    if krw > 5000:
                        if buy1 < 2:
                            krw1 = krw*0.4*0.9995
                            upbit.buy_market_order(coinname, krw1) #40% 매수                        
                            buy1 = buy1 +1  #1회 수행
                            print("1차 손절 후 재 매수 완료")

                 if loss_sell*1.03 < current_price and target_price2 < current_price < target_price3 and ma15 < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000:
                        if buy2 < 2:
                          krw2 = (krw-krw1)*(krw*0.3/(krw-krw1))*0.9995
                          upbit.buy_market_order(coinname, krw2) #30% 매수
                          buy2 = buy2 +1  #1회 수행
                          print("2차 손절 후 재 매수 완료")

                 if loss_sell*1.03 < current_price and target_price3 < current_price and ma15 < current_price:
                     krw = get_balance("KRW")
                     if krw > 5000:
                         if buy3 < 2:
                            upbit.buy_market_order(coinname, krw*0.995) #30% 매수
                            buy3 = buy3 +1  #1회 수행
                            print("3차 손절 후 재 매수 완료")
                    
               

        else:
            if upbit.get_avg_buy_price(coinname)*0.95 < current_price and btc > 0.00008:
                 loss_sell = current_price
                 upbit.sell_market_order(coinname, btc)    #-5% 손실 시 손절 
                 print("-5% 손절 완료")
                 buy1 = 1
                 buy2 = 1
                 buy3 = 1
                 buy4 = 1

        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
