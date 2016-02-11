from SBaaS_base.postgresql_orm_base import *

class data_stage02_quantification_descriptiveStats(Base):
    __tablename__ = 'data_stage02_quantification_descriptiveStats'
    id = Column(Integer, Sequence('data_stage02_quantification_descriptiveStats_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    #time_point_units = Column(String(50))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    var = Column(Float)
    cv = Column(Float)
    n = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    min = Column(Float)
    max = Column(Float)
    median = Column(Float)
    iq_1 = Column(Float)
    iq_3 = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_abbreviation','component_name','time_point'),
                      UniqueConstraint('analysis_id','experiment_id','sample_name_abbreviation','component_name','time_point','calculated_concentration_units',
                #'time_point_units',
                                       ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation'];
        self.var=row_dict_I['var'];
        self.cv=row_dict_I['cv'];
        self.iq_3=row_dict_I['iq_3'];
        self.iq_1=row_dict_I['iq_1'];
        self.median=row_dict_I['median'];
        self.mean=row_dict_I['mean'];
        self.experiment_id=row_dict_I['experiment_id'];
        self.n=row_dict_I['n'];
        self.ci_lb=row_dict_I['ci_lb'];
        self.ci_ub=row_dict_I['ci_ub'];
        self.ci_level=row_dict_I['ci_level'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.min=row_dict_I['min'];
        self.max=row_dict_I['max'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue=row_dict_I['pvalue'];
        self.test_description=row_dict_I['test_description'];
        self.test_stat=row_dict_I['test_stat'];
        self.component_name=row_dict_I['component_name'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.time_point=row_dict_I['time_point'];
        #self.time_point_units=row_dict_I['time_point_units']

    def __set__row__(self, 
                 analysis_id_I,
                 experiment_id_I, sample_name_abbreviation_I, 
                 time_point_I,
            #time_point_units_I,
            component_group_name_I, component_name_I,
                 mean_I, var_I, cv_I, n_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 min_I,max_I,median_I,iq_1_I,iq_3_I,
                 calculated_concentration_units_I, used__I, comment__I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        #self.time_point_units=time_point_units_I
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.mean=mean_I;
        self.var=var_I;
        self.cv=cv_I;
        self.n=n_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.min=min_I;
        self.max=max_I;
        self.median=median_I;
        self.iq_1=iq_1_I;
        self.iq_3=iq_3_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'component_group_name':self.component_group_name,
                'component_name':self.component_name,
                'test_stat':self.test_stat,
                'test_description':self.test_description,
                'pvalue':self.pvalue,
                'pvalue_corrected':self.pvalue_corrected,
                'pvalue_corrected_description':self.pvalue_corrected_description,
                'mean':self.mean,
                'var':self.var,
                'cv':self.cv,
                'n':self.n,
                'ci_lb':self.ci_lb,
                'ci_ub':self.ci_ub,
                'ci_level':self.ci_level,
                'min':self.min,
                'max':self.max,
                'median':self.median,
                'iq_1':self.iq_1,
                'iq_3':self.iq_3,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_descriptiveStats_replicates(Base):
    __tablename__ = 'data_stage02_quantification_descriptiveStats_replicates'
    id = Column(Integer, Sequence('data_stage02_quantification_descriptiveStats_replicates_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    var = Column(Float)
    cv = Column(Float)
    n = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    min = Column(Float)
    max = Column(Float)
    median = Column(Float)
    iq_1 = Column(Float)
    iq_3 = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_abbreviation','component_name','time_point'),
                      UniqueConstraint('analysis_id','experiment_id','sample_name_abbreviation','component_name','time_point','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                 experiment_id_I, sample_name_abbreviation_I, 
                 time_point_I, component_group_name_I, component_name_I,
                 mean_I, var_I, cv_I, n_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 min_I,max_I,median_I,iq_1_I,iq_3_I,
                 calculated_concentration_units_I, used__I, comment__I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.mean=mean_I;
        self.var=var_I;
        self.cv=cv_I;
        self.n=n_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.min=min_I;
        self.max=max_I;
        self.median=median_I;
        self.iq_1=iq_1_I;
        self.iq_3=iq_3_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'component_group_name':self.component_group_name,
                'component_name':self.component_name,
                'test_stat':self.test_stat,
                'test_description':self.test_description,
                'pvalue':self.pvalue,
                'pvalue_corrected':self.pvalue_corrected,
                'pvalue_corrected_description':self.pvalue_corrected_description,
                'mean':self.mean,
                'var':self.var,
                'cv':self.cv,
                'n':self.n,
                'ci_lb':self.ci_lb,
                'ci_ub':self.ci_ub,
                'ci_level':self.ci_level,
                'min':self.min,
                'max':self.max,
                'median':self.median,
                'iq_1':self.iq_1,
                'iq_3':self.iq_3,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_descriptiveStats_replicatesMV(Base):
    __tablename__ = 'data_stage02_quantification_descriptiveStats_replicatesMV'
    id = Column(Integer, Sequence('data_stage02_quantification_descriptiveStats_replicatesMV_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    imputation_method = Column(String(50))
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    var = Column(Float)
    cv = Column(Float)
    n = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    min = Column(Float)
    max = Column(Float)
    median = Column(Float)
    iq_1 = Column(Float)
    iq_3 = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_abbreviation','component_name','time_point'),
                      UniqueConstraint('analysis_id','imputation_method','experiment_id','sample_name_abbreviation','component_name','time_point','calculated_concentration_units'),
            )

    def __init__(self, 
                 analysis_id_I,
                 experiment_id_I, sample_name_abbreviation_I, 
                 time_point_I, component_group_name_I, component_name_I,
                 imputation_method_I,
                 mean_I, var_I, cv_I, n_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 min_I,max_I,median_I,iq_1_I,iq_3_I,
                 calculated_concentration_units_I, used__I, comment__I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.imputation_method = imputation_method_I;
        self.mean=mean_I;
        self.var=var_I;
        self.cv=cv_I;
        self.n=n_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.min=min_I;
        self.max=max_I;
        self.median=median_I;
        self.iq_1=iq_1_I;
        self.iq_3=iq_3_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'component_group_name':self.component_group_name,
                'component_name':self.component_name,
                "imputation_method":self.imputation_method,
                'test_stat':self.test_stat,
                'test_description':self.test_description,
                'pvalue':self.pvalue,
                'pvalue_corrected':self.pvalue_corrected,
                'pvalue_corrected_description':self.pvalue_corrected_description,
                'mean':self.mean,
                'var':self.var,
                'cv':self.cv,
                'n':self.n,
                'ci_lb':self.ci_lb,
                'ci_ub':self.ci_ub,
                'ci_level':self.ci_level,
                'min':self.min,
                'max':self.max,
                'median':self.median,
                'iq_1':self.iq_1,
                'iq_3':self.iq_3,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())