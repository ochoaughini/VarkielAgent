import numpy as np
from typing import Any

class StateVector:
    """Represents a state vector with coherence tracking."""
    
    def __init__(self, state: np.ndarray, coherence: float):
        self.state = state
        self.coherence = coherence  # Explicit coherence attribute
        
    def __getattr__(self, name):
        # Delegate attribute access to the underlying array
        if hasattr(self.state, name):
            return getattr(self.state, name)
        raise AttributeError(f"'StateVector' object has no attribute '{name}'")
        
    def __getitem__(self, index):
        return self.state[index]
        
    def __setitem__(self, index, value):
        self.state[index] = value
        
    def __array__(self) -> np.ndarray:
        # Support numpy operations
        return np.asarray(self.state)
        
    def __repr__(self) -> str:
        return f"StateVector(coherence={self.coherence:.2f}, state={self.state})"
        
    def __len__(self) -> int:
        return len(self.state)
        
    def tolist(self) -> list:
        return self.state.tolist()
