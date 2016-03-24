from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_tree(Base):
    #TODO
    __tablename__ = 'data_stage02_quantification_tree'
    id = Column(Integer, Sequence('data_stage02_quantification_tree_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_abbreviation = Column(String(100))
    sample_name_short = Column(String(100))
    time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    impfeat_value = Column(Float);
    impfeat_method = Column(String(50))
    impfeat_options = Column(postgresql.JSON);
    impfeat_confidence = Column(postgresql.JSON); #std, zscore, pvalue, etc.
    tree_model = Column(String(50))
    tree_method = Column(String(50))
    tree_parameters = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                        'sample_name_short',
                        'component_name',
                        'time_point',
                        'calculated_concentration_units',
                        'impfeat_method',
                        'tree_model',
                        'tree_method'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.sample_name_short = row_dict_I['sample_name_short'];
        self.sample_name_abbreviation = row_dict_I['sample_name_abbreviation'];
        self.time_point = row_dict_I['time_point'];
        self.component_group_name = row_dict_I['component_group_name'];
        self.component_name = row_dict_I['component_name'];
        self.impfeat_value=row_dict_I['impfeat_value'];
        self.impfeat_method=row_dict_I['impfeat_method'];
        self.impfeat_options=row_dict_I['impfeat_options'];
        self.impfeat_confidence=row_dict_I['impfeat_confidence'];
        self.tree_method=row_dict_I['tree_method'];
        self.tree_model=row_dict_I['tree_model'];
        self.tree_parameters=row_dict_I['tree_parameters'];
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, ):
        pass;

    def __repr__dict__(self): # not complete!
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            'sample_name_I':self.sample_name,
            'sample_name_abbreviation_I':self.sample_name_abbreviation,
            'time_point_I':self.time_point,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            "impfeat_value":self.impfeat_value,
            "impfeat_method":self.impfeat_method,
            "impfeat_options":self.impfeat_options,
            "impfeat_confidence":self.impfeat_confidence,
            'tree_model':self.tree_model,
            'tree_method':self.tree_method,
            'tree_parameters':self.tree_parameters,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_tree_validation(Base):
    __tablename__ = 'data_stage02_quantification_tree_validation'
    id = Column(Integer, Sequence('data_stage02_quantification_tree_validation_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    tree_model = Column(String(50))
    tree_method = Column(String(50))
    tree_parameters = Column(postgresql.JSON);
    metric_method = Column(String(50));
    metric_options = Column(postgresql.JSON);
    metric_score = Column(Float);
    metric_confidence = Column(postgresql.JSON);
    crossval_method = Column(String(50))
    crossval_options = Column(postgresql.JSON);
    crossval_parameters = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','tree_model','tree_method',
                                       'metric_method','crossval_method',
                                       'crossval_parameters',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.tree_method=row_dict_I['tree_method'];
        self.tree_model=row_dict_I['tree_model'];
        self.tree_parameters=row_dict_I['tree_parameters'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.crossval_options=row_dict_I['crossval_options'];
        self.crossval_method=row_dict_I['crossval_method'];
        self.crossval_parameters=row_dict_I['crossval_parameters'];
        self.metric_method=row_dict_I['metric_method'];
        self.metric_options=row_dict_I['metric_options'];
        self.metric_score=row_dict_I['metric_score'];
        self.metric_confidence=row_dict_I['metric_confidence'];

    def __set__row__(self, analysis_id_I,
            tree_model_I,
            tree_method_I,
            tree_parameters_I,
            metric_confidence_I,
            metric_score_I,
            metric_options_I,
            metric_method_I,
            crossval_method_I,
            crossval_options_I,
            crossval_parameters_I,
            calculated_concentration_units_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.tree_model=tree_model_I
        self.tree_method=tree_method_I
        self.tree_msep=tree_msep_I
        self.metric_confidence=metric_confidence_I
        self.metric_score=metric_score_I
        self.metric_options=metric_options_I
        self.metric_method=metric_method_I
        self.tree_parameters=tree_parameters_I
        self.crossval_method=crossval_method_I
        self.crossval_options=crossval_options_I
        self.crossval_parameters=crossval_parameters_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'tree_model':self.tree_model,
                'tree_method':self.tree_method,
                'metric_confidence':self.metric_confidence,
                'metric_score':self.metric_score,
                'metric_options':self.metric_options,
                'metric_method':self.metric_method,
                'tree_parameters':self.tree_parameters,
                'crossval_method':self.crossval_method,
                'crossval_options':self.crossval_options,
                'crossval_parameters':self.crossval_parameters,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())