from pydub import AudioSegment
from pydub.playback import play

def playSound(path) :
	sound = AudioSegment.from_wav(path)
	play(sound)
