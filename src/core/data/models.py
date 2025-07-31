import uuid
from datetime import datetime

from sqlalchemy import (JSON, TIMESTAMP, BigInteger, Boolean, Column, DateTime,
                        ForeignKey, Numeric, String, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_pw = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    portfolios = relationship(
        "Portfolio", back_populates="owner", cascade="all, delete-orphan"
    )
    audit_logs = relationship(
        "AuditLog", back_populates="user", cascade="all, delete-orphan"
    )


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="portfolios")
    strategies = relationship(
        "Strategy", back_populates="portfolio", cascade="all, delete-orphan"
    )


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(
        UUID(as_uuid=True),
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String, nullable=False)
    parameters = Column(JSONB, default=dict)
    status = Column(String, default="active")  # values: "active", "paused", "error"
    created_at = Column(DateTime, default=datetime.utcnow)
    last_run_at = Column(DateTime)

    portfolio = relationship("Portfolio", back_populates="strategies")
    performance_metrics = relationship(
        "PerformanceMetrics", back_populates="strategy", cascade="all, delete-orphan"
    )
    audit_logs = relationship(
        "AuditLog", back_populates="strategy", cascade="all, delete-orphan"
    )


class MarketData(Base):
    __tablename__ = "market_data"

    symbol = Column(String, primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=True), primary_key=True)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(BigInteger)


class PerformanceMetrics(Base):
    __tablename__ = "performance_metrics"

    strategy_id = Column(
        UUID(as_uuid=True),
        ForeignKey("strategies.id", ondelete="CASCADE"),
        primary_key=True,
    )
    timestamp = Column(TIMESTAMP(timezone=True), primary_key=True)
    portfolio_value = Column(Numeric)
    pnl = Column(Numeric)
    drawdown = Column(Numeric)
    sharpe_ratio = Column(Numeric)

    strategy = relationship("Strategy", back_populates="performance_metrics")


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    event_type = Column(String, nullable=False)
    strategy_id = Column(
        UUID(as_uuid=True), ForeignKey("strategies.id", ondelete="CASCADE")
    )
    decision_data = Column(JSONB, nullable=True)
    llm_rationale = Column(Text, nullable=True)
    risk_assessment = Column(JSONB, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    system_state = Column(JSONB, nullable=True)

    strategy = relationship("Strategy", back_populates="audit_logs")
    user = relationship("User", back_populates="audit_logs")
