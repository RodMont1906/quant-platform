from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.data.models import AuditLog


class AuditLogger:
    def __init__(self, db: Session):
        self.db = db

    def log_trade_decision(
        self,
        *,
        strategy_id: UUID,
        decision_data: dict,
        llm_rationale: str,
        risk_assessment: dict,
        user_id: UUID,
        system_state: dict
    ):
        log_entry = AuditLog(
            timestamp=datetime.utcnow(),
            event_type="TRADE_DECISION",
            strategy_id=strategy_id,
            decision_data=decision_data,
            llm_rationale=llm_rationale,
            risk_assessment=risk_assessment,
            user_id=user_id,
            system_state=system_state,
        )
        self.db.add(log_entry)
        self.db.commit()
