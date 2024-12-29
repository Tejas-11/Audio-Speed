import numpy as np
from scipy import fftpack
from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt
from scipy.io import wavfile
import os


def pprint(arr):
	n = arr.size
	print(arr[0], arr[1], arr[2])
	print(arr[n//2-1], arr[n//2], arr[n//2+1])
	print(arr[-3], arr[-2], arr[-1])
	print()


name = 'LJ001-0005.wav'
sr, odata = wavfile.read(name)
speed = 2
overlap = 0
# odata = np.frombuffer(data, dtype=np.int16)
window_length = 1024
step = int(window_length * (100-overlap)/100)
i=0
new_window_length = int(window_length/speed)
new_step = int(step/speed)
new_i = 0
new_data = np.zeros(int(odata.size/speed), dtype=np.int16)  # 
while i<step:
	print(i)
	data = odata[i:i+window_length]
	lee = data.size
	han = np.hanning(lee)  # np.hamming(lee)
	# data = np.multiply(data, han)
	fft_data = fftpack.fft(data)
	freq_values = np.linspace(0, 1023, num=1024)
	interpol = interp1d(freq_values, fft_data)  # , kind='cubic')
	new_freq_values = np.linspace(0, 1022, num=512)
	new_fft_data = interpol(new_freq_values)
	pprint(freq_values)
	pprint(new_freq_values)
	freq_limit = (lee+1)//2
	freq_values = np.linspace(0, freq_limit-1, num=freq_limit)
	interpol = interp1d(freq_values, fft_data[:freq_limit])  # , kind='cubic')
	new_lee = int(lee/speed)
	old_fft_data = np.zeros(new_lee, dtype=np.complex128)
	new_freq_limit = int((freq_limit-1)/speed+1)
	new_freq_values = np.linspace(0, freq_limit-1, num=new_freq_limit)
	old_fft_data[:new_freq_limit] = interpol(new_freq_values)
	for x in range(1,new_freq_limit):
		old_fft_data[new_lee-x] = old_fft_data[x].conjugate()
	pprint(new_freq_values)
	pprint(fft_data)
	pprint(new_fft_data)
	pprint(old_fft_data)
	i+=step
	new_i+=new_step
wavfile.write(f'new_{speed}x_{name}', sr, new_data)
