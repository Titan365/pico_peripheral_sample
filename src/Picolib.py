import os
import time
from machine import Pin, I2C, SPI, UART, ADC

#================================================================
# GPIO処理 class
#----------------------------------------------------------------
# from machine import Pin
#----------------------------------------------------------------
# GPIO=cls_gpio()      #宣言
# GPIO.open(25,OUT)    #PIN設定
# GPIO.write(25,1)     #PIN書き込み
# GPIO.toggle(25)      #PINトグル書き込み
# GPIO.read(25)        #PIN読み込み
# GPIO.list()          #PINのリスト
#================================================================
class cls_gpio():

    #-------------------
    # 変数
    #-------------------
    gpio=[0]*29

    #-------------------
    # PINの設定
    # pin   : pin番号 0~28 但しpin23,24:電源系統,pin25:LED
    # mode  : IN/OUT/INT_L/INT_H
    # cb    : INT時のコールバック関数
    # 戻り値 : module
    #-------------------
    def open(self, pin, mode, cb=''):

        if (0 <= pin <= 28) and (pin !=23) and (pin !=24):
            if (mode == 'INT_L') and (cb !=''):
                self.gpio[pin]=Pin(pin, Pin.IN, Pin.PULL_UP)
                self.gpio[pin].irq(trigger=Pin.IRQ_FALLING, handler=cb)
            elif (mode == 'INT_H') and (cb !=''):
                self.gpio[pin]=Pin(pin, Pin.IN, Pin.PULL_DOWN)
                self.gpio[pin].irq(trigger=Pin.IRQ_RISING, handler=cb)
            elif mode == 'IN':
                self.gpio[pin]=Pin(pin, Pin.IN)
            elif mode == 'OUT':
                self.gpio[pin]=Pin(pin, Pin.OUT)
            else:
                print("parameter error.")
        else:
            print("parameter error.")

        return self.gpio[pin]

    #-------------------
    # PINの書き込み
    # pin   : pin番号 0~28 但しpin23,24:電源系統,pin25:LED
    # val   : 0/1
    #-------------------
    def write(self, pin, val):
        if self.gpio[pin] != 0:
            self.gpio[pin].value(val)

    #-------------------
    # PINのトグル書き込み
    # pin   : pin番号 0~28 但しpin23,24:電源系統,pin25:LED
    #-------------------
    def toggle(self, pin):
        if self.gpio[pin] != 0:
            self.gpio[pin].toggle()


    #-------------------
    # PINの読み込み
    # pin   : pin番号 0~28 但しpin23,24:電源系統,pin25:LED
    # 戻り値: 0/1
    #-------------------
    def read(self, pin):
        if self.gpio[pin] != 0:
            return self.gpio[pin].value()

    #-------------------
    # PINのリスト
    # 戻り値: リスト
    #-------------------
    def list(self):
        return self.gpio


#================================================================
# ADC処理 class
#----------------------------------------------------------------
# from machine import ADC
#----------------------------------------------------------------
# ADC=cls_adc()    #宣言
# ADC.open(4)      #ADC設定
# ADC.read(4)      #ADC読み込み
# GPIO.list()      #ADCのリスト
#================================================================
class cls_adc():

    #-------------------
    # 変数
    #-------------------
    adc=[0]*5

    #-------------------
    # ADCの設定
    # set   : 0(GPIO26)/1(GPIO27)/2(GPIO28)/3(GPIO29)/4(内蔵温度センサー)
    # 戻り値 : module
    #-------------------
    def open(self, set):
        if (0 <= set <= 4):
            self.adc[set]=ADC(set)
        return self.adc[set]   

    #-------------------
    # PINの読み込み
    # set   : 0(GPIO26)/1(GPIO27)/2(GPIO28)/3(GPIO29)/4(内蔵温度センサー)
    # 戻り値: 0/1
    #-------------------
    def read(self, set):
        if self.adc[set] != 0:
            return self.adc[set].read_u16()

    #-------------------
    # ADCのリスト
    # 戻り値: リスト
    #-------------------
    def list(self):
        return self.adc


#================================================================
# I2C処理 class
#----------------------------------------------------------------
# from machine import I2C
#----------------------------------------------------------------
# I2C=cls_i2c()       #宣言
# I2C.open(0, sda_pin=1, scl_pin=2, pull_up='On', freq_hz=100000) #I2C設定
# I2C.write(0x3E,buff)#I2C書き込み
# I2C.read(0x3E,3)    #I2C読み込み
# I2C.offset_write(0x3E,buff,offset) #I2C Offset指定書き込み
# I2C.offset_read(0x3E,offset,3) #I2C Offset指定読み込み
# I2C.scan(0)         #I2Cのアドレススキャン
# I2C.list()          #I2Cのリスト

