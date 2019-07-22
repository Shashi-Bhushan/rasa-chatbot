from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json

# Import smtplib for the actual sending function
import smtplib

import csv


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

	def __init__(self):

		self.SERVER = smtplib.SMTP('smtp.gmail.com', 25)  # 587)
		self.SERVER.connect("smtp.gmail.com", 587)
		self.SERVER.ehlo()
		self.SERVER.starttls()
		self.SERVER.ehlo()

		# Next, log in to the server
		self.SERVER.login("economicviewpoint@gmail.com", "gzznfnmdgrkmzpsh")

		self.FROM = 'economicviewpoint@gmail.com'

		self.SUBJECT = "Restaurant List!"

	def run(self, dispatcher, tracker, domain):
		# Get variables
		mail_id = tracker.get_slot('user_mail_id')

		to = ["stylesense3@gmail.com"]  # must be a list

		if mail_id is not None:
			to.append(mail_id)

		# Get variables
		loc = tracker.get_slot('city')
		cuisine = tracker.get_slot('cuisine')
		people = tracker.get_slot('people')
		budget = tracker.get_slot('budget')

		# Prepare actual message
		message = """\
			From: %s
			To: %s
			Subject: %s

			Hi
			Here's the Restaurant list you asked for : 
			%s
			""" % (self.FROM, ", ".join(to), self.SUBJECT, to, ActionSearchRestaurants.get_zomato_response(loc, cuisine, people, budget))

		# Send the mail
		error = self.SERVER.sendmail(self.FROM, to, message)
		self.SERVER.quit()

		return error


class ActionCheckCity(Action):
	def name(self):
		return 'action_check_city'

	def __init__(self):
		with open('data/cities.csv', 'r', encoding="utf-8") as csvfile:
			reader = csv.reader(csvfile, delimiter=',')

			self.valid_cities = [row for row in reader][0]

	def run(self, dispatcher, tracker, domain):
		slot_city = tracker.get_slot('city')

		return [SlotSet('valid_city', any([city.lower() == slot_city.lower() for city in self.valid_cities]))]


if __name__ == '__main__':
	a = ActionCheckCity()
	a.run('','','')