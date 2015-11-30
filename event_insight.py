"""event-insight.py
    Test script."""

import event_insight_lib
import backend
import urllib

def main():
	# Tokenization and API access test.
	token = event_insight_lib.getToken()
	# backend.saveFile(event_insight_lib.annotateText('The Space Shuttle Pavilion showcases the space shuttle Enterprise, the prototype NASA orbiter that paved the way for America’s successful space shuttle program. Seventeen dynamic exhibit zones feature original artifacts, photographs, audio, and films that immerse visitors in the science and history of Enterprise and the space shuttle era.', token), 'example_output.json')

	# ConceptModel definition test.
	# a = backend.ConceptModel([], 'test@baruchmail.cuny.edu')
	# a.model = backend.fetchConceptsForUserConcept('Smithsonian', token)
	# print(a.model)
	# a.saveModel()
	# print(backend.fetchConceptsForUserConcept('Smithsonian', token))

	# ConceptModel manipulation test.
	# a = backend.ConceptModel(None, 'testA')
	# a.model = {'C': 0.5, 'D': 0.8, 'E': 0.1}
	# b = backend.ConceptModel(None, 'testB')
	# b.model = {'A': 0.4, 'B': 0.7}
	# print(backend.addObjectToConceptModel(a, b).model)
	# a.model = {'A': 0.0}
	# b.model = {'B': 0.0}
	# print(backend.addObjectToConceptModel(a, b).model)
	
	# ConceptModel comparison test.
	# a = backend.ConceptModel(None, 'testA')
	# a.model = {'A': 0.5, 'B': 0.8, 'E': 0.1}
	# b = backend.ConceptModel(None, 'testB')
	# b.model = {'A': 0.4, 'B': 0.7, 'D': 0.2}
	# print(backend.compareConceptModels(a,b))

	# Watson API plug-in test.
	# a = backend.ConceptModel([], 'test@baruchmail.cuny.edu')
	# a.model = backend.parseRawCall(backend.fetchConceptsForUserConcept('Smithsonian', token))
	# print(a.model)
	# b = backend.ConceptModel([], 'test@baruchmail.cuny.edu')
	# b.model = {'test': 0.98}
	# a = backend.addObjectToConceptModel(a, b)
	# print(a.model)

	# Conceptualization test.
	# print(backend.fetchConceptsForUserConcept('Intrepid Museum', token, cutoff=0.2))
	# print(urllib.parse.quote('Intrepid Air & Space Museum'.encode("utf8")))
	# print(urllib.parse.quote('Intrepid Sea, Air & Space Museum'.replace(' ', '_'), safe='_,'))
	# c = ['Smithsonian Institute', 'Intrepid Sea, Air & Space Museum', 'Rubin Museum']
	# r = backend.conceptualize2(c, token)
	# print(r)

	# User definition test.
	# a = backend.addNewUser('test3@baruchmail.cuny.edu', 'Random', ['Smithsonian Institute', 'Rubin Museum'], token)
	# print(a.model)

	# Concept display test.
	# concepts = backend.getConceptsByID('test@baruchmail.cuny.edu')
	# for concept in concepts:
	#	print(concept + str(concepts[concept]))

	# Concept self-add test.
	# backend.addConceptsToID('test@baruchmail.cuny.edu', ['Taoism', 'Buddhism'])
	# backend.addConceptsToID('test@baruchmail.cuny.edu', ['Test', 'Buddhism'])
	# print(to_be_added)
	# user.saveModel(to_be_added)

	# Remean test.
	'''a = backend.remean({
                    "Abstract expressionism": 0.021,
                    "India": 0.024,
                    "Vedas": 0.015,
                    "Hinduism": 0.015,
                    "Vishnu": 0.015,
                    "United States Capitol": 0.018,
                    "List of Deshastha Brahmin surnames": 0.013,
                    "Museum of Modern Art": 0.017,
                    "Bronze": 0.022,
                    "Shiva": 0.013,
                    "List of districts of India": 0.017,
                    "List of districts in India by population": 0.021,
                    "Administrative divisions of India": 0.017,
                    "Smithsonian Institution": 0.031,
                    "Krishna": 0.015,
                    "Western painting": 0.018,
                    "Vaishnavism": 0.015,
                    "United States Department of the Interior": 0.021,
                    "List of railway stations in India": 0.018,
                    "Art Institute of Chicago": 0.02,
                    "History of painting": 0.018,
                    "Mahabharata": 0.013,
                    "List of cities and towns in India": 0.019,
                    "Glossary of Hinduism terms": 0.015,
                    "Rama": 0.014,
                    "National Gallery of Art": 0.022
                })
	print(a)'''

	# Best event finder test.
	# e = backend.getBestConceptModelForID('test@baruchmail.cuny.edu')
	# print(str(e))

	# Exception getter test.
	print(backend.getExceptionsForID('test@baruchmail.cuny.edu'))
	print(backend.addExceptionForID('Test', 'test@baruchmail.cuny.edu'))

if __name__ == "__main__":
    main()