#================================================================
class cls_i2c():

    #-------------------
    # 変数
    #-------------------
    i2c=[0]*2

    #-------------------
    # I2Cの設定
    # set    : 0/1
    # sda_pin: [set0:0,4,8,12,16,20][set1:2,6,10,14,18,26]
    # scl_pin: [set0:1,5,9,13,17,21][set1:3,7,11,15,19,27]
    # pull_up: ['on','off']
    # freq_hz: 100000,400000
    # 戻り値 : module
    #-------------------
    def open(self, set=0, sda_pin=0, scl_pin=1, pull_up='On', freq_hz=100000):

        if   (set==0) and (sda_pin in [0,4,8,12,16,20]) and (scl_pin in [1,5,9,13,17,21]) and (freq_hz <= 400000):
            if (pull_up == 'on'):
                self.i2c[0] = I2C(set, scl=Pin(scl_pin,Pin.PULL_UP), sda=Pin(sda_pin,Pin.PULL_UP), freq=freq_hz)
            else:
                self.i2c[0] = I2C(set, scl=Pin(scl_pin), sda=Pin(sda_pin,Pin.PULL_UP), freq=freq_hz)

        elif (set==1) and (sda_pin in [2,6,10,14,18,26]) and (scl_pin in [3,7,11,15,19,27]) and (freq_hz <= 400000):
            if (pull_up == 'on'):
                self.i2c[1] = I2C(set, scl=Pin(scl_pin,Pin.PULL_UP), sda=Pin(sda_pin,Pin.PULL_UP), freq=freq_hz)
            else:
                self.i2c[1] = I2C(set, scl=Pin(scl_pin), sda=Pin(sda_pin,Pin.PULL_UP), freq=freq_hz)
        else:
            print("parameter error.")

        return self.i2c[set]

    #-------------------
    # I2Cの書き込み
    # set    : 0/1
    # addr   : I2C address
    # buff   : バッファ
    #-------------------
    def write(self, set, addr, buff):
        if (set<2)and(self.i2c[set]!=0):
            self.i2c[set].writeto(addr, buff)
        else:
            print('parameter error.')    

    #-------------------
    # I2Cの読み込み
    # set    : 0/1
    # addr   : I2C address
    # size   : 読み込みサイズ
    # 戻り値: buff
    #-------------------
    def read(self, set, addr, size):
        if (set<2)and(self.i2c[set]!=0):
            return self.i2c[set].readfrom(addr, size)
        else:
            print('parameter error.')
            return []             

   #-------------------
    # I2Cのアドレス指定書き込み
    # set   : 0/1
    # addr  : I2C address
    # offset: 書き込むアドレス
    # buff   : バッファ
    #-------------------
    def offset_write(self, set, addr, offset, buff):
        if (set<2)and(self.i2c[set]!=0):
            self.i2c[set].writeto(addr, offset+buff)
        else:
            print('parameter error.')    
    #-------------------
    # I2Cのアドレス指定読み込み
    # set   : 0/1
    # addr  : I2C address
    # offset: 読み出すアドレス
    # size  : 読み込みサイズ
    # 戻り値 : buff
    #-------------------
    def offset_read(self, set, addr, offset, size):
        if (set<2)and(self.i2c[set]!=0):
            self.i2c[set].writeto(addr, offset)
            return self.i2c[set].readfrom(addr, size)
        else:
            print('parameter error.')
            return []     

    #-------------------
    # I2Cのリスト
    # 戻り値: リスト
    #-------------------
    def list(self):
        return self.i2c

    #-------------------
    # I2Cのスキャン
    # set    : 0/1
    # 戻り値: アドレスリスト
    #-------------------
    def scan(self,set):
        if(set<2)and(self.i2c[set]!=0):
            return self.i2c[set].scan()
        else:
            print('NULL')
            return []

#================================================================
# SPI処理 class
#----------------------------------------------------------------
# from machine import SPI
#----------------------------------------------------------------
# SPI=cls_spi()       #宣言
# SPI.open(set=0, sck_pin=6, tx_pin=7, rx_pin=4, baud=1000000, bits=8, polrarity=0, phase=0)  # SPI open
# SPI.write(buff)     #SPI書き込み
# SPI.read(3)         #SPI読み込み
# SPI.write_read(3)   #SPI読み書き
# SPI.list()          #SPIのリスト

