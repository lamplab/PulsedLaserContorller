from pulsedlasercontroller import PulsedLaserController

_cmd_map = {
    'ReadDeviceStatus': 4,
    'ReadDeviceTemperature': 5,
    'ReadDeviceExtendedStatus': 11,
    'ReadOperationMode': 23,
    'WriteOperationMode': 24,
    'LaserEmissionOn': 30,
    'LaserEmissionOff': 31,
    'WriteOperatingPower': 32,
    'ReadOperatingPower': 34,
    'ReadOperatingPulseEnergy': 36,
    'GuideLaserOn': 40,
    'GuideLaserOff': 41,
    'SetEmissionEnableOn': 42,
    'SetEmissionEnableOff': 43,
    'ResetAlarms': 50,
}

_OperationModeResetMask = 0b11111111111111110100101101110010
_OperationModeSetMask =   0b00000000000000001000010000000000 

def _fbin(x, bits):
    return ("{0:0" + str(bits) + "b}").format(int(x))


class PulsedLaser:

    def _cmd(self, command_name, parameters=''):
        return self.controller.LaserCommand(_cmd_map[command_name], parameters)

    def __init__(self, ip='192.168.0.10', port=502):
        self.controller = PulsedLaserController(ip, port)

    def FeedWatchdog(self):
        self.controller.FeedWatchdog()

    def EnablePowerSupply(self):
        self.controller.EnablePowerSupply()

    def DisablePowerSupply(self):
        self.controller.DisablePowerSupply()

    def GetPowerSupplyStatus(self):
        return self.controller.GetPowerSupplyStatus()

    def GetControllerEstopStatus(self):
        return self.controller.GetControllerEstopStatus()

    def SetupOutputModes(self):
        mode = int(self._cmd('ReadOperationMode'))
        mode &= _OperationModeResetMask
        mode |= _OperationModeSetMask
        self._cmd('WriteOperationMode', str(mode))
        
    def ReadOperationMode(self):
        mode = self._cmd('ReadOperationMode')
        return _fbin(mode, 16)

    def EnableGuideBeam(self):
        self._cmd('GuideLaserOn')

    def DisableGuideBeam(self):
        self._cmd('GuideLaserOff')

    def ReadStatus(self):
        status = self._cmd('ReadDeviceStatus')
        return _fbin(status, 8)

    def ReadExtendedStatus(self):
        status = self._cmd('ReadDeviceExtendedStatus')
        return _fbin(status, 16)

    def ResetAlarms(self):
        self._cmd('ResetAlarms')
        
    def ReadModuleTemperature(self):
        temp = self._cmd('ReadDeviceTemperature')
        return temp

    def WriteOperatingPower(self, percent):
        assert(percent >= 0 and percent <= 100) 
        percent_formatted = "{:0.1f}".format(percent)
        self._cmd('WriteOperatingPower', percent_formatted)

    def ReadOperatingPower(self):
        power = self._cmd('ReadOperatingPower')
        return power
      
    def ReadOperatingPulseEnergy(self):
        energy = self._cmd('ReadOperatingPulseEnergy')
        return energy

    def EnableEmission(self):
        self._cmd('SetEmissionEnableOn')

    def DisableEmission(self):
        self._cmd('SetEmissionEnableOff')

    def LaserEmissionOn(self):
        self._cmd('LaserEmissionOn')

    def LaserEmissionOff(self):
        self._cmd('LaserEmissionOff')

