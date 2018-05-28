import pulsedlaser as pl
import time
import sys

if len(sys.argv) != 2:
	print "usage: " + sys.argv[0] + "<0=off | 1=on>"
	exit(-1)

state = int(sys.argv[1])

p = pl.PulsedLaser()

print "Setting laser parameters..."
p.SetupOutputModes()
p.ResetAlarms()

if state == 1:
	print "Enabling guide beam..."
	p.EnableGuideBeam()
elif state == 0:
	print "Disabling guide beam..."
	p.DisableGuideBeam()
else:
	print "usage: " + sys.argv[0] + "<0=off | 1=on>"
	exit(-1)

print "Done"

