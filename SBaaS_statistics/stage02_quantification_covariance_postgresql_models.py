from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_covariance_samples(Base):
    __tablename__ = 'data_stage02_quantification_covariance_samples'
    id = Column(Integer, Sequence('data_stage02_quantification_covariance_samples_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_short_1 = Column(String(100))
    sample_name_short_2 = Column(String(100))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    covariance = Column(Float);
    precision = Column(Float);
    covariance_method = Column(String(50))
    covariance_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','sample_name_short_1','sample_name_short_2','calculated_concentration_units',
                                       'covariance_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.sample_name_short_1 = row_dict_I['sample_name_short_1'];
        self.sample_name_abbreviation_1 = row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_short_2 = row_dict_I['sample_name_short_2'];
        self.sample_name_abbreviation_2 = row_dict_I['sample_name_abbreviation_2'];
        self.covariance=row_dict_I['covariance'];
        self.precision=row_dict_I['precision'];
        self.covariance_method=row_dict_I['covariance_method'];
        self.covariance_options=row_dict_I['covariance_options'];
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, 
                analysis_id_I,
                sample_name_short_1_I, 
                sample_name_short_2_I, 
                sample_name_abbreviation_1_I, 
                sample_name_abbreviation_2_I, 
                covariance_I, precision_I,
                covariance_method_I,
                covariance_options_I,
                calculated_concentration_units_I,
                used_I,
                comment_I
                ):
        self.analysis_id = analysis_id_I;
        self.sample_name_short_1 = sample_name_short_1_I;
        self.sample_name_short_2 = sample_name_short_2_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        self.covariance=covariance_I
        self.precision=precision_I
        self.covariance_method=covariance_method_I
        self.covariance_options=covariance_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_short_1':self.sample_name_short_1,
            'sample_name_short_2':self.sample_name_short_2,
            'sample_name_abbreviation_1':self.sample_name_abbreviation_1,
            'sample_name_abbreviation_2':self.sample_name_abbreviation_2,
            'covariance':self.covariance,
            'precision':self.precision,
            'covariance_method':self.covariance_method,
            'covariance_options':self.covariance_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_covariance_features(Base):
    __tablename__ = 'data_stage02_quantification_covariance_features'
    id = Column(Integer, Sequence('data_stage02_quantification_covariance_features_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    component_group_name_1 = Column(String(100))
    component_group_name_2 = Column(String(100))
    component_name_1 = Column(String(500))
    component_name_2 = Column(String(500))
    covariance = Column(Float);
    precision = Column(Float)
    covariance_method = Column(String(50))
    covariance_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','component_name_1','component_name_2','calculated_concentration_units',
                                       'covariance_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.component_group_name_1 = row_dict_I['component_group_name_1'];
        self.component_group_name_2 = row_dict_I['component_group_name_2'];
        self.component_name_1 = row_dict_I['component_name_1'];
        self.component_name_2 = row_dict_I['component_name_2'];
        self.covariance=row_dict_I['covariance']
        self.precision=row_dict_I['precision']
        self.covariance_method=row_dict_I['covariance_method']
        self.covariance_options=row_dict_I['covariance_options']
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, 
                analysis_id_I,
                component_group_name_1_I,
                component_group_name_2_I,
                component_name_1_I,
                component_name_2_I,
                covariance_I,
                precision_I,
                covariance_method_I,
                covariance_options_I,
                calculated_concentration_units_I, 
                used__I,
                comment__I
                ):
        self.analysis_id = analysis_id_I;
        self.component_group_name_1 = component_group_name_1_I;
        self.component_group_name_2 = component_group_name_2_I;
        self.component_name_1 = component_name_1_I;
        self.component_name_2 = component_name_2_I;
        self.covariance=covariance_I
        self.precision=precision_I
        self.covariance_options=covariance_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'component_group_name_1':self.component_group_name_1,
            'component_group_name_2':self.component_group_name_2,
            'component_name_1':self.component_name_1,
            'component_name_2':self.component_name_2,
            'covariance':self.covariance,
            'precision':self.precision,
            'covariance_method':self.covariance_method,
            'covariance_options':self.covariance_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_covariance_samples_mahalanobis(Base):
    __tablename__ = 'data_stage02_quantification_covariance_samples_mahalanobis'
    id = Column(Integer, Sequence('data_stage02_quantification_covariance_samples_mahalanobis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_short = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    mahalanobis = Column(Float);
    covariance_method = Column(String(50))
    covariance_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','sample_name_short','calculated_concentration_units',
                                       'covariance_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.sample_name_short = row_dict_I['sample_name_short'];
        self.sample_name_abbreviation = row_dict_I['sample_name_abbreviation'];
        self.mahalanobis=row_dict_I['mahalanobis'];
        self.covariance_method=row_dict_I['covariance_method'];
        self.covariance_options=row_dict_I['covariance_options'];
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, 
                analysis_id_I,
                sample_name_short_I, 
                sample_name_abbreviation_I, 
                mahalanobis_I,
                covariance_method_I,
                covariance_options_I,
                calculated_concentration_units_I,
                used_I,
                comment_I
                ):
        self.analysis_id = analysis_id_I;
        self.sample_name_short = sample_name_short_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.mahalanobis=mahalanobis_I
        self.covariance_method=covariance_method_I
        self.covariance_options=covariance_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_short':self.sample_name_short,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'mahalanobis':self.mahalanobis,
            'covariance_method':self.covariance_method,
            'covariance_options':self.covariance_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_covariance_features_mahalanobis(Base):
    __tablename__ = 'data_stage02_quantification_covariance_features_mahalanobis'
    id = Column(Integer, Sequence('data_stage02_quantification_covariance_features_mahalanobis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    mahalanobis = Column(Float)
    covariance_method = Column(String(50))
    covariance_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','component_name','calculated_concentration_units',
                                       'covariance_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.component_group_name = row_dict_I['component_group_name'];
        self.component_name = row_dict_I['component_name'];
        self.mahalanobis=row_dict_I['mahalanobis']
        self.covariance_method=row_dict_I['covariance_method']
        self.covariance_options=row_dict_I['covariance_options']
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, 
                analysis_id_I,
                component_group_name_I,
                component_name_I,
                mahalanobis_I,
                covariance_method_I,
                covariance_options_I,
                calculated_concentration_units_I, 
                used__I,
                comment__I
                ):
        self.analysis_id = analysis_id_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.mahalanobis=mahalanobis_I
        self.covariance_options=covariance_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'mahalanobis':self.mahalanobis,
            'covariance_method':self.covariance_method,
            'covariance_options':self.covariance_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_covariance_samples_score(Base):
    __tablename__ = 'data_stage02_quantification_covariance_samples_score'
    id = Column(Integer, Sequence('data_stage02_quantification_covariance_samples_score_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    log_likelihood = Column(Float);
    pvalue = Column(Float);
    covariance_method = Column(String(50))
    covariance_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','calculated_concentration_units',
                                       'covariance_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.log_likelihood=row_dict_I['log_likelihood'];
        self.pvalue=row_dict_I['pvalue'];
        self.covariance_method=row_dict_I['covariance_method'];
        self.covariance_options=row_dict_I['covariance_options'];
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, 
                analysis_id_I,
                log_likelihood_I,
                pvalue_I,
                covariance_method_I,
                covariance_options_I,
                calculated_concentration_units_I,
                used_I,
                comment_I
                ):
        self.analysis_id = analysis_id_I;
        self.log_likelihood=log_likelihood_I
        self.pvalue=pvalue_I
        self.covariance_method=covariance_method_I
        self.covariance_options=covariance_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'log_likelihood':self.log_likelihood,
            'pvalue':self.pvalue,
            'covariance_method':self.covariance_method,
            'covariance_options':self.covariance_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_covariance_features_score(Base):
    __tablename__ = 'data_stage02_quantification_covariance_features_score'
    id = Column(Integer, Sequence('data_stage02_quantification_covariance_features_score_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    log_likelihood = Column(Float)
    pvalue = Column(Float)
    covariance_method = Column(String(50))
    covariance_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','calculated_concentration_units',
                                       'covariance_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.log_likelihood=row_dict_I['log_likelihood']
        self.pvalue=row_dict_I['pvalue']
        self.covariance_method=row_dict_I['covariance_method']
        self.covariance_options=row_dict_I['covariance_options']
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, 
                analysis_id_I,
                log_likelihood_I,
                pvalue_I,
                covariance_method_I,
                covariance_options_I,
                calculated_concentration_units_I, 
                used__I,
                comment__I
                ):
        self.analysis_id = analysis_id_I;
        self.log_likelihood=log_likelihood_I
        self.pvalue=pvalue_I
        self.covariance_options=covariance_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'log_likelihood':self.log_likelihood,
            'pvalue':self.pvalue,
            'covariance_method':self.covariance_method,
            'covariance_options':self.covariance_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
