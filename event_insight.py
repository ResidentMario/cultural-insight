'''event-insight.py
    Test script for event_insight_lib.py'''

import event_insight_lib
import backend

def main():
	# Tokenization and API access test.
	token = event_insight_lib.getToken()
	# backend.saveFile(event_insight_lib.annotateText('The Space Shuttle Pavilion showcases the space shuttle Enterprise, the prototype NASA orbiter that paved the way for America’s successful space shuttle program. Seventeen dynamic exhibit zones feature original artifacts, photographs, audio, and films that immerse visitors in the science and history of Enterprise and the space shuttle era.', token), 'example_output.json')

	# ConceptModel definition and saving test.
	# a = backend.ConceptModel([], 'test@baruchmail.cuny.edu')
	# a.model = {'test': 0.98}
	# a.saveModel()
	# print(a.model)

	# ConceptModel manipulation test.
	# a = backend.ConceptModel(None, 'testA')
	# a.model = {'C': 0.5, 'D': 0.8, 'E': 0.1}
	# b = backend.ConceptModel(None, 'testB')
	# b.model = {'A': 0.4, 'B': 0.7}
	# print(backend.addObjectToConceptModel(a, b))
	# a.model = {'A': 0.0}
	# b.model = {'B': 0.0}
	# print(backend.addObjectToConceptModel(a, b))
	
	# ConceptModel comparison test.
	# a = backend.ConceptModel(None, 'testA')
	# a.model = {'A': 0.5, 'B': 0.8, 'E': 0.1}
	# b = backend.ConceptModel(None, 'testB')
	# b.model = {'A': 0.4, 'B': 0.7, 'D': 0.2}
	# print(backend.compareConceptModels(a,b))

	# print(backend.fetchConceptsForInstitution('Smithsonian', token))
	print(event_insight_lib.fetchRelatedConcepts('Smithsonian Institute', token))

if __name__ == "__main__":
    main()