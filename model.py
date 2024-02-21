from typing import List, Optional

from sqlalchemy import (
    BigInteger, 
    CheckConstraint, 
    Column, 
    Double, 
    ForeignKeyConstraint, 
    Index, 
    Integer, 
    String, 
    Text, 
    text
)
from sqlalchemy.dialects.mysql import MEDIUMTEXT, TINYINT
from sqlalchemy.orm import (
    Mapped, 
    DeclarativeBase, 
    mapped_column, 
    relationship
)
from sqlalchemy.orm.base import Mapped


class Base(DeclarativeBase):
    pass


class Experiments(Base):
    __tablename__ = 'experiments'
    __table_args__ = (
        CheckConstraint("(`lifecycle_stage` in (_utf8mb3'active',_utf8mb3'deleted'))", name='experiments_lifecycle_stage'),
        Index('name', 'name', unique=True)
    )

    experiment_id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(256), nullable=False)
    artifact_location = mapped_column(String(256))
    lifecycle_stage = mapped_column(String(32))
    creation_time = mapped_column(BigInteger)
    last_update_time = mapped_column(BigInteger)

    datasets: Mapped[List['Datasets']] = relationship('Datasets', uselist=True, back_populates='experiment')
    experiment_tags: Mapped[List['ExperimentTags']] = relationship('ExperimentTags', uselist=True, back_populates='experiment')
    runs: Mapped[List['Runs']] = relationship('Runs', uselist=True, back_populates='experiment')


class InputTags(Base):
    __tablename__ = 'input_tags'

    input_uuid = mapped_column(String(36), primary_key=True, nullable=False)
    name = mapped_column(String(255), primary_key=True, nullable=False)
    value = mapped_column(String(500), nullable=False)


class Inputs(Base):
    __tablename__ = 'inputs'
    __table_args__ = (
        Index('index_inputs_destination_type_destination_id_source_type', 'destination_type', 'destination_id', 'source_type'),
        Index('index_inputs_input_uuid', 'input_uuid')
    )

    input_uuid = mapped_column(String(36), nullable=False)
    source_type = mapped_column(String(36), primary_key=True, nullable=False)
    source_id = mapped_column(String(36), primary_key=True, nullable=False)
    destination_type = mapped_column(String(36), primary_key=True, nullable=False)
    destination_id = mapped_column(String(36), primary_key=True, nullable=False)


class RegisteredModels(Base):
    __tablename__ = 'registered_models'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    name = mapped_column(String(256), primary_key=True)
    creation_time = mapped_column(BigInteger)
    last_updated_time = mapped_column(BigInteger)
    description = mapped_column(String(5000))

    model_versions: Mapped[List['ModelVersions']] = relationship('ModelVersions', uselist=True, back_populates='registered_models')
    registered_model_aliases: Mapped[List['RegisteredModelAliases']] = relationship('RegisteredModelAliases', uselist=True, back_populates='registered_models')
    registered_model_tags: Mapped[List['RegisteredModelTags']] = relationship('RegisteredModelTags', uselist=True, back_populates='registered_models')


class Datasets(Base):
    __tablename__ = 'datasets'
    __table_args__ = (
        ForeignKeyConstraint(['experiment_id'], ['experiments.experiment_id'], name='datasets_ibfk_1'),
        Index('index_datasets_dataset_uuid', 'dataset_uuid'),
        Index('index_datasets_experiment_id_dataset_source_type', 'experiment_id', 'dataset_source_type')
    )

    dataset_uuid = mapped_column(String(36), nullable=False)
    experiment_id = mapped_column(Integer, primary_key=True, nullable=False)
    name = mapped_column(String(500), primary_key=True, nullable=False)
    digest = mapped_column(String(36), primary_key=True, nullable=False)
    dataset_source_type = mapped_column(String(36), nullable=False)
    dataset_source = mapped_column(Text, nullable=False)
    dataset_schema = mapped_column(Text)
    dataset_profile = mapped_column(MEDIUMTEXT)

    experiment: Mapped['Experiments'] = relationship('Experiments', back_populates='datasets')


