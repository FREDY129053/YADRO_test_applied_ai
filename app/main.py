import uvicorn

def main():
    uvicorn.run(
        app="app.src.server:app",
        host="localhost",
        port=8080,
    )


if __name__ == "__main__":
    main()
