# import sounddevice as sd
# import soundfile as sf

# filename = '/home/pi/Embedded-Capstone/soundFiles/ready.wav'
# # Extract data and sampling rate from file
# data, fs = sf.read(filename, dtype='float32')  
# sd.play(data, fs)
# status = sd.wait()


from pydub import AudioSegment
from pydub.playback import play

def playSound(path) :
	sound = AudioSegment.from_wav(path)
	play(sound)
