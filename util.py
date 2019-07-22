import csv
import json

def create_json(list, city):
	list.append({
		"text": "in " + city,
		"intent": "restaurant_search",
		"entities": [{
			"start": 3,
			"end": 3 + len(city),
			"value": str(city),
			"entity": "city"
		}]
	})
	list.append({
		"text": str(city),
		"intent": "restaurant_search",
		"entities": [
			{
				"start": 0,
				"end": len(city),
				"value": str(city),
				"entity": "city"
			}
		]
	})
	list.append({
        "text": "looking for a place to eat in " + city,
        "intent": "restaurant_search",
        "entities": [
          {
            "start": 30,
            "end": 30 + len(city),
            "value": str(city),
            "entity": "city"
          }
        ]
  	})
	list.append({
        "text": "anywhere in " + city + " with good food",
        "intent": "restaurant_search",
        "entities": [
          {
            "start": 12,
            "end": 12 + len(city),
            "value": str(city),
            "entity": "city"
          }
        ]
      })


if __name__ == '__main__':
    with open('data/cities.csv', 'r', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        lst = []
        [create_json(lst, city) for row in reader for city in row]

        with open('data/temp.json', 'w', encoding="utf-8") as myfile:
            print(lst)
            json.dump(lst, myfile)

