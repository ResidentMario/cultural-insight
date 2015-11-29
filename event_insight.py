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
	# a.model = backend.fetchConceptsForInstitution('Smithsonian', token)
	# print(a.model)
	# a.saveModel()
	# print(backend.fetchConceptsForInstitution('Smithsonian', token))

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
	# a.model = backend.parseRawCall(backend.fetchConceptsForInstitution('Smithsonian', token))
	# print(a.model)
	# b = backend.ConceptModel([], 'test@baruchmail.cuny.edu')
	# b.model = {'test': 0.98}
	# a = backend.addObjectToConceptModel(a, b)
	# print(a.model)

	# Conceptualization test.
	# print(backend.fetchConceptsForInstitution('Intrepid Museum', token, cutoff=0.2))
	# print(urllib.parse.quote('Intrepid Air & Space Museum'.encode("utf8")))
	# print(urllib.parse.quote('Intrepid Sea, Air & Space Museum'.replace(' ', '_'), safe='_,'))
	# c = ['Smithsonian Institute', 'Intrepid Sea, Air & Space Museum', 'Rubin Museum']
	# r = backend.conceptualize2(c, token)
	# print(r)

	# User definition test.
	# a = backend.addNewUser('test3@baruchmail.cuny.edu', 'Random', ['Smithsonian Institute', 'Rubin Museum'], token)
	# print(a.model)

	# Concept display test.
	concepts = backend.getConceptsByID('test@baruchmail.cuny.edu')
	for concept in concepts:
		print(concept + str(concepts[concept]))

if __name__ == "__main__":
    main()