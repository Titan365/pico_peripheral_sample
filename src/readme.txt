#=gpio==================================
gpio -o [pin] [type]
    "gpio -o 3 out" gpio open.
    [pin]  : pin number.
    [type] : port type (out, in, intl, inth)

------------------------
gpio -w [pin] [level]
    "gpio -w 3 h" gpio write.
    [pin]  : pin number.
    [level]: port level (h, l, t = toggle)
------------------------
gpio -r [pin]
    "gpio -r 3" gpio read.
    [pin]  : pin number.
------------------------
gpio -l
    "gpio -l" gpio list.

#=adc==================================
adc -o [port]
    "adc -o 4" adc open.
    [port] : port <0,1,2,3,4 4:temperature>
------------------------
adc -r [port]
    "adc -r 4" adc read.
    [port] : port <0,1,2,3,4 4:temperature>
------------------------
adc -l
    "adc -l" adc list.
    
#=i2c===================================
i2c -o [port] [sda] [scl] [pull] [freq]
    "i2c -o 0 0 1 on 400000" i2c open.
    [port]  : port group <0, 1> 
    [sda]   : <0 : 0,4,8,12,16,20> <1 : 2,6,10,14,18,26>
    [scl]   : <0 : 1,5,9,13,17,21> <1 : 3,7,11,15,19,27>
    [pull]  : pullup <on, off>
    [freq]  : Hz <100000, 400000>
------------------------
i2c -w [port] [addr] [data]
    "i2c -w 0 3E 006C" i2c write.
    [port]  : port group <0, 1> 
    [addr]  : hex address.
    [data]  : hex data list.
------------------------
i2c -r [port] [addr] [size]
    "i2c -r 0 3E 10" i2c read.
    [port]  : port group <0, 1> 
    [addr]  : hex address.
    [size]  : oct length.
------------------------
i2c -aw [port] [addr] [offset] [data]
    "i2c -aw 0 50 00AA 123456" i2c address set write.
    [port]  : port group <0, 1> 
    [addr]  : hex address.
    [offset]: offset hex address.
    [data]  : hex data list.
------------------------
i2c -ar [port] [addr] [offset] [size]
    "i2c -ar 0 50 00AA 12" i2c address set read.
    [port]  : port group <0, 1> 
    [addr]  : hex address.
    [offset]: offset hex address.
    [size]  : oct length.
------------------------
i2c -l
    "i2c -l" i2c list.
------------------------
i2c -s [port]
    "i2c -s 0" i2c address scan.
    [port]  : port group <0, 1> 

#=spi===================================
spi -o [port] [sck] [tx] [rx] [baud] [bits] [polrarity] [phase]
    "spi -o 0 6 7 4 1000000 8 0 0" spi open.
    [port]     : port group <0, 1> 
    [sck_pin]  : <0:2,6,18> <1:10,14>
    [tx_pin]   : <0:3,7,19> <1:11,15>
    [rx_pin]   : <0:0,4,16> <1: 8,12>
    [baud]     : bps. 1000000
    [bits]     : data bit. 8
    [polarity] : sck_pin polarity. <0=low, 1=high>
    [phase]    : sampling phase.  <0=1st, 1=2nd>
------------------------
spi -w [port] [data]
    "spi -w 0 006C" spi write.
    [port]     : port group <0, 1> 
    [data]     : hex data list.
------------------------
spi -r [port] [size]
    "spi -r 0 10" spi read.
    [port]     : port group <0, 1> 
    [size]     : oct length.
------------------------
spi -rw [port] [data]
    "spi -rw 0 006C" spi write and read.
    [port]     : port group <0, 1> 
    [data]     : hex data list. read size is same data size.    
------------------------
spi -l
    "spi -l" spi list.
    
