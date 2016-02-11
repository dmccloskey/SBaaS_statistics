from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_pca_scores(Base):
    __tablename__ = 'data_stage02_quantification_pca_scores'
    id = Column(Integer, Sequence('data_stage02_quantification_pca_scores_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    #time_point = Column(String(10))
    #time_point_units = Column(String(50))
    score = Column(Float);
    axis = Column(Integer);
    var_proportion = Column(Float);
    var_cumulative = Column(Float);
    pca_model = Column(String(50))
    pca_method = Column(String(50))
    pca_options = Column(postgresql.JSON);
    
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('analysis_id','experiment_id','sample_name_short','axis','calculated_concentration_units'),
                      UniqueConstraint('analysis_id','sample_name_short','axis',
                #'time_point',                     
                #'time_point_units',
                'calculated_concentration_units',
                                       'pca_model','pca_method'
                                       ),
            )

    def __init__(self,
                row_dict_I,
                ):
        #self.time_point=row_dict_I['time_point']
        #self.time_point_units=row_dict_I['time_point_units']
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.pca_options=row_dict_I['pca_options'];
        self.pca_method=row_dict_I['pca_method'];
        self.pca_model=row_dict_I['pca_model'];
        self.var_cumulative=row_dict_I['var_cumulative'];
        self.var_proportion=row_dict_I['var_proportion'];
        self.axis=row_dict_I['axis'];
        self.score=row_dict_I['score'];
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation'];
        self.sample_name_short=row_dict_I['sample_name_short'];
        self.analysis_id=row_dict_I['analysis_id'];

    def __set__row__(self, 
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_short_I, 
                 sample_name_abbreviation_I, 
                 #time_point_I,
            #time_point_units_I,
                 score_I, axis_I,
                 var_proportion_I, var_cumulative_I,
                pca_model_I,
                pca_method_I,
                pca_options_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        #self.time_point = time_point_I;
        #self.time_point_units = time_point_units_I;
        self.score=score_I
        self.axis=axis_I
        self.var_proportion=var_proportion_I
        self.var_cumulative=var_cumulative_I
        self.pca_model=pca_model_I
        self.pca_method=pca_method_I
        self.pca_options=pca_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_short':self.sample_name_short,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            #'time_point':self.time_point,
            #'time_point_units':self.time_point_units,
            'score':self.score,
            'axis':self.axis,
            'var_proportion':self.var_proportion,
            'var_cumulative':self.var_cumulative,
            'pca_model':self.pca_model,
            'pca_method':self.pca_method,
            'pca_options':self.pca_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_pca_loadings(Base):
    __tablename__ = 'data_stage02_quantification_pca_loadings'
    id = Column(Integer, Sequence('data_stage02_quantification_pca_loadings_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    loadings = Column(Float);
    axis = Column(Integer)
    correlations = Column(Float);
    pca_model = Column(String(50))
    pca_method = Column(String(50))
    pca_options = Column(postgresql.JSON);
    #time_point_units = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      #UniqueConstraint('analysis_id','experiment_id','component_name','axis','calculated_concentration_units'),
                      UniqueConstraint('analysis_id','component_name','axis',                
                #'time_point_units',
                                       'calculated_concentration_units',
                                       'pca_model','pca_method'
                                       ),
            )

    def __init__(self,
                row_dict_I,
                ):
        #self.time_point_units=row_dict_I['time_point_units']
        self.analysis_id=row_dict_I['analysis_id'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.component_name=row_dict_I['component_name'];
        self.loadings=row_dict_I['loadings'];
        self.axis=row_dict_I['axis'];
        self.correlations=row_dict_I['correlations'];
        self.pca_model=row_dict_I['pca_model'];
        self.pca_method=row_dict_I['pca_method'];
        self.pca_options=row_dict_I['pca_options'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
    def __set__row__(self, 
                 analysis_id_I,
                 component_group_name_I,
                 component_name_I,
                 loadings_I,
                 axis_I,
                correlations_I,
                pca_model_I,
                pca_method_I,
                pca_options_I,
                 #time_point_units_I,
                 calculated_concentration_units_I, 
                 used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        #self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.loadings=loadings_I
        self.axis=axis_I
        self.correlations=correlations_I
        self.pca_model=pca_model_I
        self.pca_method=pca_method_I
        self.pca_options=pca_options_I
        #self.time_point_units=time_point_units_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'loadings':self.loadings,
            'axis':self.axis,
            'correlations':self.correlations,
            'pca_model':self.pca_model,
            'pca_method':self.pca_method,
            'pca_options':self.pca_options,
            #'time_point_units':self.time_point_units,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_pca_validation(Base):
    __tablename__ = 'data_stage02_quantification_pca_validation'
    id = Column(Integer, Sequence('data_stage02_quantification_pca_validation_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    pca_model = Column(String(50))
    pca_method = Column(String(50))
    pca_msep = Column(Float);
    pca_rmsep = Column(Float);
    pca_r2 = Column(Float);
    pca_q2 = Column(Float);
    pca_options = Column(postgresql.JSON);
    crossValidation_ncomp = Column(Float); #the number of components used in the validation
    crossValidation_method = Column(String(50))
    crossValidation_options = Column(postgresql.JSON);
    permutation_nperm = Column(Float); #the number of components used in the validation
    permutation_pvalue = Column(Float)
    permutation_pvalue_corrected = Column(Float)
    permutation_pvalue_corrected_description = Column(String(500))
    permutation_options = Column(postgresql.JSON);
    #time_point_units = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','pca_model','pca_method',
                                       'crossValidation_ncomp','crossValidation_method',
                                       'permutation_nperm',                
                                        #'time_point_units',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.crossValidation_ncomp=row_dict_I['crossValidation_ncomp'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.permutation_options=row_dict_I['permutation_options'];
        self.permutation_pvalue_corrected_description=row_dict_I['permutation_pvalue_corrected_description'];
        self.permutation_pvalue_corrected=row_dict_I['permutation_pvalue_corrected'];
        self.permutation_pvalue=row_dict_I['permutation_pvalue'];
        self.permutation_nperm=row_dict_I['permutation_nperm'];
        self.crossValidation_options=row_dict_I['crossValidation_options'];
        self.crossValidation_method=row_dict_I['crossValidation_method'];
        self.pca_options=row_dict_I['pca_options'];
        self.pca_q2=row_dict_I['pca_q2'];
        self.pca_r2=row_dict_I['pca_r2'];
        self.pca_rmsep=row_dict_I['pca_rmsep'];
        self.pca_msep=row_dict_I['pca_msep'];
        self.pca_method=row_dict_I['pca_method'];
        self.pca_model=row_dict_I['pca_model'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_units=row_dict_I['time_point_units']

    def __set__row__(self, analysis_id_I,
            pca_model_I,
            pca_method_I,
            pca_msep_I,
            pca_rmsep_I,
            pca_r2_I,
            pca_q2_I,
            pca_options_I,
            crossValidation_ncomp_I,
            crossValidation_method_I,
            crossValidation_options_I,
            permutation_nperm_I,
            permutation_pvalue_I,
            permutation_pvalue_corrected_I,
            permutation_pvalue_corrected_description_I,
            permutation_options_I,
            #time_point_units_I,
            calculated_concentration_units_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.pca_model=pca_model_I
        self.pca_method=pca_method_I
        self.pca_msep=pca_msep_I
        self.pca_rmsep=pca_rmsep_I
        self.pca_r2=pca_r2_I
        self.pca_q2=pca_q2_I
        self.pca_options=pca_options_I
        self.crossValidation_ncomp=crossValidation_ncomp_I
        self.crossValidation_method=crossValidation_method_I
        self.crossValidation_options=crossValidation_options_I
        self.permutation_nperm=permutation_nperm_I
        self.permutation_pvalue=permutation_pvalue_I
        self.permutation_pvalue_corrected=permutation_pvalue_corrected_I
        self.permutation_pvalue_corrected_description=permutation_pvalue_corrected_description_I
        self.permutation_options=permutation_options_I
        #self.time_point_units=time_point_units_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'pca_model':self.pca_model,
                'pca_method':self.pca_method,
                'pca_msep':self.pca_msep,
                'pca_rmsep':self.pca_rmsep,
                'pca_r2':self.pca_r2,
                'pca_q2':self.pca_q2,
                'pca_options':self.pca_options,
                'crossValidation_ncomp':self.crossValidation_ncomp,
                'crossValidation_method':self.crossValidation_method,
                'crossValidation_options':self.crossValidation_options,
                'permutation_nperm':self.permutation_nperm,
                'permutation_pvalue':self.permutation_pvalue,
                'permutation_pvalue_corrected':self.permutation_pvalue_corrected,
                'permutation_pvalue_corrected_description':self.permutation_pvalue_corrected_description,
                'permutation_options':self.permutation_options,
                #'time_point_units':self.time_point_units,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())