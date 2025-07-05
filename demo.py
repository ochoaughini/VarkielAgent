import sys
import site
sys.path.append("/Users/guto.ochoa/Desktop/VarkielAgent-main/Constraint-Lattice")
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from embedding import SymbolicEmbedder
from central_controller import StructuralConstraintEngine, CentralController, RecursiveInvarianceMonitor
from symbolic_coherence_engine import SymbolicCoherenceEngine
from phenomenological_tracker import PhenomenologicalTracker
from symbolic_interpreter import SymbolicInterpreter
from state_manager import StateManager
from coherence_monitor import CoherenceMonitor
from symbolic_articulator import SymbolicArticulator
from memory_stream import MemoryStream
from introspective_layer import IntrospectiveLayer
from utils import expand_vector
from constraint_lattice_adapter import ConstraintLatticeWrapper

# Add site-packages to path
site_packages = site.getsitepackages()
if site_packages:
    sys.path.extend(site_packages)

# Sample constraint functions
def normalize(state):
    """Normalize the state vector"""
    norm = np.linalg.norm(state)
    return state / norm if norm > 0 else state

def clip_values(state, min_val=-1.0, max_val=1.0):
    """Clip state values to [min_val, max_val] range"""
    return np.clip(state, min_val, max_val)

# Initialize vectorizer with a small corpus
vectorizer = TfidfVectorizer(max_features=256)
vectorizer.fit([
    "hello world",
    "goodbye world",
    "how are you",
    "what is your name",
    "the quick brown fox",
    "jumps over the lazy dog"
])

def vectorize_input(text):
    """Convert text to vector using TF-IDF"""
    vector = vectorizer.transform([text]).toarray()[0]
    return vector

def plot_resonance_history(history):
    """Plot the resonance history"""
    if not history:
        print("No resonance history to plot")
        return
    
    plt.figure(figsize=(10, 5))
    plt.plot(history)
    plt.title("Resonance History")
    plt.xlabel("Input Step")
    plt.ylabel("Resonance Value")
    plt.grid(True)
    plt.show()

class DemoCLI:
    def __init__(self):
        self.embedder = SymbolicEmbedder()
        self.history = []
        self.resonance_history = []  # Initialize here
        self.narrative_coherence_score = 1.0
        self.commands = {
            "!exit": self.exit,
            "!weights": self.update_weights,
            "!reset": self.reset_suspension,
            "!visualize": self.plot_resonance_history,
            "!help": self.help,
            "!narrative": self.display_narrative_coherence,
            "!map": self.plot_lattice_trajectory
        }
        
    def run(self):
        print("VarkielAgent CLI - Enhanced Narrative Mode")
        print("Type 'exit' to quit\n")
        
        while True:
            try:
                user_input = input("Varkiel> ")
                if user_input.lower() == 'exit':
                    print("Exiting...")
                    break
                self.history.append(user_input)
                
                # Update narrative coherence
                if len(self.history) > 1:
                    prev_embed = self.embedder.embed_text(self.history[-2])
                    curr_embed = self.embedder.embed_text(user_input)
                    self.narrative_coherence_score = cosine_similarity([prev_embed], [curr_embed])[0][0]
                    
                if user_input == "!narrative":
                    print(f"Current coherence: {self.narrative_coherence_score:.2f}")
                
                if user_input.startswith('!'):
                    # Handle commands
                    command = user_input.split()[0]
                    if command in self.commands:
                        self.commands[command](user_input)
                    else:
                        print("Unknown command. Type '!help' for available commands.")
                else:
                    # Process natural language input
                    input_vector = vectorize_input(user_input)
                    if hasattr(self, 'controller'):
                        output = self.controller.process_input(input_vector)
                        if output is not None:
                            self.resonance_history.append(np.linalg.norm(output))
                            print(f"Output: {output}")
                            
                            # Interpret and evaluate
                            symbols = interpreter.vector_to_symbols(output, top_k=2)
                            coherence = coherence_monitor.evaluate(output)
                            
                            # Record episode
                            state_manager.record_episode(user_input, output, symbols)
                            
                            # Display interpretation
                            print(f"Symbolic interpretation: {symbols}")
                            print(f"Coherence: {coherence:.2f}")
                            
                            # Generate narrative and reflection
                            narrative = articulator.vector_to_narrative(output)
                            memory_stream.record(user_input, output, narrative)
                            reflection = introspector.generate_reflection(output, narrative)
                            
                            print(f"\nNarrative: {narrative}")
                            print(f"Reflection: {reflection}\n")
                            
                            # Autonomous weight adjustment based on reflection
                            if "diverges" in reflection:
                                # Increase phenomenological weight for novel experiences
                                new_weights = (
                                    self.controller.weights[0] * 0.9,
                                    self.controller.weights[1] * 0.9,
                                    self.controller.weights[2] * 1.2
                                )
                                total = sum(new_weights)
                                self.controller.weights = (new_weights[0]/total, new_weights[1]/total, new_weights[2]/total)
                                print(f"Adjusted weights to {self.controller.weights} based on novel experience")
                    else:
                        print("System suspended. Use '!reset' to reactivate.")
                        # Automatic recovery: adjust weights and reset
                        self.controller.weights = (0.5, 0.3, 0.2)
                        self.controller.reset_suspension()
                        print("Automatic recovery: weights adjusted and suspension reset.")
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            
            # After exiting, show symbolic trajectory
        print("\nFinal Symbolic Trajectory:")
        for i, region in enumerate(phenom_tracker.symbolic_region_history):
            print(f"Step {i}: {region}")
        
    def exit(self, _):
        """Exit the demo"""
        print("Exiting demo")
        sys.exit(0)
        
    def update_weights(self, user_input):
        """Update weights"""
        new_weights = input("Enter weights (structural,symbolic,phenomenological): ")
        try:
            weights = tuple(map(float, new_weights.split(',')))
            self.controller.weights = weights
            print(f"Weights updated: {self.controller.weights}")
        except:
            print("Invalid weights format. Use: 0.4,0.4,0.2")
            
    def reset_suspension(self, _):
        """Reset suspension"""
        self.controller.reset_suspension()
        print("Suspension reset")
        
    def plot_resonance_history(self, _):
        """Plot resonance history"""
        plot_resonance_history(self.resonance_history)
        print("Plot displayed")
        
    def help(self, _):
        """Display help"""
        print("Available commands:")
        print("  !weights - Adjust cognitive engine weights")
        print("  !reset   - Reset suspension state")
        print("  !visualize - Plot resonance history")
        print("  !exit    - Exit the demo")
        print("  !help    - Show this help")
        print("  !narrative - Display current narrative coherence")
        print("  !map     - Plot symbolic zone positions from recent resonance history")
        
    def display_narrative_coherence(self, _):
        """Display narrative coherence"""
        print(f"Current coherence: {self.narrative_coherence_score:.2f}")
        
    def plot_lattice_trajectory(self):
        """Plot symbolic zone positions from recent resonance history"""
        if not hasattr(phenom_tracker, 'symbolic_region_history') or not phenom_tracker.symbolic_region_history:
            print("No symbolic region data available")
            return
            
        # Simple visualization of the last 10 regions
        regions = [list(coords.keys())[0] for coords in phenom_tracker.symbolic_region_history[-10:]]
        print(f"Recent symbolic trajectory: {' → '.join(regions)}")
        
