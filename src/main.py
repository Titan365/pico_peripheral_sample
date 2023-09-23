import time
import os
import re
import binascii
import _thread
import Picolib
import PeriDev
import Emulator


#============================
# help('./readme.txt','utf-8', '', '')
#　ヘルプファイル出力
#============================
def help(file_name, file_codec, start_line, end_line):
    
    #フィル内すべて出力.
    if((start_line=='') and (end_line=='')):
        for i in File.read(file_name, file_codec):
            print(i.rstrip())
    #指定された行を出力
    else:
        print_on=False
        for i in File.read(file_name, file_codec):
            #開始行であれば
            if(i.startswith(start_line)):
                print_on=True
            elif(print_on==True)and(i.startswith(end_line)):
                break
            #出力
            if(print_on==True):
                print(i.rstrip())

#============================
# temperature_picoadc
#============================
def temperature_picoadc(adc):
    volt = adc * (3.3/65535)
    temp = 27 - (volt -0.706)/0.001721
    return temp

#============================
# gpio callback
#============================
def gpio_callback(pin):
    print(pin)
    
#============================
# picolib_cmd
#============================
def picolib_cmd(cmd_list):
    #GPIO
    if (len(cmd_list) > 1) and (cmd_list[0] == 'gpio'):
        #-o
        if (len(cmd_list) > 3) and (cmd_list[1] == '-o'):
            if   cmd_list[3] == 'out':
                GPIO.open(int(cmd_list[2]),'OUT')
            elif cmd_list[3] == 'in':
                GPIO.open(int(cmd_list[2]),'IN')
            elif cmd_list[3] == 'intl':
                GPIO.open(int(cmd_list[2]),'INT_L',gpio_callback)
            elif cmd_list[3] == 'inth':
                GPIO.open(int(cmd_list[2]),'INT_L',gpio_callback)
            else:
                print('parameter error.')
        #-w
        elif (len(cmd_list) > 3) and (cmd_list[1] == '-w'):
            if   (cmd_list[3] == 'h'):
                GPIO.write(int(cmd_list[2]),1)
            elif (cmd_list[3] == 'l'):
                GPIO.write(int(cmd_list[2]),0)
            elif (cmd_list[3] == 't'):
                GPIO.toggle(int(cmd_list[2]))
            else:
                print('parameter error.')
        #-r
        elif (len(cmd_list) > 2) and (cmd_list[1] == '-r'):
            print(GPIO.read(int(cmd_list[2])))
        #-l
        elif (len(cmd_list) > 1) and (cmd_list[1] == '-l'):
            print(GPIO.list())
        else:
            help('./readme.txt','utf-8', '#=gpio', '#=')

    #ADC
    elif (len(cmd_list) > 1) and (cmd_list[0] == 'adc'):
        #-o
        if (len(cmd_list) > 2) and (cmd_list[1] == '-o'):
            ADC.open(int(cmd_list[2]))
        #-r
        elif (len(cmd_list) > 2) and (cmd_list[1] == '-r'):
            volt = ADC.read(int(cmd_list[2]))
            if(int(cmd_list[2]) == 4):
                print( volt, '{:.2f}℃'.format( temperature_picoadc(volt) ) )
            else:
                print(volt)
        #-l
        elif (len(cmd_list) > 1) and (cmd_list[1] == '-l'):
            print(ADC.list())
        else:
            help('./readme.txt','utf-8', '#=adc', '#=')
                
    #I2C
    elif (len(cmd_list) > 1) and (cmd_list[0] == 'i2c'):
        #-o
        if (len(cmd_list) > 6) and (cmd_list[1] == '-o'):
            I2C.open(int(cmd_list[2]), sda_pin=int(cmd_list[3]), scl_pin=int(cmd_list[4]), pull_up=cmd_list[5], freq_hz=int(cmd_list[6]))
        #-w
        elif (len(cmd_list) > 4) and (cmd_list[1] == '-w'):
            buf      = re.sub('0x|,|\.','', cmd_list[4])
            bin_cmd_list = binascii.unhexlify(buf)
            I2C.write( int(cmd_list[2]), addr=int(cmd_list[3],16), buff=bin_cmd_list )
        #-r
        elif (len(cmd_list) > 4) and (cmd_list[1] == '-r'):
            buf = I2C.read( int(cmd_list[2]),addr=int(cmd_list[3],16),size=int(cmd_list[4]) )
            print(re.sub(r"(..)",r"\1.",buf.hex()))

        #-aw
        elif (len(cmd_list) > 5) and (cmd_list[1] == '-aw'):
            offset       = re.sub('0x|,|\.','', cmd_list[4])
            bin_cmd_list_offset = binascii.unhexlify(offset)
            buf          = re.sub('0x|,|\.','', cmd_list[5])
            bin_cmd_list_buf    = binascii.unhexlify(buf)
            I2C.offset_write( int(cmd_list[2]), addr=int(cmd_list[3],16), offset=bin_cmd_list_offset, buff=bin_cmd_list_buf )
        #-ar
        elif (len(cmd_list) > 5) and (cmd_list[1] == '-ar'):
            offset      = re.sub('0x|,|\.','', cmd_list[4])
            bin_cmd_list_offset = binascii.unhexlify(offset)
            buf = I2C.offset_read( int(cmd_list[2]), addr=int(cmd_list[3],16), offset=bin_cmd_list_offset, size=int(cmd_list[5]) )
            print(re.sub(r"(..)",r"\1.",buf.hex()))
        #-l
        elif (len(cmd_list) > 1) and (cmd_list[1] == '-l'):
            print(I2C.list())
        #-s
        elif (len(cmd_list) > 2) and (cmd_list[1] == '-s'):
            for i in I2C.scan(int(cmd_list[2])):
                print('Addr=0x{0:X}(W:0x{1:X},R:0x{2:X})'.format( i, i<<1, (i<<1)+1 ))
        else:
            help('./readme.txt','utf-8', '#=i2c', '#=')
    #SPI
    elif (len(cmd_list) > 1) and (cmd_list[0] == 'spi'):
        #-o
        if (len(cmd_list) > 9) and (cmd_list[1] == '-o'):
            SPI.open(int(cmd_list[2]), sck_pin=int(cmd_list[3]), tx_pin=int(cmd_list[4]), rx_pin=int(cmd_list[5]), baud=int(cmd_list[6]), bits=int(cmd_list[7]), polarity=int(cmd_list[8]), phase=int(cmd_list[9]))
        #-w
        elif (len(cmd_list) > 3) and (cmd_list[1] == '-w'):
            buf      = re.sub('0x|,|\.','', cmd_list[3])
            bin_cmd_list = binascii.unhexlify(buf)
            SPI.write( int(cmd_list[2]), buff=bin_cmd_list )
        #-r
        elif (len(cmd_list) > 3) and (cmd_list[1] == '-r'):
            buf = SPI.read( int(cmd_list[2]), size=int(cmd_list[3]) )
            print(re.sub(r"(..)",r"\1.",buf.hex()))
        #-rw
        elif (len(cmd_list) > 3) and (cmd_list[1] == '-rw'):
            buf      = re.sub('0x|,|\.','', cmd_list[3])
            bin_cmd_list = binascii.unhexlify(buf)
            buf      = SPI.write_read( int(cmd_list[2]), wbuff=bin_cmd_list, rbuff= bytearray(len(bin_cmd_list)))
            print(re.sub(r"(..)",r"\1.",buf.hex()))
        #-l
        elif (len(cmd_list) > 1) and (cmd_list[1] == '-l'):
            print(SPI.list())
        else:
            help('./readme.txt','utf-8', '#=spi', '#=')
    #UART
    elif (len(cmd_list) > 1) and (cmd_list[0] == 'uart'):
        #-o
        if (len(cmd_list) > 5) and (cmd_list[1] == '-o'):
            print(int(cmd_list[5]))
            UART.open(int(cmd_list[2]), tx_pin=int(cmd_list[3]), rx_pin=int(cmd_list[4]), baud=int(cmd_list[5]))
        #-w
        elif (len(cmd_list) > 3) and (cmd_list[1] == '-w'):
            UART.write( int(cmd_list[2]), buff=cmd_list[3] )
        #-r
        elif (len(cmd_list) > 3) and (cmd_list[1] == '-r'):
            print(UART.read( int(cmd_list[2]), size=int(cmd_list[3])) )
        #-l
        elif (len(cmd_list) > 1) and (cmd_list[1] == '-l'):
            print(UART.list())      
        else:
            help('./readme.txt','utf-8', '#=uart', '#=')
    #第2引数入れていない場合
    else:
        help('./readme.txt','utf-8', '#='+cmd_list[0], '#=')

