import asyncio
from src.controller import Controller


async def main():
	controller = await Controller.create("config.ini")
	print(controller.device_info)
	await controller.client.set_pixel(0, 0, "FFFF00")


if __name__ == "__main__":
	asyncio.run(main())
