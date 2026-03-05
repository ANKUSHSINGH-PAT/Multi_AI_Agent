import asyncio
import sys


async def main():
    process = await asyncio.create_subprocess_exec(
        "streamlit",
        "run",
        "frontend/streamlit_app.py",
        "--server.port", "8501"
    )

    try:
        await process.wait()
    except KeyboardInterrupt:
        process.terminate()
        await process.wait()


if __name__ == "__main__":
    asyncio.run(main())