#=uart==================================
uart -o [port] [tx_pin] [rx_pin] [boud]
    "uart -o 0 12 13 115200" uart open.
    [port]    : port group <0, 1> 
    [tx_pin]  : <0:0,12,16> <1:4,8>
    [rx_pin]  : <0:1,13,17> <1:5,9>
    [baud]    : bps. 115200
------------------------
uart -w [port] [data]
    "uart -w 0 006C" uart write.
    [port]     : port group <0, 1> 
    [data]     : hex data list.
------------------------
uart -r [port] [size]
    "uart -r 0 10" uart read.
    [port]     : port group <0, 1> 
    [size]     : oct length.
------------------------
uart -l
    "uart -l" uart list.
                
#=disp===================================  
disp -o [port]
    "disp -o 0" display init.
    [port] : I2C group. 
           : <0 sda=0/scl=1>
           : <1 sda=14/scl=15>
------------------------
disp -c
    "disp -c" display clear.
------------------------
disp -w [pos] [data]
    "disp -w 0 012345" display write.
    [pos]  : start offset.<0=current, 1=1st line, 2=2nd line>
    [data] : string.

#=audio===================================  
audio -o [port]
    "audio -o 0" audio codec init.
    [port] : I2C group. 
           : <0 sda=0/scl=1>
           : <1 sda=15/scl=15>
------------------------
audio -w [mode]
    "audio -w i2s_slave" i2s slave mode.
    [mode] : loopback/ i2s_slave/ i2s_master(not support)/ stop

#=ioexp================================== 
ioexp -o [port]
    "ioexp -o 0" ioexpander init.
    [port] : SPI group. 
           : <0:sck= 6/tx= 7/rx=4/rst=2/cs=3/int=5>
           : <1:sck=10/tx=11/rx=12/rst=14/cs=13/int=15>
------------------------
ioexp -w [client] [address] [data]
    "ioexp -w 40 00 00"
    [client] :client address 0x40
    [address]:write address
    [data]   :write data
------------------------
ioexp -r [client] [address]
    "ioexp -r 40 00"
    [client] :client address 0x40
    [address]:read address

#=emul================================== 
protocol emulator 
emul -o [mode]
    "emul -o 0" emulator mode 0 set.
    [mode] : set mode number
     mode 0:{'SPI_CLK':10, 'SPI_TX':11, 'SPI_RX':12, 'SPI_CS':13, 'I2C_SDA':14, 'I2C_SCL':15},
     mode 1:{'OUT_1':10, 'OUT_2':11, 'OUT_3':12, 'OUT_4':13, 'I2C_SDA':14, 'I2C_SCL':15},
     mode 2:{'SPI_CLK':10, 'SPI_TX':11, 'SPI_RX':12, 'SPI_CS':13, 'OUT_1':14, 'OUT_2':15}
        
------------------------
emul -l
    "emul -l" emulator mode list.
------------------------
emul gpio -w [port] [level]
    "emul gpio -w OUT_1 t" OUT_1 toggle.
    [port]  : port name.
    [level] : port level (h, l, t = toggle)
------------------------
emul i2c -w [addr] [data]
emul i2c -r [addr] [size]
emul i2c -aw [addr] [offset] [data]
emul i2c -ar [port] [addr] [offset] [size]
emul i2c -s
    ---
    "emul i2c -w 3E 006C"         write.
    "emul i2c -r 3E 10"           read.
    "emul i2c -s"                 i2c address scan.
    "emul i2c -aw 50 00AA 123456" address set write.
    "emul i2c -ar 0 50 00AA 12"   address set read.
    ---
    [addr]  : hex address.
    [data]  : hex data list. 
    [offset]: offset hex address.
    [size]  : oct length.
------------------------
emul spi -w [data]
emul spi -r [size]
emul spi -rw [data]
    ---
    "emul spi -w 010203"  write.
    "emul spi -r 3"       read.
    "emul spi -rw 010203" write and read.
    ---
    [data]  : hex data list. 
    [size]  : oct length.
    
#=EOF==================================== 
