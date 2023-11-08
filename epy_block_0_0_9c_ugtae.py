"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import socket


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, ip="127.0.0.1", port="9999"):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Socket Python Block',  # will show up in GRC
            in_sig=None,
            out_sig=[np.byte]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.ip = ip
        self.port = port
        self.b = False
        self.my_socket = socket.socket()

    def work(self, input_items, output_items):
        if not self.b:
            self.my_socket.connect(("127.0.0.1", 9999))
            self.b = True
        
        msg = self.my_socket.recv(1)

        output_items[0][:] = msg
        return len(output_items[0])
