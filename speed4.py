import numpy as np
from scipy import fftpack
from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt
from scipy.io import wavfile
import os



def speed():
	name = 'LJ001-0005.wav'
	sr, odata = wavfile.read(name)
	speed = 1.5
	overlap = 0
	# odata = np.frombuffer(data, dtype=np.int16)
	window_length = 1024
	step = int(window_length * (100-overlap)/100)
	i=0
	new_window_length = int(window_length/speed)
	new_step = int(step/speed)
	new_i = 0
	new_data = np.zeros(int(odata.size/speed), dtype=np.int16)
	while i+step<odata.size:
		print(i)
		data = odata[i:i+window_length]
		lee = data.size
		han = np.hanning(lee)  # np.hamming(lee)
		# data = np.multiply(data, han)
		fft_data = fftpack.fft(data)
		freq_limit = (lee-1)//2        # 511
		freq_values = np.linspace(0, lee-1, num=lee)
		interpol = interp1d(freq_values, fft_data)  # , kind='cubic')
		new_lee = int(lee//speed)           # 512
		new_freq_limit = (new_lee-1)//2    # 255
		new_freq_values = np.arange(new_freq_limit+1)*speed+ (1.0+speed)/2 # (speed+1)/2, freq)
		# new_freq_values = np.linspace(0, freq_limit+1, num=new_freq_limit+2)[1:-1]
		new_fft_data = np.zeros(new_lee, dtype=np.complex128)
		new_fft_data[1:new_freq_limit+2] = interpol(new_freq_values)
		new_fft_data[0] = fft_data[0]
		new_fft_data[new_freq_limit+1] = 2 * new_fft_data[new_freq_limit+1].conjugate()  # fft_data[freq_limit+1]
		for x in range(1, new_freq_limit+2):
			new_fft_data[new_lee-x] = new_fft_data[x].conjugate()
		new_data[new_i:new_i+new_window_length] += fftpack.ifft(new_fft_data).real.astype(np.int16)
		if i==0:
			# print(freq_values, new_freq_values)
			# print(fft_data, new_fft_data)
			input()
		i+=step
		new_i+=new_step
	wavfile.write(f'new_{speed}x_{name}', sr, new_data)


speed()
