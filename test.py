import scipy
import scipy.io.wavfile as wav
import timeside
from timeside.core import get_processor
import matplotlib.pyplot as plt

def main():
    decoder = get_processor('file_decoder')(uri="input/piano2.wav")
    spectrogram = get_processor('spectrogram_analyzer')(input_blocksize=2048, input_stepsize=1024)
    pipe = (decoder | spectrogram)
    pipe.run()
    result = spectrogram.results['spectrogram_analyzer']
    result.data.shape
main()
