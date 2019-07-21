from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage


class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	def run(self, dispatcher, tracker, domain):
		# Get variables
		loc = tracker.get_slot('city')
		cuisine = tracker.get_slot('cuisine')
		people = tracker.get_slot('people')
		budget = tracker.get_slot('budget')

		dispatcher.utter_message(self.get_zomato_response(loc, cuisine, people, budget))
		return [SlotSet('location', loc)]

	@staticmethod
	def get_zomato_response(location, cuisine, people, budget):
		config = {
			"user_key": "36d71bf3534eb59c18c35f06a8686879"
		}

		# Initialize Zomato App
		zomato = zomatopy.initialize_app(config)

		location_detail = zomato.get_location(location, 1)
		d1 = json.loads(location_detail)
		lat = d1["location_suggestions"][0]["latitude"]
		lon = d1["location_suggestions"][0]["longitude"]
		cuisines_dict = {
			'Mexican': 73,
			'Chinese': 25,
			'American': 1,
			'Italian': 55,
			'North Indian': 50,
			'South Indian': 85
		}
		results = zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 5)
		d = json.loads(results)

		response = ""
		if d['results_found'] == 0:
			response = """Sorry no results found for {} restaurant in {}.""".format(cuisine, location)
		else:
			response += "Found these {} restaurants in {} :\n".format(cuisine, location)

			for index, restaurant in enumerate(d['restaurants']):
				response += "{}. {} in {}\n".format(index + 1, restaurant['restaurant']['name'], restaurant['restaurant']['location']['address'])

		return response


class ActionSendMail(Action):
	def name(self):
		return 'action_send_mail'

	SERVER = smtplib.SMTP('smtp.gmail.com', 25)  # 587)
	SERVER.connect("smtp.gmail.com", 587)
	SERVER.ehlo()
	SERVER.starttls()
	SERVER.ehlo()

	# Next, log in to the server
	SERVER.login("user@gmail.com", "password")

	FROM = 'economicviewpoint@gmail.com'

	TO = ["stylesense3@gmail.com"]  # must be a list

	SUBJECT = "Hello!"

	TEXT = "This message was sent with Python's smtplib."

	def run(self, dispatcher, tracker, domain):
		# Get variables
		mail_id = tracker.get_slot('user_mail_id')

		TO = ["stylesense3@gmail.com", mail_id]  # must be a list

		# Get variables
		loc = tracker.get_slot('city')
		cuisine = tracker.get_slot('cuisine')
		people = tracker.get_slot('people')
		budget = tracker.get_slot('budget')

		to = ["stylesense3@gmail.com"]
		# Prepare actual message

		message = """\
			From: %s
			To: %s
			Subject: %s

			Sent to Subjects : 
			%s
			""" % (self.FROM, ", ".join(to), self.SUBJECT, to, ActionSearchRestaurants.get_zomato_response(loc, cuisine, people, budget))

		# Send the mail
		error = self.SERVER.sendmail(self.FROM, to, message)
		self.SERVER.quit()

		return error


if __name__ == '__main__':
	a = ActionSendMail()
	a.run('','','')