
import pyplc
import time

class PulsedLaserController:
    # IO addresses
    PowerSupplyEnableAddress = 0x4003
    PowerSupplyStatusAddress = 0x4004
    ControllerEstopStatusAddress = 0x4005
    FeedWatchdogAddress = 0x4006

    # Serial transmit buffer
    SendBufferAddress = 0x9000
    BufferLengthAddress = 0x0000

    # Serial transmit registers
    StartTransmissionAddress = 0x4000
    WriteResultAddress = 0x400F

    # Serial read buffer 
    RecieveBufferAddress = 0x9080
    RecieveBufferLengthAddress = 0x0001

    # Serial read registers
    ReadStatusAddress = 0x400A
    NumReadStatusBits = 4
    ReadSuccessOffset = 0x0
    OverflowErrorOffset = 0x1
    FirstCharacterErrorOffset = 0x2
    InterCharacterDelayErrorOffset = 0x3

    # Settings
    ReadTimeSleep = 0.01
    ReadNumRetries = 0.250 / ReadTimeSleep

    def __init__(self, ip, port = 502):
        self.plc = pyplc.PyPlc(ip)

    def FeedWatchdog(self):
        self.plc.DigitalWrite(PulsedLaserController.FeedWatchdogAddress, True)

    def EnablePowerSupply(self):
        self.plc.DigitalWrite(PulsedLaserController.PowerSupplyEnableAddress, True)

    def DisablePowerSupply(self):
        self.plc.DigitalWrite(PulsedLaserController.PowerSupplyEnableAddress, False)

    def GetPowerSupplyStatus(self):
        return self.plc.DigitalRead(PulsedLaserController.PowerSupplyStatusAddress, 1)[0]

    def GetControllerEstopStatus(self):
        return not self.plc.DigitalRead(PulsedLaserController.ControllerEstopStatusAddress, 1)[0]

    def LaserCommand(self, command_code, parameters=''):
        self._send(command_code, parameters)
        response_split = self._recieve().split(';')
        return response_split[1]

    def _recieve(self):
        counter = PulsedLaserController.ReadNumRetries
        bits = self.plc.DigitalRead(PulsedLaserController.ReadStatusAddress, 
            PulsedLaserController.NumReadStatusBits)

        while all(not bit for bit in bits) and counter:
            bits = self.plc.DigitalRead(PulsedLaserController.ReadStatusAddress, 
                PulsedLaserController.NumReadStatusBits)
            time.sleep(PulsedLaserController.ReadTimeSleep)
            counter -= 1
         
        if bits[PulsedLaserController.OverflowErrorOffset]:
            raise IOError('PLC serial buffer overflow error')

        if bits[PulsedLaserController.FirstCharacterErrorOffset]:
            raise IOError('No serial response recieved after command')

        if bits[PulsedLaserController.InterCharacterDelayErrorOffset]:
            raise IOError('Recieved long delay between response characters')

        if not bits[PulsedLaserController.ReadSuccessOffset]:
            raise IOError('Send command PLC serial recieve error')

        length = self.plc.WordRead(PulsedLaserController.RecieveBufferLengthAddress)
        response = self.plc.ReadString(PulsedLaserController.RecieveBufferAddress, length)

        return response

    def _send(self, command_code, parameters):
        commandString = '$' + str(command_code) + ';' + parameters
        self.plc.WriteString(PulsedLaserController.SendBufferAddress, commandString)
        self.plc.WordWrite(PulsedLaserController.BufferLengthAddress, len(commandString))
        self.plc.DigitalWrite(PulsedLaserController.StartTransmissionAddress, True)
        
