from fastapi import Depends
from typing import Annotated
from sqlmodel import Session, create_engine

engine = create_engine("duckdb:///Data/inmuebles.db")

def get_session():
    with Session(engine) as session:
        yield session
    
connection = Annotated[Session,Depends(get_session)]