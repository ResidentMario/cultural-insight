"""
curator.py
This administrative script is used in the command line for defining the events that make up this application's event library.
It is designed for use by a master "content curator".
"""

# Redistributables.
import click
import json
from time import strptime

# My own libraries.
import backend

@click.command()
@click.option('--event', prompt='What is the name of the event?', help='Number of greetings.')
@click.option('--description', prompt='How is the event described?', help='Description of the event.')
@click.option('--url', prompt='Do you have a link with more information?', help='Link to more information on the event.')
@click.option('--starttime', prompt='What time does it start? Format: e.g. 2016-06-13 22:00. All times military and EST.',
		help='The start time for the event.')
@click.option('--endtime', prompt='What time does it end? Format: e.g. 2016-06-13 22:00. All times military and EST.',
		help='The end time for the event.')
def script(event, description, starttime, endtime):
	"""Runtime Click script."""
	concepts = backend.fetchConceptsForEvent(description, backend.getToken())
	if starttime != ' ':
		_starttime = strptime(starttime, "%Y-%m-%d %H:%M")
	else:
		_starttime = ''
	if endtime != ' ':
		_endtime = strptime(endtime, "%Y-%m-%d %H:%M")
	else:
		_endtime = ''
	saveEvent(event, description, _url, _starttime, _endtime, concepts)
	# for concept in concepts.keys():
	#	click.echo('%s' % concept)
	click.echo('Event added to the database!')

def saveEvent(event, description, url, starttime, endtime, concepts, filename='events.json'):
	"""Saves an event. Used by the `curator.script()` execution command."""
	fp = json.load(open(filename))
	fp['events'].append({
		'name': event,
		'description': description,
		'url': url,
		'starttime': starttime,
		'endtime': endtime,
		'model': {'concepts': concepts}
	})
	backend.saveFile(fp, filename)

if __name__ == '__main__':
    script()