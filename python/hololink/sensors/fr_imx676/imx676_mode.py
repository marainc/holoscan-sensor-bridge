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
IMX676_TABLE_WAIT_MS = "imx676-table-wait-ms"
IMX676_WAIT_MS = 0x01
IMX676_WAIT_MS_START = 0x0F

# Register addresses for camera properties. They only accept 8bits of value.

STANDBY =           0x3000
REGHOLD =           0x3001
XMSTA =             0x3002

INCK_SEL =          0x3014
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

GAIN0_LOW =         0x3070
GAIN0_HIGH =        0x3071

XVS_XHS_DRV =       0x30A6

BLKLEVEL_LOW =      0x30DC
BLKLEVEL_HIGH =     0x30DD

TPG_EN_DUOUT =      0x30E0
TPG_PATSEL_DUOUT =  0x30E2
TPG_COLORWIDTH =    0x30E4
TESTCLKEN =         0x5300

EXTMODE = 0x30CE

imx676_start = [
    (IMX676_TABLE_WAIT_MS, 30),
    (STANDBY, 0x00),
    (IMX676_TABLE_WAIT_MS, 30),
    (XMSTA, 0x00),
    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
]

imx676_stop = [
    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
    (XMSTA, 0x01),
    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
    (STANDBY, 0x01),
    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
]

imx676_init_settings = [
    (LANEMODE,      0x03),
    (INCK_SEL,      0x01),

    (0x304E,        0x04),
    (0x3148,        0x00),
    (0x3460,        0x22),
    (0x347B,        0x02),
    (0x3A3C,        0x0F),
    (0x3A44,        0x0B),
    (0x3A76,        0xB5),
    (0x3A77,        0x00),
    (0x3A78,        0x03),
    (0x3B22,        0x04),
    (0x3B23,        0x44),
    (0x3C03,        0x04),
    (0x3C04,        0x04),
    (0x3C30,        0x73),
    (0x3C34,        0x6C),
    (0x3C3C,        0x20),
    (0x3C44,        0x06),
    (0x3CB8,        0x00),
    (0x3CBA,        0xFF),
    (0x3CBB,        0x03),
    (0x3CBC,        0xFF),
    (0x3CBD,        0x03),
    (0x3CC2,        0xFF),
    (0x3CC3,        0x03),
    (0x3CC8,        0xFF),
    (0x3CC9,        0x03),
    (0x3CCA,        0x00),
    (0x3CCE,        0xFF),
    (0x3CCF,        0x03),
    (0x3CD0,        0xFF),
    (0x3CD1,        0x03),
    (0x3E00,        0x1E),
    (0x3E02,        0x04),
    (0x3E03,        0x00),
    (0x3E20,        0x04),
    (0x3E21,        0x00),
    (0x3E22,        0x1E),
    (0x3E24,        0xB6),
    (0x4490,        0x07),
    (0x4494,        0x10),
    (0x4495,        0x00),
    (0x4496,        0xB2),
    (0x4497,        0x00),
    (0x44A0,        0x33),
    (0x44A2,        0x10),
    (0x44A4,        0x10),
    (0x44A6,        0x10),
    (0x44A8,        0x4B),
    (0x44AA,        0x4B),
    (0x44AC,        0x4B),
    (0x44AE,        0x46),
    (0x44B0,        0x33),
    (0x44B2,        0x10),
    (0x44B4,        0x10),
    (0x44B6,        0x10),
    (0x44B8,        0x42),
    (0x44BA,        0x42),
    (0x44BC,        0x42),
    (0x44BE,        0x42),
    (0x44C0,        0x33),
    (0x44C2,        0x10),
    (0x44C4,        0x10),
    (0x44C6,        0x10),
    (0x44C8,        0xE7),
    (0x44CA,        0xE2),
    (0x44CC,        0xE2),
    (0x44CE,        0xDD),
    (0x44D0,        0xDD),
    (0x44D2,        0xB2),
    (0x44D4,        0xB2),
    (0x44D6,        0xB2),
    (0x44D8,        0xE1),
    (0x44DA,        0xE1),
    (0x44DC,        0xE1),
    (0x44DE,        0xDD),
    (0x44E0,        0xDD),
    (0x44E2,        0xB2),
    (0x44E4,        0xB2),
    (0x44E6,        0xB2),
    (0x44E8,        0xDD),
    (0x44EA,        0xDD),
    (0x44EC,        0xDD),
    (0x44EE,        0xDD),
    (0x44F0,        0xDD),
    (0x44F2,        0xB2),
    (0x44F4,        0xB2),
    (0x44F6,        0xB2),
    (0x4538,        0x15),
    (0x4539,        0x15),
    (0x453A,        0x15),
    (0x4544,        0x15),
    (0x4545,        0x15),
    (0x4546,        0x15),
    (0x4550,        0x10),
    (0x4551,        0x10),
    (0x4552,        0x10),
    (0x4553,        0x10),
    (0x4554,        0x10),
    (0x4555,        0x10),
    (0x4556,        0x10),
    (0x4557,        0x10),
    (0x4558,        0x10),
    (0x455C,        0x10),
    (0x455D,        0x10),
    (0x455E,        0x10),
    (0x455F,        0x10),
    (0x4560,        0x10),
    (0x4561,        0x10),
    (0x4562,        0x10),
    (0x4563,        0x10),
    (0x4564,        0x10),
    (0x4604,        0x04),
    (0x4608,        0x22),
    (0x479C,        0x04),
    (0x47A0,        0x22),
    (0x4E3C,        0x07),

    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
]

