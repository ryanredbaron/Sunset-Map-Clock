#sudo apt install python3-pip
#sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
#sudo pip install requests
#sudo apt-get install ntpdate
#cd Sunset
#sudo python3 Sunset.py
#nohup sudo python3 Sunset.py &

from os import system, name 
import time
import board
import neopixel
import requests
from datetime import datetime, timedelta

StartPixel = 0
EndPixel = 17
SunsetPadding = 60

ORDER = neopixel.GRB
num_pixels = EndPixel - StartPixel
pixel_pin = board.D18
pixels = neopixel.NeoPixel(pixel_pin, EndPixel, brightness=255, auto_write=False,pixel_order=ORDER)

def reset_LEDs_Sunrise():
	for LEDinitialSetup in range(StartPixel,EndPixel):
		red=250
		green=190
		blue=60
		pixels[LEDinitialSetup]=(red, green, blue)
		pixels.show()
		
def reset_LEDs_Sunset():
	for LEDinitialSetup in range(StartPixel,EndPixel):
		red=0
		green=0
		blue=0
		pixels[LEDinitialSetup]=(red, green, blue)
		pixels.show()
 
def clear(): 
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 

SetupMode = 1
UpdateTimesTimer = 3600
TransitTimeSeconds = 10800
CurrentProgramTime = (datetime.strptime('00:00:01 AM', '%H:%M:%S %p'))
reset_LEDs_Sunset()
while True:
	#CurrentLocalTime = (datetime.strptime('16:00:00', '%H:%M:%S'))
	CurrentLocalTime = (datetime.strptime(datetime.now().strftime("%H:%M:%S"), '%H:%M:%S'))
	clear()
	UpdateTimesTimer += 1
	if UpdateTimesTimer >= 3600:
		EastRequestData = requests.get('http://api.sunrise-sunset.org/json?lat=39.14496&lng=-79.28147&date=today')
		WestRequestData = requests.get('http://api.sunrise-sunset.org/json?lat=38.924921&lng=-119.993874&date=today')
		EastCoastSunrise = ((datetime.strptime((((EastRequestData.json())['results'])['sunrise']), '%I:%M:%S %p')) - timedelta(hours=8) - timedelta(minutes=SunsetPadding)).replace(year=1900, month=1, day=1)
		WestCoastSunrise = ((datetime.strptime((((WestRequestData.json())['results'])['sunrise']), '%I:%M:%S %p')) - timedelta(hours=8) + timedelta(minutes=SunsetPadding)).replace(year=1900, month=1, day=1)
		EastCoastSunset = ((datetime.strptime((((EastRequestData.json())['results'])['sunset']), '%I:%M:%S %p')) - timedelta(hours=8) - timedelta(minutes=SunsetPadding)).replace(year=1900, month=1, day=1)
		WestCoastSunset = ((datetime.strptime((((WestRequestData.json())['results'])['sunset']), '%I:%M:%S %p')) + timedelta(hours=16) + timedelta(minutes=SunsetPadding)).replace(year=1900, month=1, day=1)
		UpdateTimesTimer = 0
		print('Data Updated')
	print('-----------------Waiting for event!-----------------')
	print('Current Local Time-',CurrentLocalTime)
	print('Sunrise Starts-    ',EastCoastSunrise)
	print('Sunrise Ends-      ',WestCoastSunrise)
	print('Sunset Starts-     ',EastCoastSunset)
	print('Sunset Ends-       ',WestCoastSunset)
	print('----------------------------------------------------')
	time.sleep(1)
	
	TransitTimeSeconds = int((WestCoastSunrise - EastCoastSunrise).total_seconds())
	if CurrentLocalTime >= EastCoastSunrise and CurrentLocalTime <= WestCoastSunrise:
		CurrentProgramTime = EastCoastSunrise
		print("Entering Sunrise")
		for pixelcount in range(StartPixel,EndPixel):
			red=0;green=0;blue=0
			while red != 250:
				if red != 250:
					red = red + 1
				if green != 190:
					green = green + 1
				if blue != 60:
					blue = blue + 1
				pixels[pixelcount]=(red, green, blue)
				pixels.show()
				if SetupMode == 1:
					CurrentProgramTime = CurrentProgramTime + timedelta(seconds=(TransitTimeSeconds)/(num_pixels*250))
					if CurrentProgramTime >= CurrentLocalTime:
						SetupMode = 0
				else:
					time.sleep((TransitTimeSeconds)/(num_pixels*250))
					clear()
					print('-----------------Sunrise Mode-----------------')
					print('Current Local Time-',CurrentLocalTime)
					print('Sunrise Starts-    ',EastCoastSunrise)
					print('Sunrise Ends-      ',WestCoastSunrise)
					print('Sunset Starts-     ',EastCoastSunset)
					print('Sunset Ends-       ',WestCoastSunset)
					print('Pixel Number-',pixelcount,'|','Red-',red,'Sleep Time-',(TransitTimeSeconds)/(num_pixels*250))
					print('----------------------------------------------------')
		print("Exiting Sunrise")
	if CurrentLocalTime > WestCoastSunrise and SetupMode == 1:
		reset_LEDs_Sunrise()
	
	TransitTimeSeconds = int((WestCoastSunset - EastCoastSunset).total_seconds())
	if CurrentLocalTime >= EastCoastSunset and CurrentLocalTime <= WestCoastSunset:
		CurrentProgramTime = EastCoastSunset
		print("Entering Sunset")
		for pixelcount in range(StartPixel,EndPixel):
			red=250;green=190;blue=60
			while red != 0:
				if red != 0:
					red = red - 1
				if green != 0:
					green = green - 1
				if blue != 0:
					blue = blue - 1
				pixels[pixelcount]=(red, green, blue)
				pixels.show()
				if SetupMode == 1:
					CurrentProgramTime = CurrentProgramTime + timedelta(seconds=(TransitTimeSeconds)/(num_pixels*250))
					if CurrentProgramTime >= CurrentLocalTime:
						SetupMode = 0
				else:
					time.sleep((TransitTimeSeconds)/(num_pixels*250))
					clear()
					print('-----------------Sunset Mode-----------------')
					print('Current Local Time-',CurrentLocalTime)
					print('Sunrise Starts-    ',EastCoastSunrise)
					print('Sunrise Ends-      ',WestCoastSunrise)
					print('Sunset Starts-     ',EastCoastSunset)
					print('Sunset Ends-       ',WestCoastSunset)
					print('Pixel Number-',pixelcount,'|','Red-',red,'Sleep Time-',(TransitTimeSeconds)/(num_pixels*250))
					print('----------------------------------------------------')
		print("Exiting Sunset")
	if CurrentLocalTime > WestCoastSunset and SetupMode == 1:
		reset_LEDs_Sunset()
	SetupMode = 0