#================================================================
class cls_spi():

    #-------------------
    # 変数
    #-------------------
    spi=[0]*2

    #-------------------
    # SPIの設定
    # set        : 0/1
    # sck_pin    : [set0:2,6,18][set1:10,14]
    # tx_pin     : [set0:3,7,19][set1:11,15]
    # rx_pin     : [set0:0,4,16][set1: 8,12]
    # baud       : 1000000
    # bits       : 8
    # polarity  : 0/1
    # phase      : 0/1
    # 戻り値     : module
    #-------------------
    def open(self, set=0, sck_pin=6, tx_pin=7, rx_pin=4, baud=1000000, bits=8, polarity=0, phase=0):
        
        if  (set==0) and (sck_pin in [2,6,18]) and (tx_pin in [3,7,19]) and (rx_pin in [0,4,16]):
            self.spi[0] = SPI(id=set, sck=Pin(sck_pin), mosi=Pin(tx_pin), miso=Pin(rx_pin), baudrate=baud, bits=bits, polarity=polarity, phase=phase)
        elif (set==1) and (sck_pin in [10,14]) and (tx_pin in [11,15]) and (rx_pin in [8,12]):
            self.spi[1] = SPI(id=set, sck=Pin(sck_pin), mosi=Pin(tx_pin), miso=Pin(rx_pin), baudrate=baud, bits=bits, polarity=polarity, phase=phase)
        else:
            print("parameter error.")

        return self.spi[set]

    #-------------------
    # SPIの書き込み
    # set    : 0/1
    # buff   : バッファ
    #-------------------
    def write(self, set, buff):
        self.spi[set].write(buff)
    spi
    #-------------------
    # SPIの読み込み
    # set    : 0/1
    # size   : 読み込みサイズ
    # 戻り値: buff
    #-------------------
    def read(self, set, size):
        return self.spi[set].read(size)

    #-------------------
    #SPI読み書き
    # set    : 0/1
    # wbuff   : 書き込みバッファ
    # rbuff   : 読み込みバッファ
    #-------------------
    def write_read(self, set, wbuff, rbuff):
        self.spi[set].write_readinto(wbuff,rbuff)
        return rbuff

    #-------------------
    # SPIのリスト
    # 戻り値: リスト
    #-------------------
    def list(self):
        return self.spi

#================================================================
# UART処理 class
#----------------------------------------------------------------
# from machine import UART
#----------------------------------------------------------------
# UART=cls_uart()       #宣言
# UART.open(set=0, sck_pin=6, tx_pin=7, rx_pin=4, baud=1000000, bits=8, polrarity=0, phase=0)  # SPI open
# UART.write(buff)     #UART書き込み
# UART.read(3)         #UART読み込み
# UART.list()          #UARTのリスト

#================================================================
class cls_uart():

    #-------------------
    # 変数
    #-------------------
    uart=[0]*2

    #-------------------
    # UARTの設定
    # set        : 0/1
    # tx_pin     : [set0:0,12,16][set1:4,8]
    # rx_pin     : [set0:1,13,17][set1: 5,9]
    # baud       : 38400
    # 戻り値     : module
    #-------------------
    def open(self, set=1, tx_pin=8, rx_pin=9, baud=38400):

        if   (set==0) and (tx_pin in [0,12,16]) and (rx_pin in [1,13,17]):
            self.uart[0] = UART(id=set, tx=Pin(tx_pin), rx=Pin(rx_pin), baudrate=baud)

        elif (set==1) and (tx_pin in [4,8]) and (rx_pin in [5,9]):
            self.uart[1] = UART(id=set, tx=Pin(tx_pin), rx=Pin(rx_pin), baudrate=baud)
        else:
            print("parameter error.")

        return self.uart[set]

    #-------------------
    # UARTの書き込み
    # set    : 0/1
    # buff   : バッファ
    #-------------------
    def write(self, set, buff):
        self.uart[set].write(buff)

    #-------------------
    # UARTの読み込み
    # set    : 0/1
    # size   : 読み込みサイズ
    # 戻り値: buff
    #-------------------
    def read(self, set, size):
        return self.uart[set].read(size)

    #-------------------
    # UARTのリスト
    # 戻り値: リスト
    #-------------------
    def list(self):
        return self.uart


#================================================================
# ファイル処理 class
#----------------------------------------------------------------
#
#----------------------------------------------------------------
# File=cls_file()          #宣言
# File.date('./main.py')                   #ファイルの更新日時print
# File.read('./test.txt','cp932')          #ファイル読み出し
# File.write('./test.txt','w','hogehoge')  #新規作成上書き
# File.write('./test.txt','a','hogehoge')  #追記
#================================================================
class cls_file():

    #-------------------
    # 変数
    #-------------------
    write_num = 1       #write回数上限確認用
    write_max = 10      #書き込み上限


    #-------------------
    # ファイルの更新日時
    # file_name : ファイルのパス
    # 戻り値    : なし
    #-------------------
    def date(self, file_name):
        d=time.localtime(os.stat(file_name)[8])
        print('{:04}/{:02}/{:02}_{:02}:{:02}:{:02} [{}]'.format(d[0],d[1],d[2],d[3],d[4],d[5],file_name))

    #-------------------
    # ファイル読み込み
    # file_name : ファイルのパス
    # encod     : 'cp932', 'utf-8'
    # 戻り値    : 読み込んだデータ
    #-------------------
    def read(self, file_name, encod='utf-8'):
        try:
            with open(file_name, encoding = encod) as f:
                read_line= f.readlines()
                return read_line
        except:
            print("cls_file.read():file not found.")
            return NULL

    #-------------------
    # ファイル読み込み
    # file_name  : ファイルのパス
    # write_mode : 書き込みモード 'w'新規作成/'a'追記
    # 戻り値     : なし
    #-------------------
    def write(self ,file_name, write_mode, data):

        if(self.write_num < self.write_max):
            try:
                with open(file_name, mode=write_mode) as f:
                    f.write(data)
                    self.write_num+=1
            except:
                print("cls_file.write():file not found.")
        else:
            print("cls_file.write(): Reached the limit %d times."%  self.write_num)


