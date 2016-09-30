from SBaaS_base.postgresql_orm_base import *

class data_stage02_quantification_pairWiseTable(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseTable'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseTable_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    #time_point_1 = Column(String(10))
    #time_point_2 = Column(String(10))
    #time_point_units = Column(String(50))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    value_name = Column(String(500))
    value_1 = Column(Float)
    value_2 = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','sample_name_abbreviation_1','sample_name_abbreviation_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'component_name',
                                        'value_name',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.sample_name_abbreviation_1=row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_abbreviation_2=row_dict_I['sample_name_abbreviation_2'];
        self.component_name=row_dict_I['component_name'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.value_name=row_dict_I['value_name'];
        self.value_1=row_dict_I['value_1'];
        self.value_2=row_dict_I['value_2'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            component_group_name_I, component_name_I,
            value_name_I,
            value_1_I,
            value_2_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.value_name=value_name_I
        self.value_1=value_1_I
        self.value_2=value_2_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviation_1':self.sample_name_abbreviation_1,
            'sample_name_abbreviation_2':self.sample_name_abbreviation_2,
                'component_group_name':self.component_group_name,
                'component_name':self.component_name,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
            'value_name':self.value_name,
            'value_1':self.value_1,
            'value_2':self.value_2,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_pairWiseTable_replicates(Base):
    #pairedttest
    __tablename__ = 'data_stage02_quantification_pairWiseTable_replicates'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseTable_replicates_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    sample_name_short_1 = Column(String(100))
    sample_name_short_2 = Column(String(100))
    #time_point_1 = Column(String(10))
    #time_point_2 = Column(String(10))
    #time_point_units = Column(String(50))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    calculated_concentration_1 = Column(Float)
    calculated_concentration_2 = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','sample_name_short_1','sample_name_short_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'component_name',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.sample_name_abbreviation_1=row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_abbreviation_2=row_dict_I['sample_name_abbreviation_2'];
        self.sample_name_short_1=row_dict_I['sample_name_short_1'];
        self.sample_name_short_2=row_dict_I['sample_name_short_2'];
        self.component_name=row_dict_I['component_name'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.calculated_concentration_1=row_dict_I['calculated_concentration_1'];
        self.calculated_concentration_2=row_dict_I['calculated_concentration_2'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 sample_name_short_1_I, sample_name_short_2_I,
            component_group_name_I, component_name_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            calculated_concentration_1_I,
            calculated_concentration_2_I,
                 calculated_concentration_units_I, used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        self.sample_name_short_1 = sample_name_short_1_I;
        self.sample_name_short_2 = sample_name_short_2_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.calculated_concentration_1 = calculated_concentration_1_I;
        self.calculated_concentration_2 = calculated_concentration_2_I;
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
                'component_group_name':self.component_group_name,
                'component_name':self.component_name,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
                "calculated_concentration_1":self.calculated_concentration_1,
                "calculated_concentration_2":self.calculated_concentration_2,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_pairWiseTableFeatures(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseTableFeatures'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseTableFeatures_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    component_name_1 = Column(String(100))
    component_name_2 = Column(String(100))
    component_group_name_1 = Column(String(100))
    component_group_name_2 = Column(String(100))
    value_name = Column(String(100))
    value_1 = Column(Float)
    value_2 = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','component_name_1','component_name_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'value_name',
                                       'calculated_concentration_units',),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.component_name_1=row_dict_I['component_name_1'];
        self.component_name_2=row_dict_I['component_name_2'];
        self.component_group_name_1=row_dict_I['component_group_name_1'];
        self.component_group_name_2=row_dict_I['component_group_name_2'];
        self.value_2=row_dict_I['value_2'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.value_1=row_dict_I['value_1'];
        self.value_name=row_dict_I['value_name'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 component_name_1_I, component_name_2_I,
                 component_group_name_1_I, component_group_name_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            value_name_I,
                value_1_I,
                 value_2_I,
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
        self.value_1=value_1_I
        self.value_2=value_2_I;
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
            'value_1':self.value_1,
            'value_2':self.value_2,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_pairWiseTableCrossUnits(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseTableCrossUnits'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseTableCrossUnits_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    sample_name_abbreviation_1 = Column(String(100))
    sample_name_abbreviation_2 = Column(String(100))
    #time_point_1 = Column(String(10))
    #time_point_2 = Column(String(10))
    #time_point_units = Column(String(50))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    value_name = Column(String(500))
    value_1 = Column(Float)
    value_2 = Column(Float)
    calculated_concentration_units_1 = Column(String(50))
    calculated_concentration_units_2 = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','sample_name_abbreviation_1','sample_name_abbreviation_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'component_name',
                                        'value_name',
                                       'calculated_concentration_units_1',
                                       'calculated_concentration_units_2'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.sample_name_abbreviation_1=row_dict_I['sample_name_abbreviation_1'];
        self.sample_name_abbreviation_2=row_dict_I['sample_name_abbreviation_2'];
        self.component_name=row_dict_I['component_name'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.calculated_concentration_units_1=row_dict_I['calculated_concentration_units_1'];
        self.calculated_concentration_units_2=row_dict_I['calculated_concentration_units_2'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.value_name=row_dict_I['value_name'];
        self.value_1=row_dict_I['value_1'];
        self.value_2=row_dict_I['value_2'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 sample_name_abbreviation_1_I, sample_name_abbreviation_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            component_group_name_I, component_name_I,
            value_name_I,
            value_1_I,
            value_2_I,
                 calculated_concentration_units_1_I, 
                 calculated_concentration_units_2_I,used_I, comment_I):
        self.analysis_id = analysis_id_I;
        #self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation_1 = sample_name_abbreviation_1_I;
        self.sample_name_abbreviation_2 = sample_name_abbreviation_2_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        #self.time_point_1 = time_point_1_I;
        #self.time_point_2 = time_point_2_I;
        #self.time_point_units=time_point_units_I
        self.value_name=value_name_I
        self.value_1=value_1_I
        self.value_2=value_2_I
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
                'component_group_name':self.component_group_name,
                'component_name':self.component_name,
            #'time_point_1':self.time_point_1,
            #'time_point_2':self.time_point_2,
            #'time_point_units':self.time_point_units,
            'value_name':self.value_name,
            'value_1':self.value_1,
            'value_2':self.value_2,
            'calculated_concentration_units_1':self.calculated_concentration_units_1,
            'calculated_concentration_units_2':self.calculated_concentration_units_2,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_pairWiseTableFeaturesCrossUnits(Base):
    __tablename__ = 'data_stage02_quantification_pairWiseTableFeaturesCrossUnits'
    id = Column(Integer, Sequence('data_stage02_quantification_pairWiseTableFeaturesCrossUnits_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    #experiment_id = Column(String(50))
    component_name_1 = Column(String(100))
    component_name_2 = Column(String(100))
    component_group_name_1 = Column(String(100))
    component_group_name_2 = Column(String(100))
    value_name = Column(String(100))
    value_1 = Column(Float)
    value_2 = Column(Float)
    calculated_concentration_units_1 = Column(String(50))
    calculated_concentration_units_2 = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','component_name_1','component_name_2',
                                       #time_point_1, time_point_2,
                                        #time_point_units,
                                        'value_name',
                                       'calculated_concentration_units_1',
                                       'calculated_concentration_units_2'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.component_name_1=row_dict_I['component_name_1'];
        self.component_name_2=row_dict_I['component_name_2'];
        self.component_group_name_1=row_dict_I['component_group_name_1'];
        self.component_group_name_2=row_dict_I['component_group_name_2'];
        self.value_2=row_dict_I['value_2'];
        self.calculated_concentration_units_1=row_dict_I['calculated_concentration_units_1'];
        self.calculated_concentration_units_2=row_dict_I['calculated_concentration_units_2'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_1=row_dict_I['time_point_1']
        #self.time_point_2=row_dict_I['time_point_2']
        #self.time_point_units=row_dict_I['time_point_units']
        self.value_1=row_dict_I['value_1'];
        self.value_name=row_dict_I['value_name'];

    def __set__row__(self,
                 analysis_id_I,
                 #experiment_id_I,
                 component_name_1_I, component_name_2_I,
                 component_group_name_1_I, component_group_name_2_I,
                 #time_point_1_I, time_point_2_I,
            #time_point_units_I,
            value_name_I,
                value_1_I,
                 value_2_I,
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
        self.value_1=value_1_I
        self.value_2=value_2_I;
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
            'value_1':self.value_1,
            'value_2':self.value_2,
            'calculated_concentration_units_1':self.calculated_concentration_units_1,
            'calculated_concentration_units_2':self.calculated_concentration_units_2,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())