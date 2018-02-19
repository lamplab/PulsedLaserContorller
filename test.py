import pulsedlaser as pl
import time
import sys

if len(sys.argv) != 3:
    print "usage: " + sys.argv[0] + " <power_percent> <ontime_seconds>"
    exit(-1)

power = float(sys.argv[1])
ontime = float(sys.argv[2])

p = pl.PulsedLaser()

p.SetupOutputModes()
p.ResetAlarms()
p.DisableGuideBeam()

print "Enabling power supply"
p.FeedWatchdog()
p.EnablePowerSupply()

p.WriteOperatingPower(power)

countdown = 5
for _ in xrange(0, 5):
	print "countdown: ", countdown
	countdown -= 1
	for _ in xrange(0, 100):
		p.FeedWatchdog()
		time.sleep(0.01)

print "Turning on laser"
p.EnableEmission()
p.LaserEmissionOn()
for _ in xrange(0, int(ontime/0.01)):
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

