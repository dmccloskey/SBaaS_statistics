from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_glogNormalized(Base):
    __tablename__ = 'data_stage02_quantification_glogNormalized'
    id = Column(Integer, Sequence('data_stage02_quantification_glogNormalized_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    time_point = Column(String(10))
    #time_point_units = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_short','time_point','component_name'),
                      UniqueConstraint('analysis_id','experiment_id','sample_name_short','time_point',
                            'component_name','calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.experiment_id=row_dict_I['experiment_id'];
        self.sample_name_short=row_dict_I['sample_name_short'];
        self.time_point=row_dict_I['time_point'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.component_name=row_dict_I['component_name'];
        self.calculated_concentration=row_dict_I['calculated_concentration'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];

    def __set__row__(self, 
                 analysis_id_I,
                 experiment_id_I, sample_name_short_I, time_point_I,
            #time_point_units_I,
                 component_group_name_I, component_name_I, calculated_concentration_I,calculated_concentration_units_I,
                 used_I,comment_I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        self.time_point = time_point_I;
        #self.time_point_units=time_point_units_I
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            "experiment_id":self.experiment_id,
                "sample_name_short":self.sample_name_short,
                "time_point":self.time_point,
            #'time_point_units':self.time_point_units,
                "component_group_name":self.component_group_name,
                "component_name":self.component_name,
                "calculated_concentration":self.calculated_concentration,
                "calculated_concentration_units":self.calculated_concentration_units,
                "used_":self.used_,
                'comment_':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())