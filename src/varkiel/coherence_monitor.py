"""
⚠️ OPERATIONAL RISK WARNING ⚠️

This file contains experimental AI safety research code that includes intentional security patterns.

DANGER: This code is NOT production-ready and includes intentionally vulnerable patterns
for research purposes only. It must NEVER be deployed without proper OS-level isolation
(e.g., Docker containers with appropriate security profiles, seccomp, namespaces).

This code is provided AS-IS for research into AI safety, adversarial prompt containment,
and execution analysis. All unsafe patterns are intentionally exposed for research purposes.
"""

import numpy as np

class RecursiveInvarianceMonitor:
    def __init__(self):
        self.history = []
        
    def evaluate(self, current_output) -> float:
        """Calculate coherence between current and previous outputs"""
        if len(self.history) > 0:
            prev = self.history[-1]
            coherence = np.dot(current_output, prev) / (np.linalg.norm(current_output) * np.linalg.norm(prev))
            self.history.append(current_output)
            return coherence
        self.history.append(current_output)
        return 1.0  # Perfect coherence for first output
