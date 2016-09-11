from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_dataPreProcessing_points(Base):
    __tablename__ = 'data_stage02_quantification_dataPreProcessing_points'
    id = Column(Integer, Sequence('data_stage02_quantification_dataPreProcessing_points_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    #time_point_units = Column(String(50))
    file_dir = Column(Text)
    file_type = Column(String(50))
    component_exclusion_list = Column(postgresql.ARRAY(String));
    calculated_concentration_units = Column(String(50))
    imputation_method = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','experiment_id','sample_name_abbreviation','time_point','calculated_concentration_units',
                #'time_point_units',
                                       ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation'];
        self.file_dir=row_dict_I['file_dir'];
        self.file_type=row_dict_I['file_type'];
        self.experiment_id=row_dict_I['experiment_id'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.component_exclusion_list=row_dict_I['component_exclusion_list'];
        self.time_point=row_dict_I['time_point'];
        #self.time_point_units=row_dict_I['time_point_units']
        self.imputation_method=row_dict_I['imputation_method'];

    def __set__row__(self, 
                 analysis_id_I,
                 experiment_id_I, 
                 sample_name_abbreviation_I, 
                 time_point_I,
            #time_point_units_I,            
            component_exclusion_list_I,
                 file_dir_I, file_type_I,
                 calculated_concentration_units_I, 
                 imputation_method_I,
                 used__I, comment__I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        #self.time_point_units=time_point_units_I
        self.component_exclusion_list = component_exclusion_list_I;
        self.file_dir=file_dir_I;
        self.file_type=file_type_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.imputation_method = imputation_method_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'component_exclusion_list':self.component_exclusion_list,
                'file_dir':self.file_dir,
                'file_type':self.file_type,
                'calculated_concentration_units':self.calculated_concentration_units,
                "imputation_method":self.imputation_method,
                'used_':self.used_,
                'comment_':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_dataPreProcessing_points_mv(Base):
    __tablename__ = 'data_stage02_quantification_dataPreProcessing_points_mv'
    id = Column(Integer, Sequence('data_stage02_quantification_dataPreProcessing_points_mv_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    missing_values = Column(Integer)
    missing_fraction = Column(Float)
    calculated_concentration_units = Column(String(50))
    mv_value = Column(Float)
    mv_operator = Column(String(50))
    mv_feature = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_abbreviation','time_point','component_exclusion_list'),
                      UniqueConstraint('analysis_id',
                            'calculated_concentration_units',
                            'mv_value',
                            'mv_operator',
                            'mv_feature'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.missing_values=row_dict_I['missing_values'];
        self.missing_fraction=row_dict_I['missing_fraction'];
        self.mv_value=row_dict_I['mv_value'];
        self.mv_operator=row_dict_I['mv_operator'];
        self.mv_feature=row_dict_I['mv_feature'];

    def __set__row__(self, 
                 analysis_id_I,
                 missing_values_I,
                 missing_fraction_I,
                 calculated_concentration_units_I,
                 mv_value_I,
                 mv_operator_I,
                 mv_feature_I,
                 used_I,comment_I):
        self.analysis_id = analysis_id_I;
        self.missing_values = missing_values_I;
        self.missing_fraction = missing_fraction_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.mv_value = mv_value_I;
        self.mv_operator = mv_operator_I;
        self.mv_feature = mv_feature_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            "missing_values":self.missing_values,
            "missing_fraction":self.missing_fraction,
            "calculated_concentration_units":self.calculated_concentration_units,
            "mv_value":self.mv_value,
            "mv_operator":self.operator,
            "mv_feature":self.mv_feature,
            "used_":self.used_,
            'comment_I':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_dataPreProcessing_points_im(Base):
    __tablename__ = 'data_stage02_quantification_dataPreProcessing_points_im'
    id = Column(Integer, Sequence('data_stage02_quantification_dataPreProcessing_points_im_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    imputation_method = Column(String(50))
    imputation_options = Column(postgresql.JSON);
    normalization_method = Column(String(50))
    normalization_options = Column(postgresql.JSON);
    mv_feature = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id',
                            'imputation_method',
                            'normalization_method',
                            'mv_feature',
                            'calculated_concentration_units',),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.imputation_method=row_dict_I['imputation_method'];
        self.imputation_options=row_dict_I['imputation_options'];
        self.normalization_method=row_dict_I['normalization_method'];
        self.normalization_options=row_dict_I['normalization_options'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.mv_feature=row_dict_I['mv_feature'];

    def __set__row__(self, 
                 analysis_id_I,
                 imputation_method_I,
                 imputation_options_I,
                 normalization_method_I,
                 normalization_options_I,
                 mv_feature_I,
                 calculated_concentration_units_I,
                 used_I,comment_I):
        self.analysis_id = analysis_id_I;
        self.imputation_method = imputation_method_I;
        self.imputation_options = imputation_options_I;
        self.normalization_method = normalization_method_I;
        self.normalization_options = normalization_options_I;
        self.mv_feature = mv_feature_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {'id':self.id,
            "analysis_id":self.analysis_id,
            "imputation_method":self.imputation_method,
            "imputation_options":self.imputation_options,
            "normalization_method":self.normalization_method,
            "normalization_options":self.normalization_options,
            "calculated_concentration_units":self.calculated_concentration_units,
            "used_":self.used_,
            'comment_I':self.comment_,
            "mv_feature":self.mv_feature,
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())