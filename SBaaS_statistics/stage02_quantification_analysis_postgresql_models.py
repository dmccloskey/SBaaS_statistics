from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_analysis(Base):
    __tablename__ = 'data_stage02_quantification_analysis'
    id = Column(Integer, Sequence('data_stage02_quantification_analysis_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    #time_point_units = Column(String(50))
    analysis_type = Column(String(100)); # time-course (i.e., multiple time points), paired (i.e., control compared to multiple replicates), group (i.e., single grouping of samples).
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint(
                'experiment_id','sample_name_short','sample_name_abbreviation',
                'time_point',
                #'time_point_units',
                'analysis_type','analysis_id'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.analysis_id=row_dict_I['analysis_id']
        self.experiment_id=row_dict_I['experiment_id']
        self.sample_name_short=row_dict_I['sample_name_short']
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation']
        self.time_point=row_dict_I['time_point']
        #self.time_point_units=row_dict_I['time_point_units']
        self.analysis_type=row_dict_I['analysis_type']
        self.used_=row_dict_I['used_']
        self.comment_=row_dict_I['comment_']

    def __set__row__(self,analysis_id_I,
                 experiment_id_I,
            sample_name_short_I,
            sample_name_abbreviation_I,
            time_point_I,
            #time_point_units_I,
            analysis_type_I,
            used__I,
            comment__I):
        self.analysis_id=analysis_id_I
        self.experiment_id=experiment_id_I
        self.sample_name_short=sample_name_short_I
        self.sample_name_abbreviation=sample_name_abbreviation_I
        self.time_point=time_point_I
        #self.time_point_units=time_point_units_I
        self.analysis_type=analysis_type_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'experiment_id':self.experiment_id,
            'sample_name_short':self.sample_name_short,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'time_point':self.time_point,
            #'time_point_units':self.time_point_units,
            'analysis_type':self.analysis_type,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())