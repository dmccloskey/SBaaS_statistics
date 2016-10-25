from SBaaS_base.postgresql_orm_base import *
'''
USE CASES
1. pipeline for an individual analysis
2. pipeline for a group of individual analyses
'''
class data_stage02_quantification_analysis(Base):
    __tablename__ = 'data_stage02_quantification_analysis'
    id = Column(Integer, Sequence('data_stage02_quantification_analysis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    #time_point_units = Column(String(50))
    experiment_type = Column(String(50))
    analysis_type = Column(String(100)); # time-course (i.e., multiple time points), paired (i.e., control compared to multiple replicates), group (i.e., single grouping of samples).
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint(
                'experiment_id',
                'sample_name_short',
                'sample_name_abbreviation',
                'time_point',
                #'time_point_units',
                'analysis_type',
                'analysis_id',
                'experiment_type'
                ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id']
        self.experiment_id=row_dict_I['experiment_id']
        self.sample_name_short=row_dict_I['sample_name_short']
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation']
        self.time_point=row_dict_I['time_point']
        self.experiment_type=row_dict_I['experiment_type']
        #self.time_point_units=row_dict_I['time_point_units']
        self.analysis_type=row_dict_I['analysis_type']
        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,
                 experiment_id_I,
            sample_name_short_I,
            sample_name_abbreviation_I,
            time_point_I,
            #time_point_units_I,
                 experiment_type_I,
            analysis_type_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.experiment_id=experiment_id_I
        self.sample_name_short=sample_name_short_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        #self.time_point_units=time_point_units_I
        self.experiment_type=experiment_type_I
        self.analysis_type=analysis_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'experiment_id':self.experiment_id,
            'sample_name_short':self.sample_name_short,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
            #'time_point_units':self.time_point_units,
            'experiment_type':self.experiment_type,
            'analysis_type':self.analysis_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_analysis_group(Base):
    __tablename__ = 'data_stage02_quantification_analysis_group'
    id = Column(Integer, Sequence('data_stage02_quantification_analysis_group_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    analysis_group_id = Column(String(500))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint(
                'analysis_id',
                'analysis_group_id',
                ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id']
        self.analysis_group_id=row_dict_I['analysis_group_id']
        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,
                 analysis_group_id_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.analysis_group_id=analysis_group_id_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'analysis_group_id':self.analysis_group_id,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_analysis_connection(Base):
    __tablename__ = 'data_stage02_quantification_analysis_connection'
    id = Column(Integer, Sequence('data_stage02_quantification_analysis_connection_id_seq'), primary_key=True)
    analysis_id = Column(String(500)) #may change between query and transform/store steps to allow for grouping of analyses
    connection_id = Column(String(500));
    connection_order = Column(Integer);
    execute_object = Column(String(500)) #only 1 object per connection
    execute_parameters = Column(postgresql.JSON);
    execute_method = Column(String(500))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint(
                'analysis_id',
                'connection_id',
                'connection_order',
                'execute_object',
                'execute_method',
                ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id']
        self.connection_id=row_dict_I['connection_id']
        self.connection_order=row_dict_I['connection_order']
        self.execute_object=row_dict_I['execute_object']
        self.execute_parameters=row_dict_I['execute_parameters']
        self.execute_method=row_dict_I['execute_method']
        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,

            used__I,
            comment__I):
        self.analysis_id=analysis_id_I

        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'connection_id':self.connection_id,
            'connection_order':self.connection_order,
            'execute_object':self.execute_object,
            'execute_parameters':self.execute_parameters,
            'execute_method':self.execute_method,

            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_analysis_pipeline(Base):
    __tablename__ = 'data_stage02_quantification_analysis_pipeline'
    id = Column(Integer, Sequence('data_stage02_quantification_analysis_pipeline_id_seq'), primary_key=True)
    pipeline_id = Column(String(500));
    pipeline_order = Column(Integer);
    connection_id = Column(String(500));
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint(
                'connection_id',
                'pipeline_id',
                'pipeline_order',
                ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.connection_id=row_dict_I['connection_id']
        self.pipeline_id=row_dict_I['pipeline_id']
        self.pipeline_order=row_dict_I['pipeline_order']

        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,

            used__I,
            comment__I):
        self.analysis_id=analysis_id_I

        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'connection_id':self.connection_id,
                'pipeline_id':self.pipeline_id,
                'connection_id':self.connection_id,

            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_analysis_diagnostics(Base):
    __tablename__ = 'data_stage02_quantification_analysis_diagnostics'
    id = Column(Integer, Sequence('data_stage02_quantification_analysis_diagnostics_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    pipeline_id = Column(String(500));
    connection_id = Column(String(500));
    connection_step = Column(Integer);
    execution_time = Column(Float);
    execution_time_units = Column(String(50))
    execution_startTime = Column(DateTime)
    memory_virtual = Column(postgresql.JSON)
    memory_swap = Column(postgresql.JSON)
    memory_process = Column(Float)
    memory_objects = Column(Float)
    memory_data = Column(Float)
    memory_units = Column(String(50))
    disk_io = Column(postgresql.JSON)
    network_io = Column(postgresql.JSON)
    message_log = Column(postgresql.JSON) #dictionary with keys: 'message','level'
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint(
                'analysis_id',
                'connection_id',
                'connection_step',
                'pipeline_id',
                'execution_startTime',
                ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id']
        self.pipeline_id=row_dict_I['pipeline_id']
        self.connection_id=row_dict_I['connection_id']
        self.connection_step=row_dict_I['connection_step']
        self.execution_time=row_dict_I['execution_time']
        self.execution_time_units=row_dict_I['execution_time_units']
        self.execution_startTime=row_dict_I['execution_startTime']
        self.memory_virtual=row_dict_I['memory_virtual']
        self.memory_swap=row_dict_I['memory_swap']
        self.memory_process=row_dict_I['memory_process']
        self.memory_objects=row_dict_I['memory_objects']
        self.memory_data=row_dict_I['memory_data']
        self.memory_units=row_dict_I['memory_units']
        self.disk_io=row_dict_I['disk_io']
        self.network_io=row_dict_I['network_io']
        self.message_log=row_dict_I['message_log']
        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,

            used__I,
            comment__I):
        self.analysis_id=analysis_id_I

        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'connection_id':self.connection_id,
            'connection_order':self.connection_order,
            'execute_object':self.execute_object,
            'execute_parameters':self.execute_parameters,
            'execute_method':self.execute_method,

            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())    
class data_stage02_quantification_analysis_partitions(Base):
    __tablename__ = 'data_stage02_quantification_analysis_partitions'
    id = Column(Integer, Sequence('data_stage02_quantification_analysis_partitions_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    partition_id = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint(
                'partition_id',
                'analysis_id',
                ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id']
        self.partition_id=row_dict_I['partition_id']
        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,
                 partition_id_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.partition_id=partition_id_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
             'analysis_id':self.analysis_id,
            'partition_id':self.partition_id,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

#TODO: class data_stage02_quantification_analysis_scheduler

#class data_stage02_quantification_analysis_pipeline(Base):
#    __tablename__ = 'data_stage02_quantification_analysis_pipeline'
#    id = Column(Integer, Sequence('data_stage02_quantification_analysis_pipeline_id_seq'), primary_key=True)
#    analysis_id = Column(String(500))
#    pipeline_id = Column(String(500));
#    pipeline_order = Column(Integer);
#    #module
#    execute_object = Column(String(500))
#    execute_queryData_parameters = Column(postgresql.JSON);
#    execute_transformData_parameters = Column(postgresql.JSON);
#    execute_storeData_parameters = Column(postgresql.JSON);
#    execute_queryData_func = Column(String(500))
#    execute_transformData_func = Column(String(500))
#    execute_storeData_func = Column(String(500))
#    #module parameters
#    input_query_object = Column(String(500))
#    input_query_func = Column(String(500))
#    input_query_parameters = Column(postgresql.JSON);
#    data_transform_func = Column(String(500))
#    data_transform_parameters = Column(postgresql.JSON);
#    output_query_object = Column(String(500))
#    output_query_func = Column(String(500))
#    output_query_parameters = Column(postgresql.JSON);
#    used_ = Column(Boolean);
#    comment_ = Column(Text);

#    __table_args__ = (
#            UniqueConstraint(
#                'analysis_id',
#                'pipeline_id',
#                'pipeline_order',
#                'execute_module',
#                'input_query_object',
#                'input_query_func',
#                'output_query_object',
#                'output_query_func',
#                ),
#            )

#    def __init__(self,
#                row_dict_I,
#                ):
#        self.analysis_id=row_dict_I['analysis_id']

#        self.used_=row_dict_I['used_']
#        self.comment_=row_dict_I['comment_']

#    def __set__row__(self,analysis_id_I,

#            used__I,
#            comment__I):
#        self.analysis_id=analysis_id_I

#        self.used_=used__I
#        self.comment_=comment__I

#    def __repr__dict__(self):
#        return {'id':self.id,
#                'analysis_id':self.analysis_id,

#            'used_':self.used_,
#            'comment_':self.comment_}
    
#    def __repr__json__(self):
#        return json.dumps(self.__repr__dict__())