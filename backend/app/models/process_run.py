from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.connection import Base


class ProcessRun(Base):
    __tablename__ = "process_runs"

    id = Column(Integer, primary_key=True, index=True)

    pipeline_id = Column(
        Integer,
        ForeignKey("pipelines.id"),
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="running"
    )

    start_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    end_time = Column(
        DateTime,
        nullable=True
    )

    error_message = Column(
        String,
        nullable=True
    )


