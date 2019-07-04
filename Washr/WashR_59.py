from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.config import Config
from kivy.graphics import *
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width',  500)
Config.set('graphics', 'height', 400)
Config.set('kivy', 'exit_on_escape', '0')
from kivy.core.window import Window
from time import sleep
import pyrebase
from win10toast import ToastNotifier
import matplotlib.pyplot as plt


url = 'https://week4-raspberry-pi.firebaseio.com/'  # URL to Firebase database
apikey = '-'
config = {
    "apiKey": apikey,
    "databaseURL": url,
    "authDomain": "week4-raspberry-pi.firebaseapp.com",
    "storageBucket": "week4-raspberry-pi.appspot.com"
}

firebase = pyrebase.initialize_app(config) # initialize the firebase database
db = firebase.database()
toaster =  ToastNotifier()

# Mains
class Mains(Widget):
	def __init__(self):
		# make sure that we are not overriding any important
		super().__init__()

		with self.canvas:
			image = "resources/background.jpg"
			image2 = "resources/Washr.png"
			image3 = "resources/washingmachine2.png"
			image4 = "resources/dryer2.png"
			Rectangle(pos=(0, 0), size=(500, 500), source= image)
			#Rectangle(pos =(10,10), size= (200,75), source = image2)
			Rectangle(pos =(40,310), size= (70,75), source = image3)
			Rectangle(pos =(40,230), size= (70,75), source = image3)
			Rectangle(pos =(40,150), size= (70,75), source = image3)
			Rectangle(pos =(40,70), size= (70,75), source = image3)

			Rectangle(pos =(140,310), size= (70,75), source = image3)
			Rectangle(pos =(140,230), size= (70,75), source = image3)
			Rectangle(pos =(140,150), size= (70,75), source = image3)
			Rectangle(pos =(140,70), size= (70,75), source = image3)

			Rectangle(pos =(265,310), size= (70,75), source = image3)
			Rectangle(pos =(265,230), size= (70,75), source = image3)
			Rectangle(pos =(265,150), size= (70,75), source = image3)

			Rectangle(pos =(390,310), size= (70,75), source = image4)
			Rectangle(pos =(390,230), size= (70,75), source = image4)
			Rectangle(pos =(390,150), size= (70,75), source = image4)

			Rectangle(pos =(390,20), size= (70,75), source = image4)
			Rectangle(pos =(310,20), size= (70,75), source = image4)
			Rectangle(pos =(230,20), size= (70,75), source = image4)



		# take RGB values and divide by 100 to get colours
		blue = (0, 0, 1.5, 2.5)
		red = (2.55, 0.45, 0.41, 1.0)
		red1 = (2.5, 0, 0, 1.5)
		green = (0.06,1.70,0.93, 1.0)
		##Column1
		self.W1 = Button(text= '', size= (16,16), background_color=red, font_size=14, pos= (85, 365))
		self.W2 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (85,285))
		self.W3 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (85,205))
		self.W4 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (85,125))
		##Column2
		self.W5 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (185, 365))
		self.W6 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (185,285))
		self.W7 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (185,205))
		self.W8 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (185,125))
		##Column3
		self.W9 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (310, 365))
		self.W10 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (310,285))
		self.W11 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (310,205))
		##Dryers
		self.D1 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (435, 365))
		self.D2 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (435,285))
		self.D3 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (435,205))

		self.D4 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (435,75))
		self.D5 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (355,75))
		self.D6 = Button(text='', size= (16,16), background_color=red, font_size=14, pos= (275,75))
		
		self.ML = Button(text='Block 59 usage information', size= (200,50), on_press= self.MLcalculate, font_size=14, pos= (5,5))

		self.add_widget(self.W1)
		self.add_widget(self.W2)
		self.add_widget(self.W3)
		self.add_widget(self.W4)
		self.add_widget(self.W5)
		self.add_widget(self.W6)
		self.add_widget(self.W7)
		self.add_widget(self.W8)
		self.add_widget(self.W9)
		self.add_widget(self.W10)
		self.add_widget(self.W11)
		self.add_widget(self.D1)
		self.add_widget(self.D2)
		self.add_widget(self.D3)
		self.add_widget(self.D4)
		self.add_widget(self.D5)
		self.add_widget(self.D6)

		self.add_widget(self.ML)
		# stream handler to get the real time data
		def stream_handler(message):
			on_off_state = message["data"]
			print(on_off_state)
			
			if on_off_state == 0:
				self.W4.background_color = green
				toaster.show_toast("Washing Machine 4 is free to use",
									"Get yo' laundry and detergent ready",
                   					icon_path=None,
                   					duration=5,
                   					threaded=True)
				#while toaster.notification_active(): sleep(0.1)

			else:
				self.W4.background_color = red

		# get values from "W1/On" in our firebase
		my_stream = db.child("W1/On").stream(stream_handler)
		self.stream = my_stream

	def MLcalculate(self, instance): # button takes 2 inputs
		plt.style.use('seaborn')
		
		# take all the values from firebase and append it to hourly form
		d = {'0000': 0, '0100': 0, '0200': 0, '0300': 0, '0400': 0, '0500': 0, '0600': 0, '0700': 0, '0800': 0, '0900': 0, '1000': 0, '1100': 0, '1200': 0, '1300': 0, '1400': 0, '1500': 0, '1600': 0, '1700': 0, '1800': 0, '1900': 0, '2000': 0, '2100': 0, '2200': 0, '2300': 0}
		logger = db.child("W1/logger").get().val()

		for i in logger:
			if i[0].startswith("00"):
				d["0000"] += i[1]
			elif i[0].startswith("01"):
				d["0100"] += i[1]
			elif i[0].startswith("02"):
				d["0200"] += i[1]
			elif i[0].startswith("03"):
				d["0300"] += i[1]
			elif i[0].startswith("04"):
				d["0400"] += i[1]
			elif i[0].startswith("05"):
				d["0500"] += i[1]
			elif i[0].startswith("06"):
				d["0600"] += i[1]
			elif i[0].startswith("07"):
				d["0700"] += i[1]
			elif i[0].startswith("08"):
				d["0800"] += i[1]
			elif i[0].startswith("09"):
				d["0900"] += i[1]
			elif i[0].startswith("10"):
				d["1000"] += i[1]
			elif i[0].startswith("11"):
				d["1100"] += i[1]
			elif i[0].startswith("12"):
				d["1200"] += i[1]
			elif i[0].startswith("13"):
				d["1300"] += i[1]
			elif i[0].startswith("14"):
				d["1400"] += i[1]
			elif i[0].startswith("15"):
				d["1500"] += i[1]
			elif i[0].startswith("16"):
				d["1600"] += i[1]
			elif i[0].startswith("17"):
				d["1700"] += i[1]
			elif i[0].startswith("18"):
				d["1800"] += i[1]
			elif i[0].startswith("19"):
				d["1900"] += i[1]
			elif i[0].startswith("20"):
				d["2000"] += i[1]
			elif i[0].startswith("21"):
				d["2100"] += i[1]
			elif i[0].startswith("22"):
				d["2200"] += i[1]
			elif i[0].startswith("23"):
				d["2300"] += i[1]

		timevalues = list(d.keys())
		statevalues = list(d.values())
		
		plt.ylabel("Usage frequency")
		plt.yticks([])
		plt.xticks(rotation=60)
		besttime = []
		weehours = ["0300","0400","0500","0600","0200"]
		for i in d:

			if d[i] == (min(statevalues)) and i not in weehours:
				besttime.append(i)


		besttimestr = (", ".join(besttime))
		plt.title("Best timings to use: " + besttimestr)
		
		plt.bar(timevalues, statevalues)

		plt.show()	

class WashingApp(App):
	# stop the stream
	def on_stop(self):
		self.root.stream.close()

	def build(self):
		self.title = 'Washing Machine Block - 59'
		self.icon = 'resources/Washing-Machine-256.png'
		return(Mains())



if __name__ == "__main__":
	WashingApp().run()
