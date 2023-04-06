import numpy as np
from gnuradio import gr

class range_calc(gr.sync_block):
    def __init__(self, bandwidth=2e6, chirp_period=200e-6):
        gr.sync_block.__init__(self,
            name="range_calc",
            in_sig=[np.float32],
            out_sig=[np.float32])
        self.bandwidth = bandwidth
        self.chirp_period = chirp_period
        self.speed_of_light = 300000000


    def work(self, input_items, output_items):
        in0 = input_items[0]
	
	# calculating range
        output_items[0][:] = ( in0[:]*self.speed_of_light*self.chirp_period ) / (2*self.bandwidth) 

        return len(output_items[0])
