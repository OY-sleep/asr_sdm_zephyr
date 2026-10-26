#!/usr/bin/env python3
import glob, sys, time
import serial

def find_port():
    for pat in ("/dev/serial/by-id/usb-Zephyr_Project_*", "/dev/ttyACM*"):
        for p in sorted(glob.glob(pat)):
            return p
    return None

print("waiting for serial device...", flush=True)
while True:
    port = find_port()
    if port is None:
        time.sleep(0.2)
        continue
    try:
        with serial.Serial(port, 115200, timeout=0.2) as s:
            print(f"\n--- connected {port} ---", flush=True)
            while True:
                data = s.read(256)
                if data:
                    sys.stdout.buffer.write(data)
                    sys.stdout.buffer.flush()
    except (serial.SerialException, OSError):
        print("\n--- disconnected, reconnecting ---", flush=True)
        time.sleep(0.3)
