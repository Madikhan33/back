from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel



app = FastAPI()





if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, reload=True)