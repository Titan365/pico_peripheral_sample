import os
import time
import Picolib

#================================================================
# I2C display zettler 制御 class
#----------------------------------------------------------------
# from lib import Picolib
#----------------------------------------------------------------
# DISP=cls_dispzettler()  #宣言
# DISP.init(I2C,0)        #初期化
#================================================================
class cls_dispzettler():

    #-------------------
    # 変数
    #-------------------
    i2c_class=''
    i2c_set  = 0
    offset   = 0

    #-------------------
    # 初期化
    # i2c    : Openが完了したI2Cのclass
    # set    : 使用するi2cのポート0/1
    # 戻り値 : なし
    #-------------------
    def init(self, i2c, set):
        self.i2c_class = i2c
        self.i2c_set   = set
        self.offset    = 0
        
        #初期パラメータ
        buf=[
                bytearray([0x00,0x38]),
                bytearray([0x00,0x39]),
                bytearray([0x00,0x14]),
                bytearray([0x00,0x73]),
                bytearray([0x00,0x56]),
                bytearray([0x00,0x6C]),
                bytearray([0x00,0x38]),
                bytearray([0x00,0x01]),
                bytearray([0x00,0x0C])
            ]
        for i in buf:
            self.i2c_class.write(self.i2c_set, 0x3E, i)
            time.sleep(0.02)
        
        #初期文字
        self.write(0, 'Start display!')

    #-------------------
    # 表示をクリア
    # 戻り値 : なし
    #-------------------
    def clear(self):
        # 00.01: Clear
        # 00.02: Return Home
        buf=[
            bytearray([0x00,0x01]),
            bytearray([0x00,0x02])
            ]
        for i in buf:
            self.i2c_class.write(self.i2c_set, 0x3E, i)
            time.sleep(0.02)
        
        #postion初期化
        self.offset = 0

    #-------------------
    # 書き込み
    # pos    : 0:続き 1:1行目先頭 2:2行目先頭
    # data   : 文字列
    # 戻り値  : なし
    #-------------------
    def write(self, pos, data):
        # 1行目先頭 00-0F
        # 2行目先頭 40-4F
        # postion設定
        if(pos==1):
            self.offset = 0x00
        elif(pos==2):
            self.offset = 0x40
        
        #文字列->byte列変換
        datalist = data.encode()
        
        #書き込み
        for i in datalist:
            # DRAM Address
            self.i2c_class.write(self.i2c_set, 0x3E, bytearray([0x00,(0x80|self.offset)]))
            # data
            self.i2c_class.write(self.i2c_set, 0x3E, bytearray([0x40,i]))
            # postion++
            self.offset = self.offset+1
            # 行跨ぎ
            if(self.offset == 0x10):
                self.offset=0x40
            elif(self.offset >= 0x50):
                self.offset=0x00

#================================================================
# MBED Audio Codec 制御 class
#----------------------------------------------------------------
# from lib import Picolib
#----------------------------------------------------------------
# AUDIO=cls_mbedaudiocodec()  #宣言
# AUDIO.init(I2C,0)           #初期化
#================================================================
class cls_mbedaudiocodec():

    #-------------------
    # 変数
    #-------------------
    i2c_class=''
    i2c_set  = 0

    #-------------------
    # 初期化
    # i2c    : Openが完了したI2Cのclass
    # set    : 使用するi2cのポート0/1
    # 戻り値 : なし
    #-------------------
    def init(self, i2c, set):
        self.i2c_class = i2c
        self.i2c_set   = set
        self.offset    = 0
             
        #初期文字
        print('MBED audio codec start.')

    #-------------------
    # 書き込み
    # i2c    : Openが完了したI2Cのclass
    # set    : 使用するi2cのポート0/1
    # pos    : 0:続き 1:1行目先頭 2:2行目先頭
    # data   : 文字列
    # 戻り値  : なし
    #-------------------  
    def write(self, mode):
        if(mode=='loopback'):
            print('loopback mode.')
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x0C,0x02]))
        elif(mode=='i2s_slave'):
            print('i2s_slave mode.')
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x01,0x19]))
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x03,0x19]))
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x0C,0x02]))
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x08,0x12]))
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x0A,0x07]))
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x0E,0x02]))
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x12,0x01]))
        elif(mode=='i2s_master'):
            print('i2s_master mode not support.')
        elif(mode=='stop'):
            print('reset.')
            self.i2c_class.write(self.i2c_set,0x1A, bytearray([0x1E,0x00]))
        else:
            print('parameter error.')            

                
#================================================================
# IO exopander 制御 class
#----------------------------------------------------------------
# from lib import Picolib
#----------------------------------------------------------------
# IOEXP=cls_ioexpander()  #宣言
# IOEXP.init(SPI,0,GPIO,2,3,8) #初期化
#================================================================
class cls_ioexpander():

    #-------------------
    # 変数
    #-------------------
    spi_class=''
    spi_set = 0
    gpio_class=''
    rst_pin = 0
    cs_pin  = 0
    int_pin = 0

    #-------------------
    # 初期化
    # spi    : Openが完了したSPIのclass
    # set    : 使用するspiのポート0/1
    # gpio   : Openが完了したGPIOのclass
    # rst_pin: rstピン番号
    # cs_pin : cs ピン番号
    # int_pin: /intピン番号
    # 戻り値 : なし
    #-------------------
    def init(self, spi, set, gpio, rst_pin, cs_pin, int_pin):
        self.spi_class = spi
        self.spi_set   = set
        self.gpio_class= gpio
        self.rst_pin   = rst_pin
        self.cs_pin    = cs_pin
        self.int_pin   = int_pin
        
        #リセット
        self.gpio_class.write(self.rst_pin,0)
        self.gpio_class.write(self.cs_pin,1)
        #リセット解除
        self.gpio_class.write(self.rst_pin,1)

    #-------------------
    # 書き込み
    # client :デバイスアドレス
    # address:書き込みアドレス
    # data   :書き込みデータ
    # 戻り値 : なし
    #-------------------
    def write_address(self, client, address, data):
        #/CS low
        self.gpio_class.write(self.cs_pin,0)
        # write clientAddress=0x40
        self.spi_class.write(self.spi_set,bytearray([client,address,data]))
        #/CS high
        self.gpio_class.write(self.cs_pin,1)

    #-------------------
    # 読み込み
    # client :デバイスアドレス
    # address:書き込みアドレス
    # 戻り値 : 読み出しデータ
    #-------------------
    def read_address(self, client, address):
        read_buf = bytearray([0x00,0x00,0x00])
        #/CS low
        self.gpio_class.write(self.cs_pin,0)
        # read clientAddress=0x40+1
        self.spi_class.write_read(self.spi_set,bytearray([client+1,address,0x00]),read_buf)
        #/CS high
        self.gpio_class.write(self.cs_pin,1)

        return hex(read_buf[2])
