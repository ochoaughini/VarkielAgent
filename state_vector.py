import numpy as np

class StateVector:
    """Represents a state vector with additional metadata."""
    
    def __init__(self, data: np.ndarray, coherence_level: float):
        self.data = data
        self.coherence_level = coherence_level
        
    def __getattr__(self, name):
        # Delegate attribute access to the underlying array
        if hasattr(self.data, name):
            return getattr(self.data, name)
        raise AttributeError(f"'StateVector' object has no attribute '{name}'")
        
    def __getitem__(self, index):
        return self.data[index]
        
    def __setitem__(self, index, value):
        self.data[index] = value
        
    def __array__(self):
        # Support numpy operations
        return np.asarray(self.data)
        
    def __repr__(self):
        return f"StateVector(data={self.data}, coherence={self.coherence_level})"
