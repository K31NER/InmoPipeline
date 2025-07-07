from pydantic import BaseModel
from enum import Enum

class Regiones(str,Enum):
    caribe = "Caribe"
    amazonia = "Amazonia"
    pacifico = "Pacífico"
    orinoquia = "Orinoquía"
    andina = "Andina"
    insular = "Insular"
    

class Datainput(BaseModel):
    habs: int
    baños: int
    m2: float
    region: Regiones