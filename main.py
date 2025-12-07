import asyncio
from src.controller import Controller


async def main():
	controller = await Controller.create_async("config.ini")
	


if __name__ == "__main__":
	asyncio.run(main())
