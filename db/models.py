import sqlalchemy.sql
from sqlalchemy import text, Column, Integer, String, DateTime, Boolean, SmallInteger, UniqueConstraint, Index, REAL, Numeric, PrimaryKeyConstraint
from database import Base

class VMInventory(Base):
    __tablename__ = 'instances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # customer = Column(String, default='CCS')
    #region = Column(String, CheckConstraint("region IN ('KR', 'EU', 'NA')"), default='KR')
    # region = Column(String, default='EU')
    project_id = Column(String, default='')

    instance_id = Column(String, default='')  # Specify default value for all columns
    instance_name = Column(String, default='')  # Specify default value for all columns
    status = Column(String, default='')
    flavor = Column(String, default='')
    address = Column(String, default='')
    
    availability_zone = Column(String, default='')
    hostname = Column(String, default='')
    vm_created_at = Column(DateTime, default='')
    vm_updated_at = Column(DateTime, default='')

    created_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최초생성일시
    updated_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최종수정일시
    __table_args__ = (
        UniqueConstraint("instance_id", name="unq_instances"),
    )

class AggInstances(Base):
    __tablename__ = 'agg_instances'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 시리얼아이디
    year = Column(String(length=4), nullable=False)  # 발생년도
    month = Column(String(length=2), nullable=False)  # 발생월
    day = Column(String(length=2), nullable=False)  # 발생일
    project_id = Column(String(length=50), nullable=False)  # 운영계/검증계

    count = Column(Integer, nullable=False)  # 수량

    created_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최초생성일시
    updated_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최종수정일시
    __table_args__ = (
        Index("idx_agg_instances", "year", "month", "day"),
    )

class AddedInstances(Base):
    __tablename__ = 'added_instances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String(length=4), nullable=False)  # 발생년도
    month = Column(String(length=2), nullable=False)  # 발생월
    day = Column(String(length=2), nullable=False)  # 발생일
    project_id = Column(String, default='')

    instance_id = Column(String, default='')  # Specify default value for all columns
    instance_name = Column(String, default='')  # Specify default value for all columns
    status = Column(String, default='')
    flavor = Column(String, default='')
    address = Column(String, default='')
    
    availability_zone = Column(String, default='')
    hostname = Column(String, default='')
    vm_created_at = Column(DateTime, default='')
    vm_updated_at = Column(DateTime, default='')

    created_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최초생성일시
    updated_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최종수정일시
    __table_args__ = (
        Index("idx_added_instances", "year", "month", "day"),
    )

class DeletedInstances(Base):
    __tablename__ = 'deleted_instances'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String(length=4), nullable=False)  # 발생년도
    month = Column(String(length=2), nullable=False)  # 발생월
    day = Column(String(length=2), nullable=False)  # 발생일
    project_id = Column(String, default='')

    instance_id = Column(String, default='')  # Specify default value for all columns
    instance_name = Column(String, default='')  # Specify default value for all columns
    status = Column(String, default='')
    flavor = Column(String, default='')
    address = Column(String, default='')
    
    availability_zone = Column(String, default='')
    hostname = Column(String, default='')
    vm_created_at = Column(DateTime, default='')
    vm_updated_at = Column(DateTime, default='')

    created_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최초생성일시
    updated_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최종수정일시
    __table_args__ = (
        Index("idx_deleted_instances", "year", "month", "day"),
    )        

# ============================================================================================

class LBInventory(Base):
    __tablename__ = 'loadbalancers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant = Column(String, default='')

    ns_ip = Column(String, default='')
    lb_name = Column(String, default='')
    lb_vip = Column(String, default='')
    port = Column(Integer, default='')
    service_type = Column(String, default='')
    created_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최초생성일시
    updated_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최종수정일시
    
class AggLB(Base):
    __tablename__ = 'agg_loadbalancers'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 시리얼아이디
    year = Column(String(length=4), nullable=False)  # 발생년도
    month = Column(String(length=2), nullable=False)  # 발생월
    day = Column(String(length=2), nullable=False)  # 발생일
    tenant = Column(String(length=50), nullable=False)  # 운영계/검증계

    count = Column(Integer, nullable=False)  # 수량

    created_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최초생성일시
    updated_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최종수정일시
    __table_args__ = (
        Index("idx_agg_loadbalancers", "year", "month", "day"),
    )

class AddedLB(Base):
    __tablename__ = 'added_loadbalancers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String(length=4), nullable=False)  # 발생년도
    month = Column(String(length=2), nullable=False)  # 발생월
    day = Column(String(length=2), nullable=False)  # 발생일
    tenant = Column(String, default='')

    ns_ip = Column(String, default='')
    lb_name = Column(String, default='')
    lb_vip = Column(String, default='')
    port = Column(Integer, default='')
    service_type = Column(String, default='')

    created_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최초생성일시
    updated_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최종수정일시
    __table_args__ = (
        Index("idx_added_loadbalancers", "year", "month", "day"),
    )

class DeletedLB(Base):
    __tablename__ = 'deleted_loadbalancers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String(length=4), nullable=False)  # 발생년도
    month = Column(String(length=2), nullable=False)  # 발생월
    day = Column(String(length=2), nullable=False)  # 발생일
    tenant = Column(String, default='')

    ns_ip = Column(String, default='')
    lb_name = Column(String, default='')
    lb_vip = Column(String, default='')
    port = Column(Integer, default='')
    service_type = Column(String, default='')

    created_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최초생성일시
    updated_at = Column(
        DateTime, server_default=sqlalchemy.sql.func.now(), nullable=False)  # 최종수정일시
    __table_args__ = (
        Index("idx_deleted_loadbalancers", "year", "month", "day"),
    )

# ============================================================================================



