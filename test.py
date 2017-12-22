import pulsedlaser as pl
import time

p = pl.PulsedLaser()

p.SetupOutputModes()
p.ResetAlarms()
p.DisableGuideBeam()

print "Enabling power supply"
p.FeedWatchdog()
p.EnablePowerSupply()

p.WriteOperatingPower(100)

print "Waiting 5 seconds"
for _ in xrange(0, 500):
        p.FeedWatchdog()
        time.sleep(0.01)

print "Turning on laser"
p.EnableEmission()
p.LaserEmissionOn()
for _ in xrange(0, 200):
        p.FeedWatchdog()
        time.sleep(0.01)
print "Pulse Energy (mJ): " + str(p.ReadOperatingPulseEnergy())
p.LaserEmissionOff()
p.DisableEmission()

print "Laser off"

p.WriteOperatingPower(0)

print "Waiting 5 seconds"
for _ in xrange(0, 500):
        p.FeedWatchdog()
        time.sleep(0.01)

p.DisablePowerSupply()
p.EnableGuideBeam()


print "Done"

