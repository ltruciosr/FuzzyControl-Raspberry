import smbus
import time

bus = smbus.SMBus(1)

#Chequear su direccion tipeando 'sudo i2cdetect -y 1' en el terminal

def setup(Addr):
    global address
    address = 0x48

def read(chn):  #Canal de lectura A0-A3
    try:
    	if chn == 0:
        	bus.write_byte(address, 0x40)
    	if chn == 1:
        	bus.write_byte(address, 0x41)
    	if chn == 2:
        	bus.write_byte(address, 0x42)
    	if chn == 3:
	        bus.write_byte(address, 0x43)

    	bus.read_byte(address)
    
    except Exception, e:
        print "Address: %s" % address
        print e
    
    return bus.read_byte(address)

def write(val):
    try:
    	temp = int(val) #Convertimos el valor
    	bus.write_byte_data(address, 0x40, temp)    #The value of temp have 
    
    except Exception, e:
        print "Error: Device Address: 0x%2X" % address
        print e
        
if __name__== "__main__":
    setup(0x48)
    while True:
        print 'AIN0 = ', read(0)
        print ' '
        tmp = read(0)
        write(tmp)
        time.sleep(0.5)

        
    
