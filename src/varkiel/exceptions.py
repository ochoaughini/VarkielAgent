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

Custom exceptions for the Varkiel system.
"""


class GovernanceError(Exception):
    """Exception raised for governance constraint violations."""
    pass


class SafetyViolationError(Exception):
    """Exception raised when safety thresholds are violated."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details or message


class CoherenceError(Exception):
    """Exception raised for coherence violations."""
    pass


class StructuralConstraintError(Exception):
    """Exception raised when structural constraints are violated."""
    pass
