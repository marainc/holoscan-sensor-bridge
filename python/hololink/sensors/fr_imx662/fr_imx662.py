"""
SPDX-FileCopyrightText: Copyright (c) 2025 FRAMOS
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import time
from collections import OrderedDict

import hololink as hololink_module

from . import imx662_mode, li_i2c_expander, li_gpio_expander

# Camera I2C address.
CAM_I2C_ADDRESS = 0x1a

IMX662_MIN_FRAME_LENGTH_DELTA = 70
IMX662_MIN_SHR0_LENGTH = 4
IMX662_MIN_INTEGRATION_LINES = 1
IMX662_GAIN_MIN = 0
IMX662_GAIN_MAX = 240
IMX662_MAX_BLACK_LEVEL_10BPP = 1023
IMX662_MAX_BLACK_LEVEL_12BPP = 4095
IMX662_DEFAULT_BLACK_LEVEL_10BPP = 50
IMX662_DEFAULT_BLACK_LEVEL_12BPP = 200

class Imx662Cam:
    def __init__(
        self,
        hololink_channel,
        i2c_controller_address=hololink_module.CAM_I2C_BUS,
        expander_configuration=0,
    ):
        self._hololink = hololink_channel.hololink()
        self._i2c = self._hololink.get_i2c(i2c_controller_address)
        self._mode = imx662_mode.imx662_Mode.Unknown
        self._min_frame_length_delta = IMX662_MIN_FRAME_LENGTH_DELTA
        # Configure i2c expander
        self._i2c_expander = li_i2c_expander.LII2CExpander(
            self._hololink, i2c_controller_address
        )
        if expander_configuration == 1:
            self._i2c_expander_configuration = (
                li_i2c_expander.I2C_Expander_Output_EN.OUTPUT_3
            )
        else:
            self._i2c_expander_configuration = (
                li_i2c_expander.I2C_Expander_Output_EN.OUTPUT_1
            )
        self._gpio_expander = li_gpio_expander.LIGPIOExpander(
            self._hololink, i2c_controller_address
        )

    #configure reset pin on gpio expander
    def configure_gpio_expander(self):
        logging.info("Configure GPIO expander")
        self._i2c_expander.configure(self._i2c_expander_configuration.value)
        self._gpio_expander.set_direction_gpio(li_gpio_expander.GPIO_Expander_pin.CAM_RST, "OUTPUT")
        self._gpio_expander.set_output_gpio(li_gpio_expander.GPIO_Expander_pin.CAM_RST, 0)
        self._gpio_expander.set_output_gpio(li_gpio_expander.GPIO_Expander_pin.CAM_RST, 1)

    def configure(self, imx662_mode_set):
        self.configure_gpio_expander()

        logging.info("Configure_camera wait for regulator stabilisation")
        time.sleep(0.04)

        # configure the camera based on the selected mode
        self.configure_camera(imx662_mode_set)

    def start(self):
        """Start Streaming"""
        self._running = True
        # Setting these register is time-consuming.
        for reg, val in imx662_mode.imx662_start:
            if reg == imx662_mode.IMX662_TABLE_WAIT_MS:
                time.sleep(val / 1000)  # the val is in ms
            else:
                self.set_register(reg, val)

        time.sleep(0.03)

    def stop(self):
        """Stop Streaming"""
        for reg, val in imx662_mode.imx662_stop:
            if reg == imx662_mode.IMX662_TABLE_WAIT_MS:
                time.sleep(val / 1000)
            else:
                self.set_register(reg, val)
        # Let the egress buffer drain.
        self._gpio_expander.set_output_gpio(li_gpio_expander.GPIO_Expander_pin.CAM_RST, 0)
        time.sleep(0.1)
        self._running = False

    def get_register(self, register):
        logging.debug("get_register(register=%d(0x%X))" % (register, register))
        self._i2c_expander.configure(self._i2c_expander_configuration.value)
        write_bytes = bytearray(100)
        serializer = hololink_module.Serializer(write_bytes)
        serializer.append_uint16_be(register)
        read_byte_count = 1
        reply = self._i2c.i2c_transaction(
            CAM_I2C_ADDRESS, write_bytes[: serializer.length()], read_byte_count
        )
        deserializer = hololink_module.Deserializer(reply)
        r = deserializer.next_uint8()
        logging.debug(
            "get_register(register=%d(0x%X))=%d(0x%X)" % (register, register, r, r)
        )
        return r

    def set_register(self, register, value, timeout=None):
        logging.debug(
            "set_register(register=%d(0x%X), value=%d(0x%X))"
            % (register, register, value, value)
        )
        self._i2c_expander.configure(self._i2c_expander_configuration.value)
        write_bytes = bytearray(100)
        serializer = hololink_module.Serializer(write_bytes)
        serializer.append_uint16_be(register)
        serializer.append_uint8(value)
        read_byte_count = 0
        self._i2c.i2c_transaction(
            CAM_I2C_ADDRESS,
            write_bytes[: serializer.length()],
            read_byte_count,
            timeout=timeout,
        )

    def configure_camera(self, imx662_mode_set):
        self.set_mode(imx662_mode_set)

        mode_list = OrderedDict()

        mode_list = imx662_mode.imx662_init_settings

        if (
            imx662_mode_set.value
            == imx662_mode.imx662_Mode.imx662_mode_1920x1080_12BPP.value
        ):
            mode_list += imx662_mode.imx662_mode_1920x1080_12BPP
        elif (
            imx662_mode_set.value
            == imx662_mode.imx662_Mode.imx662_mode_1920x1080_10BPP.value
        ):
            mode_list += imx662_mode.imx662_mode_1920x1080_10BPP
        elif (
            imx662_mode_set.value
            == imx662_mode.imx662_Mode.imx662_mode_1280x720_12BPP.value
        ):
            mode_list += imx662_mode.imx662_mode_1280x720_12BPP
        elif (
            imx662_mode_set.value
            == imx662_mode.imx662_Mode.imx662_mode_1280x720_10BPP.value
        ):
            mode_list += imx662_mode.imx662_mode_1280x720_10BPP
        else:
            logging.error(f"{imx662_mode_set} mode is not present.")

        for reg, val in mode_list:
            if reg == imx662_mode.IMX662_TABLE_WAIT_MS:
                time.sleep(val / 1000)  # the val is in ms
            else:
                self.set_register(reg, val)

    def set_frame_rate(self, value):
        min_frame_length = self._height + self._min_frame_length_delta

        hmax_low = self.get_register(imx662_mode.HMAX_LOW)
        hmax_high = self.get_register(imx662_mode.HMAX_HIGH)
        hmax = (hmax_high << 8) | (hmax_low & 0xFF)
        logging.debug(f"HMAX value = {hmax}")
        
        line_time = hmax / 74250000
        logging.debug(f"Line time = {line_time}")

        max_frame_rate = 1 / (min_frame_length * line_time)
        logging.debug(f"Max frame rate = {max_frame_rate}")

        if(value > max_frame_rate):
            logging.warn(f"Frame rate value {value} is higher than the max {max_frame_rate}")
            value = max_frame_rate

        frame_length = int(1 / (value * line_time))

        if(frame_length % 2):
            frame_length = frame_length + 1
        logging.debug(f"Frame_length(VMAX) = {frame_length}")

        self._min_frame_length_delta = frame_length - self._height
        logging.debug(f"self._min_frame_length_delta = {self._min_frame_length_delta}")

        self.set_register(imx662_mode.VMAX_HIGH, (frame_length >> 16) & 0xFF)
        self.set_register(imx662_mode.VMAX_MID, (frame_length >> 8) & 0xFF)
        self.set_register(imx662_mode.VMAX_LOW, frame_length & 0xFF)
        time.sleep(imx662_mode.IMX662_WAIT_MS / 1000)

    def set_exposure_reg(self, value=0x04):
        exposure_max = self._height + self._min_frame_length_delta - IMX662_MIN_INTEGRATION_LINES

        if value < IMX662_MIN_SHR0_LENGTH:
            logging.warn(f"Exposure value {value} is lower than the minimum {IMX662_MIN_SHR0_LENGTH}")
            value = IMX662_MIN_SHR0_LENGTH

        if value > exposure_max:
            logging.warn(f"Exposure value {value} is higher than the maximum {exposure_max}")
            value = exposure_max

        self.set_register(imx662_mode.SHR0_HIGH, (value >> 16) & 0xFF)
        self.set_register(imx662_mode.SHR0_MID, (value >> 8) & 0xFF)
        self.set_register(imx662_mode.SHR0_LOW, value & 0xFF)
        time.sleep(imx662_mode.IMX662_WAIT_MS / 1000)

    def set_gain_reg(self, value=0x0):
        if value < IMX662_GAIN_MIN:
            logging.warn(f"Gain value {value} is lower than the minimum {IMX662_GAIN_MIN}")
            value = IMX662_GAIN_MIN

        if value > IMX662_GAIN_MAX:
            logging.warn(f"Gain value {value} is higher than the maximum {IMX662_GAIN_MAX}")
            value = IMX662_GAIN_MAX

        self.set_register(imx662_mode.GAIN_HIGH, (value >> 8) & 0xFF)
        self.set_register(imx662_mode.GAIN_LOW, value & 0xFF)
        time.sleep(imx662_mode.IMX662_WAIT_MS / 1000)

    def set_black_level(self, value):
        if self._pixel_format == hololink_module.sensors.csi.PixelFormat.RAW_12:
            if value > IMX662_MAX_BLACK_LEVEL_12BPP:
                logging.warn(f"Black level value {value} is higher than the maximum {IMX662_MAX_BLACK_LEVEL_12BPP}")
                value = IMX662_MAX_BLACK_LEVEL_12BPP
            value = value >> 2
        elif self._pixel_format == hololink_module.sensors.csi.PixelFormat.RAW_10:
            if value > IMX662_MAX_BLACK_LEVEL_10BPP:
                logging.warn(f"Black level value {value} is higher than the maximum {IMX662_MAX_BLACK_LEVEL_10BPP}")
                value = IMX662_MAX_BLACK_LEVEL_10BPP

        if value < 0:
            logging.warn(f"Black level value {value} is lower than the minimum 0")
            value = 0

        self.set_register(imx662_mode.BLKLEVEL_HIGH, (value >> 8) & 0xFF)
        self.set_register(imx662_mode.BLKLEVEL_LOW, value & 0xFF)

    def set_mode(self, imx662_mode_set):
        if imx662_mode_set.value < len(imx662_mode.imx662_Mode):
            self._mode = imx662_mode_set
            mode = imx662_mode.imx_frame_format[self._mode.value]
            self._height = mode.height
            self._width = mode.width
            self._pixel_format = mode.pixel_format
            self._framerate = mode.framerate
            self._pixel_bit_depth = mode.pixel_bit_depth
            
        else:
            logging.error("Incorrect mode for IMX662")
            self._mode = -1

    def configure_converter(self, converter):
        # Get the starting byte from the converter
        start_byte = converter.receiver_start_byte()
        
        # Calculate transmitted and received line bytes
        transmitted_line_bytes = converter.transmitted_line_bytes(
            self._pixel_format, self._width
        )
        received_line_bytes = converter.received_line_bytes(transmitted_line_bytes)
        
        # Calculate metadata size based on mode
        if self._mode.value == imx662_mode.imx662_Mode.imx662_mode_1920x1080_12BPP.value:
            logging.info("FRAMOS MODE imx662_mode_1920x1080_12BPP")
            metadata_size = 2880  # line metadata bytes

        elif self._mode.value == imx662_mode.imx662_Mode.imx662_mode_1920x1080_10BPP.value:
            logging.info("FRAMOS MODE imx662_mode_1920x1080_10BPP")
            metadata_size = 2400  # line metadata bytes

        elif self._mode.value == imx662_mode.imx662_Mode.imx662_mode_1280x720_12BPP.value:
            logging.info("FRAMOS MODE imx662_mode_1280x720_12BPP")
            metadata_size = 1920  # line metadata bytes

        elif self._mode.value == imx662_mode.imx662_Mode.imx662_mode_1280x720_10BPP.value:
            logging.info("FRAMOS MODE imx662_mode_1280x720_10BPP")
            metadata_size = 1600  # line metadata bytes
        else:
            metadata_size = 0
        
        # Add metadata size to start_byte (metadata comes before image data)
        start_byte += converter.received_line_bytes(metadata_size)
        
        # Skip margin_top lines (20 lines of optical black)
        margin_top = 20
        start_byte += received_line_bytes * margin_top
        
        converter.configure(
            start_byte,
            received_line_bytes,
            self._width,
            self._height,
            self._pixel_format,
        )

    def pixel_format(self):
        return self._pixel_format
    
    def pixel_bit_depth(self):
        return self._pixel_bit_depth

    def framerate(self):
        return self._framerate

    def bayer_format(self):
        return hololink_module.sensors.csi.BayerFormat.RGGB
    
    def optical_black(self):
        if self._pixel_format == hololink_module.sensors.csi.PixelFormat.RAW_10:
            optical_black_val = IMX662_DEFAULT_BLACK_LEVEL_10BPP
            return optical_black_val

        elif self._pixel_format == hololink_module.sensors.csi.PixelFormat.RAW_12:
            optical_black_val = IMX662_DEFAULT_BLACK_LEVEL_12BPP
            return optical_black_val

    def test_pattern(self, pattern=None):
        """If pattern==None then we disable test mode."""
        if pattern is None:
            self.set_register(imx662_mode.BLKLEVEL_LOW, 0x32)
            self.set_register(imx662_mode.TPG_EN_DUOUT, 0x00)
            self.set_register(imx662_mode.TPG_COLORWIDTH, 0x00)
            self.set_register(imx662_mode.TESTCLKEN, 0x02)
        else:
            self.set_register(imx662_mode.BLKLEVEL_LOW, 0x00)
            self.set_register(imx662_mode.TPG_EN_DUOUT, 0x01)
            self.set_register(imx662_mode.TPG_COLORWIDTH, 0x00)
            self.set_register(imx662_mode.TESTCLKEN, 0x0A)
            self.set_register(imx662_mode.TPG_PATSEL_DUOUT, pattern)
