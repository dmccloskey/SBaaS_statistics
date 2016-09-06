from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_cluster_responseClassification(Base):
    __tablename__ = 'data_stage02_quantification_cluster_responseClassification'
    id = Column(Integer, Sequence('data_stage02_quantification_cluster_responseClassification_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    response_name = Column(String(100))
    sample_name_short = Column(String(100))
    test_size = Column(Float);
    response_class_value = Column(Float);
    response_class_method = Column(String(50))
    response_class_options = Column(postgresql.JSON);
    response_class_statistics = Column(postgresql.JSON); #std, zscore, pvalue, etc.
    pipeline_id = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                        'test_size',
                        'sample_name_short',
                        'calculated_concentration_units',
                        'response_class_method',
                        'pipeline_id',
                        ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.sample_name_short = row_dict_I['sample_name_short'];
        self.test_size = row_dict_I['test_size'];
        self.response_name = row_dict_I['response_name'];
        self.response_class_value=row_dict_I['response_class_value'];
        self.response_class_method=row_dict_I['response_class_method'];
        self.response_class_options=row_dict_I['response_class_options'];
        self.response_class_statistics=row_dict_I['response_class_statistics'];
        self.pipeline_id=row_dict_I['pipeline_id'];
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, ):
        pass;

    def __repr__dict__(self): # not complete!
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            'test_size':self.test_size,
            'sample_name_short':self.sample_name_short,
            'response_name':self.response_name,
            "response_class_value":self.response_class_value,
            "response_class_method":self.response_class_method,
            "response_class_options":self.response_class_options,
            "response_class_statistics":self.response_class_statistics,
            'pipeline_id':self.pipeline_id,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_cluster_hyperparameter(Base):
    __tablename__ = 'data_stage02_quantification_cluster_hyperparameter'
    id = Column(Integer, Sequence('data_stage02_quantification_cluster_hyperparameter_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    pipeline_id = Column(String(50))
    pipeline_parameters = Column(postgresql.JSON);
    test_size = Column(Float);
    hyperparameter_id = Column(Integer)
    hyperparameter_method = Column(String(50)); #i.e. hyperparmeter search
    hyperparameter_options = Column(postgresql.JSON);
    metric_method = Column(String(50));
    metric_options = Column(postgresql.JSON);
    metric_score = Column(Float);
    metric_statistics = Column(postgresql.JSON);
    crossval_method = Column(String(50))
    crossval_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id',
                        'pipeline_id',
                        'hyperparameter_id',
                        'test_size',
                        'hyperparameter_method',
                        'metric_method',
                        'crossval_method',
                        'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.pipeline_id=row_dict_I['pipeline_id'];
        self.test_size=row_dict_I['test_size'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.crossval_options=row_dict_I['crossval_options'];
        self.crossval_method=row_dict_I['crossval_method'];
        self.hyperparameter_id=row_dict_I['hyperparameter_id'];
        self.hyperparameter_method=row_dict_I['hyperparameter_method'];
        self.hyperparameter_options=row_dict_I['hyperparameter_options'];
        self.metric_method=row_dict_I['metric_method'];
        self.metric_options=row_dict_I['metric_options'];
        self.metric_score=row_dict_I['metric_score'];
        self.metric_statistics=row_dict_I['metric_statistics'];
        self.pipeline_parameters=row_dict_I['pipeline_parameters'];

    def __set__row__(self, analysis_id_I,
            pipeline_id_I,
            pipeline_parameters_I,
            test_size_I,
            hyperparameter_id_I,
            hyperparameter_method_I,
            hyperparameter_options_I,
            metric_statistics_I,
            metric_score_I,
            metric_options_I,
            metric_method_I,
            crossval_method_I,
            crossval_options_I,
            calculated_concentration_units_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.pipeline_id=pipeline_id_I
        self.pipeline_parameters=pipeline_parameters_I
        self.test_size=test_size_I
        self.hyperparameter_id=hyperparameter_id_I
        self.hyperparameter_options=hyperparameter_options_I
        self.hyperparameter_method=hyperparameter_method_I
        self.metric_statistics=metric_statistics_I
        self.metric_score=metric_score_I
        self.metric_options=metric_options_I
        self.metric_method=metric_method_I
        self.crossval_method=crossval_method_I
        self.crossval_options=crossval_options_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'pipeline_id':self.pipeline_id,
                'pipeline_parameters':self.pipeline_parameters,
                'test_size':self.test_size,
                'hyperparameter_id':self.hyperparameter_id,
                'hyperparameter_options':self.hyperparameter_options,
                'hyperparameter_method':self.hyperparameter_method,
                'metric_statistics':self.metric_statistics,
                'metric_score':self.metric_score,
                'metric_options':self.metric_options,
                'metric_method':self.metric_method,
                'crossval_method':self.crossval_method,
                'crossval_options':self.crossval_options,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_cluster_validation(Base):
    __tablename__ = 'data_stage02_quantification_cluster_validation'
    id = Column(Integer, Sequence('data_stage02_quantification_cluster_validation_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    pipeline_id = Column(String(50))
    test_size = Column(Float);
    metric_method = Column(String(50));
    metric_options = Column(postgresql.JSON);
    metric_score = Column(Float);
    metric_statistics = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','pipeline_id','test_size',
                                       'metric_method',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.pipeline_id=row_dict_I['pipeline_id'];
        self.test_size=row_dict_I['test_size'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.metric_method=row_dict_I['metric_method'];
        self.metric_options=row_dict_I['metric_options'];
        self.metric_score=row_dict_I['metric_score'];
        self.metric_statistics=row_dict_I['metric_statistics'];

    def __set__row__(self, analysis_id_I,
            pipeline_id_I,
            test_size_I,
            metric_statistics_I,
            metric_score_I,
            metric_options_I,
            metric_method_I,
            calculated_concentration_units_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.pipeline_id=pipeline_id_I
        self.test_size=test_size_I
        self.metric_statistics=metric_statistics_I
        self.metric_score=metric_score_I
        self.metric_options=metric_options_I
        self.metric_method=metric_method_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'pipeline_id':self.pipeline_id,
                'test_size':self.test_size,
                'metric_statistics':self.metric_statistics,
                'metric_score':self.metric_score,
                'metric_options':self.metric_options,
                'metric_method':self.metric_method,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_cluster_pipeline(Base):
    __tablename__ = 'data_stage02_quantification_cluster_pipeline'
    id = Column(Integer, Sequence('data_stage02_quantification_cluster_pipeline_id_seq'), primary_key=True)
    pipeline_id = Column(String(500))
    pipeline_model = Column(String(50))
    pipeline_method = Column(String(50))
    pipeline_parameters = Column(postgresql.JSON);
    pipeline_order = Column(Integer);
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('pipeline_id',
                                       'pipeline_model',
                                       'pipeline_method',
                                       'pipeline_order',
                                       ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.pipeline_method=row_dict_I['pipeline_method'];
        self.pipeline_model=row_dict_I['pipeline_model'];
        self.pipeline_parameters=row_dict_I['pipeline_parameters'];
        self.pipeline_order=row_dict_I['pipeline_order'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.pipeline_id=row_dict_I['pipeline_id'];

    def __set__row__(self, pipeline_id_I,
            pipeline_model_I,
            pipeline_method_I,
            pipeline_parameters_I,
            pipeline_order_I,
            used__I,
            comment__I,):
        self.pipeline_pipeline_id=pipeline_id_I
        self.pipeline_model=pipeline_model_I
        self.pipeline_method=pipeline_method_I
        self.pipeline_order=pipeline_order_I
        self.pipeline_parameters=pipeline_parameters_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'pipeline_id':self.pipeline_id,
                'pipeline_model':self.pipeline_model,
                'pipeline_method':self.pipeline_method,
                'pipeline_order':self.pipeline_pipeline_order,
                'pipeline_parameters':self.pipeline_parameters,
                'used_':self.used_,
                'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())