from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_pairWiseTest(Base):
    #pairedttest
    __tablename__ = 'data_stage02_quantification_pairWiseTest'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseTest_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id_1 = Column(String(50))
    #experiment_id_2 = Column(String(50))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    #time_point_1 = Column(String(10))
    #time_point_2 = Column(String(10))
    #time_point_units_1 = Column(String(50))
    #time_point_units_2 = Column(String(50))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    test_stat = Column(Float)
    test_description = Column(String(500));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    mean = Column(Float)
    ci_lb = Column(Float)
    ci_ub = Column(Float)
    ci_level = Column(Float)
    fold_change = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                    'sample_name_abbreviation_1','sample_name_abbreviation_2',
                    #'experiment_id_1','experiment_id_2,'
                    #time_point_1, time_point_2,
                    #time_point_units_1,time_point_units_2,
                    'component_name','calculated_concentration_units','test_description'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.sample_name_abbreviation_1=row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_abbreviation_2=row_dict_I['sample_name_abbreviation_2'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.component_name=row_dict_I['component_name'];
        self.test_stat=row_dict_I['test_stat'];
        self.test_description=row_dict_I['test_description'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.mean=row_dict_I['mean'];
        self.ci_lb=row_dict_I['ci_lb'];
        self.ci_ub=row_dict_I['ci_ub'];
        self.ci_level=row_dict_I['ci_level'];
        self.fold_change=row_dict_I['fold_change'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.experiment_id_1=row_dict_I['experiment_id_1']
        #self.experiment_id_2=row_dict_I['experiment_id_2']
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units_1=row_dict_I['time_point_units_1']
        #self.time_point_units_2=row_dict_I['time_point_units_2']

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_1_I,experiment_id_2_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 #time_point_1_I, time_point_2_I,
                #time_point_units_1_I,time_point_units_2_I,
                 component_group_name_I, component_name_I,
                 mean_I, test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 ci_lb_I, ci_ub_I, ci_level_I,
                 fold_change_I, calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id_1 = experiment_id_1_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units_1=time_point_units_1_I
        #self.time_point_units_2=time_point_units_2_I
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.mean=mean_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.ci_lb=ci_lb_I;
        self.ci_ub=ci_ub_I;
        self.ci_level=ci_level_I;
        self.fold_change=fold_change_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviation_1':self.sample_name_abbreviation_1,
            'sample_name_abbreviation_2':self.sample_name_abbreviation_2,
            #'experiment_id_1':self.experiment_id_1,
            #'experiment_id_2':self.experiment_id_2,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units_1':self.time_point_units_1,
            #'time_point_units_2':self.time_point_units_2,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'test_stat':self.test_stat,
            'test_description':self.test_description,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'mean':self.mean,
            'ci_lb':self.ci_lb,
            'ci_ub':self.ci_ub,
            'ci_level':self.ci_level,
            'fold_change':self.fold_change,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
