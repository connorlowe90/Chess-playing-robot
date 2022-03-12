# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file is for playing the wav files for audio 
# feedback to the user.

from pydub import AudioSegment
from pydub.playback import play

# playSound() is a function that will use
# the parameter 'path' to play the correct
# audio file for user feedback.
def playSound(path) :
	sound = AudioSegment.from_wav(path)
	play(sound)
