from gpiozero import LED
from time import sleep
import cli

def runPump(seconds):
	# convert seconds from string to integer
	seconds_int = int(seconds)

	# pin 2 means GPIO2, or physical pin 3
	pump = LED(2)

	pump.on()
	sleep(seconds_int)
	pump.off()

cli.argsFromCLI(runPump)