# Mode: 3520x3556 12 bits
imx676_mode_3520x3556_12BPP = [
    (HMAX_LOW,      0x74),
    (HMAX_HIGH,     0x02),
    (SHR0_LOW,      0x08),
    (SHR0_MID,      0x00),
    (SHR0_HIGH,     0x00),

    (VMAX_LOW,      0x2C),
    (VMAX_MID,      0x0E),
    (VMAX_HIGH,     0x00),

    (DATARATE_SEL,  0x03),

    (0x4498,        0x4C),
    (0x449A,        0x4B),
    (0x449C,        0x4B),
    (0x449E,        0x49),

    (0x48A7,        0x01),
    (0x4EE8,        0x00),

    (ADBIT,        	0x01),
    (MDBIT,        	0x01),

    (0x355A,        0x10),

    (0x3C0A,        0x1F),
    (0x3C0B,        0x1F),
    (0x3C0C,        0x1F),
    (0x3C0D,        0x1F),
    (0x3C0E,        0x1F),
    (0x3C0F,        0x1F),

    (WINMODE,       0x04),
    (ADDMODE,       0x00),
    (WDMODE,        0x00),
    (VCMODE,        0x01),

    (PIX_HST_HIGH,      0x00),
    (PIX_HST_LOW,       0x10),
    (PIX_HWIDTH_HIGH,   0x0D),
    (PIX_HWIDTH_LOW,    0xC0),

    (PIX_VST_HIGH,      0x00),
    (PIX_VST_LOW,       0x00),
    (PIX_VWIDTH_HIGH,   0x0D),
    (PIX_VWIDTH_LOW,    0xE4),

    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
]

# Mode: 3456x3556 10 bits
imx676_mode_3456x3556_10BPP = [
    (HMAX_LOW,      0x74),
    (HMAX_HIGH,     0x02),
    (SHR0_LOW,      0x08),
    (SHR0_MID,      0x00),
    (SHR0_HIGH,     0x00),

    (VMAX_LOW,      0x2C),
    (VMAX_MID,      0x0E),
    (VMAX_HIGH,     0x00),

    (DATARATE_SEL,  0x04),

    (0x4498,        0x4C),
    (0x449A,        0x4B),
    (0x449C,        0x4B),
    (0x449E,        0x49),

    (0x48A7,        0x01),
    (0x4EE8,        0x00),

    (ADBIT,        	0x00),
    (MDBIT,        	0x00),

    (0x355A,        0x1C),

    (0x3C0A,        0x03),
    (0x3C0B,        0x03),
    (0x3C0C,        0x03),
    (0x3C0D,        0x03),
    (0x3C0E,        0x03),
    (0x3C0F,        0x03),

    (WINMODE,       0x04),
    (ADDMODE,       0x00),
    (WDMODE,        0x00),
    (VCMODE,        0x01),

    (PIX_HST_HIGH,      0x00),
    (PIX_HST_LOW,       0x30),
    (PIX_HWIDTH_HIGH,   0x0D),
    (PIX_HWIDTH_LOW,    0x80),

    (PIX_VST_HIGH,      0x00),
    (PIX_VST_LOW,       0x00),
    (PIX_VWIDTH_HIGH,   0x0D),
    (PIX_VWIDTH_LOW,    0xE4),

    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
]

