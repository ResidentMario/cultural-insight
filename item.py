from conceptmodel import ConceptModel
import os
import json

class Item:
	"""
	The Item object is a generic container for the objects that the application is trying to recommend to its users.
	In this applicaton, Item is extended by Event. In other scenarios it would be extended by e.g. Talk, Repice, etc.
	It contains two parts: a string textual description of the event, `description` (what is mined for the Item's concepts);
	And the model produced by mining these concepts.
	"""
	description = ""
	name = ""
	model = ConceptModel()

	def __init__(self, description="", name=""):
		name = self.name
		self.description = description
		if description:
			model = ConceptModel().addUserInputToConceptModel(self.description)
		else:
			model = ConceptModel()

	def deleteItem(self, filename="items.json"):
		if filename not in [f for f in os.listdir('.') if os.path.isfile(f)]:
			raise IOError('Error: events file ' + filename + ' not found.')
		else:
			data = json.load(open(filename))
			event_index = 0
			for i in range(0, len(data['events'])):
				if data['events'][i]['name'] == self.name:
					events_index = i
					break
			data['events'].pop(event_index)
			with open(filename, 'w') as outfile:
				json.dump(data, outfile, indent=4)

	def compareTo(self, second_concept_model):
		"""
		Compares two concept models and returns a measure of average overlap (a mock correlation).
		Input is a pair of object models.
		Open question: two-iter, or one-iter?
		Two-iter would be more accurate, especially with low information, but more costly, and harder to implement. Might be necessary?
		Another open question is whether or not a more sophisticated model could or should be used.
		Output is a standardized 0-to-1 three-decimal number describing correlation.
		"""
		overlap = 0
		num = 0
		for pair in zip(sorted(self.model.model.keys()), sorted(second_concept_model.model.model.keys())):
			if pair[0] == pair[1]:
				overlap += self.model.model[pair[0]] + second_concept_model.model.model[pair[1]]
				num += 1
		if num == 0:
			return 0.0
		else:
			return round((overlap/num)/min(len(self.model.model),len(second_concept_model.model.model)),3)