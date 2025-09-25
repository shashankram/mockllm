import uvicorn
import os


def main() -> None:
    """Run the mock LLM server."""
    uvicorn.run(
        "mockllm.server:app",
        host="0.0.0.0",
        port=int(os.getenv("SERVER_PORT", 9000)),
        reload=True,
    )


if __name__ == "__main__":
    main()
