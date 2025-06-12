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

from collections import namedtuple
from enum import Enum

import hololink

# values are on hex number system to be consistent with rest of the list
IMX662_TABLE_WAIT_MS = "imx662-table-wait-ms"
IMX662_WAIT_MS = 0x01
IMX662_WAIT_MS_START = 0x0F

# Register addresses for camera properties. They only accept 8bits of value.

STANDBY =           0x3000
REGHOLD =           0x3001
XMSTA =             0x3002

INCK_SEL=           0x3014
DATARATE_SEL =      0x3015
WINMODE =           0x3018

WDMODE =            0x301A
ADDMODE =           0x301B
VCMODE =            0x301E

HREVERSE =          0x3020
VREVERSE =          0x3021
ADBIT =             0x3022
MDBIT =             0x3023
VMAX_LOW =          0x3028
VMAX_MID =          0x3029
VMAX_HIGH =         0x302A
HMAX_LOW =          0x302C
HMAX_HIGH =         0x302D

PIX_HST_LOW =       0x303C
PIX_HST_HIGH =      0x303D
PIX_HWIDTH_LOW =    0x303E
PIX_HWIDTH_HIGH =   0x303F

LANEMODE =          0x3040

PIX_VST_LOW =       0x3044
PIX_VST_HIGH =      0x3045
PIX_VWIDTH_LOW =    0x3046
PIX_VWIDTH_HIGH =   0x3047

SHR0_LOW =          0x3050
SHR0_MID =          0x3051
SHR0_HIGH =         0x3052

GAIN_LOW =          0x3070
GAIN_HIGH =         0x3071

XVS_XHS_DRV =       0x30A6

EXTMODE =           0x30CE
BLKLEVEL_LOW =      0x30DC
BLKLEVEL_HIGH =     0x30DD

TPG_EN_DUOUT =      0x30E0
TPG_PATSEL_DUOUT =  0x30E2
TPG_COLORWIDTH =    0x30E4
TESTCLKEN =         0x4900

imx662_start = [
    (IMX662_TABLE_WAIT_MS, 30),
    (STANDBY, 0x00),
    (IMX662_TABLE_WAIT_MS, 30),
    (XMSTA, 0x00),
    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
]

imx662_stop = [
    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
    (XMSTA, 0x01),
    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
    (STANDBY, 0x01),
    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
]

imx662_init_settings = [
    (LANEMODE,      0x03),
    (INCK_SEL,      0x01),

    (0x3444,        0xAC),
    (0x3460,        0x21),
    (0x3492,        0x08),
    (0x3A50,        0x62),
    (0x3A51,        0x01),
    (0x3A52,        0x19),
    (0x3B00,        0x39),
    (0x3B23,        0x2D),
    (0x3B45,        0x04),
    (0x3C0A,        0x1F),
    (0x3C0B,        0x1E),
    (0x3C38,        0x21),

    (0x3C44,        0x00),
    (0x3CB6,        0xD8),
    (0x3CC4,        0xDA),
    (0x3E24,        0x79),
    (0x3E2C,        0x15),
    (0x3EDC,        0x2D),
    (0x4498,        0x05),
    (0x449C,        0x19),
    (0x449D,        0x00),
    (0x449E,        0x32),
    (0x449F,        0x01),
    (0x44A0,        0x92),
    (0x44A2,        0x91),
    (0x44A4,        0x8C),
    (0x44A6,        0x87),
    (0x44A8,        0x82),
    (0x44AA,        0x78),
    (0x44AC,        0x6E),
    (0x44AE,        0x69),
    (0x44B0,        0x92),
    (0x44B2,        0x91),
    (0x44B4,        0x8C),
    (0x44B6,        0x87),
    (0x44B8,        0x82),
    (0x44BA,        0x78),
    (0x44BC,        0x6E),
    (0x44BE,        0x69),
    (0x44C0,        0x7F),
    (0x44C1,        0x01),
    (0x44C2,        0x7F),
    (0x44C3,        0x01),
    (0x44C4,        0x7A),
    (0x44C5,        0x01),
    (0x44C6,        0x7A),
    (0x44C7,        0x01),
    (0x44C8,        0x70),
    (0x44C9,        0x01),
    (0x44CA,        0x6B),
    (0x44CB,        0x01),
    (0x44CC,        0x6B),
    (0x44CD,        0x01),
    (0x44CE,        0x5C),
    (0x44CF,        0x01),
    (0x44D0,        0x7F),
    (0x44D1,        0x01),
    (0x44D2,        0x7F),
    (0x44D3,        0x01),
    (0x44D4,        0x7A),
    (0x44D5,        0x01),
    (0x44D6,        0x7A),
    (0x44D7,        0x01),
    (0x44D8,        0x70),
    (0x44D9,        0x01),
    (0x44DA,        0x6B),
    (0x44DB,        0x01),
    (0x44DC,        0x6B),
    (0x44DD,        0x01),
    (0x44DE,        0x5C),
    (0x44DF,        0x01),
    (0x4534,        0x1C),
    (0x4535,        0x03),
    (0x4538,        0x1C),
    (0x4539,        0x1C),
    (0x453A,        0x1C),
    (0x453B,        0x1C),
    (0x453C,        0x1C),
    (0x453D,        0x1C),
    (0x453E,        0x1C),
    (0x453F,        0x1C),
    (0x4540,        0x1C),
    (0x4541,        0x03),
    (0x4542,        0x03),
    (0x4543,        0x03),
    (0x4544,        0x03),
    (0x4545,        0x03),
    (0x4546,        0x03),
    (0x4547,        0x03),
    (0x4548,        0x03),
    (0x4549,        0x03),

    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
]