class ExperimentTags(Base):
    __tablename__ = 'experiment_tags'
    __table_args__ = (
        ForeignKeyConstraint(['experiment_id'], ['experiments.experiment_id'], name='experiment_tags_ibfk_1'),
        Index('experiment_id', 'experiment_id')
    )

    key = mapped_column(String(250), primary_key=True, nullable=False)
    experiment_id = mapped_column(Integer, primary_key=True, nullable=False)
    value = mapped_column(String(5000))

    experiment: Mapped['Experiments'] = relationship('Experiments', back_populates='experiment_tags')


class ModelVersions(Base):
    __tablename__ = 'model_versions'
    __table_args__ = (
        ForeignKeyConstraint(['name'], ['registered_models.name'], onupdate='CASCADE', name='model_versions_ibfk_1'),
    )

    name = mapped_column(String(256), primary_key=True, nullable=False)
    version = mapped_column(Integer, primary_key=True, nullable=False)
    creation_time = mapped_column(BigInteger)
    last_updated_time = mapped_column(BigInteger)
    description = mapped_column(String(5000))
    user_id = mapped_column(String(256))
    current_stage = mapped_column(String(20))
    source = mapped_column(String(500))
    run_id = mapped_column(String(32))
    status = mapped_column(String(20))
    status_message = mapped_column(String(500))
    run_link = mapped_column(String(500))
    storage_location = mapped_column(String(500))

    registered_models: Mapped['RegisteredModels'] = relationship('RegisteredModels', back_populates='model_versions')
    model_version_tags: Mapped[List['ModelVersionTags']] = relationship('ModelVersionTags', uselist=True, back_populates='model_versions')


class RegisteredModelAliases(Base):
    __tablename__ = 'registered_model_aliases'
    __table_args__ = (
        ForeignKeyConstraint(['name'], ['registered_models.name'], ondelete='CASCADE', onupdate='CASCADE', name='registered_model_alias_name_fkey'),
    )

    alias = mapped_column(String(256), primary_key=True, nullable=False)
    version = mapped_column(Integer, nullable=False)
    name = mapped_column(String(256), primary_key=True, nullable=False)

    registered_models: Mapped['RegisteredModels'] = relationship('RegisteredModels', back_populates='registered_model_aliases')


class RegisteredModelTags(Base):
    __tablename__ = 'registered_model_tags'
    __table_args__ = (
        ForeignKeyConstraint(['name'], ['registered_models.name'], onupdate='CASCADE', name='registered_model_tags_ibfk_1'),
        Index('name', 'name')
    )

    key = mapped_column(String(250), primary_key=True, nullable=False)
    name = mapped_column(String(256), primary_key=True, nullable=False)
    value = mapped_column(String(5000))

    registered_models: Mapped['RegisteredModels'] = relationship('RegisteredModels', back_populates='registered_model_tags')


class Runs(Base):
    __tablename__ = 'runs'
    __table_args__ = (
        CheckConstraint("(`lifecycle_stage` in (_utf8mb3'active',_utf8mb3'deleted'))", name='runs_lifecycle_stage'),
        CheckConstraint("(`source_type` in (_utf8mb3'NOTEBOOK',_utf8mb3'JOB',_utf8mb3'LOCAL',_utf8mb3'UNKNOWN',_utf8mb3'PROJECT'))", name='source_type'),
        CheckConstraint("(`status` in (_utf8mb3'SCHEDULED',_utf8mb3'FAILED',_utf8mb3'FINISHED',_utf8mb3'RUNNING',_utf8mb3'KILLED'))", name='runs_chk_1'),
        ForeignKeyConstraint(['experiment_id'], ['experiments.experiment_id'], name='runs_ibfk_1'),
        Index('experiment_id', 'experiment_id')
    )

    run_uuid = mapped_column(String(32), primary_key=True)
    name = mapped_column(String(250))
    source_type = mapped_column(String(20))
    source_name = mapped_column(String(500))
    entry_point_name = mapped_column(String(50))
    user_id = mapped_column(String(256))
    status = mapped_column(String(9))
    start_time = mapped_column(BigInteger)
    end_time = mapped_column(BigInteger)
    source_version = mapped_column(String(50))
    lifecycle_stage = mapped_column(String(20))
    artifact_uri = mapped_column(String(200))
    experiment_id = mapped_column(Integer)
    deleted_time = mapped_column(BigInteger)

    experiment: Mapped[Optional['Experiments']] = relationship('Experiments', back_populates='runs')
    latest_metrics: Mapped[List['LatestMetrics']] = relationship('LatestMetrics', uselist=True, back_populates='runs')
    metrics: Mapped[List['Metrics']] = relationship('Metrics', uselist=True, back_populates='runs')
    params: Mapped[List['Params']] = relationship('Params', uselist=True, back_populates='runs')
    tags: Mapped[List['Tags']] = relationship('Tags', uselist=True, back_populates='runs')


