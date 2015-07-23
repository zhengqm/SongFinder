from scipy.io import wavfile
from scipy.fftpack import fft
from sys import argv
from collections import Counter
import glob
import pickle

class SFEngine():
    """SongFinder Engine"""
    def __init__(self):
        self.freq_dict = {}

    def index(self, folder):
        for song in glob.glob(folder + "/*.wav"):
            try:
                self.sample(song, 0, 0, self.store_feature)
            except:
                print "Error in processing: " + song

    def search(self, target):
        target_tuple = []
        if not target.endswith(".wav"):
            print "Only wav file is supported"

        def callback(filename, start, feature):
            for freq in feature:
                if freq not in self.freq_dict:
                    continue
                for (origianl_filename, origianl_time) in self.freq_dict[freq]:
                    target_tuple.append((origianl_filename, (origianl_time - int(start)) / 44100))

        self.sample(target, 0, 0, callback)
        counter = Counter(target_tuple)
        for pair, count in counter.most_common(5):
            print pair[0].split(".")[0], pair[1]#, count

    def save(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self.freq_dict, handle)

    def load(self, filename):
        with open(filename, 'rb') as handle:
            self.freq_dict = pickle.load(handle)

    def extract_feature(self, scaled, start, interval):
        end = start + interval
        dst = fft(scaled[start: end]) 
        length = len(dst)/2  
        normalized = abs(dst[:(length-1)])
        feature = [ normalized[:50].argmax(), \
                    50 +  normalized[50:100].argmax(), \
                    100 + normalized[100:200].argmax(), \
                    200 + normalized[200:300].argmax(), \
                    300 + normalized[300:400].argmax(), \
                    400 + normalized[400:].argmax()]
        return feature

    def read_and_scale(self, filename):
        rate, data = wavfile.read(filename) # load the data
        bits = data.dtype.itemsize * 8
        if data.ndim == 2:
            data = data.T[0] # this is a two channel soundtrack, I get the first track
        scaled = data / (2. ** (bits - 1)) 
        return scaled

    def store_feature(self, filename, start, feature):
        for freq in feature:
            if freq not in self.freq_dict:
                self.freq_dict[freq] = []

            self.freq_dict[freq].append((filename, start))


    def sample(self, filename, start_second, duration = 5, callback = None):
        
        start = start_second * 44100
        if duration == 0:
            end = 1e15
        else:
            end = start + 44100 * duration
        interval = 8192
        scaled = self.read_and_scale(filename)
        length = scaled.size
        while start < min(length, end):
            feature = self.extract_feature(scaled, start, interval)
            if callback != None:
                callback(filename, start, feature)
            start += interval

        