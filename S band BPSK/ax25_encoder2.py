class AX25Encoder:
    def __init__(self):
        self.bit_stuffing_threshold = 5
        self.flag = "7e"
        self.control_field_ui = "03"  # UI frame control field
        self.fcs_poly = 0x8408  # Polynomial x^16 + x^12 + x^5 + 1

    def crc16(self, data):
        fcs = 0xFFFF
        for byte in data:
            fcs ^= ord(byte) << 8
            for _ in range(8):
                if fcs & 0x8000:
                    fcs = (fcs << 1) ^ self.fcs_poly
                else:
                    fcs <<= 1
                fcs &= 0xFFFF
        return fcs

    def encode_ui_frame(self, source_address, dest_address, protocol_id, info):
        frame = self.text_to_hex(dest_address) + self.text_to_hex(source_address) + self.control_field_ui + protocol_id + self.text_to_hex(info)
        print("Frame", frame)

        # Calculate FCS
        fcs = self.crc16(frame)
        fcs_bytes = bytearray([fcs >> 8, fcs & 0xFF])

        # Construct the complete frame
        complete_frame = self.flag + frame + fcs_bytes.hex() + self.flag
        print("Complete Frame", complete_frame)

        print("---Flag", self.flag, "\n---Dest", dest_address, "\n---Src ", source_address, "\n---Ctrl", self.control_field_ui, "\n---Prot", protocol_id, "\n---Data", info, "\n---FCS ", fcs_bytes.hex(), "\n---Flag", self.flag)

        binary_string = self.hex_to_binary(complete_frame)
        print("Binary String", binary_string)

        nrzified = self.nrzi(binary_string)
        stuffed = self.bit_stuff(nrzified)

        return stuffed

    def bit_stuff(self, data):
        stuffed_data = ""
        count = 0
        for bit in data:
            if bit == "1":
                count += 1
                if count == self.bit_stuffing_threshold:
                    stuffed_data += "0"
                    count = 0
            else:
                count = 0
            stuffed_data += bit
        return stuffed_data

    def hex_to_binary(self, hex_string):
        binary_string = ""
        for char in hex_string:
            if char != ' ':
                # Convert each hexadecimal digit to its binary representation
                binary = bin(int(char, 16))[2:].zfill(4)
                binary_string += binary
        return binary_string

    def text_to_hex(self, text):
        hex_string = ""
        for char in text:
            # Convert each character to its ASCII code and then to hexadecimal representation
            hex_char = hex(ord(char))[2:].upper()
            hex_string += hex_char + " "
        # Remove the trailing space at the end
        hex_string = hex_string.strip()
        return hex_string

    def nrzi(self, data):
        nrzified = ""
        current = ""

        for bit in data:
            if current == "":
                current = bit
            elif bit == "1":
                if current == "1":
                    current = "0"
                elif current == "0":
                    current = "1"

            nrzified += current

        return nrzified


encoder = AX25Encoder()

# Example usage
source_address = "aaaaaa"
dest_address = "bbbbbb"
protocol_id = "f0"
info = "abcd"

encoded_ui_frame = encoder.encode_ui_frame(source_address, dest_address, protocol_id, info)
print("Encoded UI frame:", encoded_ui_frame)