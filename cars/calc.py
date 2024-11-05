def calc_price(price, currency, year, volume, table): 
    try:
        if table == "china":
            comission = 0
            
        if table == "stats":
            comission = 0
        
        one_rub = currency.jpy / 100
        price_rus = round(price / one_rub)
        if table == "china":
            one_rub = currency.cny / 100

            price_rus = round(price * one_rub)

        if price_rus < 200000:
            tof = 775
        elif (price_rus < 450000) and (price_rus >= 200000):
            tof = 1550
        elif (price_rus < 1200000) and (price_rus >= 450000):
            tof = 3100
        elif (price_rus < 2700000) and (price_rus >= 1200000):
            tof = 8530
        elif (price_rus < 4200000) and (price_rus >= 2700000):
            tof = 12000
        elif (price_rus < 5500000) and (price_rus >= 4200000):
            tof = 15550
        elif (price_rus < 7000000) and (price_rus >= 5500000):
            tof = 20000
        elif (price_rus < 8000000) and (price_rus >= 7000000):
            tof = 23000
        elif (price_rus < 9000000) and (price_rus >= 8000000):
            tof = 25000
        elif (price_rus < 10000000) and (price_rus >= 9000000):
            tof = 27000
        else:
            tof = 30000
      
        age = datetime.now().year - year
            
        if age < 3:
            if volume >= 3500:
                yts = 1235200
            elif (volume >= 3000) and (volume <= 3499):
                yts = 970000
            else:
                yts = 3400
            evroprice = price_rus / currency.eur
            if evroprice < 8500:
                duty = evroprice * 0.54
                if duty / volume < 2.5:
                    duty = volume * 2.5
            elif (evroprice >= 8500) and (evroprice < 16700):
                duty = evroprice * 0.48
                if duty / volume < 3.5:
                    duty = volume * 3.5
            elif (evroprice >= 16700) and (evroprice < 42300):
                duty = evroprice * 0.48
                if duty / volume < 5.5:
                    duty = volume * 5.5
            elif (evroprice >= 42300) and (evroprice < 84500):
                duty = evroprice * 0.48
                if duty / volume < 7.5:
                    duty = volume * 7.5
            elif (evroprice >= 84500) and (evroprice < 169000):
                duty = evroprice * 0.48
                if duty / volume < 15:
                    duty = volume * 15
            else:
                duty = evroprice * 0.48
                if duty / volume < 20:
                    duty = volume * 20

        elif (age >= 3) and (age < 5):
            if volume >= 3500:
                yts = 1623800
            elif (volume >= 3000) and (volume <= 3499):
                yts = 1485000
            else:
                yts = 5200

            if volume <= 1000:
                duty = volume * 1.5
            elif (volume >= 1001) and (volume <= 1500):
                duty = volume * 1.7
            elif (volume >= 1501) and (volume <= 1800):
                duty = volume * 2.5
            elif (volume >= 1801) and (volume <= 2300):
                duty = volume * 2.7
            elif (volume >= 2301) and (volume <= 3000):
                duty = volume * 3
            else:
                duty = volume * 3.6
        elif age >= 5:
            if volume >= 3500:
                yts = 1623800
            elif (volume >= 3000) and (volume <= 3499):
                yts = 1485000
            else:
                yts = 5200

            if volume <= 1000:
                duty = volume * 3
            elif (volume >= 1001) and (volume <= 1500):
                duty = volume * 3.2
            elif (volume >= 1501) and (volume <= 1800):
                duty = volume * 3.5
            elif (volume >= 1801) and (volume <= 2300):
                duty = volume * 4.8
            elif (volume >= 2301) and (volume <= 3000):
                duty = volume * 5
            else:
                duty = volume * 5.7

        toll = duty * currency.eur + tof

        res_rus = toll + yts + comission
        res_jpn = (comission + price) * one_rub
        

        return round((res_jpn + res_rus) / 1000) * 1000, int(res_rus), int(res_jpn), toll
    except Exception as e:
        print(e)