# Mode : 1920x1080 12 bits
imx662_mode_1920x1080_12BPP = [
    (HMAX_LOW,      0xDE),
    (HMAX_HIGH,     0x03),
    (SHR0_LOW,      0x04),
    (SHR0_MID,      0x00),
    (SHR0_HIGH,     0x00),

    (VMAX_LOW,      0x7E),
    (VMAX_MID,      0x04),
    (VMAX_HIGH,     0x00),

    (DATARATE_SEL,  0x04),

    (ADBIT,         0x01),
    (MDBIT,         0x01),
    (0x3A50,        0xFF),
    (0x3A51,        0x03),
    (0x3A52,        0x00),

    (WINMODE,       0x04),
    (ADDMODE,       0x00),
    (WDMODE,        0x00),
    (VCMODE,        0x01),

    (PIX_HST_HIGH,      0x00),
    (PIX_HST_LOW,       0x08),
    (PIX_HWIDTH_HIGH,   0x07),
    (PIX_HWIDTH_LOW,    0x80),

    (PIX_VST_HIGH,      0x00),
    (PIX_VST_LOW,       0x0C),
    (PIX_VWIDTH_HIGH,   0x04),
    (PIX_VWIDTH_LOW,    0x38),

    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
]

# Mode: 1920x1080 10 bits
imx662_mode_1920x1080_10BPP = [
    (HMAX_LOW,      0x94),
    (HMAX_HIGH,     0x02),
    (SHR0_LOW,      0x04),
    (SHR0_MID,      0x00),
    (SHR0_HIGH,     0x00),

    (VMAX_LOW,      0x7E),
    (VMAX_MID,      0x04),
    (VMAX_HIGH,     0x00),

    (DATARATE_SEL,  0x03),

    (ADBIT,         0x00),
    (MDBIT,         0x00),
    (0x3A50,        0x62),
    (0x3A51,        0x01),
    (0x3A52,        0x19),

    (WINMODE,       0x04),
    (ADDMODE,       0x00),
    (WDMODE,        0x00),
    (VCMODE,        0x01),

    (PIX_HST_HIGH,      0x00),
    (PIX_HST_LOW,       0x08),
    (PIX_HWIDTH_HIGH,   0x07),
    (PIX_HWIDTH_LOW,    0x80),

    (PIX_VST_HIGH,      0x00),
    (PIX_VST_LOW,       0x0C),
    (PIX_VWIDTH_HIGH,   0x04),
    (PIX_VWIDTH_LOW,    0x38),

    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
]

