from pydub import AudioSegment
from scipy.fftpack import rfft, rfftfreq
import numpy as np
import matplotlib.pyplot as plt
import database
import multiprocessing as mp

def rfft_and_bins(audio_segment):
    # find loudest 60 sec of song
    # use a search window 0.5 sec wide
    duration = 60000 # 60 sec
    loudest = audio_segment[0:duration]
    loudest_dBFS = loudest.dBFS

    for i in range(0, len(audio_segment) - duration, 500):
        if audio_segment[i:i+duration].dBFS > loudest_dBFS:
            loudest = audio_segment[i:i+duration]
            loudest_dBFS = loudest.dBFS

    # convert to mono
    loudest = loudest.set_channels(1)

    # get samples
    samples = loudest.get_array_of_samples()
    one_second = len(samples) // (duration//1000) # should be 44100
    quarter_second = one_second // 4

    # split the song into quarter second chunks and get the fourier transform of each chunk
    all_bins = []
    for chunk in range(duration//250):
        yf = rfft(samples[chunk*quarter_second:(chunk+1)*quarter_second])
        xf = rfftfreq(quarter_second, 1/44100)
        
        # get the average amplitude in each bin
        freq_bins = [(0,80), (80, 120), (120, 300), (300, 500), (500, 900), (900, 1500), (1500, 2500), (2500, 5000), (5000, 10000), (10000, 20000)]
        bins = []
        for i in range(len(freq_bins)):
            bins.append(np.mean(np.abs(yf[(xf >= freq_bins[i][0]) & (xf < freq_bins[i][1])])))
        bins = np.array(bins)
        all_bins.append(bins)

    return all_bins

def rfft_and_bins_diff(audio_segment):
    # find loudest 60 sec of song
    # use a search window 0.5 sec wide
    duration = 60000 # 60 sec
    loudest = audio_segment[0:duration]
    loudest_dBFS = loudest.dBFS

    for i in range(0, len(audio_segment) - duration, 500):
        if audio_segment[i:i+duration].dBFS > loudest_dBFS:
            loudest = audio_segment[i:i+duration]
            loudest_dBFS = loudest.dBFS

    # convert to mono
    loudest = loudest.set_channels(1)

    # get samples
    samples = loudest.get_array_of_samples()
    one_second = len(samples) // (duration//1000) # should be 44100
    quarter_second = one_second // 4

    chunk_sizes = [one_second//500, one_second//100, one_second//50, one_second//10,
                    one_second//4, one_second//2, one_second, one_second*2, one_second*4, one_second*10, duration]

    freq_bins = [(0,80), (80, 120), (120, 300), (300, 500), (500, 900), (900, 1500), (1500, 2500), (2500, 5000), (5000, 10000), (10000, 20000)]

    # np.seterr('raise')

    # split the song into chunks based on chunk size, and for each chunk size
    # get the average difference between the fourier transfor of all the chunks for each frequency bin
    diffs = []
    for chunk_size in chunk_sizes:
        num_chunks = len(samples) // chunk_size
        all_bins = []
        for chunk in range(num_chunks):
            yf = rfft(samples[chunk*chunk_size:(chunk+1)*chunk_size])
            xf = rfftfreq(chunk_size, 1/44100)
            
            # get the average amplitude in each bin
            bins = []
            for i in range(len(freq_bins)):
                # when the chunk size is too small, there are not enough samples to get a good average
                if one_second//chunk_size > freq_bins[i][1]:
                    bins.append(0)
                else:
                    val = np.mean(np.abs(yf[(xf >= freq_bins[i][0]) & (xf < freq_bins[i][1])]))
                    if np.isnan(val):
                        val = 0
                    bins.append(val)
            bins = np.array(bins)
            all_bins.append(bins)
        all_bins = np.array(all_bins)
        diffs.append(np.mean(np.diff(all_bins), axis=0))

    return diffs

def preprocess_0(filepath, filename):
    song = AudioSegment.from_mp3(filepath + filename)

    all_bins = rfft_and_bins(song)
    
    print(f"Finished preprocessing for song: {filename}")

    # save the numpy array
    processed_filepath = filepath + "processed/" + filename[:-4]
    np.save(processed_filepath, np.array(all_bins))
    return processed_filepath

def preprocess_1(filepath, filename):
    song = AudioSegment.from_mp3(filepath + filename)

    all_bins = rfft_and_bins_diff(song)
    
    print(f"Finished preprocessing for song: {filename}")

    # save the numpy array
    processed_filepath = filepath + "processed1/" + filename[:-4]
    np.save(processed_filepath, np.array(all_bins))

    # add the path to the database
    db = database.Database()
    db.add_preprocessed_file(filename[:-4], processed_filepath)
    return processed_filepath

def preprocess_in_mem(filepath, filename, function):
    song = AudioSegment.from_mp3(filepath + filename)

    all_bins = function(song)
    
    all_bins = np.array(all_bins)
    return all_bins

def redo_preprocessing(function):
    db = database.Database()

    # get all songs from database
    cur = db.dbh.cursor()
    cur.execute("SELECT * FROM all_songs")
    records = cur.fetchall()
    cur.close()

    args = []
    for record in records:
        args.append((record[3][:-(len(record[5])+4)], record[5]+".mp3"))

    # use multiprocessing pool to preprocess all songs
    with mp.Pool(20) as pool:
        pool.starmap(function, args)

def add_new_preprocessing(function):
    db = database.Database()

    # get all songs from database
    cur = db.dbh.cursor()
    cur.execute("SELECT * FROM all_songs")
    records = cur.fetchall()
    cur.close()

    args = []
    for record in records:
        args.append((record[3][:-(len(record[5])+4)], record[5]+".mp3"))

    # use multiprocessing pool to preprocess all songs
    with mp.Pool(20) as pool:
        pool.starmap(function, args)

if __name__ == "__main__":
    # test_song = "new4DemoV5.mp3"
    # bins = preprocess(test_song)

    # # plot bins
    # plt.plot(bins[2])
    # plt.show()
    # redo_preprocessing()

    redo_preprocessing(preprocess_1)