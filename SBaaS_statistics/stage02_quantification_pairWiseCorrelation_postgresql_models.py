from SBaaS_base.postgresql_orm_base import *

class data_stage02_quantification_pairWiseCorrelation(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseCorrelation'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseCorrelation_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    #time_point_1 = Column(String(10))
    #time_point_2 = Column(String(10))
    #time_point_units = Column(String(50))
    value_name = Column(String(100))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','sample_name_abbreviation_1','sample_name_abbreviation_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'value_name',
                                       'calculated_concentration_units',
                                       'distance_measure',
                                       'pvalue_corrected_description'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.sample_name_abbreviation_1=row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_abbreviation_2=row_dict_I['sample_name_abbreviation_2'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];
        self.value_name=row_dict_I['value_name'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            value_name_I,
                distance_measure_I,
                correlation_coefficient_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.value_name=value_name_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviation_1':self.sample_name_abbreviation_1,
            'sample_name_abbreviation_2':self.sample_name_abbreviation_2,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
            'value_name':self.value_name,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_pairWiseCorrelation_replicates(Base):
    #pairedttest
    __tablename__ = 'data_stage02_quantification_pairWiseCorrelation_replicates'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseCorrelation_replicates_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    sample_name_short_1 = Column(String(100))
    sample_name_short_2 = Column(String(100))
    #time_point_1 = Column(String(10))
    #time_point_2 = Column(String(10))
    #time_point_units = Column(String(50))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','sample_name_short_1','sample_name_short_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                       'calculated_concentration_units',
                                       'distance_measure',
                                       'pvalue_corrected_description'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.sample_name_abbreviation_1=row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_abbreviation_2=row_dict_I['sample_name_abbreviation_2'];
        self.sample_name_short_1=row_dict_I['sample_name_short_1'];
        self.sample_name_short_2=row_dict_I['sample_name_short_2'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 sample_name_short_1_I, sample_name_short_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
                distance_measure_I,
                correlation_coefficient_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        self.sample_name_short_1 = sample_name_short_1_I;
        self.sample_name_short_2 = sample_name_short_2_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviation_1':self.sample_name_abbreviation_1,
            'sample_name_abbreviation_2':self.sample_name_abbreviation_2,
            'sample_name_short_1':self.sample_name_short_1,
            'sample_name_short_2':self.sample_name_short_2,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_pairWiseCorrelationFeatures(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseCorrelationFeatures'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseCorrelationFeatures_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    component_name_1 = Column(String(100))
    component_name_2 = Column(String(100))
    component_group_name_1 = Column(String(100))
    component_group_name_2 = Column(String(100))
    value_name = Column(String(100))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','component_name_1','component_name_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'value_name',
                                       'calculated_concentration_units',
                                       'distance_measure',
                                       'pvalue_corrected_description'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.component_name_1=row_dict_I['component_name_1'];
        self.component_name_2=row_dict_I['component_name_2'];
        self.component_group_name_1=row_dict_I['component_group_name_1'];
        self.component_group_name_2=row_dict_I['component_group_name_2'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];
        self.value_name=row_dict_I['value_name'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 component_name_1_I, component_name_2_I,
                 component_group_name_1_I, component_group_name_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            value_name_I,
                distance_measure_I,
                correlation_coefficient_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.component_name_1 = component_name_1_I;
        self.component_name_2 = component_name_2_I;
        self.component_group_name_1 = component_group_name_1_I;
        self.component_group_name_2 = component_group_name_2_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.value_name=value_name_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'component_name_1':self.component_name_1,
            'component_name_2':self.component_name_2,
            'component_group_name_1':self.component_group_name_1,
            'component_group_name_2':self.component_group_name_2,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
            'value_name':self.value_name,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_pairWiseCorrFeatures_replicates(Base):
    #pairedttest
    __tablename__ = 'data_stage02_quantification_pairWiseCorrFeatures_replicates'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseCorrFeatures_replicates_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    component_name_1 = Column(String(100))
    component_name_2 = Column(String(100))
    component_group_name_1 = Column(String(100))
    component_group_name_2 = Column(String(100))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','component_name_1','component_name_2',
                                       'calculated_concentration_units',
                                       'distance_measure',
                                       'pvalue_corrected_description'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.component_name_1=row_dict_I['component_name_1'];
        self.component_name_2=row_dict_I['component_name_2'];
        self.component_group_name_1=row_dict_I['component_group_name_1'];
        self.component_group_name_2=row_dict_I['component_group_name_2'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];

    def __set__row__(self,
                 analysis_id_I,
                 component_name_1_I, component_name_2_I,
                 component_group_name_1_I, component_group_name_2_I,
                distance_measure_I,
                correlation_coefficient_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        self.component_name_1 = component_name_1_I;
        self.component_name_2 = component_name_2_I;
        self.component_group_name_1 = component_group_name_1_I;
        self.component_group_name_2 = component_group_name_2_I;
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'component_name_1':self.component_name_1,
            'component_name_2':self.component_name_2,
            'component_group_name_1':self.component_group_name_1,
            'component_group_name_2':self.component_group_name_2,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_pairWiseCorrFeaturesAndConditions(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseCorrFeaturesAndConditions'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseCorrFeaturesAndConditions_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    component_name_1 = Column(String(100))
    component_name_2 = Column(String(100))
    component_group_name_1 = Column(String(100))
    component_group_name_2 = Column(String(100))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    value_name = Column(String(100))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','component_name_1','component_name_2','sample_name_abbreviation_1','sample_name_abbreviation_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'value_name',
                                       'calculated_concentration_units',
                                       'distance_measure',
                                       'pvalue_corrected_description'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.component_name_1=row_dict_I['component_name_1'];
        self.component_name_2=row_dict_I['component_name_2'];
        self.component_group_name_1=row_dict_I['component_group_name_1'];
        self.component_group_name_2=row_dict_I['component_group_name_2'];
        self.sample_name_abbreviation_1=row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_abbreviation_2=row_dict_I['sample_name_abbreviation_2'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];
        self.value_name=row_dict_I['value_name'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 component_name_1_I, component_name_2_I,
                 component_group_name_1_I, component_group_name_2_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            value_name_I,
                distance_measure_I,
                correlation_coefficient_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.component_name_1 = component_name_1_I;
        self.component_name_2 = component_name_2_I;
        self.component_group_name_1 = component_group_name_1_I;
        self.component_group_name_2 = component_group_name_2_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.value_name=value_name_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'component_name_1':self.component_name_1,
            'component_name_2':self.component_name_2,
            'component_group_name_1':self.component_group_name_1,
            'component_group_name_2':self.component_group_name_2,
            'sample_name_abbreviation_1':self.sample_name_abbreviation_1,
            'sample_name_abbreviation_2':self.sample_name_abbreviation_2,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
            'value_name':self.value_name,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_pairWiseCorrelationCrossUnits(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseCorrelationCrossUnits'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseCorrelationCrossUnits_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    #time_point_1 = Column(String(10))
    #time_point_2 = Column(String(10))
    #time_point_units = Column(String(50))
    value_name = Column(String(500))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units_1 = Column(String(50))
    calculated_concentration_units_2 = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','sample_name_abbreviation_1','sample_name_abbreviation_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'value_name',
                                       'calculated_concentration_units_1',
                                       'calculated_concentration_units_2',
                                       'distance_measure',
                                       'pvalue_corrected_description'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.sample_name_abbreviation_1=row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_abbreviation_2=row_dict_I['sample_name_abbreviation_2'];
        self.calculated_concentration_units_1=row_dict_I['calculated_concentration_units_1'];
        self.calculated_concentration_units_2=row_dict_I['calculated_concentration_units_2'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.value_name=row_dict_I['value_name'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            value_name_I,
            distance_measure_I,
                correlation_coefficient_I,
                pvalue_I,
				pvalue_corrected_I,
				pvalue_corrected_description_I,
                 calculated_concentration_units_1_I, 
                 calculated_concentration_units_2_I,used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.value_name=value_name_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units_1 = calculated_concentration_units_1_I;
        self.calculated_concentration_units_2 = calculated_concentration_units_2_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviation_1':self.sample_name_abbreviation_1,
            'sample_name_abbreviation_2':self.sample_name_abbreviation_2,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
            'value_name':self.value_name,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'calculated_concentration_units_1':self.calculated_concentration_units_1,
            'calculated_concentration_units_2':self.calculated_concentration_units_2,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_pairWiseCorrFeaturesCrossUnits(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseCorrFeaturesCrossUnits'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseCorrFeaturesCrossUnits_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    component_name_1 = Column(String(100))
    component_name_2 = Column(String(100))
    component_group_name_1 = Column(String(100))
    component_group_name_2 = Column(String(100))
    value_name = Column(String(100))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units_1 = Column(String(50))
    calculated_concentration_units_2 = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','component_name_1','component_name_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'value_name',
                                       'calculated_concentration_units_1',
                                       'calculated_concentration_units_2',
                                       'distance_measure',
                                       'pvalue_corrected_description'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.component_name_1=row_dict_I['component_name_1'];
        self.component_name_2=row_dict_I['component_name_2'];
        self.component_group_name_1=row_dict_I['component_group_name_1'];
        self.component_group_name_2=row_dict_I['component_group_name_2'];
        self.calculated_concentration_units_1=row_dict_I['calculated_concentration_units_1'];
        self.calculated_concentration_units_2=row_dict_I['calculated_concentration_units_2'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];
        self.value_name=row_dict_I['value_name'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 component_name_1_I, component_name_2_I,
                 component_group_name_1_I, component_group_name_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            value_name_I,
                distance_measure_I,
                correlation_coefficient_I,
                pvalue_I,
				pvalue_corrected_I,
				pvalue_corrected_description_I,
                 calculated_concentration_units_1_I, 
                 calculated_concentration_units_2_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.component_name_1 = component_name_1_I;
        self.component_name_2 = component_name_2_I;
        self.component_group_name_1 = component_group_name_1_I;
        self.component_group_name_2 = component_group_name_2_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.value_name=value_name_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units_1 = calculated_concentration_units_1_I;
        self.calculated_concentration_units_2 = calculated_concentration_units_2_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'component_name_1':self.component_name_1,
            'component_name_2':self.component_name_2,
            'component_group_name_1':self.component_group_name_1,
            'component_group_name_2':self.component_group_name_2,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
            'value_name':self.value_name,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            'calculated_concentration_units_1':self.calculated_concentration_units_1,
            'calculated_concentration_units_2':self.calculated_concentration_units_2,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())