# Mode: 1280x720 12 bits
imx662_mode_1280x720_12BPP = [
    (HMAX_LOW,      0xDE),
    (HMAX_HIGH,     0x03),
    (SHR0_LOW,      0x04),
    (SHR0_MID,      0x00),
    (SHR0_HIGH,     0x00),

    (VMAX_LOW,      0x16),
    (VMAX_MID,      0x03),
    (VMAX_HIGH,     0x00),

    (DATARATE_SEL,  0x04),

    (ADBIT,         0x01),
    (MDBIT,         0x01),
    (0x3A50,        0xFF),
    (0x3A51,        0x03),
    (0x3A52,        0x00),

    (WINMODE,       0x04),
    (ADDMODE,       0x00),
    (WDMODE,        0x00),
    (VCMODE,        0x01),

    (PIX_HST_HIGH,      0x01),
    (PIX_HST_LOW,       0x48),
    (PIX_HWIDTH_HIGH,   0x05),
    (PIX_HWIDTH_LOW,    0x00),

    (PIX_VST_HIGH,      0x00),
    (PIX_VST_LOW,       0xC0),
    (PIX_VWIDTH_HIGH,   0x02),
    (PIX_VWIDTH_LOW,    0xD0),

    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
]

# Mode: 1280x720 10 bits
imx662_mode_1280x720_10BPP = [
    (HMAX_LOW,      0x94),
    (HMAX_HIGH,     0x02),
    (SHR0_LOW,      0x04),
    (SHR0_MID,      0x00),
    (SHR0_HIGH,     0x00),

    (VMAX_LOW,      0x16),
    (VMAX_MID,      0x03),
    (VMAX_HIGH,     0x00),

    (DATARATE_SEL,  0x03),

    (ADBIT,         0x00),
    (MDBIT,         0x00),
    (0x3A50,        0x62),
    (0x3A51,        0x01),
    (0x3A52,        0x19),

    (WINMODE,       0x04),
    (ADDMODE,       0x00),
    (WDMODE,        0x00),
    (VCMODE,        0x01),

    (PIX_HST_HIGH,      0x01),
    (PIX_HST_LOW,       0x48),
    (PIX_HWIDTH_HIGH,   0x05),
    (PIX_HWIDTH_LOW,    0x00),

    (PIX_VST_HIGH,      0x00),
    (PIX_VST_LOW,       0xC0),
    (PIX_VWIDTH_HIGH,   0x02),
    (PIX_VWIDTH_LOW,    0xD0),

    (IMX662_TABLE_WAIT_MS, IMX662_WAIT_MS),
]

class imx662_Mode(Enum):
    imx662_mode_1920x1080_12BPP = 0
    imx662_mode_1920x1080_10BPP = 1
    imx662_mode_1280x720_12BPP = 2
    imx662_mode_1280x720_10BPP = 3
    Unknown = 4


frame_format = namedtuple(
    "FrameFormat", ["width", "height", "framerate", "pixel_format", "pixel_bit_depth"]
)

imx_frame_format = []
imx_frame_format.insert(
    imx662_Mode.imx662_mode_1920x1080_12BPP.value,
    frame_format(1920, 1080, 60, hololink.sensors.csi.PixelFormat.RAW_12, 12),
)
imx_frame_format.insert(
    imx662_Mode.imx662_mode_1920x1080_10BPP.value,
    frame_format(1920, 1080, 90, hololink.sensors.csi.PixelFormat.RAW_10, 10),
)
imx_frame_format.insert(
    imx662_Mode.imx662_mode_1280x720_12BPP.value,
    frame_format(1280, 720, 95, hololink.sensors.csi.PixelFormat.RAW_12, 12),
)
imx_frame_format.insert(
    imx662_Mode.imx662_mode_1280x720_10BPP.value,
    frame_format(1280, 720, 143, hololink.sensors.csi.PixelFormat.RAW_10, 10),
)
