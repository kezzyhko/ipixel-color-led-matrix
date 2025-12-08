import asyncio
from src.controller import Controller


async def main():
	controller = await Controller.create("config.ini")
	_ = controller
	


if __name__ == "__main__":
	asyncio.run(main())
