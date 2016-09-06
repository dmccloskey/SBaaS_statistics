from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_spls_scores(Base):
    __tablename__ = 'data_stage02_quantification_spls_scores'
    id = Column(Integer, Sequence('data_stage02_quantification_spls_scores_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_short = Column(String(100))
    response_name = Column(String(100))
    test_size = Column(Float);
    axis = Column(Integer);
    
    metric_value = Column(Float);
    metric_method = Column(String(50))
    metric_options = Column(postgresql.JSON);
    metric_statistics = Column(postgresql.JSON); #std, zmetric_options, pvalue, etc.

    pipeline_id = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                        'test_size',
                                       'sample_name_short',
                                       'metric_method',
                                       'response_name',
                                       'axis',
                                       'calculated_concentration_units',
                                       'pipeline_id'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id'];
        self.test_size=row_dict_I['test_size'];
        self.sample_name_short=row_dict_I['sample_name_short'];
        self.response_name=row_dict_I['response_name'];
        self.axis=row_dict_I['axis'];
        self.metric_value=row_dict_I['metric_value'];
        self.metric_method=row_dict_I['metric_method'];
        self.metric_options=row_dict_I['metric_options'];
        self.metric_statistics=row_dict_I['metric_statistics'];
        self.pipeline_id=row_dict_I['pipeline_id'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];

    def __set__row__(self, 
                 analysis_id_I,
                 sample_name_short_I,
                response_name_I,
                metric_options_I,
                metric_statistics_I,
                axis_I,
                metric_method_I,
                metric_value_I,
                pipeline_id_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.sample_name_short=sample_name_short_I
        self.response_name=response_name_I
        self.metric_options=metric_options_I
        self.metric_statistics=metric_statistics_I
        self.axis=axis_I
        self.metric_method=metric_method_I
        self.metric_value=metric_value_I
        self.pipeline_id=pipeline_id_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'test_size':self.test_size,
            'sample_name_short':self.sample_name_short,
            'response_name':self.response_name,
            'metric_options':self.metric_options,
            'metric_statistics':self.metric_statistics,
            'metric_method':self.metric_method,
            'metric_value':self.metric_value,
            'axis':self.axis,
            'pipeline_id':self.pipeline_id,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());
class data_stage02_quantification_spls_loadings(Base):
    __tablename__ = 'data_stage02_quantification_spls_loadings'
    id = Column(Integer, Sequence('data_stage02_quantification_spls_loadings_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    test_size = Column(Float);
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    axis = Column(Integer)
    
    metric_value = Column(Float);
    metric_method = Column(String(50))
    metric_options = Column(postgresql.JSON);
    metric_statistics = Column(postgresql.JSON); #std, zscore, pvalue, etc.

    pipeline_id = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id',
                        'test_size',
                                       'component_name',
                                       'axis',
                                       'metric_method',
                                       'pipeline_id',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id'];
        self.test_size=row_dict_I['test_size'];
        self.metric_value=row_dict_I['metric_value'];
        self.metric_method=row_dict_I['metric_method'];
        self.metric_options=row_dict_I['metric_options'];
        self.metric_statistics=row_dict_I['metric_statistics'];
        self.pipeline_id=row_dict_I['pipeline_id'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.axis=row_dict_I['axis'];
        self.component_name=row_dict_I['component_name'];
        self.component_group_name=row_dict_I['component_group_name'];

    def __set__row__(self, 
                 analysis_id_I,
                component_group_name_I,
                component_name_I,
                axis_I,
                pipeline_id_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.component_group_name=component_group_name_I
        self.component_name=component_name_I
        self.axis=axis_I
        self.pipeline_id=pipeline_id_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'test_size':self.test_size,
            'metric_options':self.metric_options,
            'metric_statistics':self.metric_statistics,
            'metric_method':self.metric_method,
            'metric_value':self.metric_value,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'axis':self.axis,
            'pipeline_id':self.pipeline_id,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_spls_loadingsResponse(Base):
    __tablename__ = 'data_stage02_quantification_spls_loadingsResponse'
    id = Column(Integer, Sequence('data_stage02_quantification_spls_loadingsResponse_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    test_size = Column(Float);
    response_name = Column(String(100))
    axis = Column(Integer)
    
    metric_value = Column(Float);
    metric_method = Column(String(50))
    metric_options = Column(postgresql.JSON);
    metric_statistics = Column(postgresql.JSON); #std, zscore, pvalue, etc.
    
    pipeline_id = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id',
                                       'response_name',
                        'test_size',
                                       'axis',
                                       'metric_method',
                                       'pipeline_id',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.pipeline_id=row_dict_I['pipeline_id'];
        self.test_size=row_dict_I['test_size'];
        self.metric_value=row_dict_I['metric_value'];
        self.metric_method=row_dict_I['metric_method'];
        self.metric_options=row_dict_I['metric_options'];
        self.metric_statistics=row_dict_I['metric_statistics'];
        self.axis=row_dict_I['axis'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.response_name=row_dict_I['response_name'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];

    def __set__row__(self, 
                 analysis_id_I,
                response_name_I,
                axis_I,
                pipeline_id_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.response_name=response_name_I
        self.axis=axis_I
        self.pipeline_id=pipeline_id_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'test_size':self.test_size,
            'response_name':self.response_name,
            'metric_options':self.metric_options,
            'metric_statistics':self.metric_statistics,
            'metric_method':self.metric_method,
            'metric_value':self.metric_value,
            'axis':self.axis,
            'pipeline_id':self.pipeline_id,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_spls_impfeat(Base):
    __tablename__ = 'data_stage02_quantification_spls_impfeat'
    id = Column(Integer, Sequence('data_stage02_quantification_spls_impfeat_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    response_name = Column(String(100))
    test_size = Column(Float);
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    impfeat_value = Column(Float);
    impfeat_method = Column(String(50))
    impfeat_options = Column(postgresql.JSON);
    impfeat_statistics = Column(postgresql.JSON); #std, zscore, pvalue, etc.
    pipeline_id = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                        'response_name',
                        'test_size',
                        'component_name',
                        'calculated_concentration_units',
                        'impfeat_method',
                        'pipeline_id',
                        ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.response_name=row_dict_I['response_name'];
        self.test_size=row_dict_I['test_size'];
        self.component_group_name = row_dict_I['component_group_name'];
        self.component_name = row_dict_I['component_name'];
        self.impfeat_value=row_dict_I['impfeat_value'];
        self.impfeat_method=row_dict_I['impfeat_method'];
        self.impfeat_options=row_dict_I['impfeat_options'];
        self.impfeat_statistics=row_dict_I['impfeat_statistics'];
        self.pipeline_id=row_dict_I['pipeline_id'];
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, ):
        pass;

    def __repr__dict__(self):
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            'response_name':self.response_name,
            'test_size':self.test_size,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            "impfeat_value":self.impfeat_value,
            "impfeat_method":self.impfeat_method,
            "impfeat_options":self.impfeat_options,
            "impfeat_statistics":self.impfeat_statistics,
            'pipeline_id':self.pipeline_id,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_spls_hyperparameter(Base):
    __tablename__ = 'data_stage02_quantification_spls_hyperparameter'
    id = Column(Integer, Sequence('data_stage02_quantification_spls_hyperparameter_id_seq'), primary_key=True)
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
class data_stage02_quantification_spls_pipeline(Base):
    __tablename__ = 'data_stage02_quantification_spls_pipeline'
    id = Column(Integer, Sequence('data_stage02_quantification_spls_pipeline_id_seq'), primary_key=True)
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
class data_stage02_quantification_spls_validation(Base):
    __tablename__ = 'data_stage02_quantification_spls_validation'
    id = Column(Integer, Sequence('data_stage02_quantification_spls_validation_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    pipeline_id = Column(String(50))
    test_size = Column(Float);
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
                      UniqueConstraint('analysis_id','pipeline_id','test_size',
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
            crossval_method_I,
            crossval_options_I,
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
        self.crossval_method=crossval_method_I
        self.crossval_options=crossval_options_I
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
                'crossval_method':self.crossval_method,
                'crossval_options':self.crossval_options,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_spls_axis(Base):
    __tablename__ = 'data_stage02_quantification_spls_axis'
    id = Column(Integer, Sequence('data_stage02_quantification_spls_axis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    test_size = Column(Float);
    axis = Column(Integer);
    
    metric_value = Column(Float);
    metric_method = Column(String(50))
    metric_options = Column(postgresql.JSON);
    metric_statistics = Column(postgresql.JSON); #std, zscore, pvalue, etc.
   
    pipeline_id = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                                       'test_size',
                                       'axis',
                                       'metric_method',
                                       'calculated_concentration_units',
                                       'pipeline_id'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id'];
        self.test_size=row_dict_I['test_size'];
        self.metric_value=row_dict_I['metric_value'];
        self.metric_method=row_dict_I['metric_method'];
        self.metric_options=row_dict_I['metric_options'];
        self.metric_statistics=row_dict_I['metric_statistics'];
        self.axis=row_dict_I['axis'];
        self.pipeline_id=row_dict_I['pipeline_id'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];

    def __set__row__(self, 
                 analysis_id_I,
                axis_I,
                pipeline_id_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.axis=axis_I
        self.pipeline_id=pipeline_id_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'test_size':self.test_size,
            'axis':self.axis,
            'metric_options':self.metric_options,
            'metric_statistics':self.metric_statistics,
            'metric_method':self.metric_method,
            'metric_value':self.metric_value,
            'pipeline_id':self.pipeline_id,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());
