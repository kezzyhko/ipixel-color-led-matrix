#!/usr/bin/env python3
"""
Simple example script to control iPixel Color LED matrix.
This script connects to the device and changes a couple of pixels to different colors.
"""

import asyncio
from bleak import BleakClient

# Bluetooth UUIDs for iPixel devices
WRITE_UUID = "0000fa02-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "0000fa03-0000-1000-8000-00805f9b34fb"

# Replace with your device's Bluetooth MAC address
# You can find it by scanning for devices with name starting with "LED_BLE_"
# DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"
DEVICE_ADDRESS = "BC:42:CD:38:12:D3"


def make_command_payload(opcode: int, payload: bytes) -> bytes:
    """Create command with header format: [LEN_L, LEN_H, CMD_L, CMD_H, DATA...]"""
    total_length = len(payload) + 4  # +4 for length and opcode
    command = bytearray()
    command.extend(total_length.to_bytes(2, 'little'))  # Length (little-endian)
    command.extend(opcode.to_bytes(2, 'little'))        # Opcode (little-endian)
    command.extend(payload)                             # Payload data
    return bytes(command)


def make_diy_mode_command(enabled: bool) -> bytes:
    """Enable/disable DIY mode (required for pixel control).
    
    Command: 0x0104
    """
    mode_byte = 1 if enabled else 0
    return bytes([5, 0, 4, 1, mode_byte])


def make_set_pixel_command(x: int, y: int, r: int, g: int, b: int, a: int = 255) -> bytes:
    """Set individual pixel color.
    
    Command: 0x0105
    Format: [10, 0, 5, 1, r, g, b, a, x, y]
    
    Args:
        x: X coordinate (0-based)
        y: Y coordinate (0-based)
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        a: Alpha component (0-255, default 255 for opaque)
    """
    return bytes([10, 0, 5, 1, r, g, b, a, x, y])


def make_power_command(on: bool) -> bytes:
    """Turn device on/off.
    
    Command: 0x0107
    """
    on_byte = 1 if on else 0
    return bytes([5, 0, 7, 1, on_byte])


def make_brightness_command(brightness: int) -> bytes:
    """Set brightness level (1-100).
    
    Command: 0x8004
    """
    if brightness < 1 or brightness > 100:
        raise ValueError("Brightness must be between 1 and 100")
    return make_command_payload(0x8004, bytes([brightness]))


async def control_ipixel():
    """Main function to connect and control the iPixel device."""
    
    if DEVICE_ADDRESS == "XX:XX:XX:XX:XX:XX":
        print("ERROR: Please set DEVICE_ADDRESS to your device's Bluetooth MAC address")
        print("You can find it by scanning for devices with name starting with 'LED_BLE_'")
        return
    
    print(f"Connecting to iPixel device at {DEVICE_ADDRESS}...")
    
    async with BleakClient(DEVICE_ADDRESS) as client:
        print("Connected successfully!")
        
        # Enable notifications (required for some devices)
        try:
            await client.start_notify(NOTIFY_UUID, lambda sender, data: None)
            print("Notifications enabled")
        except Exception as e:
            print(f"Note: Could not enable notifications: {e}")
        
        # Turn on the device
        print("\nTurning device on...")
        await client.write_gatt_char(WRITE_UUID, make_power_command(True))
        await asyncio.sleep(0.5)
        
        # Set brightness to 50%
        print("Setting brightness to 50%...")
        await client.write_gatt_char(WRITE_UUID, make_brightness_command(50))
        await asyncio.sleep(0.5)
        
        # Enable DIY mode (required for pixel control)
        print("Enabling DIY mode...")
        await client.write_gatt_char(WRITE_UUID, make_diy_mode_command(True))
        await asyncio.sleep(0.5)
        
        # Set a few pixels to different colors
        print("\nSetting pixels to different colors...")
        
        # Pixel 1: Red at position (5, 5)
        print("  Setting pixel (5, 5) to RED")
        await client.write_gatt_char(WRITE_UUID, make_set_pixel_command(5, 5, 255, 0, 0))
        await asyncio.sleep(0.2)
        
        # Pixel 2: Green at position (10, 5)
        print("  Setting pixel (10, 5) to GREEN")
        await client.write_gatt_char(WRITE_UUID, make_set_pixel_command(10, 5, 0, 255, 0))
        await asyncio.sleep(0.2)
        
        # Pixel 3: Blue at position (15, 5)
        print("  Setting pixel (15, 5) to BLUE")
        await client.write_gatt_char(WRITE_UUID, make_set_pixel_command(15, 5, 0, 0, 255))
        await asyncio.sleep(0.2)
        
        # Pixel 4: Yellow at position (5, 10)
        print("  Setting pixel (5, 10) to YELLOW")
        await client.write_gatt_char(WRITE_UUID, make_set_pixel_command(5, 10, 255, 255, 0))
        await asyncio.sleep(0.2)
        
        # Pixel 5: Magenta at position (10, 10)
        print("  Setting pixel (10, 10) to MAGENTA")
        await client.write_gatt_char(WRITE_UUID, make_set_pixel_command(10, 10, 255, 0, 255))
        await asyncio.sleep(0.2)
        
        # Pixel 6: Cyan at position (15, 10)
        print("  Setting pixel (15, 10) to CYAN")
        await client.write_gatt_char(WRITE_UUID, make_set_pixel_command(15, 10, 0, 255, 255))
        await asyncio.sleep(0.2)
        
        print("\nDone! The pixels should now be displayed on your device.")
        print("Press Ctrl+C to exit, or wait 10 seconds...")
        
        # Keep connection alive for a few seconds to see the result
        await asyncio.sleep(10)
        
        print("\nDisconnecting...")


async def scan_for_devices():
    """Helper function to scan for iPixel devices."""
    from bleak import BleakScanner
    
    print("Scanning for iPixel devices (this may take 10-15 seconds)...")
    print("Look for devices with names starting with 'LED_BLE_'")
    print()
    
    devices = await BleakScanner.discover(timeout=15.0)
    
    ipixel_devices = []
    for device in devices:
        if device.name and device.name.startswith("LED_BLE_"):
            ipixel_devices.append(device)
            print(f"Found iPixel device: {device.name}")
            print(f"  Address: {device.address}")
            print(f"  RSSI: {device.rssi} dBm")
            print()
    
    if not ipixel_devices:
        print("No iPixel devices found. Make sure:")
        print("  1. Your device is powered on")
        print("  2. Bluetooth is enabled on your computer")
        print("  3. The device is in range")
    else:
        print(f"\nFound {len(ipixel_devices)} device(s).")
        print("Copy one of the addresses above and set it as DEVICE_ADDRESS in the script.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        # Scan for devices
        asyncio.run(scan_for_devices())
    else:
        # Run the main control script
        try:
            asyncio.run(control_ipixel())
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        except Exception as e:
            print(f"\nError: {e}")
            print("\nTip: Run 'python ipixel_example.py scan' to find your device address")

