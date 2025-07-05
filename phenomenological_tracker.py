"""Phenomenological Tracker - Affect-state resonance modeling

This module models cognitive-affective dynamics by encoding memory
engrams as PatternResonanceVectors within a high-dimensional resonance
manifold. It maintains dimensional consistency across temporal slices.

Key Components:
- PatternResonanceVectors: Tracks memory states as resonance vectors
- State Projection: Maintains dimensional consistency

Performance Notes:
- Incremental SVD for dimensionality reduction
- Streaming updates for memory efficiency
"""
import numpy as np
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import IncrementalPCA
import uuid
import logging
from typing import Optional
from state_vector import StateVector  # Ensure this import exists

class PatternResonanceVectors:
    """Represents memory engrams as dynamically evolving resonance vectors.
    
    Attributes:
        vectors: Matrix of resonance vectors (n_vectors x dimension)
        decay_factor: Exponential decay factor for old memories
    """
    def __init__(self, dimension: int = 256, decay_factor: float = 0.01, lattice_wrapper=None):
        self.dimension = dimension
        self.decay_factor = decay_factor
        self.vectors = np.zeros((0, dimension))
        self.lattice_wrapper = lattice_wrapper
        self.symbolic_region_history = []
        
    def update(self, new_vector: np.ndarray):
        """Update resonance vectors with a new observation.
        
        Args:
            new_vector: New state vector to incorporate
        """
        if self.vectors.size == 0:
            self.vectors = new_vector[np.newaxis, :]
        else:
            # Apply decay to existing vectors
            self.vectors *= (1 - self.decay_factor)
            # Add new vector
            self.vectors = np.vstack([self.vectors, new_vector])
        if self.lattice_wrapper:
            symbolic_coordinates = self.lattice_wrapper.get_symbolic_coordinates(new_vector)
            self.symbolic_region_history.append(symbolic_coordinates)
            
    def project(self, target_dimension: int = 3) -> np.ndarray:
        """Project high-dimensional vectors to lower dimension for visualization.
        
        Args:
            target_dimension: Output dimension (typically 2 or 3)
            
        Returns:
            Projected vectors
        """
        if self.vectors.shape[0] == 0:
            return np.zeros((0, target_dimension))
            
        # Simple PCA projection for demonstration
        cov = np.cov(self.vectors, rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        return self.vectors @ eigenvectors[:, -target_dimension:]

class PhenomenologicalTracker:
    """Tracks phenomenological state across sessions"""
    
    def __init__(self, embedding_dim=768, latent_dim=128, lattice_wrapper=None) -> None:
        self.embedding_dim = embedding_dim
        self.latent_dim = latent_dim
        self.state_dim = embedding_dim
        # Initialize IncrementalPCA with dummy data to create components_
        # Use min(n_components, state_dim, batch_size) to avoid errors
        self.pca = IncrementalPCA(n_components=min(50, self.state_dim, 1000))
        # Generate dummy data with multiple samples (batch_size=10)
        dummy_data = np.random.rand(10, self.state_dim)
        self.pca.partial_fit(dummy_data)
        self.resonance_history = []
        self.session_history = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("Initialized PhenomenologicalTracker")
        self.current_session = str(uuid.uuid4())  # Start a new session by default
        self.valence_map = {self.current_session: []}  # Map session id to list of resonance vectors
        self.lattice_wrapper = lattice_wrapper

    def calibrate_space(self, embedding_matrix: np.ndarray):
        """Calibrate PCA with initial embeddings"""
        self.pca.partial_fit(embedding_matrix)
        
    def project_to_semantic_space(self, vector: np.ndarray) -> np.ndarray:
        """Project to calibrated phenomenological space"""
        return self.pca.transform(vector.reshape(1, -1))[0]
    
    def update_resonance(self, coherent_input: np.ndarray) -> np.ndarray:
        """Track phenomenological state and return the resonance vector for the current input"""
        try:
            projected = self.project_to_semantic_space(coherent_input)
            self.resonance_history.append(projected)
            # Maintain fixed-length history
            if len(self.resonance_history) > 1000:
                self.resonance_history.pop(0)
            # Ensure current session exists in valence_map
            if self.current_session not in self.valence_map:
                self.valence_map[self.current_session] = []
            self.valence_map[self.current_session].append(coherent_input)
            # Wrap state in StateVector class with coherence metadata
            return StateVector(coherent_input, coherence_level=0.8)
        except Exception as e:
            self.logger.error(f"State tracking failed: {str(e)}")
            return np.zeros((1,))

    def start_new_session(self, session_id: Optional[str] = None) -> str:
        """Start a new session, returns the session id"""
        if session_id is None:
            session_id = str(uuid.uuid4())
        self.current_session = session_id
        self.valence_map[session_id] = []
        return session_id

    def get_current_mood(self, session_id: Optional[str] = None) -> np.ndarray:
        """Compute the current mood as the average of the last 10 resonance vectors in the session"""
        if session_id is None:
            session_id = self.current_session
        vectors = self.valence_map.get(session_id, [])
        if not hasattr(self.pca, 'components_'):
            # Return a zero vector of target dimension if PCA not fitted
            return np.zeros(self.latent_dim)
        if not vectors:
            return np.zeros(1)  # Return a default vector of length 1 if no data
        # Return the average of the last 10 vectors
        last_vectors = vectors[-10:]
        avg_vector = np.mean(last_vectors, axis=0)
        return avg_vector

    def measure_affective_congruence(self, new_state: np.ndarray) -> np.ndarray:
        """Measure affective congruence between new state and resonance history"""
        if len(self.valence_map[self.current_session]) == 0:
            return np.array([0.0])
        
        # Compute cosine similarity against each resonance vector
        similarities = []
        for vec in self.valence_map[self.current_session]:
            sim = cosine_similarity([new_state], [vec])[0][0]
            similarities.append(sim)
        
        return np.array(similarities)

    def track_state(self, state: np.ndarray) -> None:
        """Track a state vector"""
        self.resonance_history.append(state)
        
        # Check if we have enough states to update
        if len(self.resonance_history) >= 1000:
            states = np.array(self.resonance_history[-1000:])
            
            # Update PCA
            self.pca.partial_fit(states)
            
            # Only compute if PCA is fitted
            if hasattr(self.pca, 'components_'):
                # Compute the projection on the principal components
                projection = self.pca.transform(states)
                
                # Compute the rate of change in the projection space
                if len(projection) > 1:
                    diff = np.diff(projection, axis=0)
                    velocity = np.linalg.norm(diff, axis=1).mean()
                    
                    # Update suspension level based on velocity
                    self.suspension_level = max(0.0, min(1.0, velocity * 10.0))
                    
                    # Log suspension level
                    self.logger.info(f"Suspension level updated: {self.suspension_level:.2f}")
                else:
                    self.logger.warning("Not enough states to compute velocity")
            else:
                self.logger.warning("PCA not fitted yet")
        else:
            self.logger.info(f"Collecting states: {len(self.resonance_history)}/1000")