#============================
# peridev_cmd
#============================
def peridev_cmd(cmd_list):
    #Display
    if (cmd_list[0] == 'disp'):
        #-o
        if (len(cmd_list) > 2) and (cmd_list[1] == '-o'):
            if(cmd_list[2] == '0'): #sda=0/scl=1
                I2C.open(0, sda_pin=0, scl_pin=1, pull_up='on', freq_hz=40000)
                DZ.init(I2C,0)
            elif(cmd_list[2] == '1'): #sda=14/scl=15
                I2C.open(1, sda_pin=14, scl_pin=15, pull_up='on', freq_hz=40000)
                DZ.init(I2C,1)
        #-c
        elif (len(cmd_list) > 1) and (cmd_list[1] == '-c'):
            DZ.clear()
        #-w
        elif (len(cmd_list) > 3) and (cmd_list[1] == '-w'):
            DZ.write(pos=int(cmd_list[2]),data=cmd_list[3])
        else:
            help('./readme.txt','utf-8', '#=disp', '#=')

    #Audio Codec
    elif (cmd_list[0] == 'audio'):
        #-o
        if (len(cmd_list) > 2) and (cmd_list[1] == '-o'):
            if(cmd_list[2] == '0'): #sda=0/scl=1
                I2C.open(0, sda_pin=0, scl_pin=1, pull_up='on', freq_hz=40000)
                AUDIO.init(I2C,0)
            elif(cmd_list[2] == '1'): #sda=14/scl=15
                I2C.open(1, sda_pin=14, scl_pin=15, pull_up='on', freq_hz=40000)
                AUDIO.init(I2C,0)
        #-w
        elif (len(cmd_list) > 2) and (cmd_list[1] == '-w'):
            AUDIO.write(cmd_list[2])
        else:
            help('./readme.txt','utf-8', '#=audio', '#=')

    #IO Expander
    elif (cmd_list[0] == 'ioexp'):
        #-o
        if (len(cmd_list) > 2) and (cmd_list[1] == '-o'):
            if(cmd_list[2] == '0'): #sck=6/tx=7/rx=4/rst=2/cs=3/int=5
                SPI.open(0, sck_pin=6, tx_pin=7, rx_pin=4, baud=1000000, bits=8, polarity=0, phase=0)
                GPIO.open(2,'OUT')
                GPIO.open(3,'OUT')
                GPIO.open(5,'OUT')
                IOEXP.init(SPI,0,GPIO,2,3,5)
            elif(cmd_list[2] == '1'): #sck=10/tx=11/rx=12/rst=14/cs=13/int=15
                SPI.open(1, sck_pin=10, tx_pin=11, rx_pin=12, baud=1000000, bits=8, polarity=0, phase=0)
                GPIO.open(14,'OUT')
                GPIO.open(13,'OUT')
                GPIO.open(15,'OUT')
                IOEXP.init(SPI,1,GPIO,14,13,15)
        #-w
        elif (len(cmd_list) > 4) and (cmd_list[1] == '-w'):
            IOEXP.write_address(int(cmd_list[2],16),int(cmd_list[3],16),int(cmd_list[4],16))
        #-r
        elif (len(cmd_list) > 3) and (cmd_list[1] == '-r'):
            print(IOEXP.read_address(int(cmd_list[2],16),int(cmd_list[3],16)))   
        else:
            help('./readme.txt','utf-8', '#=ioexp', '#=')


