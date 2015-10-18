'''event-insight.py
    Proof of concept script for the event insight tool. Console-based wrapper for event-insight-lib.py'''

import argparse
import event_insight_lib

def someFunction():
	return 'That\'s neat!'

def main():
	token = event_insight_lib.generateToken()
	ret = event_insight_lib.annotateText("""Family Fridays at MoMath presented by Time Warner Cable: “Math Makes Music”
Friday, October 23, 6:30 pm

Over two thousand years ago, the Pythagoreans discovered relationships between the shapes of vibration of simple strings and the combinations of sound that please our ears and brains.  Since then, mathematicians and scientists have learned a great deal about how sizes, shapes, and nonlinear dynamics of instruments determine their special sounds.  Indeed, modern makers use math(!) as they design and build new instruments.  Participants ages 7 and up are invited to join Dr. Bruce Bayly, a singer and violinist as well as a mathematician, as he shows us the math behind the music.  This presentation is free to attendees, as part of Time Warner Cable’s Connect a Million Minds campaign.  For more information and to register, visit familyfridays.momath.org.
- See more at: http://momath.org/about/upcoming-events/#sthash.4q1gixlM.dpuf""", token)
	print(ret)
	event_insight_lib.saveFile(ret, 'momath_example_output.json')

if __name__ == "__main__":
    main()