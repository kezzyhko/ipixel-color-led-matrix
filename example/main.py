import asyncio
from ledmatrix.controller import Controller
from pathlib import Path


async def main():
	controller = await Controller.create(Path(__file__).parent / "config.ini")
	canvas = controller.canvas
	layer = canvas.create_layer()
	# await controller.client.set_pixel(0, 0, "000000")


if __name__ == "__main__":
	asyncio.run(main())
