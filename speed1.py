import numpy as np
from scipy import fftpack
from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt
from scipy.io import wavfile


name = 'LJ001-0005.wav'
sr, odata = wavfile.read(name)
speed = 2
overlap = 50
# odata = np.frombuffer(data, dtype=np.int16)
window_length = 1024  # int(sr*0.05)
step = int(window_length * (100-overlap)/100)
i=0
new_data = np.zeros(odata.size, dtype=np.int16)
while i<odata.size:
    data = odata[i:i+window_length]
    lee = data.size
    print(window_length, lee)
    han = np.hanning(lee)
    data = np.multiply(data, han)
    fft_data = fftpack.fft(data)
    freq_limit = (lee+1)//2
    freq_values = np.linspace(0, freq_limit-1, num=freq_limit)
    # interpolating fft to new frequency range
    interpol = interp1d(freq_values, fft_data[:freq_limit], kind='cubic')
    new_fft_data = np.zeros(lee, dtype=np.complex128)
    new_freq_limit = int((freq_limit-1)/speed+1)
    new_freq_values = np.linspace(0, freq_limit-1, num=new_freq_limit)
    new_freq_values = new_freq_values[:freq_limit]
    new_freq_limit = min(freq_limit, new_freq_limit)
    new_fft_data[:new_freq_limit] = interpol(new_freq_values)
    for x in range(1,new_freq_limit):
        new_fft_data[lee-x] = new_fft_data[x].conjugate()
    new_data[i:i+window_length] += fftpack.ifft(new_fft_data).astype(np.int16)
    # xax = np.arange(lee)
    # xax = np.linspace(0.0, sr//2, num=lee//2)
    # fig1, ax1=plt.subplots()
    # ax1=plt.plot(xax, odata[i:i+window_length])
    # ax1=plt.plot(xax, 2/lee * np.abs(fft_data[:(lee+1)//2]))
    # fig2, ax2=plt.subplots()
    # ax2=plt.plot(xax, new_data[i:i+window_length])
    # ax2=plt.plot(xax, 2/lee * np.abs(new_fft_data[:(lee+1)//2]))
    # plt.show()
    i+=step
wavfile.write(f'{speed}x_{name}', sr*speed, new_data)
# with open(f'{speed}x_beam.raw', 'wb') as f:
#    f.write(new_data.tobytes())
