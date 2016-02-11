from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_correlationProfile(Base):
    __tablename__ = 'data_stage02_quantification_correlationProfile'
    id = Column(Integer, Sequence('data_stage02_quantification_correlationProfile_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_abbreviations = Column(postgresql.ARRAY(String(100))) #order of sample_name_abbreviations
    #time_points = Column(postgresql.ARRAY(Float)) #order of sample_name_abbreviations
    profile_match = Column(String(500)) #string profile (0-1-2-3)
    profile_match_description = Column(String(500)) #"increase"
    component_match = Column(String(500)) #component_name
    component_match_units = Column(String(50)) #component_name calculated_concentration_units
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    component_profile = Column(String(500))
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    #time_point_units = Column(String(50))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                                       'sample_name_abbreviations',
                                       #'time_points',
                                       'profile_match',
                                       'component_match',
                                       'component_match_units',
                                       'distance_measure',
                                       'component_name',
                                    #'time_point_units',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):        
        self.component_name=row_dict_I['component_name'];
        self.component_match=row_dict_I['component_match'];
        self.component_match_units=row_dict_I['component_match_units'];
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];
        self.component_group_name=row_dict_I['component_group_name'];
        #self.time_points=row_dict_I['time_points']
        #self.time_point_units=row_dict_I['time_point_units']
        self.analysis_id=row_dict_I['analysis_id'];
        self.sample_name_abbreviations=row_dict_I['sample_name_abbreviations'];
        self.profile_match=row_dict_I['profile_match'];
        self.profile_match_description=row_dict_I['profile_match_description'];
        self.component_profile=row_dict_I['component_profile'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];


    def __set__row__(self, 
                 analysis_id_I,
                sample_name_abbreviations_I,
                #time_points_I,
                profile_match_I,
                profile_match_description_I,
                component_match_I,
                component_match_units_I,
                distance_measure_I,
                correlation_coefficient_I,
                component_group_name_I,
                component_name_I,
                component_profile_I,
                pvalue_I,
                pvalue_corrected_I,
                pvalue_corrected_description_I,
                #time_point_units_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.sample_name_abbreviations=sample_name_abbreviations_I
        #self.time_points=time_points_I
        self.profile_match=profile_match_I
        self.profile_match_description=profile_match_description_I
        self.component_match=component_match_I
        self.component_match_units=component_match_units_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.component_group_name=component_group_name_I
        self.component_name=component_name_I
        self.component_profile=component_profile_I
        self.pvalue=pvalue_I
        self.pvalue_corrected=pvalue_corrected_I
        self.pvalue_corrected_description=pvalue_corrected_description_I
        #self.time_point_units=time_point_units_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self): 
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviations':self.sample_name_abbreviations,
            #'time_points':self.time_points,
            'profile_match':self.profile_match,
            'profile_match_description':self.profile_match_description,
            'component_match':self.component_match,
            'component_match_units':self.component_match_units,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'component_profile':self.component_profile,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            #'time_point_units':self.time_point_units,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_correlationTrend(Base):
    __tablename__ = 'data_stage02_quantification_correlationTrend'
    id = Column(Integer, Sequence('data_stage02_quantification_correlationTrend_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_abbreviations = Column(postgresql.ARRAY(String(100))) #order of sample_name_abbreviations
    trend_match = Column(String(500)) #string trend (0-1-2-3)
    trend_match_description = Column(String(500)) #"increase"
    component_match = Column(String(500)) #component_name
    component_match_units = Column(String(50)) #component_name calculated_concentration_units
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    component_trend = Column(String(500))
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                                       'sample_name_abbreviations',
                                       'trend_match',
                                       'component_match',
                                       'component_match_units',
                                       'distance_measure',
                                       'component_name',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):        
        self.comment_=row_dict_I['comment_'];
        #self.time_point_units=row_dict_I['time_point_units']
        self.analysis_id=row_dict_I['analysis_id'];
        self.sample_name_abbreviations=row_dict_I['sample_name_abbreviations'];
        self.trend_match=row_dict_I['trend_match'];
        self.trend_match_description=row_dict_I['trend_match_description'];
        self.component_match=row_dict_I['component_match'];
        self.component_match_units=row_dict_I['component_match_units'];
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.component_name=row_dict_I['component_name'];
        self.component_trend=row_dict_I['component_trend'];
        self.pvalue=row_dict_I['pvalue'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];



    def __set__row__(self, 
                 analysis_id_I,
                sample_name_abbreviations_I,
                trend_match_I,
                trend_match_description_I,
                component_match_I,
                component_match_units_I,
                distance_measure_I,
                correlation_coefficient_I,
                component_group_name_I,
                component_name_I,
                component_trend_I,
                pvalue_I,
                pvalue_corrected_I,
                pvalue_corrected_description_I,
            #time_point_units_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.sample_name_abbreviations=sample_name_abbreviations_I
        self.trend_match=trend_match_I
        self.trend_match_description=trend_match_description_I
        self.component_match=component_match_I
        self.component_match_units=component_match_units_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.component_group_name=component_group_name_I
        self.component_name=component_name_I
        self.component_trend=component_trend_I
        self.pvalue=pvalue_I
        self.pvalue_corrected=pvalue_corrected_I
        self.pvalue_corrected_description=pvalue_corrected_description_I
        #self.time_point_units=time_point_units_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self): 
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviations':self.sample_name_abbreviations,
            'trend_match':self.trend_match,
            'trend_match_description':self.trend_match_description,
            'component_match':self.component_match,
            'component_match_units':self.component_match_units,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'component_trend':self.component_trend,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            #'time_point_units':self.time_point_units,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_correlationPattern(Base):
    __tablename__ = 'data_stage02_quantification_correlationPattern'
    id = Column(Integer, Sequence('data_stage02_quantification_correlationPattern_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_abbreviations = Column(postgresql.ARRAY(String(100))) #order of sample_name_abbreviations
    pattern_match = Column(String(500)) #string pattern (0-1-2-3)
    pattern_match_description = Column(String(500)) #"increase"
    component_match = Column(String(500)) #component_name
    component_match_units = Column(String(50)) #component_name calculated_concentration_units
    distance_measure = Column(String(50)); #pearson or spearman
    correlation_coefficient = Column(Float)
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    component_pattern = Column(String(500))
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id',
                                       'sample_name_abbreviations',
                                       'pattern_match',
                                       'component_match',
                                       'component_match_units',
                                       'distance_measure',
                                       'component_name',
                                       'calculated_concentration_units'),
            )

    def __init__(self,
                row_dict_I,
                ):        
        self.pvalue=row_dict_I['pvalue'];
        self.component_pattern=row_dict_I['component_pattern'];
        self.component_name=row_dict_I['component_name'];
        self.sample_name_abbreviations=row_dict_I['sample_name_abbreviations'];
        self.pattern_match=row_dict_I['pattern_match'];
        self.pattern_match_description=row_dict_I['pattern_match_description'];
        self.component_match=row_dict_I['component_match'];
        self.component_match_units=row_dict_I['component_match_units'];
        self.distance_measure=row_dict_I['distance_measure'];
        self.correlation_coefficient=row_dict_I['correlation_coefficient'];
        self.component_group_name=row_dict_I['component_group_name'];
        #self.time_point_units=row_dict_I['time_point_units']
        self.analysis_id=row_dict_I['analysis_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];


    def __set__row__(self, 
                 analysis_id_I,
                sample_name_abbreviations_I,
                pattern_match_I,
                pattern_match_description_I,
                component_match_I,
                component_match_units_I,
                distance_measure_I,
                correlation_coefficient_I,
                component_group_name_I,
                component_name_I,
                component_pattern_I,
                pvalue_I,
                pvalue_corrected_I,
                pvalue_corrected_description_I,
            #time_point_units_I,
                calculated_concentration_units_I,
                used__I,
                comment__I,):
        self.analysis_id=analysis_id_I
        self.sample_name_abbreviations=sample_name_abbreviations_I
        self.pattern_match=pattern_match_I
        self.pattern_match_description=pattern_match_description_I
        self.component_match=component_match_I
        self.component_match_units=component_match_units_I
        self.distance_measure=distance_measure_I
        self.correlation_coefficient=correlation_coefficient_I
        self.component_group_name=component_group_name_I
        self.component_name=component_name_I
        self.component_pattern=component_pattern_I
        self.pvalue=pvalue_I
        self.pvalue_corrected=pvalue_corrected_I
        self.pvalue_corrected_description=pvalue_corrected_description_I
        #self.time_point_units=time_point_units_I
        self.calculated_concentration_units=calculated_concentration_units_I
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self): 
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_abbreviations':self.sample_name_abbreviations,
            'pattern_match':self.pattern_match,
            'pattern_match_description':self.pattern_match_description,
            'component_match':self.component_match,
            'component_match_units':self.component_match_units,
            'distance_measure':self.distance_measure,
            'correlation_coefficient':self.correlation_coefficient,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'component_pattern':self.component_pattern,
            'pvalue':self.pvalue,
            'pvalue_corrected':self.pvalue_corrected,
            'pvalue_corrected_description':self.pvalue_corrected_description,
            #'time_point_units':self.time_point_units,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_,}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())