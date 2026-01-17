# Holoscan Sensor Bridge

## Supported Hardware

- Nvidia Jetson AGX Orin developer kit
- Lattice CPNX100-ETH-SENSOR-BRIDGE
- FRAMOS FPA-4.A-AGX-V1A

## Flashing an HSB (Orin)

This must be done:

- From an Orin
- Over ethernet connected to SFP 0
- Using <https://github.com/marainc/holoscan-sensor-bridge/tree/framos-holoscan-2.0.0>

### Steps for a new HSB (with Orin already set up)

1. Connect ethernet
2. Connect power
3. Bring up the network interface:

   ```bash
   sudo nmcli connection up hololink-eno1
   ```

4. Verify connectivity:

   ```bash
   ping 192.168.0.2
   ```

5. Enter the container:

   ```bash
   cd ~/holoscan-sensor-bridge && sh docker/demo.sh
   ```

6. Program the HSB (to 2412):

   ```bash
   hololink --force program scripts/manifest-2507.yaml
   ```

7. Program to 2507:

   ```bash
   program_lattice_cpnx100 --force scripts/manifest-2507.yaml
   ```

8. Verify the update:

   ```bash
   hololink enumerate
   ```

   This should now show 2507.

## Detailed documentation

### 1. Flash and setup Nvidia Jetson AGX Orin

See [Installation and building the Framos Holoscan Sensor Bridge container](https://github.com/framosimaging/framos-holoscan-drivers/wiki/Installation-and-building-the-Framos-Holoscan-Sensor-Bridge-container)

### 2. Run Framos Holoscan Sensor Bridge container examples

See [Framos Holoscan Sensor Bridge container examples guide](https://github.com/framosimaging/framos-holoscan-drivers/wiki/Framos-Holoscan-Sensor-Bridge-container-examples-guide)
