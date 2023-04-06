import numpy as np
from gnuradio import gr

class peak_detector(gr.sync_block):
    def __init__(self, sampling_rate=4e6, f_max=2e6, f_min=5e3, fft_size=8192):
        gr.sync_block.__init__(self,
            name="peak_detector",
            in_sig=[(np.float32, fft_size)],
            out_sig=[np.float32])
        self.fft_size = fft_size
        self.sampling_rate = sampling_rate
        self.f_max = f_max
        self.f_min = f_min

        #setting up frequency interval 
        T_samp = 1/self.sampling_rate
        self.f = np.fft.fftfreq(self.fft_size, d=T_samp)
        self.mask = np.logical_or(np.abs(self.f) > f_max, np.abs(self.f) < f_min)


    def work(self, input_items, output_items):
        in0 = input_items[0][0]

        #input data conditions check
        if(len(in0) != self.fft_size):
            raise ValueError('Input vector size does not match fft size')

        # applying fourier transform and lowpass filter
        fft_signal = np.fft.fft(in0)
        fft_signal[self.mask] = 0

        # retrieving frequency peak and set belonging frequency to output
        idx = np.argmax(np.abs(fft_signal))
        if(idx >= len(self.f)):
            idx = len(self.f) - 1
        output_items[0][0] = abs(self.f[idx])

        return len(output_items)