def run_demo():
    """Run interactive demo with weight adjustment"""
    # Initialize structural engine with ConstraintLattice
    lattice_wrapper = ConstraintLatticeWrapper("Constraint-Lattice/lattice_schema.json")
    structural_engine = StructuralConstraintEngine(lattice_wrapper)
    
    # Initialize engines with required arguments
    coherence_engine = SymbolicCoherenceEngine(input_dim=256)  # Example input_dim
    phenom_tracker = PhenomenologicalTracker(lattice_wrapper=lattice_wrapper)
    monitor = RecursiveInvarianceMonitor()
    
    # Create controller with engines
    controller = CentralController(
        structural_engine,
        coherence_engine,
        phenom_tracker,
        monitor
    )
    
    # Initialize components
    symbol_map = {
        "existence": np.pad(np.array([0.8, 0.2, 0.1]), (0, 125), 'constant'),
        "consciousness": np.pad(np.array([0.1, 0.9, 0.3]), (0, 125), 'constant'),
        "perception": np.pad(np.array([0.3, 0.4, 0.8]), (0, 125), 'constant'),
        "reality": np.pad(np.array([0.7, 0.5, 0.2]), (0, 125), 'constant'),
        "being": np.pad(np.array([0.9, 0.1, 0.4]), (0, 125), 'constant'),
    }
    interpreter = SymbolicInterpreter(symbol_map)
    state_manager = StateManager()
    coherence_monitor = CoherenceMonitor()
    
    archetype_map = {
        "Being": expand_vector(np.array([0.9, 0.1, 0.2])),
        "Consciousness": expand_vector(np.array([0.1, 0.9, 0.3])),
        "Time": expand_vector(np.array([0.3, 0.4, 0.8])),
        "Nothingness": expand_vector(np.array([0.7, 0.2, 0.5])),
        "Freedom": expand_vector(np.array([0.2, 0.6, 0.7])),
    }
    articulator = SymbolicArticulator(archetype_map)
    memory_stream = MemoryStream()
    introspector = IntrospectiveLayer(memory_stream)
    
    cli = DemoCLI()
    cli.controller = controller
    cli.run()

if __name__ == "__main__":
    run_demo()
