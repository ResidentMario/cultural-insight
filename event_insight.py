'''event-insight.py
    Test script for event_insight_lib.py'''

# import argparse
import event_insight_lib
import backend
# import os
# import json
# import pprint

def main():
	# token = event_insight_lib.getToken()
	# backend.saveFile(event_insight_lib.annotateText('The Space Shuttle Pavilion showcases the space shuttle Enterprise, the prototype NASA orbiter that paved the way for America’s successful space shuttle program. Seventeen dynamic exhibit zones feature original artifacts, photographs, audio, and films that immerse visitors in the science and history of Enterprise and the space shuttle era.', token), 'example_output.json')

	a = backend.ConceptModel([], 'test@baruchmail.cuny.edu')
	a.model = ['test', 0.99]
	a.saveModel()
	# print(a.model)

if __name__ == "__main__":
    main()