#============================
# emulator_cmd
#============================
def emulator_cmd(cmd_list):
    
    gpio_dic=[
        {'SPI_CLK':10, 'SPI_TX':11, 'SPI_RX':12, 'SPI_CS':13, 'I2C_SDA':14, 'I2C_SCL':15},
        {'OUT_1':10, 'OUT_2':11, 'OUT_3':12, 'OUT_4':13, 'I2C_SDA':14, 'I2C_SCL':15},
        {'SPI_CLK':10, 'SPI_TX':11, 'SPI_RX':12, 'SPI_CS':13, 'OUT_1':14, 'OUT_2':15}
    ]
    
    #Emulator
    if(len(cmd_list) > 1) and (cmd_list[0] == 'emul'):
        #-l
        if (len(cmd_list) > 1) and (cmd_list[1] == '-l'):
            for cnt,val in enumerate(gpio_dic):
                print('mode={0:02d}'.format(cnt),val)
        #-o
        elif (len(cmd_list) > 2) and (cmd_list[1] == '-o') and (len(gpio_dic)>int(cmd_list[2])):
            mode = int(cmd_list[2])
            #i2c setting
            if( ('I2C_SDA' in gpio_dic[mode]) and ('I2C_SCL' in gpio_dic[mode]) ):
                i2c_speed = int(input("i2c_speed (kHz)     # "))
                i2c_pulup = input("i2c_pullup (on/off)# ")
                I2C.open(1, sda_pin = gpio_dic[mode]['I2C_SDA'], scl_pin=gpio_dic[mode]['I2C_SCL'], pull_up = i2c_pulup, freq_hz = i2c_speed*1000)
            #spi setting
            if( ('SPI_CLK' in gpio_dic[mode]) and ('SPI_TX' in gpio_dic[mode]) and ('SPI_RX' in gpio_dic[mode])):                
                spi_speed    = int(input("spi_speed (MHz)    # "))
                spi_polarity = int(input("clk_polarity (0/1)# "))
                spi_phase    = int(input("output_phase (0/1)# "))
                SPI.open(1, sck_pin = gpio_dic[mode]['SPI_CLK'], tx_pin = gpio_dic[mode]['SPI_TX'], rx_pin = gpio_dic[mode]['SPI_RX'], baud = spi_speed*1000000, bits=8, polarity = spi_polarity, phase = spi_phase)
            if('SPI_CS' in gpio_dic[mode]):
                GPIO.open(gpio_dic[mode]['SPI_CS'],'OUT')
            #gpio setting
            for key,value in gpio_dic[mode].items():
                if(key.startswith('OUT')):
                    GPIO.open(gpio_dic[mode][key],'OUT')                    

            EMUL.init(I2C,1,SPI,1,GPIO,gpio_dic[mode])
            
        #gpio               
        elif (cmd_list[1] == 'gpio'):
            #-w
            if(len(cmd_list) > 4) and (cmd_list[2] == '-w'):
                EMUL.gpio_write(cmd_list[3],cmd_list[4])
            else:
                print('emul gpio parameter error.')
        #i2c
        elif (cmd_list[1] == 'i2c'):
            #-w
            if(len(cmd_list) > 4) and (cmd_list[2] == '-w'):
                wbuf      = re.sub('0x|,|\.','', cmd_list[4])
                bin_cmd_list = binascii.unhexlify(wbuf)
                EMUL.i2c_write(addr=int(cmd_list[3],16), buff=bin_cmd_list)
            #-r
            elif (len(cmd_list) > 4) and (cmd_list[2] == '-r'):
                rbuf = EMUL.i2c_read(addr=int(cmd_list[3],16),size=int(cmd_list[4]) )
                print('i2c-r:{0:04d}:{1:}'.format(len(rbuf), re.sub(r"(..)",r"\1.",rbuf.hex())))
            #-aw
            elif (len(cmd_list) > 5) and (cmd_list[2] == '-aw'):
                offset       = re.sub('0x|,|\.','', cmd_list[4])
                bin_cmd_list_offset = binascii.unhexlify(offset)
                wbuf          = re.sub('0x|,|\.','', cmd_list[5])
                bin_cmd_list_buf    = binascii.unhexlify(wbuf)
                EMUL.i2c_offset_write( addr=int(cmd_list[3],16), offset=bin_cmd_list_offset, buff=bin_cmd_list_buf )
            #-ar
            elif (len(cmd_list) > 5) and (cmd_list[2] == '-ar'):
                offset      = re.sub('0x|,|\.','', cmd_list[4])
                bin_cmd_list_offset = binascii.unhexlify(offset)
                rbuf = EMUL.i2c_offset_read( addr=int(cmd_list[3],16), offset=bin_cmd_list_offset, size=int(cmd_list[5]) )
                print('i2c-r:{0:04d}:{1:}'.format(len(rbuf), re.sub(r"(..)",r"\1.",rbuf.hex())))
            #-s
            elif (len(cmd_list) > 2) and (cmd_list[2] == '-s'):
                for i in EMUL.i2c_scan():
                    print('Addr=0x{0:X}(W:0x{1:X},R:0x{2:X})'.format( i, i<<1, (i<<1)+1 ))
            else:
                print('emul i2c parameter error.')
        #spi
        elif (cmd_list[1] == 'spi'):
            #-w
            if(len(cmd_list) > 3) and (cmd_list[2] == '-w'):
                wbuf      = re.sub('0x|,|\.','', cmd_list[3])
                bin_cmd_list = binascii.unhexlify(wbuf)
                EMUL.spi_write(wbuff = bin_cmd_list)
            #-r
            elif (len(cmd_list) > 3) and (cmd_list[2] == '-r'):
                rbuf = EMUL.spi_read(size = int(cmd_list[3]) )
                print('spi-r:{0:04d}:{1:}'.format(len(rbuf), re.sub(r"(..)",r"\1.",rbuf.hex())))
            #-rw
            elif (len(cmd_list) > 3) and (cmd_list[2] == '-rw'):
                wbuf      = re.sub('0x|,|\.','', cmd_list[3])
                bin_cmd_list = binascii.unhexlify(wbuf)
                rbuf = EMUL.spi_write_read(wbuff = bin_cmd_list, rbuff= bytearray(len(bin_cmd_list)))
                print('spi-r:{0:04d}:{1:}'.format(len(rbuf), re.sub(r"(..)",r"\1.",rbuf.hex())))
            else:
                print('emul spi parameter error.')                
        else:
            print('emul parameter error.')            
    else:
        help('./readme.txt','utf-8', '#=emul', '#=')

            
