import time
import pyupbit
import datetime
import schedule
#from fbprophet import Prophet

access = "m0uV5VEpMw9uNrvDlxUXvahxvYYG2O3KGNW3vRsJ"
secret = "iRmSf6ovpVTpSzPnyxDLYEMcvKYmbsPo9QE8gQuw"

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



# predicted_close_price = 0
# def predict_price(ticker):
#     """Prophet으로 당일 종가 가격 예측"""
#     global predicted_close_price
#     df = pyupbit.get_ohlcv(ticker, interval="minute60")
#     df = df.reset_index()
#     df['ds'] = df['index']
#     df['y'] = df['close']
#     data = df[['ds','y']]
#     model = Prophet()
#     model.fit(data)
#     future = model.make_future_dataframe(periods=24, freq='H')
#     forecast = model.predict(future)
#     closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=17)]
#     if len(closeDf) == 0:
#         closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=17)]
#     closeValue = closeDf['yhat'].values[0]
#     predicted_close_price = closeValue
# predict_price("KRW-OMG")
# schedule.every().hour.do(lambda: predict_price("KRW-OMG"))

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start - V2 210911 ")


# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        # start_time = get_start_time("KRW-OMG") - datetime.timedelta(hours=4)  #05:00
        start_time = get_start_time("KRW-OMG")   #0:00
        end_time = start_time + datetime.timedelta(hours=9)  #18:00 
        schedule.run_pending()
        target_price = get_target_price("KRW-OMG", 0.2)
        current_price = get_current_price("KRW-OMG")
        a=1
        b=1
        c=1
        d=1

        print("현재시간",now,"수익률:",(1-upbit.get_avg_buy_price('KRW-OMG')/current_price)*100,"%")
        
            # 05:00~16:59 에 예측가격과 변동성돌파 조건에 만족하면 70% 매수 한다.
        if start_time < now < end_time - datetime.timedelta(seconds=60): #09:00~17:59
            # print("주간 매수")                            
            
            if target_price < current_price : #17시 예상가격보다 낮으면 매수
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-OMG", krw*0.7*0.9995) #보유금의 70% 매수 (수수로 감안)
                    print(a,"매수 평균단가:",upbit.get_avg_buy_price('KRW-OMG')) 
                    a+1
            
            if upbit.get_avg_buy_price('KRW-OMG')*1.05 < current_price :
                btc = get_balance("BTC-OMG")

                if btc > 0.00008:
                     upbit.sell_market_order("KRW-OMG", btc)
                     print("익절 횟수:",b) 
                     b+1
                   

        else: # 18:00 ~ 08:59 까지 
            # print("야간 매수") 
          
            
            if c<2 and upbit.get_avg_buy_price('KRW-OMG') > 100 and current_price < upbit.get_avg_buy_price('KRW-OMG') * 0.95 : # 18시까지 수익 못본상태에서 -5%되면 추매(1/3) 
                krw = get_balance("KRW")
                if krw > 15000:
                    upbit.buy_market_order("KRW-OMG", (krw/3)*0.9995) 
                    print("1차 추가 매수")
                    c+1
                    print(c)

           
            if d<2 and upbit.get_avg_buy_price('KRW-OMG') > 100 and current_price < upbit.get_avg_buy_price('KRW-OMG') * 0.90 : # 18시까지 수익 못본상태에서 -10%되면 추매(All) 
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-OMG", krw*0.9995) 
                    print("2차 추가 매수")       
                    d+1
                    print(d)
                    

            if upbit.get_avg_buy_price('KRW-OMG') > 100 and current_price < upbit.get_avg_buy_price('KRW-OMG') * 0.86 : #-14% 손절
                btc = get_balance("BTC")
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-OMG", btc)
                    print("손절 진행")
                
                
        time.sleep(1)
    except Exception as e:
        
        print(e)
        
        time.sleep(1)
