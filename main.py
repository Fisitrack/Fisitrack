from fastapi import FastAPI

app = FastAPI(title="Fisitrack")


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0", "environment": "development"}