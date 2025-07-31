from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from src.api.routes import auth, portfolios, strategies, users
from src.core.logging.http_logger import HTTPLoggingMiddleware
from src.core.logging.logger import configure_logging
from src.core.security.middleware import InputValidationMiddleware

configure_logging()

app = FastAPI(title="Quant Platform API")

# Add middleware
app.add_middleware(InputValidationMiddleware)
app.add_middleware(HTTPLoggingMiddleware)

# Register routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(portfolios.router, prefix="/portfolios", tags=["Portfolios"])
app.include_router(strategies.router, prefix="/strategies", tags=["Strategies"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "Quant Platform API", "version": "0.1.0"}
