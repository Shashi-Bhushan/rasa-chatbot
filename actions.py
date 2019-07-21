from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json


class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	def run(self, dispatcher, tracker, domain):
		config = {
			"user_key": "36d71bf3534eb59c18c35f06a8686879"
		}

		# Initialize Zomato App
		zomato = zomatopy.initialize_app(config)

		# Get variables
		loc = tracker.get_slot('city')
		cuisine = tracker.get_slot('cuisine')
		people = tracker.get_slot('people')
		budget = tracker.get_slot('budget')

		location_detail=zomato.get_location(loc, 1)
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
			response = """Sorry no results found for {} restaurant in {}.""".format(cuisine, loc)
		else:
			response += "Found these {} restaurants in {} :\n".format(cuisine, loc)

			for index, restaurant in enumerate(d['restaurants']):
				response += "{}. {} in {}\n".format(index + 1, restaurant['restaurant']['name'], restaurant['restaurant']['location']['address'])

		dispatcher.utter_message(response)
		return [SlotSet('location', loc)]


if __name__ == '__main__':
	a = ActionSearchRestaurants()
	a.run('','','')