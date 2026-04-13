import struct

class WaveFileHeader:
    @staticmethod
    def from_file(file_source):
        ident = file_source.read(4)
        if ident != b"RIFF":
            raise ValueError(f"Expected RIFF header, got {ident}.")
        file_size = struct.unpack("I",
            file_source.read(4))
        file_type = file_source.read(8)
        if file_type[:7] != b"WAVEfmt":
            raise ValueError(f"Not WAVE type. Got {file_type}")
        fmt = "IHHIIHHHI"
        fmt_size, wave_fmt, channels, sample_rate, byte_rate, block_align, bits_per_sample, extra, data_size = struct.unpack(fmt,
            file_source.read(struct.calcsize(fmt)))

        header = WaveFileHeader()
        header.wave_fmt = wave_fmt
        header.channels = channels
        header.sample_rate = sample_rate
        byte_rate = byte_rate
        block_align = block_align
        header.bits_per_sample = bits_per_sample
        header.data_size = data_size
        return header

    def __init__(self):
        self.data_size = 0xFFFF
        self.wave_fmt = 1 # PCM
        self.channels = 1
        self.sample_rate = 22_050
        self.bits_per_sample = 16

    @property
    def byte_rate(self):
        return self.sample_rate * self.channels * self.bits_per_sample // 8

    @property
    def block_align(self):
        return self.channels * self.bits_per_sample // 8

    def to_bytes(self):
        data = bytes(b"RIFF") # riff header
        data += (self.data_size + 36).to_bytes(4, "little") # 32, unsigned, excluding size and riff
        data += bytes(b"WAVE") # file type
        data += bytes(b"fmt ")  # format chunk
        data += (16).to_bytes(4, "little") # length of format data above
        data += self.wave_fmt.to_bytes(2, "little")
        data += self.channels.to_bytes(2, "little")
        data += self.sample_rate.to_bytes(4, "little")
        data += self.byte_rate.to_bytes(4, "little")
        data += self.block_align.to_bytes(2, "little")
        data += self.bits_per_sample.to_bytes(2, "little")
        data += bytes(b"data")
        data += self.data_size.to_bytes(4, "little")
        return data

@contextmanager
def create_wave_writer(output_filename, bits_per_sample, sample_rate, channels):
    """Create a wav output stream.
    """
    wave_header = wave_file.WaveFileHeader()
    wave_header.bits_per_sample = bits_per_sample
    wave_header.sample_rate = sample_rate
    wave_header.channels = 1

    output_file = None
    try:
        output_file = open(output_filename, "wb")

        print("File open, writing header")
        # write the dummy header
        output_file.write(wave_header.to_bytes())
        audio_bytes_written = 0

        def write_function(bytes_to_write):
            bytes_written = output_file.write(bytes_to_write)
            audio_bytes_written += bytes_written

        try:
            yield write_function
        finally:
            # update header
            print("Recording complete. Finalising header")
            output_file.seek(0)
            wave_header.data_size = audio_bytes_written
            _  = output_file.write(wave_header.to_bytes())
    finally:
        if output_file:
            output_file.close()
