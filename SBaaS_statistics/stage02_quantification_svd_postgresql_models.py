from SBaaS_base.postgresql_orm_base import *
class data_stage02_quantification_svd_u(Base):
    __tablename__ = 'data_stage02_quantification_svd_u'
    id = Column(Integer, Sequence('data_stage02_quantification_svd_u_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    sample_name_short = Column(String(100))
    sample_name_abbreviation = Column(String(100))
    u_matrix = Column(Float);
    singular_value_index = Column(Integer);
    svd_method = Column(String(50))
    svd_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','sample_name_short','singular_value_index','calculated_concentration_units',
                                       'svd_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.sample_name_short = row_dict_I['sample_name_short'];
        self.sample_name_abbreviation = row_dict_I['sample_name_abbreviation'];
        self.u_matrix=row_dict_I['u_matrix'];
        self.singular_value_index=row_dict_I['singular_value_index'];
        self.svd_method=row_dict_I['svd_method'];
        self.svd_options=row_dict_I['svd_options'];
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, 
                analysis_id_I,
                sample_name_short_I, 
                sample_name_abbreviation_I, 
                u_matrix_I, singular_value_index_I,
                svd_method_I,
                svd_options_I,
                calculated_concentration_units_I,
                used_I,
                comment_I
                ):
        self.analysis_id = analysis_id_I;
        self.sample_name_short = sample_name_short_I;
        self.sample_name_abbreviation = sample_name_abbreviation_I;
        self.u_matrix=u_matrix_I
        self.singular_value_index=singular_value_index_I
        self.svd_method=svd_method_I
        self.svd_options=svd_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used_I;
        self.comment_ = comment_I;

    def __repr__dict__(self):
        return {
            'id':self.id,
            'analysis_id':self.analysis_id,
            'sample_name_short':self.sample_name_short,
            'sample_name_abbreviation':self.sample_name_abbreviation,
            'u_matrix':self.u_matrix,
            'singular_value_index':self.singular_value_index,
            'svd_method':self.svd_method,
            'svd_options':self.svd_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_svd_d(Base):
    __tablename__ = 'data_stage02_quantification_svd_d'
    id = Column(Integer, Sequence('data_stage02_quantification_svd_d_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    d_vector = Column(Float);
    d_fraction = Column(Float);
    d_fraction_cumulative = Column(Float);
    singular_value_index = Column(Integer)
    svd_method = Column(String(50))
    svd_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','singular_value_index','calculated_concentration_units',
                                       'svd_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                 ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.d_vector=row_dict_I['d_vector']
        self.d_fraction=row_dict_I['d_fraction']
        self.d_fraction_cumulative=row_dict_I['d_fraction_cumulative']
        self.singular_value_index=row_dict_I['singular_value_index']
        self.svd_method=row_dict_I['svd_method']
        self.svd_options=row_dict_I['svd_options']
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];

    def __set__row__(self, 
                 analysis_id_I,
                 d_vector_I,
                 singular_value_index_I,
                svd_method_I,
                svd_options_I,
                 calculated_concentration_units_I, 
                 used__I,
                 comment__I
                 ):
        self.analysis_id = analysis_id_I;
        self.d_vector=d_vector_I
        self.singular_value_index=singular_value_index_I
        self.svd_method=svd_method_I
        self.svd_options=svd_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'd_vector':self.d_vector,
            'd_fraction':self.d_fraction,
            'd_fraction_cumulative':self.d_fraction_cumulative,
            'singular_value_index':self.singular_value_index,
            'svd_method':self.svd_method,
            'svd_options':self.svd_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())

class data_stage02_quantification_svd_v(Base):
    __tablename__ = 'data_stage02_quantification_svd_v'
    id = Column(Integer, Sequence('data_stage02_quantification_svd_v_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    component_group_name = Column(String(100))
    component_name = Column(String(500))
    v_matrix = Column(Float);
    singular_value_index = Column(Integer)
    svd_method = Column(String(50))
    svd_options = Column(postgresql.JSON);
    calculated_concentration_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (
                      UniqueConstraint('analysis_id','component_name','singular_value_index','calculated_concentration_units',
                                       'svd_method'
                                       ),
            )

    def __init__(self, 
                row_dict_I,
                #analysis_id_I,
                #component_group_name_I,
                #component_name_I,
                #u_matrix_I,
                #singular_value_index_I,
                #svd_method_I,
                #svd_options_I,
                #calculated_concentration_units_I, 
                #used__I,
                #comment__I
                ):
        self.analysis_id = row_dict_I['analysis_id'];
        self.component_group_name = row_dict_I['component_group_name'];
        self.component_name = row_dict_I['component_name'];
        self.v_matrix=row_dict_I['v_matrix']
        self.singular_value_index=row_dict_I['singular_value_index']
        self.svd_method=row_dict_I['svd_method']
        self.svd_options=row_dict_I['svd_options']
        self.calculated_concentration_units = row_dict_I['calculated_concentration_units'];
        self.used_ = row_dict_I['used_'];
        self.comment_ = row_dict_I['comment_'];
        #self.analysis_id = analysis_id_I;
        #self.component_group_name = component_group_name_I;
        #self.component_name = component_name_I;
        #self.u_matrix=u_matrix_I
        #self.singular_value_index=singular_value_index_I
        #self.svd_options=svd_options_I
        #self.calculated_concentration_units = calculated_concentration_units_I;
        #self.used_ = used__I;
        #self.comment_ = comment__I;

    def __set__row__(self, 
                analysis_id_I,
                component_group_name_I,
                component_name_I,
                u_matrix_I,
                singular_value_index_I,
                svd_method_I,
                svd_options_I,
                calculated_concentration_units_I, 
                used__I,
                comment__I
                ):
        self.analysis_id = analysis_id_I;
        self.component_group_name = component_group_name_I;
        self.component_name = component_name_I;
        self.u_matrix=u_matrix_I
        self.singular_value_index=singular_value_index_I
        self.svd_options=svd_options_I
        self.calculated_concentration_units = calculated_concentration_units_I;
        self.used_ = used__I;
        self.comment_ = comment__I;

    def __repr__dict__(self):
        return {'id':self.id,
            'analysis_id':self.analysis_id,
            'component_group_name':self.component_group_name,
            'component_name':self.component_name,
            'v_matrix':self.v_matrix,
            'singular_value_index':self.singular_value_index,
            'svd_method':self.svd_method,
            'svd_options':self.svd_options,
            'calculated_concentration_units':self.calculated_concentration_units,
            'used_':self.used_,
            'comment_':self.comment_}
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__())