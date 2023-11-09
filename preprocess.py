from pydub import AudioSegment
from scipy.fftpack import rfft, rfftfreq
import numpy as np
import matplotlib.pyplot as plt

def preprocess(filepath, filename):
    song = AudioSegment.from_mp3(filepath + filename)

    # find loudest 20 sec of song
    # use a search window 0.5 sec wide
    loudest = song[0:20000]
    loudest_dBFS = loudest.dBFS

    for i in range(0, len(song) - 20000, 500):
        if song[i:i+20000].dBFS > loudest_dBFS:
            loudest = song[i:i+20000]
            loudest_dBFS = loudest.dBFS

    # convert to mono
    loudest = loudest.set_channels(1)

    # get samples
    samples = loudest.get_array_of_samples()
    one_second = len(samples) // 20 # should be 44100
    quarter_second = one_second // 4

    # split the song into quarter second chunks and get the fourier transform of each chunk
    all_bins = []
    for chunk in range(20):
        yf = rfft(samples[chunk*quarter_second:(chunk+1)*quarter_second])
        xf = rfftfreq(quarter_second, 1/44100)
        
        # get the average amplitude in each bin
        freq_bins = [(0,80), (80, 120), (120, 300), (300, 1000), (1000, 2000), (2000, 5000), (5000, 10000), (10000, 20000)]
        bins = []
        for i in range(8):
            bins.append(np.mean(np.abs(yf[(xf >= freq_bins[i][0]) & (xf < freq_bins[i][1])])))
        bins = np.array(bins)
        all_bins.append(bins)
    print(f"Finished preprocessing for song: {filename}")

    # save the numpy array
    processed_filepath = filepath + "processed/" + filename[:-4]
    np.save(processed_filepath, np.array(all_bins))
    return processed_filepath

def preprocess_in_mem(filepath, filename):
    song = AudioSegment.from_mp3(filepath + filename)

    # find loudest 20 sec of song
    # use a search window 0.5 sec wide
    loudest = song[0:20000]
    loudest_dBFS = loudest.dBFS

    for i in range(0, len(song) - 20000, 500):
        if song[i:i+20000].dBFS > loudest_dBFS:
            loudest = song[i:i+20000]
            loudest_dBFS = loudest.dBFS

    # convert to mono
    loudest = loudest.set_channels(1)

    # get samples
    samples = loudest.get_array_of_samples()
    one_second = len(samples) // 20 # should be 44100
    quarter_second = one_second // 4

    # split the song into quarter second chunks and get the fourier transform of each chunk
    all_bins = []
    for chunk in range(20):
        yf = rfft(samples[chunk*quarter_second:(chunk+1)*quarter_second])
        xf = rfftfreq(quarter_second, 1/44100)
        
        # get the average amplitude in each bin
        freq_bins = [(0,80), (80, 120), (120, 300), (300, 1000), (1000, 2000), (2000, 5000), (5000, 10000), (10000, 20000)]
        bins = []
        for i in range(8):
            bins.append(np.mean(np.abs(yf[(xf >= freq_bins[i][0]) & (xf < freq_bins[i][1])])))
        bins = np.array(bins)
        all_bins.append(bins)
    print(f"Finished preprocessing for song: {filename}")
    
    all_bins = np.array(all_bins)
    return all_bins

if __name__ == "__main__":
    test_song = "new4DemoV5.mp3"
    bins = preprocess(test_song)

    # plot bins
    plt.plot(bins[2])
    plt.show()