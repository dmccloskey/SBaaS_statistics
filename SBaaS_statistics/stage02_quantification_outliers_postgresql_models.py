from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_outliersDeviation(Base):
    __tablename__ = 'data_stage02_quantification_outliersDeviation'
    id = Column(Integer, Sequence('data_stage02_quantification_outliersDeviation_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    #time_point_units = Column(String(50))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    outlier_method = Column(String(10))
    outlier_deviation = Column(Float)
    outlier = Column(Boolean);
    relative_deviation_change = Column(Float)
    subset_index = Column(postgresql.ARRAY(Integer))
    subset_names = Column(postgresql.ARRAY(String(100)))
    calculated_concentration = Column(Float)
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_short','time_point','component_name'),
                      UniqueConstraint('analysis_id','experiment_id','sample_name_short','time_point','component_name',
                #'time_point_units',
                                       'calculated_concentration_units',
                                       'outlier_method','outlier_deviation','subset_index'
                                       ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.subset_index=row_dict_I['subset_index'];
        self.subset_names=row_dict_I['subset_names'];
        self.calculated_concentration=row_dict_I['calculated_concentration'];
        self.analysis_id=row_dict_I['analysis_id'];
        #self.time_point_units=row_dict_I['time_point_units']
        self.experiment_id=row_dict_I['experiment_id'];
        self.sample_name_short=row_dict_I['sample_name_short'];
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation'];
        self.used_=row_dict_I['used_'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.comment_=row_dict_I['comment_'];
        self.component_name=row_dict_I['component_name'];
        self.outlier_method=row_dict_I['outlier_method'];
        self.outlier_deviation=row_dict_I['outlier_deviation'];
        self.outlier=row_dict_I['outlier'];
        self.time_point=row_dict_I['time_point'];
        self.relative_deviation_change=row_dict_I['relative_deviation_change'];

    def __set__row__(self, 
                 analysis_id_I,
                 experiment_id_I,
                 sample_name_short_I,
                 sample_name_abbreviation_I,
                 time_point_I,
            #time_point_units_I,
                 component_group_name_I,
                 component_name_I, 
                 outlier_method_I,
                outlier_deviation_I,
                outlier_I,
                relative_deviation_change_I,
                subset_index_I,
                subset_names_I,
                 calculated_concentration_I,
                 calculated_concentration_units_I,
                 used_I,
                 comment_I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_short = sample_name_short_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        #self.time_point_units=time_point_units_I
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.outlier_method=outlier_method_I
        self.outlier_deviation=outlier_deviation_I
        self.outlier=outlier_I
        self.relative_deviation_change=relative_deviation_change_I
        self.subset_index=subset_index_I
        self.subset_names=subset_names_I
        self.calculated_concentration = calculated_concentration_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            "experiment_id":self.experiment_id,
            "sample_name_short":self.sample_name_short,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            "time_point":self.time_point,
            #'time_point_units':self.time_point_units,
            "component_group_name":self.component_group_name,
            "component_name":self.component_name,
            'outlier_method':self.outlier_method,
            'outlier_deviation':self.outlier_deviation,
            'outlier':self.outlier,
            'relative_deviation_change':self.relative_deviation_change,
            'subset_index':self.subset_index,
            'subset_names':self.subset_names,
            "calculated_concentration":self.calculated_concentration,
            "calculated_concentration_units":self.calculated_concentration_units,
            "used_":self.used_,
            'comments_I':self.comments_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())