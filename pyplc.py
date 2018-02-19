#! /usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient
import struct 

class PyPlc:
    def __init__(self, ip, port = 502):
        self.client = ModbusTcpClient(ip, port=502)
        connected = self.client.connect()

    def AnalogRead(self, address):
        rr = self.client.read_holding_registers(address, count=2, unit=1)

        a = int(rr.registers[0])
        b = int(rr.registers[1])

        return struct.unpack("<f", struct.pack("<HH", a, b))[0] #read from modbus   

    def AnalogWrite(self, address, value):
        assert(type(value) is float)
    
        [a, b] = struct.unpack("<HH", struct.pack("<f", value)) 

        rr = self.client.write_register(address, a)
        rr = self.client.write_register(address + 1, b)
        return rr

    def WordRead(self, address):
        rr = self.client.read_holding_registers(address, count=1)
        return rr.registers[0]

    def WordWrite(self, address, value):
        assert(value >=0 and value <= 0xFFFF)

        rr = self.client.write_register(address, value)
        return rr

    def ReadString(self, address, length):
        assert(length >= 0)

        if length == 0:
            return

        num_words = length/2 + length%2
        rr = self.client.read_holding_registers(address, count=num_words)
        raw = struct.pack('%sH' % num_words, *rr.registers)
        return raw[:length]

    def WriteString(self, address, string):
        if len(string) % 2:
            string += '\0'

        words = struct.unpack('%sH' % (len(string)/2), string)
        rr = self.client.write_registers(address, words)

        return rr

    def DigitalWrite(self, address, value):
        assert(value == True or value == False)
        rq = self.client.write_coil(address, value)
        return rq

    def DigitalRead(self, address, count):
        rq = self.client.read_coils(address, count=count, unit=1)
        return rq.bits[:count]

    def __del__(self):
        self.client.close() 
