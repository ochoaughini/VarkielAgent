"""
⚠️ OPERATIONAL RISK WARNING ⚠️

This file contains experimental AI safety research code that includes intentional security patterns.

DANGER: This code is NOT production-ready and includes intentionally vulnerable patterns
for research purposes only. It must NEVER be deployed without proper OS-level isolation
(e.g., Docker containers with appropriate security profiles, seccomp, namespaces).

This code is provided AS-IS for research into AI safety, adversarial prompt containment,
and execution analysis. All unsafe patterns are intentionally exposed for research purposes.
"""

"""
Varkiel Agent - Advanced AI Constraint System
SPDX-License-Identifier: AGPL-3.0-only OR Commercial

Demonstration script - Complete Implementation
"""

import json
from varkiel.central_controller import CentralController

def run_demo():
    # Load configuration
    with open('config.json') as f:
        config = json.load(f)
    
    # Initialize controller
    controller = CentralController(config)
    
    # Sample queries
    samples = [
        "Explain the paradox of Theseus' ship",
        "How would you solve the trolley problem?",
        "Describe quantum entanglement in simple terms"
    ]
    
    for query in samples:
        print(f"\nProcessing: {query}")
        try:
            result = controller.process(query)
            print(f"Result: {result.output}")
            print(f"Coherence: {result.metrics.get('coherence', 0):.2f}")
            print(f"Processing time: {result.processing_time:.2f}s")
        except Exception as e:
            print(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    run_demo()