# Mode: 1920x1080 12 bits
imx676_mode_1920x1080_12BPP = [
    (HMAX_LOW,      0x74),
    (HMAX_HIGH,     0x02),
    (SHR0_LOW,      0x08),
    (SHR0_MID,      0x00),
    (SHR0_HIGH,     0x00),

    (VMAX_LOW,      0x80),
    (VMAX_MID,      0x04),
    (VMAX_HIGH,     0x00),

    (DATARATE_SEL,  0x03),

    (0x4498,        0x4C),
    (0x449A,        0x4B),
    (0x449C,        0x4B),
    (0x449E,        0x49),

    (0x48A7,        0x01),
    (0x4EE8,        0x00),

    (ADBIT,        	0x01),
    (MDBIT,        	0x01),

    (0x355A,        0x10),

    (0x3C0A,        0x1F),
    (0x3C0B,        0x1F),
    (0x3C0C,        0x1F),
    (0x3C0D,        0x1F),
    (0x3C0E,        0x1F),
    (0x3C0F,        0x1F),

    (WINMODE,       0x04),
    (ADDMODE,       0x00),
    (WDMODE,        0x00),
    (VCMODE,        0x01),

    (PIX_HST_HIGH,      0x03),
    (PIX_HST_LOW,       0x30),
    (PIX_HWIDTH_HIGH,   0x07),
    (PIX_HWIDTH_LOW,    0x80),

    (PIX_VST_HIGH,      0x04),
    (PIX_VST_LOW,       0xD6),
    (PIX_VWIDTH_HIGH,   0x04),
    (PIX_VWIDTH_LOW,    0x38),

    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
]

# Mode: 1920x1080 10 bits
imx676_mode_1920x1080_10BPP = [
    (HMAX_LOW,      0x3A),
    (HMAX_HIGH,     0x01),
    (SHR0_LOW,      0x08),
    (SHR0_MID,      0x00),
    (SHR0_HIGH,     0x00),

    (VMAX_LOW,      0x80),
    (VMAX_MID,      0x04),
    (VMAX_HIGH,     0x00),

    (DATARATE_SEL,  0x00),

    (0x4498,        0x4C),
    (0x449A,        0x4B),
    (0x449C,        0x4B),
    (0x449E,        0x49),

    (0x48A7,        0x01),
    (0x4EE8,        0x00),

    (ADBIT,        	0x00),
    (MDBIT,        	0x00),

    (0x355A,        0x1C),

    (0x3C0A,        0x03),
    (0x3C0B,        0x03),
    (0x3C0C,        0x03),
    (0x3C0D,        0x03),
    (0x3C0E,        0x03),
    (0x3C0F,        0x03),

    (WINMODE,       0x04),
    (ADDMODE,       0x00),
    (WDMODE,        0x00),
    (VCMODE,        0x01),

    (PIX_HST_HIGH,      0x03),
    (PIX_HST_LOW,       0x30),
    (PIX_HWIDTH_HIGH,   0x07),
    (PIX_HWIDTH_LOW,    0x80),

    (PIX_VST_HIGH,      0x04),
    (PIX_VST_LOW,       0xD6),
    (PIX_VWIDTH_HIGH,   0x04),
    (PIX_VWIDTH_LOW,    0x38),

    (IMX676_TABLE_WAIT_MS, IMX676_WAIT_MS),
]

class imx676_Mode(Enum):
    imx676_mode_3520x3556_12BPP = 0
    imx676_mode_3456x3556_10BPP = 1
    imx676_mode_1920x1080_12BPP = 2
    imx676_mode_1920x1080_10BPP = 3
    Unknown = 4


frame_format = namedtuple(
    "FrameFormat", ["width", "height", "framerate", "pixel_format", "pixel_bit_depth"]
)

imx_frame_format = []
imx_frame_format.insert(
    imx676_Mode.imx676_mode_3520x3556_12BPP.value,
    frame_format(3520, 3556, 30, hololink.sensors.csi.PixelFormat.RAW_12, 12),
)
imx_frame_format.insert(
    imx676_Mode.imx676_mode_3456x3556_10BPP.value,
    frame_format(3456, 3556, 30, hololink.sensors.csi.PixelFormat.RAW_10, 10),
)
imx_frame_format.insert(
    imx676_Mode.imx676_mode_1920x1080_12BPP.value,
    frame_format(1920, 1080, 103, hololink.sensors.csi.PixelFormat.RAW_12, 12),
)
imx_frame_format.insert(
    imx676_Mode.imx676_mode_1920x1080_10BPP.value,
    frame_format(1920, 1080, 205, hololink.sensors.csi.PixelFormat.RAW_10, 10),
)
