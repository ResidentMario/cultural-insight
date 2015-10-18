'''event-insight.py
    Proof of concept script for the event insight tool. Console-based wrapper for event-insight-lib.py'''

import argparse
import event_insight_lib

def someFunction():
	return 'That\'s neat!'

def main():
	token = event_insight_lib.generateToken()
	ret = event_insight_lib.annotateText("""The Intrepid Museum’s new exhibition On the Line: Intrepid and the Vietnam War explores the events and impact of the Vietnam War through the lens of Intrepid’s history. The exhibition, which coincides with the 40th anniversary of the conclusion of the war, offers a site-specific immersion into an important chapter of American history.The legendary aircraft carrier Intrepid served three tours of duty in Vietnam between 1966 and 1969. Set within the very spaces where men lived and served, the exhibition focuses on the experiences of Intrepid and its crew “on the line”—the periods when the ship was active in the Gulf of Tonkin, launching aircraft for missions over mainland Vietnam. This localized history serves as the starting point for understanding the larger historical landscape, including the Cold War, Operation Rolling Thunder and protests at home.

The exhibition includes artifacts, photographs and film clips from the Museum’s collection, many of which are on display for the first time. The exhibition also draws from the Museum’s Oral History Project, an initiative launched in 2013 to record and preserve the stories of those who served on Intrepid, offering visitors the chance to hear the experiences of veterans in their own words, and to learn history firsthand.

The exhibition is free with the price of admission.

In conjunction with the exhibition, the Museum is offering education programs for teachers and students, and a series of public programs to generate conversation and artistic expression. Bank of America is generously providing free Museum admission to U.S. active military, retired military and veterans. Proper ID is requested, and tickets may only be obtained at the Museum Box Office.

If you are interested in supporting the exhibition, please click here. All gifts are fully tax-deductible and donors of $250 or more will be acknowledged in the exhibition.""", token)
	# event_insight_lib.saveFile(ret, 'intrepid_example_output.json')
	print(ret)

if __name__ == "__main__":
    main()