from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.module_loader import ModuleLoader
from utils.config_manager import ConfigManager
from utils.logger import get_logger
from utils.formatting import Formatting
from utils.service_manager import ServiceManager
from utils.constants import Constants

app = FastAPI(title="Utility Suite UI Backend")
loader = ModuleLoader()
logger = get_logger(__name__)


class RunRequest(BaseModel):
    package_id: str
    feature_id: str
    args: dict | None = None


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/packages")
async def packages():
    return {"packages": loader.discover_packages()}


@app.post("/run")
async def run_feature(req: RunRequest):
    module = loader.load_package(req.package_id)
    if module is None:
        raise HTTPException(status_code=404, detail="Package not found")
    ctx = {
        "logger": logger,
        "format": Formatting(),
        "config_manager": ConfigManager(),
        "service_manager": ServiceManager(),
        "constants": Constants(),
    }
    try:
        result = module.run(req.feature_id, args=req.args or {}, ctx=ctx)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
