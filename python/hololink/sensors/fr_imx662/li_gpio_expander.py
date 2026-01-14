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

from enum import Enum
import logging

import hololink

INPUT_PORT_REGISTER     = 0x00
OUTPUT_PORT_REGISTER    = 0x01
POLARITY_REGISTER       = 0x02
CONFIGURATION_REGISTER  = 0x03

class GPIO_Expander_Output_EN(Enum):
    CAM_RST_OUTPUT = 0x00  # set all GPIO to output
    CAM_RST_ON = 0x04 # set all pins to high
    CAM_RST_OFF = 0x00


class GPIO_Expander_pin(Enum):
    PW_EN       = 0
    CRESETB     = 1
    CAM_RST     = 2
    XMASTER     = 3
    SLAMODE0    = 4
    SLAMODE1    = 5
    SLAMODE2    = 6
    TENABLE     = 7



class LIGPIOExpander:
    GPIO_EXPANDER_ADDRESS = 0x20

    def __init__(self, hololink, i2c_address):
        self._i2c = hololink.get_i2c(i2c_address)

    def set_register(self, register, value, timeout=None):
        logging.debug(
            "set_gpio_expander_register(register=%d(0x%X), value=%d(0x%X))"
            % (register, register, value, value)
        )
        write_bytes = bytearray(100)
        serializer = hololink.Serializer(write_bytes)
        serializer.append_uint8(register)
        serializer.append_uint8(value)
        read_byte_count = 0
        self._i2c.i2c_transaction(
            self.GPIO_EXPANDER_ADDRESS,
            write_bytes[: serializer.length()],
            read_byte_count,
            timeout=timeout,
        )
    
    def get_register(self, register):
        logging.debug("get_gpio_expander_register(register=%d(0x%X))"
                      % (register, register))
        write_bytes = bytearray(100)
        serializer = hololink.Serializer(write_bytes)
        serializer.append_uint8(register)
        read_byte_count = 1
        reply = self._i2c.i2c_transaction(
            self.GPIO_EXPANDER_ADDRESS,
            write_bytes[: serializer.length()],
            read_byte_count
        )
        deserializer = hololink.Deserializer(reply)
        r = deserializer.next_uint8()
        logging.debug(
            "get_register(register=%d(0x%X))=%d(0x%X)" % (register, register, r, r)
        )
        return r


    def set_direction_gpio(self, gpio, direciton):
        gpio_sate = self.get_register(CONFIGURATION_REGISTER)
        
        if direciton == "OUTPUT":
            gpio_sate &= ~(1 << gpio.value)
            self.set_register(CONFIGURATION_REGISTER, gpio_sate)
        elif direciton == "INPUT":
            gpio_sate |= (1 << gpio.value)
            self.set_register(CONFIGURATION_REGISTER, gpio_sate)
        else:
            logging.error("Incorrect GPIO direction")

    def set_output_gpio(self, gpio, value):
        gpio_value = self.get_register(OUTPUT_PORT_REGISTER)

        if value == 1:
            gpio_value |= (1 << gpio.value)
            self.set_register(OUTPUT_PORT_REGISTER, gpio_value)
        elif value == 0:
            gpio_value &= ~(1 << gpio.value)
            self.set_register(OUTPUT_PORT_REGISTER, gpio_value)
        else:
            logging.error("Incorrect GPIO output state")
