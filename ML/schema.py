from pydantic import BaseModel
from enum import Enum

class Regiones(str,Enum):
    caribe = "Caribe"
    amazonia = "Amazonia"
    pacifico = "Pacífico"
    orinoquia = "Orinoquía"
    andina = "Andina"
    insular = "Insular"
    

class Testinput(BaseModel):
    habs: int
    baños: int
    m2: int
    region: Regiones