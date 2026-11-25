from dataclasses import dataclass


@dataclass
class EquationResponse:
    delta: float
    sol1: float|None
    sol2: float|None