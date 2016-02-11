from SBaaS_base.postgresql_orm_base import *
    
class data_stage02_quantification_count(Base):
    __tablename__ = 'data_stage02_quantification_count'
    id = Column(Integer, Sequence('data_stage02_quantification_count_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    feature_id = Column(String(500))
    feature_units = Column(String(50))
    element_id = Column(String(500))
    frequency = Column(Integer)
    fraction = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('analysis_id','feature_id','feature_units','element_id',),
            )

    #def __init__(self,
    #            row_dict_I,
    #            ):

    def __set__row(self,analysis_id_I,
            feature_id_I,
            feature_units_I,
            element_id_I,
            frequency_I,
            fraction_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.feature_id=feature_id_I
        self.feature_units=feature_units_I
        self.element_id=element_id_I
        self.frequency=frequency_I
        self.fraction=fraction_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'feature_id':self.feature_id,
                'feature_units':self.feature_units,
                'element_id':self.element_id,
                'frequency':self.frequency,
                'fraction':self.fraction,
                'used_':self.used_,
                'comment_':self.comment_,
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_countCorrelationProfile(Base):
    __tablename__ = 'data_stage02_quantification_countCorrelationProfile'
    id = Column(Integer, Sequence('data_stage02_quantification_countCorrelationProfile_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    feature_id = Column(String(500))
    feature_units = Column(String(50))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient_threshold = Column(String(50));
    element_id = Column(String(500))
    frequency = Column(Integer)
    fraction = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('analysis_id','feature_id','feature_units','distance_measure','correlation_coefficient_threshold','element_id',),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.comment_=data_dict_I['comment_'];
        self.analysis_id=data_dict_I['analysis_id'];
        self.feature_id=data_dict_I['feature_id'];
        self.feature_units=data_dict_I['feature_units'];
        self.distance_measure=data_dict_I['distance_measure'];
        self.correlation_coefficient_threshold=data_dict_I['correlation_coefficient_threshold'];
        self.element_id=data_dict_I['element_id'];
        self.frequency=data_dict_I['frequency'];
        self.fraction=data_dict_I['fraction'];
        self.used_=data_dict_I['used_'];

    def __set__row__(self,analysis_id_I,
            feature_id_I,
            feature_units_I,
            distance_measure_I,
            correlation_coefficient_threshold_I,
            element_id_I,
            frequency_I,
            fraction_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.feature_id=feature_id_I
        self.feature_units=feature_units_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient_threshold=correlation_coefficient_threshold_I
        self.element_id=element_id_I
        self.frequency=frequency_I
        self.fraction=fraction_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'feature_id':self.feature_id,
                'feature_units':self.feature_units,
                'distance_measure':self.distance_measure,
                'correlation_coefficient_threshold':self.correlation_coefficient_threshold,
                'element_id':self.element_id,
                'frequency':self.frequency,
                'fraction':self.fraction,
                'used_':self.used_,
                'comment_':self.comment_,
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_countCorrelationTrend(Base):
    __tablename__ = 'data_stage02_quantification_countCorrelationTrend'
    id = Column(Integer, Sequence('data_stage02_quantification_countCorrelationTrend_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    feature_id = Column(String(500))
    feature_units = Column(String(50))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient_threshold = Column(String(50));
    element_id = Column(String(500))
    frequency = Column(Integer)
    fraction = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('analysis_id','feature_id','feature_units','distance_measure','correlation_coefficient_threshold','element_id',),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.comment_=data_dict_I['comment_'];
        self.analysis_id=data_dict_I['analysis_id'];
        self.feature_id=data_dict_I['feature_id'];
        self.feature_units=data_dict_I['feature_units'];
        self.distance_measure=data_dict_I['distance_measure'];
        self.correlation_coefficient_threshold=data_dict_I['correlation_coefficient_threshold'];
        self.element_id=data_dict_I['element_id'];
        self.frequency=data_dict_I['frequency'];
        self.fraction=data_dict_I['fraction'];
        self.used_=data_dict_I['used_'];

    def __set__row__(self,analysis_id_I,
            feature_id_I,
            feature_units_I,
            distance_measure_I,
            correlation_coefficient_threshold_I,
            element_id_I,
            frequency_I,
            fraction_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.feature_id=feature_id_I
        self.feature_units=feature_units_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient_threshold=correlation_coefficient_threshold_I
        self.element_id=element_id_I
        self.frequency=frequency_I
        self.fraction=fraction_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'feature_id':self.feature_id,
                'feature_units':self.feature_units,
                'distance_measure':self.distance_measure,
                'correlation_coefficient_threshold':self.correlation_coefficient_threshold,
                'element_id':self.element_id,
                'frequency':self.frequency,
                'fraction':self.fraction,
                'used_':self.used_,
                'comment_':self.comment_,
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_countCorrelationPattern(Base):
    __tablename__ = 'data_stage02_quantification_countCorrelationPattern'
    id = Column(Integer, Sequence('data_stage02_quantification_countCorrelationPattern_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    feature_id = Column(String(500))
    feature_units = Column(String(50))
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient_threshold = Column(String(50));
    element_id = Column(String(500))
    frequency = Column(Integer)
    fraction = Column(Float)
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
            UniqueConstraint('analysis_id','feature_id','feature_units','distance_measure','correlation_coefficient_threshold','element_id',),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.comment_=data_dict_I['comment_'];
        self.analysis_id=data_dict_I['analysis_id'];
        self.feature_id=data_dict_I['feature_id'];
        self.feature_units=data_dict_I['feature_units'];
        self.distance_measure=data_dict_I['distance_measure'];
        self.correlation_coefficient_threshold=data_dict_I['correlation_coefficient_threshold'];
        self.element_id=data_dict_I['element_id'];
        self.frequency=data_dict_I['frequency'];
        self.fraction=data_dict_I['fraction'];
        self.used_=data_dict_I['used_'];

    def __set__row__(self,analysis_id_I,
            feature_id_I,
            feature_units_I,
            distance_measure_I,
            correlation_coefficient_threshold_I,
            element_id_I,
            frequency_I,
            fraction_I,
            used__I,
            comment__I,):
        self.analysis_id=analysis_id_I
        self.feature_id=feature_id_I
        self.feature_units=feature_units_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient_threshold=correlation_coefficient_threshold_I
        self.element_id=element_id_I
        self.frequency=frequency_I
        self.fraction=fraction_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'feature_id':self.feature_id,
                'feature_units':self.feature_units,
                'distance_measure':self.distance_measure,
                'correlation_coefficient_threshold':self.correlation_coefficient_threshold,
                'element_id':self.element_id,
                'frequency':self.frequency,
                'fraction':self.fraction,
                'used_':self.used_,
                'comment_':self.comment_,
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())