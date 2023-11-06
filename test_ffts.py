from pydub import AudioSegment

test_song = "new4DemoV5.mp3"
song = AudioSegment.from_mp3(test_song)

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

# get FFT of first second
from scipy.fftpack import rfft, rfftfreq
import numpy as np
quarter_second = one_second // 4
yf = rfft(samples[:quarter_second])
xf = rfftfreq(quarter_second, 1/44100)

# plot FFT with log scaling for x axis
import matplotlib.pyplot as plt
# plt.plot(xf, np.abs(yf))
# plt.xscale('symlog')
# plt.show()

# combine bins into 8 bins with the following frequencies
[(0,80), (80, 120), (120, 300), (300, 1000), (1000, 2000), (2000, 5000), (5000, 10000), (10000, 20000)]
# and find the average amplitude in each bin
bins = []
for i in range(8):
    bins.append(np.mean(np.abs(yf[(xf >= 80 * 2**i) & (xf < 80 * 2**(i+1))])))
bins = np.array(bins)

print(bins.shape)

# plot bins
plt.plot(bins)
plt.show()