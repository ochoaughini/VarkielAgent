from state_vector import StateVector
from typing import Optional

class RiskBalancer:
    def __init__(self, coherence_threshold: float = 0.7):
        self.coherence_threshold = coherence_threshold
        
    def allow_inference(self, state_vector: StateVector) -> bool:
        """Determine if inference is allowed based on coherence."""
        return state_vector.coherence >= self.coherence_threshold
    
    def adjust_threshold(self, risk_level: float):
        self.coherence_threshold = max(0.5, min(0.9, 0.7 + (risk_level - 0.5) * 0.4))
