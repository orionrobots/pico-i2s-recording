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

    wave_writer = create_wave_writer(output_filename, bits_per_sample, sample_rate, 1)

    try:
        mic_samples = bytearray(SAMPLE_BUF_LENGTH)
        mic_samples_mv = memoryview(mic_samples)

        while not stop_event_cb():
            bytes_from_mic = mic.readinto(mic_samples_mv)
            if bytes_from_mic > 0:
                wave_writer(mic_samples_mv[:bytes_from_mic])
    finally:
        print("Cleaning up")
        mic.deinit()
