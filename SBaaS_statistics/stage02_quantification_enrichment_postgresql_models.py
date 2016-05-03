﻿from SBaaS_base.postgresql_orm_base import *

class data_stage02_quantification_enrichment(Base):
    __tablename__ = 'data_stage02_quantification_enrichment'
    id = Column(Integer, Sequence('data_stage02_quantification_enrichment_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    experiment_id = Column(String(50))
    sample_name_abbreviation = Column(String(100))
    time_point = Column(String(10))
    #time_point_units = Column(String(50))
    enrichment_class = Column(String(500))
    enrichment_method = Column(String(50))
    enrichment_options = Column(postgresql.JSON);
    enrichment_class_database = Column(String(50))
    test_stat = Column(Float)
    test_description = Column(String(50));
    pvalue = Column(Float)
    pvalue_corrected = Column(Float)
    pvalue_corrected_description = Column(String(500))
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','experiment_id','sample_name_abbreviation','enrichment_method','time_point','calculated_concentration_units',
                                       'enrichment_class','enrichment_method',
                                       'enrichment_class_database',
                                       'test_description'
                                        #'time_point_units',
                                       ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.sample_name_abbreviation=row_dict_I['sample_name_abbreviation'];
        self.enrichment_options=row_dict_I['enrichment_options'];
        self.experiment_id=row_dict_I['experiment_id'];
        self.calculated_concentration_units=row_dict_I['calculated_concentration_units'];
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.pvalue_corrected_description=row_dict_I['pvalue_corrected_description'];
        self.pvalue_corrected=row_dict_I['pvalue_corrected'];
        self.pvalue=row_dict_I['pvalue'];
        self.test_description=row_dict_I['test_description'];
        self.test_stat=row_dict_I['test_stat'];
        self.enrichment_method=row_dict_I['enrichment_method'];
        self.enrichment_class=row_dict_I['enrichment_class'];
        self.time_point=row_dict_I['time_point'];
        #self.time_point_units=row_dict_I['time_point_units']
        self.enrichment_class_database=row_dict_I['enrichment_class_database'];

    def __set__row__(self, 
                 analysis_id_I,
                 experiment_id_I, sample_name_abbreviation_I, 
                 time_point_I,
            #time_point_units_I,
            enrichment_class_I, enrichment_method_I,
                 enrichment_options_I,enrichment_class_database_I,
                 test_stat_I, test_description_I,
                 pvalue_I, pvalue_corrected_I, pvalue_corrected_description_I,
                 calculated_concentration_units_I, used__I, comment__I):
        self.analysis_id = analysis_id_I;
        self.experiment_id = experiment_id_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.time_point = time_point_I;
        #self.time_point_units=time_point_units_I
        self.enrichment_class = enrichment_class_I;
        self.enrichment_method = enrichment_method_I;
        self.enrichment_options=enrichment_options_I;
        self.enrichment_class_database=enrichment_class_database_I;
        self.test_stat=test_stat_I;
        self.test_description=test_description_I;
        self.pvalue=pvalue_I;
        self.pvalue_corrected=pvalue_corrected_I;
        self.pvalue_corrected_description=pvalue_corrected_description_I;
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
                'experiment_id':self.experiment_id,
                'sample_name_abbreviation':self.sample_name_abbreviation,
                'time_point':self.time_point,
                'enrichment_class':self.enrichment_class,
                'enrichment_method':self.enrichment_method,
                'enrichment_options':self.enrichment_options,
                'enrichment_class_database':self.enrichment_class_database,
                'test_stat':self.test_stat,
                'test_description':self.test_description,
                'pvalue':self.pvalue,
                'pvalue_corrected':self.pvalue_corrected,
                'pvalue_corrected_description':self.pvalue_corrected_description,
                'enrichment_options':self.enrichment_options,
                'calculated_concentration_units':self.calculated_concentration_units,
                'used_':self.used_,
                'comment_':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())
class data_stage02_quantification_enrichmentClasses(Base):
    __tablename__ = 'data_stage02_quantification_enrichmentClasses'
    id = Column(Integer, Sequence('data_stage02_quantification_enrichmentClasses_id_seq'), primary_key=True)
    enrichment_class = Column(String(500))
    enrichment_class_description = Column(String(500))
    enrichment_class_weight = Column(Float)
    enrichment_class_database = Column(String(50))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('enrichment_class','component_name','enrichment_class_database'
                                       ),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.used_=row_dict_I['used_'];
        self.comment_=row_dict_I['comment_'];
        self.enrichment_class_description=row_dict_I['enrichment_class_description'];
        self.enrichment_class_weight=row_dict_I['enrichment_class_weight'];
        self.enrichment_class=row_dict_I['enrichment_class'];
        self.component_name=row_dict_I['component_name'];
        self.component_group_name=row_dict_I['component_group_name'];
        self.enrichment_class_database=row_dict_I['enrichment_class_database'];

    def __set__row__(self, 
            enrichment_class_I, enrichment_class_description_I,
            enrichment_class_weight_I,enrichment_class_database_I,
            component_group_name_I, component_name_I,
            used__I, comment__I):
        self.enrichment_class = enrichment_class_I;
        self.enrichment_class_description = enrichment_class_description_I;
        self.enrichment_class_weight = enrichment_class_weight_I;
        self.enrichment_class_database = enrichment_class_database_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self): 
        return {'id':self.id,
                'enrichment_class':self.enrichment_class,
                'enrichment_class_description':self.enrichment_class_description,
                'enrichment_class_weight':self.enrichment_class_weight,
                'enrichment_class_database':self.enrichment_class_database,
                'component_group_name':self.component_group_name,
                'component_name':self.component_name,
                'used_':self.used_,
                'comment_':self.comment_
                }
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())