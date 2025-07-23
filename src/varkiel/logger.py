"""
⚠️ OPERATIONAL RISK WARNING ⚠️

This file contains experimental AI safety research code that includes intentional security patterns.

DANGER: This code is NOT production-ready and includes intentionally vulnerable patterns
for research purposes only. It must NEVER be deployed without proper OS-level isolation
(e.g., Docker containers with appropriate security profiles, seccomp, namespaces).

This code is provided AS-IS for research into AI safety, adversarial prompt containment,
and execution analysis. All unsafe patterns are intentionally exposed for research purposes.
"""

import logging

# Create a shared logger instance
logger = logging.getLogger('varkiel')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('varkiel.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ReflectiveLogger:
    def __init__(self):
        self.logger = logging.getLogger('reflective')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('reflective.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def log_decision(self, decision_data):
        self.logger.info(decision_data)
