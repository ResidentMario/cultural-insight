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
from event import Event

@click.command()
@click.option('--name', prompt='What is the name of the event?', help='Succint name for the event.')
@click.option('--description', prompt='How is the event described?', help='Description of the event.')
@click.option('--location', prompt='Where is the event being held?', help='Location where the event is being held.')
@click.option('--url', prompt='Do you have a link with more information?', help='Link to more information on the event.')
@click.option('--starttime', prompt='What time does it start? Format: e.g. 2016-06-13 22:00. All times military and EST.',
		help='The start time for the event.')
@click.option('--endtime', prompt='What time does it end? Format: e.g. 2016-06-13 22:00. All times military and EST.',
		help='The end time for the event.')
@click.option('--picture', prompt='Do you have a link to a picture of the event?', help='Picture of the event, if possible.')
def script(name, description, location, url, starttime, endtime, picture):
	"""Runtime Click script."""
	event = Event(description=description, name=name)
	event.location = location
	event.url = url
	event.starttime = starttime
	if starttime != ' ':
		event.starttime = strptime(starttime, "%Y-%m-%d %H:%M")
	else:
		event.starttime = ''
	if endtime != ' ':
		event.endtime = strptime(endtime, "%Y-%m-%d %H:%M")
	else:
		event.endtime = ''
	event.saveEvent()
	click.echo('Event added to the database!')

def saveEvent2(event, description, url, starttime, endtime, concepts, filename='events.json'):
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