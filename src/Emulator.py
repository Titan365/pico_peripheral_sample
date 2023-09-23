import os
import time
import Picolib

#================================================================
# Plotocol Emulator class
#----------------------------------------------------------------
# from lib import Picolib
#----------------------------------------------------------------
# EMUL=cls_emulator()  #宣言
# EMUL.init(I2C,0,SPI,0,GPIO.gpio_list)   #初期化
#================================================================
class cls_emulator():

    #-------------------
    # 変数
    #-------------------
    i2c_class=''
    i2c_set=0
    spi_class=''
    spi_set=0
    gpio_class=''
    gpio_set={}

    #-------------------
    # 初期化
    # i2c    : Openが完了したI2Cのclass
    # i2c_set: 使用するi2cのポート0/1
    # spi    : Openが完了したSPIのclass
    # spi_set: 使用するspiのポート0/1
    # gpio   : Openが完了したGPIOのclass
    # spi_set: 使用するgpioのポート1/2/3/4/5/6
    # 戻り値 : なし
    #-------------------
    def init(self, i2c, i2c_set, spi, spi_set, gpio, gpio_set):
        self.i2c_class  = i2c
        self.i2c_set    = i2c_set
        self.spi_class  = spi
        self.spi_set    = spi_set
        self.gpio_class = gpio
        self.gpio_set   = gpio_set

    #-------------------
    # GPIOの書き込み
    # port  : GPIO port name.
    # value : h/l/t
    #-------------------
    def gpio_write(self, port, value):
        if(port in self.gpio_set):
            if(value == 'h'):
                self.gpio_class.write(self.gpio_set[port],1)
            elif(value == 'l'):
                self.gpio_class.write(self.gpio_set[port],0)
            elif(value == 't'):
                self.gpio_class.toggle(self.gpio_set[port])
            else:
                print('gpio_write error.')
        else:
            print('gpio pin is not available.')
            
    #-------------------
    # I2Cの書き込み
    #-------------------
    def i2c_write(self, addr, buff):
        self.i2c_class.write(self.i2c_set, addr, buff)  
    #-------------------
    # I2Cの読み込み
    #-------------------
    def i2c_read(self, addr, size):
        return self.i2c_class.read(self.i2c_set, addr, size)  
    #-------------------
    # I2Cのアドレス指定書き込み
    #-------------------
    def i2c_offset_write(self, addr, offset, buff):
        self.i2c_class.offset_write(self.i2c_set, addr, offset, buff)
    #-------------------
    # I2Cのアドレス指定読み込み
    #-------------------
    def i2c_offset_read(self, addr, offset, size):
        return self.i2c_class.offset_read(self.i2c_set, addr, offset, size)   
    #-------------------
    # I2Cのスキャン
    #-------------------
    def i2c_scan(self):
        return self.i2c_class.scan(self.i2c_set)

    #-------------------
    # SPIの書き込み
    # set    : 0/1
    # buff   : バッファ
    #-------------------
    def spi_write(self, wbuff):
        self.gpio_class.write(self.gpio_set['SPI_CS'],0)
        self.spi_class.write(self.spi_set, wbuff)
        self.gpio_class.write(self.gpio_set['SPI_CS'],1)
        
    #-------------------
    # SPIの読み込み
    # set    : 0/1
    # size   : 読み込みサイズ
    # 戻り値: buff
    #-------------------
    def spi_read(self, size):
        self.gpio_class.write(self.gpio_set['SPI_CS'],0)
        rbuff = self.spi_class.read(self.spi_set, size)
        self.gpio_class.write(self.gpio_set['SPI_CS'],1)
        return rbuff

    #-------------------
    #SPI読み書き
    # set    : 0/1
    # wbuff   : 書き込みバッファ
    # rbuff   : 読み込みバッファ
    #-------------------
    def spi_write_read(self, wbuff, rbuff):
        self.gpio_class.write(self.gpio_set['SPI_CS'],0)
        self.spi_class.write_read(self.spi_set,wbuff,rbuff)
        self.gpio_class.write(self.gpio_set['SPI_CS'],1)
        return rbuff
    
        
