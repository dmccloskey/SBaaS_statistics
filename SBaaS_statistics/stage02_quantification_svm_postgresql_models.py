from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_svm(Base):
    __tablename__ = 'data_stage02_quantification_svm'
    id = Column(Integer, Sequence('data_stage02_quantification_svm_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_abbreviation = Column(String(100))
    sample_name_short = Column(String(100))
    time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    decfunc_value = Column(Float);
    decfunc_method = Column(String(50))
    decfunc_options = Column(postgresql.JSON);
    decfunc_statistics = Column(postgresql.JSON); #std, zscore, pvalue, etc.
    model = Column(String(50))
    method = Column(String(50))
    parameters = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                        'sample_name_short',
                        'component_name',
                        'time_point',
                        'calculated_concentration_units',
                        'decfunc_method',
                        'model',
                        'method'),
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
        self.decfunc_value=row_dict_I['decfunc_value'];
        self.decfunc_method=row_dict_I['decfunc_method'];
        self.decfunc_options=row_dict_I['decfunc_options'];
        self.decfunc_statistics=row_dict_I['decfunc_statistics'];
        self.method=row_dict_I['method'];
        self.model=row_dict_I['model'];
        self.parameters=row_dict_I['parameters'];
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
            "decfunc_value":self.decfunc_value,
            "decfunc_method":self.decfunc_method,
            "decfunc_options":self.decfunc_options,
            "decfunc_statistics":self.decfunc_statistics,
            'model':self.model,
            'method':self.method,
            'parameters':self.parameters,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_svm_impfeat(Base):
    __tablename__ = 'data_stage02_quantification_svm_impfeat'
    id = Column(Integer, Sequence('data_stage02_quantification_svm_impfeat_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    response_name = Column(String(100))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    impfeat_value = Column(Float);
    impfeat_method = Column(String(50))
    impfeat_options = Column(postgresql.JSON);
    impfeat_statistics = Column(postgresql.JSON); #std, zscore, pvalue, etc.
    model = Column(String(50))
    method = Column(String(50))
    parameters = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','response_name',
                        'component_name',
                        'calculated_concentration_units',
                        'impfeat_method',
                        'model',
                        'method'),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.response_name=row_dict_I['response_name'];
        self.component_group_name = row_dict_I['component_group_name'];
        self.component_name = row_dict_I['component_name'];
        self.impfeat_value=row_dict_I['impfeat_value'];
        self.impfeat_method=row_dict_I['impfeat_method'];
        self.impfeat_options=row_dict_I['impfeat_options'];
        self.impfeat_statistics=row_dict_I['impfeat_statistics'];
        self.method=row_dict_I['method'];
        self.model=row_dict_I['model'];
        self.parameters=row_dict_I['parameters'];
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, ):
        pass;

    def __repr__dict__(self):
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            'response_name':self.response_name,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            "impfeat_value":self.impfeat_value,
            "impfeat_method":self.impfeat_method,
            "impfeat_options":self.impfeat_options,
            "impfeat_statistics":self.impfeat_statistics,
            'model':self.model,
            'method':self.method,
            'parameters':self.parameters,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())