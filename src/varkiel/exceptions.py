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
    pass


class CoherenceError(Exception):
    """Exception raised for coherence violations."""
    pass


class StructuralConstraintError(Exception):
    """Exception raised when structural constraints are violated."""
    pass
