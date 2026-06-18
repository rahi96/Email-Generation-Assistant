"""
email_log.py - SQLAlchemy ORM Model for logging generated emails.

Every email generated via the /api/v1/email/generate endpoint is persisted
here for audit trail and history tracking.
"""

import json
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class EmailLog(Base):
    """ORM model representing a single generated email log entry."""

    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    intent = Column(String(500), nullable=False)
    key_facts = Column(Text, nullable=False)  # JSON-serialized list
    tone = Column(String(100), nullable=False)
    strategy = Column(String(50), nullable=False)
    generated_email = Column(Text, nullable=False)
    thinking = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def set_key_facts(self, facts: list[str]):
        """Serialize a list of key facts to JSON for storage."""
        self.key_facts = json.dumps(facts)

    def get_key_facts(self) -> list[str]:
        """Deserialize the stored JSON key facts back to a list."""
        return json.loads(self.key_facts) if self.key_facts else []

    def __repr__(self):
        return (
            f"<EmailLog(id={self.id}, intent='{self.intent[:40]}...', "
            f"strategy='{self.strategy}', created_at='{self.created_at}')>"
        )
