from .database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, Numeric
from datetime import date as date_type
from decimal import Decimal
from typing import List

class Fund(Base):
    __tablename__ = "funds"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    vintage_year: Mapped[int] = mapped_column(nullable=False)

    # back_populates is used to define the reverse relationship in the related model, 
    # cascade="all, delete-orphan" means that when a Fund is deleted, all related CashFlow and NavSnapshot records will also be deleted
    nav_snapshots: Mapped[List["NavSnapshot"]] = relationship("NavSnapshot", back_populates="fund", cascade="all, delete-orphan")
    cash_flows: Mapped[List["CashFlowEvent"]] = relationship("CashFlowEvent", back_populates="fund", cascade="all, delete-orphan")


class CashFlowEvent(Base):
    __tablename__ = "cash_flow_events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    fund_id: Mapped[int] = mapped_column(ForeignKey("funds.id"), nullable=False)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)  # Assuming 12 digits total, 2 after the decimal

    fund: Mapped["Fund"] = relationship("Fund", back_populates="cash_flows")

class NavSnapshot(Base):
    __tablename__ = "nav_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    fund_id: Mapped[int] = mapped_column(ForeignKey("funds.id"), nullable=False)
    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)  # Assuming 12 digits total, 2 after the decimal

    fund: Mapped["Fund"] = relationship("Fund", back_populates="nav_snapshots")
