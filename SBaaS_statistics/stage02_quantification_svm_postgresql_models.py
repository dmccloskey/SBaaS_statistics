from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_svm(Base):
    #TODO
    __tablename__ = 'data_stage02_quantification_svm'
    id = Column(Integer, Sequence('data_stage02_quantification_svm_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_short = Column(String(100))
    time_point = Column(String(10))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    #...
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('experiment_id','sample_name_short','component_name'),
                      #UniqueConstraint('analysis_id','experiment_id','sample_name_short','component_name',''),
            )

    def __init__(self, 
                 #analysis_id_I,
                 experiment_id_I, sample_name_I, sample_name_abbreviation_I,
                 time_point_I, dilution_I, replicate_number_I, met_id_I, used_I, comment_I):
        #self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name = sample_name_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        self.dilution = dilution_I;
        self.replicate_number = replicate_number_I;
        self.met_id = met_id_I;
        #...
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self): # not complete!
        return {'id':self.id,
            #"analysis_id":self.analysis_id,
            'experiment_id_I':self.experiment_id,
                'sample_name_I':self.sample_name,
                'sample_name_abbreviation_I':self.sample_name_abbreviation,
                'time_point_I':self.time_point,
                'dilution_I':self.dilution,
                'replicate_number_I':self.replicate_number,
                'met_id_I':self.met_id,
                #...
                'used_I':self.used_,
                'comments_I':self.comments_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())