#============================
# bash_cmd
#============================
def bash_cmd(cmd_list):
    #cat
    if (len(cmd_list) > 1) and (cmd_list[0] == 'cat'):
        for i in File.read(cmd_list[1],'utf-8'):
            print(i.rstrip())
    #ls
    elif (len(cmd_list) > 0) and (cmd_list[0] == 'ls'):
        print(os.listdir())
    #cd
    elif (len(cmd_list) > 1) and (cmd_list[0] == 'cd'):
        os.chdir(cmd_list[1])
    #rm
    elif (len(cmd_list) > 1) and (cmd_list[0] == 'rm'):
        if cmd_list[1] == '-r':
            os.rmdir(cmd_list[2])
        else:
            os.remove(cmd_list[1])
    #mkdir
    elif (len(cmd_list) > 1) and (cmd_list[0] == 'mkdir'):
        os.mkdir(cmd_list[2])
        
#============================
# core_0
#============================
def core_0():

    global File
    while(1):
        #print("\n")
        #print(File.read('./test.txt','utf-8'))
        time.sleep(10)
#============================
#core_1
#============================
def core_1():
    global File
    global GPIO
                
    while(1):
        cmd_dat = input("bash# ")

        cmd_list = cmd_dat.split()

        if (len(cmd_list) == 0):
            pass
        #gpio/i2c/spi/adc/uart
        elif ((cmd_list[0] == 'gpio')or(cmd_list[0] == 'adc')or(cmd_list[0] == 'i2c')or(cmd_list[0] == 'spi')or(cmd_list[0] == 'uart')):
            picolib_cmd(cmd_list)            
        #disp/audio/ioexp
        elif ((cmd_list[0] == 'disp')or(cmd_list[0] == 'audio')or(cmd_list[0] == 'ioexp')):   
            peridev_cmd(cmd_list)
        #emul
        elif (cmd_list[0] == 'emul'):   
            emulator_cmd(cmd_list)
        #cat/ls/cd/rm/mkdir
        elif ((cmd_list[0] == 'cat')or(cmd_list[0] == 'ls')or(cmd_list[0] == 'cd')or(cmd_list[0] == 'rm')or(cmd_list[0] == 'mkdir')):          
            bash_cmd(cmd_list)
        #HELP
        else:
            help('./readme.txt','utf-8', '', '')

        #File.write('./log/log.txt','a',dat)


#============================
#main
#============================
if __name__ == '__main__':

    File = Picolib.cls_file()
    GPIO = Picolib.cls_gpio()
    I2C  = Picolib.cls_i2c()
    SPI  = Picolib.cls_spi()
    UART = Picolib.cls_uart()
    ADC  = Picolib.cls_adc()
    DZ   = PeriDev.cls_dispzettler()
    AUDIO= PeriDev.cls_mbedaudiocodec()
    IOEXP= PeriDev.cls_ioexpander()
    EMUL = Emulator.cls_emulator()
                    
    print("======================================")
    File.date('./main.py')
    File.date('./Picolib.py')
    File.date('./Emulator.py')
    File.date('./PeriDev.py')
    File.date('./readme.txt')
    print("======================================")

    #LED ON
    GPIO.open(25,'OUT')
    GPIO.write(25,1)
                    
    #core_0の開始
    _thread.start_new_thread(core_0,())

    #core_1の開始
    core_1()


