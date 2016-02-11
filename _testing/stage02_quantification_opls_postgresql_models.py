from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_opls_scores(Base):
    __tablename__ = 'data_stage02_quantification_opls_scores'
    id = Column(Integer, Sequence('data_stage02_quantification_opls_scores_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_short = Column(String(100))
    response_name = Column(String(100))
    score = Column(Float);
    score_response = Column(Float);
    axis = Column(Integer);
    var_proportion = Column(Float);
    var_cumulative = Column(Float);
    pls_model = Column(String(50))
    pls_method = Column(String(50))
    pls_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','sample_name_short','response_name','axis','calculated_concentration_units','pls_model','pls_method'),
            )

    def __init__(self, 
                 analysis_id_I,
                 sample_name_short_I,
                response_name_I,
                score_I,
                score_response_I,
                axis_I,
                var_proportion_I,
                var_cumulative_I,
                pls_model_I,
                pls_method_I,
                pls_options_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.sample_name_short=sample_name_short_I
        self.response_name=response_name_I
        self.score=score_I
        self.score_response=score_response_I
        self.axis=axis_I
        self.var_proportion=var_proportion_I
        self.var_cumulative=var_cumulative_I
        self.pls_model=pls_model_I
        self.pls_method=pls_method_I
        self.pls_options=pls_options_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_short':self.sample_name_short,
            'response_name':self.response_name,
            'score':self.score,
            'score_response':self.score_response,
            'axis':self.axis,
            'var_proportion':self.var_proportion,
            'var_cumulative':self.var_cumulative,
            'pls_model':self.pls_model,
            'pls_method':self.pls_method,
            'pls_options':self.pls_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_opls_loadings(Base):
    __tablename__ = 'data_stage02_quantification_opls_loadings'
    id = Column(Integer, Sequence('data_stage02_quantification_opls_loadings_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    loadings = Column(Float);
    axis = Column(Integer)
    correlations = Column(Float);
    pls_model = Column(String(50))
    pls_method = Column(String(50))
    pls_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      #UniqueConstraint('analysis_id','experiment_id','component_name','axis','calculated_concentration_units'),
                      UniqueConstraint('analysis_id','component_name','axis','pls_model','pls_method','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                component_group_name_I,
                component_name_I,
                loadings_I,
                axis_I,
                correlations_I,
                pls_model_I,
                pls_method_I,
                pls_options_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.component_group_name=component_group_name_I
        self.component_name=component_name_I
        self.loadings=loadings_I
        self.axis=axis_I
        self.correlations=correlations_I
        self.pls_model=pls_model_I
        self.pls_method=pls_method_I
        self.pls_options=pls_options_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'loadings':self.loadings,
            'axis':self.axis,
            'correlations':self.correlations,
            'pls_model':self.pls_model,
            'pls_method':self.pls_method,
            'pls_options':self.pls_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_opls_validation(Base):
    __tablename__ = 'data_stage02_quantification_opls_validation'
    id = Column(Integer, Sequence('data_stage02_quantification_opls_validation_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    pls_model = Column(String(50))
    pls_method = Column(String(50))
    pls_msep = Column(Float);
    pls_rmsep = Column(Float);
    pls_r2 = Column(Float);
    pls_r2x = Column(Float);
    pls_q2 = Column(Float);
    pls_options = Column(postgresql.JSON);
    crossValidation_ncomp = Column(Float); #the number of components used in the validation
    crossValidation_method = Column(String(50))
    crossValidation_options = Column(postgresql.JSON);
    permutation_nperm = Column(Float); #the number of components used in the validation
    permutation_pvalue = Column(Float)
    permutation_pvalue_corrected = Column(Float)
    permutation_pvalue_corrected_description = Column(String(500))
    permutation_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','pls_model','pls_method',
                                       'crossValidation_ncomp','crossValidation_method',
                                       'permutation_nperm',
                                       'calculated_concentration_units'),
            )

    def __init__(self, analysis_id_I,
            pls_model_I,
            pls_method_I,
            pls_msep_I,
            pls_rmsep_I,
            pls_r2_I,
            pls_r2x_I,
            pls_q2_I,
            pls_options_I,
            crossValidation_ncomp_I,
            crossValidation_method_I,
            crossValidation_options_I,
            permutation_nperm_I,
            permutation_pvalue_I,
            permutation_pvalue_corrected_I,
            permutation_pvalue_corrected_description_I,
            permutation_options_I,
            calculated_concentration_units_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.pls_model=pls_model_I
        self.pls_method=pls_method_I
        self.pls_msep=pls_msep_I
        self.pls_rmsep=pls_rmsep_I
        self.pls_r2=pls_r2_I
        self.pls_r2x=pls_r2x_I
        self.pls_q2=pls_q2_I
        self.pls_options=pls_options_I
        self.crossValidation_ncomp=crossValidation_ncomp_I
        self.crossValidation_method=crossValidation_method_I
        self.crossValidation_options=crossValidation_options_I
        self.permutation_nperm=permutation_nperm_I
        self.permutation_pvalue=permutation_pvalue_I
        self.permutation_pvalue_corrected=permutation_pvalue_corrected_I
        self.permutation_pvalue_corrected_description=permutation_pvalue_corrected_description_I
        self.permutation_options=permutation_options_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'pls_model':self.pls_model,
                'pls_method':self.pls_method,
                'pls_msep':self.pls_msep,
                'pls_rmsep':self.pls_rmsep,
                'pls_r2':self.pls_r2,
                'pls_r2x':self.pls_r2x,
                'pls_q2':self.pls_q2,
                'pls_options':self.pls_options,
                'crossValidation_ncomp':self.crossValidation_ncomp,
                'crossValidation_method':self.crossValidation_method,
                'crossValidation_options':self.crossValidation_options,
                'permutation_nperm':self.permutation_nperm,
                'permutation_pvalue':self.permutation_pvalue,
                'permutation_pvalue_corrected':self.permutation_pvalue_corrected,
                'permutation_pvalue_corrected_description':self.permutation_pvalue_corrected_description,
                'permutation_options':self.permutation_options,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_opls_permutation(Base):
    __tablename__ = 'data_stage02_quantification_opls_permutation'
    id = Column(Integer, Sequence('data_stage02_quantification_opls_permutation_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    pls_model = Column(String(50))
    pls_method = Column(String(50))
    pls_scale = Column(Boolean);
    pls_msep = Column(String(100))
    pls_rmsep = Column(String(500))
    pls_r2 = Column(Float);
    pls_q2 = Column(Integer)
    pls_options = Column(postgresql.JSON);
    crossValidation_ncomp = Column(Float); #the number of components used in the validation
    crossValidation_method = Column(String(50))
    crossValidation_options = Column(postgresql.JSON);
    permutation_nperm = Column(Float); #the number of components used in the validation
    permutation_pvalue = Column(Float)
    permutation_pvalue_corrected = Column(Float)
    permutation_pvalue_corrected_description = Column(String(500))
    permutation_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','pls_model','pls_method',
                                       'crossValidation_ncomp','crossValidation_method',
                                       'permutation_nperm',
                                       'calculated_concentration_units'),
            )

    def __init__(self, analysis_id_I,
            pls_model_I,
            pls_method_I,
            pls_scale_I,
            pls_msep_I,
            pls_rmsep_I,
            pls_r2_I,
            pls_q2_I,
            pls_options_I,
            crossValidation_ncomp_I,
            crossValidation_method_I,
            crossValidation_options_I,
            permutation_nperm_I,
            permutation_pvalue_I,
            permutation_pvalue_corrected_I,
            permutation_pvalue_corrected_description_I,
            permutation_options_I,
            calculated_concentration_units_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.pls_model=pls_model_I
        self.pls_method=pls_method_I
        self.pls_scale=pls_scale_I
        self.pls_msep=pls_msep_I
        self.pls_rmsep=pls_rmsep_I
        self.pls_r2=pls_r2_I
        self.pls_q2=pls_q2_I
        self.pls_options=pls_options_I
        self.crossValidation_ncomp=crossValidation_ncomp_I
        self.crossValidation_method=crossValidation_method_I
        self.crossValidation_options=crossValidation_options_I
        self.permutation_nperm=permutation_nperm_I
        self.permutation_pvalue=permutation_pvalue_I
        self.permutation_pvalue_corrected=permutation_pvalue_corrected_I
        self.permutation_pvalue_corrected_description=permutation_pvalue_corrected_description_I
        self.permutation_options=permutation_options_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'pls_model':self.pls_model,
                'pls_method':self.pls_method,
                'pls_scale':self.pls_scale,
                'pls_msep':self.pls_msep,
                'pls_rmsep':self.pls_rmsep,
                'pls_r2':self.pls_r2,
                'pls_q2':self.pls_q2,
                'pls_options':self.pls_options,
                'crossValidation_ncomp':self.crossValidation_ncomp,
                'crossValidation_method':self.crossValidation_method,
                'crossValidation_options':self.crossValidation_options,
                'permutation_nperm':self.permutation_nperm,
                'permutation_pvalue':self.permutation_pvalue,
                'permutation_pvalue_corrected':self.permutation_pvalue_corrected,
                'permutation_pvalue_corrected_description':self.permutation_pvalue_corrected_description,
                'permutation_options':self.permutation_options,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_opls_vip(Base):
    __tablename__ = 'data_stage02_quantification_opls_vip'
    id = Column(Integer, Sequence('data_stage02_quantification_opls_vip_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    response_name = Column(String(100))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    pls_vip = Column(Float);
    pls_model = Column(String(50))
    pls_method = Column(String(50))
    pls_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','response_name','component_name','pls_model','pls_method','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                response_name_I,
                component_group_name_I,
                component_name_I,
                pls_vip_I,
                pls_model_I,
                pls_method_I,
                pls_options_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.response_name=response_name_I
        self.component_group_name=component_group_name_I
        self.component_name=component_name_I
        self.pls_vip=pls_vip_I
        self.pls_model=pls_model_I
        self.pls_method=pls_method_I
        self.pls_options=pls_options_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'response_name':self.response_name,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'pls_vip':self.pls_vip,
            'pls_model':self.pls_model,
            'pls_method':self.pls_method,
            'pls_options':self.pls_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_opls_coefficients(Base):
    __tablename__ = 'data_stage02_quantification_opls_coefficients'
    id = Column(Integer, Sequence('data_stage02_quantification_opls_coefficients_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    response_name = Column(String(100))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    pls_coefficients = Column(Float);
    pls_model = Column(String(50))
    pls_method = Column(String(50))
    pls_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','response_name','component_name','pls_model','pls_method','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                response_name_I,
                component_group_name_I,
                component_name_I,
                pls_coefficients_I,
                pls_model_I,
                pls_method_I,
                pls_options_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.response_name=response_name_I
        self.component_group_name=component_group_name_I
        self.component_name=component_name_I
        self.pls_coefficients=pls_coefficients_I
        self.pls_model=pls_model_I
        self.pls_method=pls_method_I
        self.pls_options=pls_options_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'response_name':self.response_name,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'pls_coefficients':self.pls_coefficients,
            'pls_model':self.pls_model,
            'pls_method':self.pls_method,
            'pls_options':self.pls_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_opls_loadingsResponse(Base):
    __tablename__ = 'data_stage02_quantification_opls_loadingsResponse'
    id = Column(Integer, Sequence('data_stage02_quantification_opls_loadingsResponse_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    response_name = Column(String(100))
    loadings_response = Column(Float);
    axis = Column(Integer)
    correlations = Column(Float);
    pls_model = Column(String(50))
    pls_method = Column(String(50))
    pls_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      #UniqueConstraint('analysis_id','experiment_id','component_name','axis','calculated_concentration_units'),
                      UniqueConstraint('analysis_id','response_name','axis','pls_model','pls_method','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                response_name_I,
                loadings_response_I,
                axis_I,
                correlations_response_I,
                pls_model_I,
                pls_method_I,
                pls_options_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.response_name=response_name_I
        self.loadings_response=loadings_response_I
        self.axis=axis_I
        self.correlations_response=correlations_response_I
        self.pls_model=pls_model_I
        self.pls_method=pls_method_I
        self.pls_options=pls_options_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'response_name':self.response_name,
            'loadings_response':self.loadings_response,
            'axis':self.axis,
            'correlations_response':self.correlations_response,
            'pls_model':self.pls_model,
            'pls_method':self.pls_method,
            'pls_options':self.pls_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())