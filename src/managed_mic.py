#audio mic record
from machine import Pin, I2S
import wave_file


def record_from_mic_until(
        output_filename,
        stop_event_cb,
        sck_pin_number=18,
        ws_pin_number=19,
        sd_pin_number=20,
        bits_per_sample=32,
        sample_rate=22_050,
        ):
    """
    output_filename - wave file to output to. will overwrite
    stop_event_cb - function returning false until recording should stop
    """
    I2S_INTERNAL_BUF_LENGTH = 40000
    SAMPLE_BUF_LENGTH = 10000

    wave_header = wave_file.WaveFileHeader()
    wave_header.bits_per_sample = bits_per_sample
    wave_header.sample_rate = sample_rate
    wave_header.channels = 1
    mic = I2S(1,
                sck=Pin(sck_pin_number),
                ws=Pin(ws_pin_number),
                sd=Pin(sd_pin_number),
                mode=I2S.RX,
                format=I2S.MONO,
                bits=wave_header.bits_per_sample,
                rate=wave_header.sample_rate,
                ibuf=I2S_INTERNAL_BUF_LENGTH,
            )
    output_file = None
    try:
        output_file = open(output_filename, "wb")
        print("File open, writing header")
        # write the dummy header
        output_file.write(wave_header.to_bytes())
        audio_bytes_written = 0

        mic_samples = bytearray(SAMPLE_BUF_LENGTH)
        mic_samples_mv = memoryview(mic_samples)

        last_buf_position = 0
        while not stop_event_cb():
            bytes_from_mic = mic.readinto(mic_samples_mv)
            if bytes_from_mic > 0:
                bytes_written = output_file.write(mic_samples_mv[:bytes_from_mic])
                audio_bytes_written += bytes_written
        # update header
        print("Recording complete. Finalising header")
        output_file.seek(0)
        wave_header.data_size = audio_bytes_written
        _  = output_file.write(wave_header.to_bytes())

    finally:
        print("Cleaning up")
        if output_file:
            output_file.close()
        mic.deinit()
