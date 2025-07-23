"""
⚠️ OPERATIONAL RISK WARNING ⚠️

This file contains experimental AI safety research code that includes intentional security patterns.

DANGER: This code is NOT production-ready and includes intentionally vulnerable patterns
for research purposes only. It must NEVER be deployed without proper OS-level isolation
(e.g., Docker containers with appropriate security profiles, seccomp, namespaces).

This code is provided AS-IS for research into AI safety, adversarial prompt containment,
and execution analysis. All unsafe patterns are intentionally exposed for research purposes.
"""

from central_controller import CentralController
from structural_constraint_engine import StructuralConstraintEngine
from constraint_lattice_adapter import ConstraintLatticeAdapter
from semantic_resonance import FormStateVector

if __name__ == "__main__":
    # Initialize components
    constraint_lattice = ConstraintLatticeAdapter()
    structural_engine = StructuralConstraintEngine(constraint_lattice)
    
    # Initialize controller
    controller = CentralController(
        structural_engine=structural_engine,
        coherence_engine=structural_engine,  # Using same engine for simplicity
        phenomenological_tracker=FormStateVector(),
        recursive_invariance_monitor=structural_engine
    )
    
    # Run interactive session
    while True:
        prompt = input("User: ")
        if prompt.lower() in ['exit', 'quit']:
            break
        response = controller.process_query(prompt)
        print(f"System: {response}")
