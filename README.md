# Holoscan Sensor Bridge

> **Reference:** [holoscan-sensor-bridge (GitHub)](https://github.com/marainc/holoscan-sensor-bridge/tree/main)

---

## Running Example (Thor)

1. Connect the Thor directly to an HDMI display (not SSH)
2. Connect over QSFP port to SFP 0 on the HSB
3. Connect power
4. Run the following commands:

```bash
xhost +
sudo nmcli connection up hololink-eno1 
ping 192.168.0.2
cd holoscan-sensor-bridge && sh docker/demo.sh
pytest  # No test should fail but some may skip
hololink enumerate # should not show error
python3 examples/framos_single_network_stereo_player.py --camera-type fr_imx676
```

---

## Known Problems

### Pytest failing with Python Fatal Error

**Solution:**  
Run from the host machine. This is a problem with display forwarding.

---

### `program_lattice_cpnx100` throws `RESPONSE_INVALID_CMD`

**Error:**

```
program_lattice_cpnx100 scripts/manifest.yaml
Press 'y' or 'Y' to accept this end user license agreement: y
INFO 0.0000 programmer.cpp:398 check_images tid=0xc7 -- context=cpnx content_name=fpga_cpnx_v2510_ea.bit
INFO 0.4531 programmer.cpp:398 check_images tid=0xc7 -- context=clnx content_name=fpga_clnx_v2510_ea.bit
INFO 1.5859 hololink.cpp:1776 configure_hsb tid=0xc7 -- HSB IP version=0x2412 datecode=0xc5e6cc11
terminate called after throwing an instance of 'std::runtime_error'
  what():  write_uint32((0x110,0x2)) response_code=0X4(RESPONSE_INVALID_CMD)
Aborted (core dumped)
```

**Solution:**  
_Unknown_


---

### Unsure of FPGA Version

**Solution:**  
Run `hololink enumerate` — it will show the current firmware version under "HSB IP".

---

### `framos_player.py` FW Version Check Error

**Error:**

```
FW version check error. should be 0x2501 or newer
```

**Related:** `hololink enumerate` may also show:

```
enumerator.cpp:216 deserialize_bootp_request tid=0x87 -- Unable to deserialize bootp request vendor data.
```

**Workaround:**  
Flash the firmware:

```bash
hololink --force program scripts/manifest.yaml        # to 2412
program_lattice_cpnx100 --force scripts/manifest-2507.yaml  # to 2507
```

---

### `hololink --force program` Unsupported Strategy Error

**Error:**

```
root@ubuntu:/home/spotter/holoscan-sensor-bridge# hololink --force program scripts/manifest.yaml
…
   raise Exception(f'Unsupported strategy "{strategy_name}" specified.')
Exception: Unsupported strategy "sensor_bridge_10" specified.
```

**Solution:**  
_Unknown_

---

### Pytest `DEFAULT_MTU` AttributeError


**Error:**

```
tests/test_imx274_pattern.py:484: in <module>
    hololink_module.DEFAULT_MTU,
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: module 'hololink' has no attribute 'DEFAULT_MTU'
```
**Solution:**  
_Unknown_
