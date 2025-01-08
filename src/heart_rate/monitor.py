import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import sqlite3
import json
from typing import Optional, Dict


class HeartRateMonitor:
    def __init__(self):
        self.device_name = "Polar Verity Sense"  # This might need adjustment based on actual device name
        self.hr_uuid = "00002a37-0000-1000-8000-00805f9b34fb"  # Standard HR Measurement characteristic UUID
        self.client: Optional[BleakClient] = None
        self.connected = False
        self.buffer: list[Dict] = []
        self.buffer_size = 100  # Adjust based on your needs

    async def scan_for_device(self):
        """Scan for the Polar device"""
        print("Scanning for Polar Verity device...")
        devices = await BleakScanner.discover()
        for device in devices:
            if device.name and self.device_name.lower() in device.name.lower():
                print(f"Found device: {device.name} ({device.address})")
                return device
        return None

    async def connect(self):
        """Connect to the device"""
        device = await self.scan_for_device()
        if not device:
            raise Exception("Polar device not found")

        try:
            self.client = BleakClient(device)
            await self.client.connect()
            self.connected = True
            print(f"Connected to {device.name}")
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            self.connected = False
            raise

    def handle_hr_data(self, sender: int, data: bytearray):
        """Handle incoming heart rate data"""
        # First byte contains flags
        flags = data[0]
        # Second byte contains HR value
        hr = data[1]

        timestamp = datetime.now().isoformat()
        hr_data = {
            "timestamp": timestamp,
            "heart_rate": hr,
            "raw_flags": flags
        }

        # Add to buffer
        self.buffer.append(hr_data)

        # Handle buffer overflow
        if len(self.buffer) >= self.buffer_size:
            self._process_buffer()

    def _process_buffer(self):
        """Process and store buffered data"""
        # TODO: Implement database storage
        print(f"Processing {len(self.buffer)} readings")
        self.buffer.clear()

    async def start_monitoring(self):
        """Start heart rate monitoring"""
        if not self.connected:
            await self.connect()

        await self.client.start_notify(self.hr_uuid, self.handle_hr_data)
        print("Started heart rate monitoring")

    async def stop_monitoring(self):
        """Stop heart rate monitoring"""
        if self.connected and self.client:
            await self.client.stop_notify(self.hr_uuid)
            await self.client.disconnect()
            self.connected = False
            print("Stopped heart rate monitoring")


async def main():
    monitor = HeartRateMonitor()
    try:
        await monitor.start_monitoring()
        # Keep running for testing
        await asyncio.sleep(30)  # Run for 30 seconds
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await monitor.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(main())