from scipy.signal import butter, filtfilt
import numpy as np

# Low-Pass Butterworth Filter
def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs  
    normal_cutoff = cutoff / nyquist 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

# Function to count steps based on peaks in 'az'
def count_peaks(series, height):
    peaks, _ = find_peaks(series, height=height)  
    return len(peaks)