class LatestMetrics(Base):
    __tablename__ = 'latest_metrics'
    __table_args__ = (
        CheckConstraint('(`is_nan` in (0,1))', name='latest_metrics_chk_1'),
        ForeignKeyConstraint(['run_uuid'], ['runs.run_uuid'], name='latest_metrics_ibfk_1'),
        Index('index_latest_metrics_run_uuid', 'run_uuid')
    )

    key = mapped_column(String(250), primary_key=True, nullable=False)
    value = mapped_column(Double(asdecimal=True), nullable=False)
    step = mapped_column(BigInteger, nullable=False)
    is_nan = mapped_column(TINYINT(1), nullable=False)
    run_uuid = mapped_column(String(32), primary_key=True, nullable=False)
    timestamp = mapped_column(BigInteger)

    runs: Mapped['Runs'] = relationship('Runs', back_populates='latest_metrics')


class Metrics(Base):
    __tablename__ = 'metrics'
    __table_args__ = (
        CheckConstraint('(`is_nan` in (0,1))', name='metrics_chk_1'),
        CheckConstraint('(`is_nan` in (0,1))', name='metrics_chk_2'),
        ForeignKeyConstraint(['run_uuid'], ['runs.run_uuid'], name='metrics_ibfk_1'),
        Index('index_metrics_run_uuid', 'run_uuid')
    )

    key = mapped_column(String(250), primary_key=True, nullable=False)
    value = mapped_column(Double(asdecimal=True), primary_key=True, nullable=False)
    timestamp = mapped_column(BigInteger, primary_key=True, nullable=False)
    run_uuid = mapped_column(String(32), primary_key=True, nullable=False)
    step = mapped_column(BigInteger, primary_key=True, nullable=False, server_default=text("'0'"))
    is_nan = mapped_column(TINYINT(1), primary_key=True, nullable=False, server_default=text("'0'"))

    runs: Mapped['Runs'] = relationship('Runs', back_populates='metrics')


class ModelVersionTags(Base):
    __tablename__ = 'model_version_tags'
    __table_args__ = (
        ForeignKeyConstraint(['name', 'version'], ['model_versions.name', 'model_versions.version'], onupdate='CASCADE', name='model_version_tags_ibfk_1'),
        Index('name', 'name', 'version')
    )

    key = mapped_column(String(250), primary_key=True, nullable=False)
    name = mapped_column(String(256), primary_key=True, nullable=False)
    version = mapped_column(Integer, primary_key=True, nullable=False)
    value = mapped_column(String(5000))

    model_versions: Mapped['ModelVersions'] = relationship('ModelVersions', back_populates='model_version_tags')


class Params(Base):
    __tablename__ = 'params'
    __table_args__ = (
        ForeignKeyConstraint(['run_uuid'], ['runs.run_uuid'], name='params_ibfk_1'),
        Index('index_params_run_uuid', 'run_uuid')
    )

    key = mapped_column(String(250), primary_key=True, nullable=False)
    value = mapped_column(String(8000), nullable=False)
    run_uuid = mapped_column(String(32), primary_key=True, nullable=False)

    runs: Mapped['Runs'] = relationship('Runs', back_populates='params')


class Tags(Base):
    __tablename__ = 'tags'
    __table_args__ = (
        ForeignKeyConstraint(['run_uuid'], ['runs.run_uuid'], name='tags_ibfk_1'),
        Index('index_tags_run_uuid', 'run_uuid')
    )

    key = mapped_column(String(250), primary_key=True, nullable=False)
    run_uuid = mapped_column(String(32), primary_key=True, nullable=False)
    value = mapped_column(String(5000))

    runs: Mapped['Runs'] = relationship('Runs', back_populates='tags')
