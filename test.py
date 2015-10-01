from pyAudioAnalysis import audioFeatureExtraction
from pyAudioAnalysis import audioBasicIO
import scipy.io.wavfile

def main():
    [Fs, x] = audioBasicIO.readAudioFile("input/piano2.wav"); 
    F = audioFeatureExtraction.stFeatureExtraction(x, Fs, Fs, Fs)
    print(F)

main()
