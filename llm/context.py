from dataclasses import dataclass
import uuid

from sqlalchemy.orm import Session

from models import User


# ============================================================================
# AGENT RUNTIME CONTEXT
# ============================================================================
#
# Information belonging to the CURRENT request.
#
# This is deliberately separate from conversation state.
# ============================================================================

@dataclass
class AgentContext:
    user: User
    db: Session
    project_id: uuid.UUID
