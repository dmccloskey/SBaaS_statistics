from SBaaS_base.postgresql_orm_base import *

class data_stage02_quantification_dendrogram(Base):
    __tablename__ = 'data_stage02_quantification_dendrogram'
    id = Column(Integer, Sequence('data_stage02_quantification_dendrogram_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    leaves = Column(postgresql.ARRAY(Float))
    icoord = Column(postgresql.JSON)
    dcoord = Column(postgresql.JSON)
    ivl = Column(postgresql.ARRAY(String(100)))
    colors = Column(postgresql.ARRAY(String(25)))
    pdist_metric = Column(String(100))
    linkage_method = Column(String(100))
    value_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','ivl','pdist_metric','linkage_method','value_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.comment_=row_dict_I['comment_'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.leaves=row_dict_I['leaves'];
        self.icoord=row_dict_I['icoord'];
        self.dcoord=row_dict_I['dcoord'];
        self.ivl=row_dict_I['ivl'];
        self.colors=row_dict_I['colors'];
        self.pdist_metric=row_dict_I['pdist_metric'];
        self.linkage_method=row_dict_I['linkage_method'];
        self.value_units=row_dict_I['value_units'];
        self.used_=row_dict_I['used_'];


    def __set__row__(self,analysis_id_I,
                leaves_I,
                icoord_I,
                dcoord_I,
                ivl_I,
                colors_I,
                pdist_metric_I,
                linkage_method_I,
                value_units_I,
                used__I,
                comment__I):
        self.analysis_id=analysis_id_I
        self.leaves=leaves_I
        self.icoord=icoord_I
        self.dcoord=dcoord_I
        self.ivl=ivl_I
        self.colors=colors_I
        self.pdist_metric=pdist_metric_I
        self.linkage_method=linkage_method_I
        self.value_units = value_units_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'leaves':self.leaves,
            'icoord':self.icoord,
            'dcoord':self.dcoord,
            'ivl':self.ivl,
            'colors':self.colors,
            'pdist_metric':self.pdist_metric,
            'linkage_method':self.linkage_method,
            'value_units':self.value_units,
            'used_':self.used_,
            'comment_':self.comment_};
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());

class data_stage02_quantification_heatmap(Base):
    __tablename__ = 'data_stage02_quantification_heatmap'
    id = Column(Integer, Sequence('data_stage02_quantification_heatmap_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    col_index = Column(Integer)
    row_index = Column(Integer)
    value = Column(Float)
    col_leaves = Column(Integer)
    row_leaves = Column(Integer)
    col_label = Column(String(100))
    row_label = Column(String(100))
    col_pdist_metric = Column(String(100))
    row_pdist_metric = Column(String(100))
    col_linkage_method = Column(String(100))
    row_linkage_method = Column(String(100))
    value_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_short','time_point','component_name'),
                      UniqueConstraint('analysis_id','col_label','row_label','col_pdist_metric','row_pdist_metric','col_linkage_method','row_linkage_method','value_units'),
            )

    def __init__(self,
                row_dict_I,
                ):       
        self.col_linkage_method=row_dict_I['col_linkage_method'];
        self.row_pdist_metric=row_dict_I['row_pdist_metric'];
        self.col_index=row_dict_I['col_index'];
        self.row_index=row_dict_I['row_index'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.value_units=row_dict_I['value_units'];
        self.col_pdist_metric=row_dict_I['col_pdist_metric'];
        self.row_label=row_dict_I['row_label'];
        self.col_label=row_dict_I['col_label'];
        self.row_leaves=row_dict_I['row_leaves'];
        self.col_leaves=row_dict_I['col_leaves'];
        self.value=row_dict_I['value'];
        self.row_linkage_method=row_dict_I['row_linkage_method'];


    def __set__row__(self,analysis_id_I,
                col_index_I,
                row_index_I,
                value_I,
                col_leaves_I,
                row_leaves_I,
                col_label_I,
                row_label_I,
                col_pdist_metric_I,
                row_pdist_metric_I,
                col_linkage_method_I,
                row_linkage_method_I,
                value_units_I,
                used__I,
                comment__I):
        self.analysis_id=analysis_id_I
        self.col_index=col_index_I
        self.row_index=row_index_I
        self.value=value_I
        self.col_leaves=col_leaves_I
        self.row_leaves=row_leaves_I
        self.col_label=col_label_I
        self.row_label=row_label_I
        self.col_pdist_metric=col_pdist_metric_I
        self.row_pdist_metric=row_pdist_metric_I
        self.col_linkage_method=col_linkage_method_I
        self.row_linkage_method=row_linkage_method_I
        self.value_units = value_units_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'col_index':self.col_index,
            'row_index':self.row_index,
            'value':self.value,
            'col_leaves':self.col_leaves,
            'row_leaves':self.row_leaves,
            'col_label':self.col_label,
            'row_label':self.row_label,
            'col_pdist_metric':self.col_pdist_metric,
            'row_pdist_metric':self.row_pdist_metric,
            'col_linkage_method':self.col_linkage_method,
            'row_linkage_method':self.row_linkage_method,
            'value_units':self.value_units,
            'used_':self.used_,
            'comment_':self.comment_};
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());

class data_stage02_quantification_dendrogram_descriptiveStats(Base):
    __tablename__ = 'data_stage02_quantification_dendrogram_descriptiveStats'
    id = Column(Integer, Sequence('data_stage02_quantification_dendrogram_descriptiveStats_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    leaves = Column(postgresql.ARRAY(Float))
    icoord = Column(postgresql.JSON) #allowable byte size is exceeded for large data sets
                                     #test using posgresql.BYTEA
    dcoord = Column(postgresql.JSON)
    ivl = Column(postgresql.ARRAY(String(100)))
    colors = Column(postgresql.ARRAY(String(25)))
    pdist_metric = Column(String(100))
    linkage_method = Column(String(100))
    value_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (UniqueConstraint('analysis_id','ivl','pdist_metric','linkage_method','value_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.icoord=row_dict_I['icoord'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.value_units=row_dict_I['value_units'];
        self.linkage_method=row_dict_I['linkage_method'];
        self.pdist_metric=row_dict_I['pdist_metric'];
        self.colors=row_dict_I['colors'];
        self.ivl=row_dict_I['ivl'];
        self.dcoord=row_dict_I['dcoord'];
        self.leaves=row_dict_I['leaves'];
        self.analysis_id=row_dict_I['analysis_id'];

    def __set__row__(self,analysis_id_I,
                leaves_I,
                icoord_I,
                dcoord_I,
                ivl_I,
                colors_I,
                pdist_metric_I,
                linkage_method_I,
                value_units_I,
                used__I,
                comment__I):
        self.analysis_id=analysis_id_I
        self.leaves=leaves_I
        self.icoord=icoord_I
        self.dcoord=dcoord_I
        self.ivl=ivl_I
        self.colors=colors_I
        self.pdist_metric=pdist_metric_I
        self.linkage_method=linkage_method_I
        self.value_units = value_units_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self):
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'leaves':self.leaves,
            'icoord':self.icoord,
            'dcoord':self.dcoord,
            'ivl':self.ivl,
            'colors':self.colors,
            'pdist_metric':self.pdist_metric,
            'linkage_method':self.linkage_method,
            'value_units':self.value_units,
            'used_':self.used_,
            'comment_':self.comment_};
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());

class data_stage02_quantification_heatmap_descriptiveStats(Base):
    __tablename__ = 'data_stage02_quantification_heatmap_descriptiveStats'
    id = Column(Integer, Sequence('data_stage02_quantification_heatmap_descriptiveStats_id_seq'), primary_key=True)
    analysis_id = Column(String(500))
    col_index = Column(Integer)
    row_index = Column(Integer)
    value = Column(Float)
    col_leaves = Column(Integer)
    row_leaves = Column(Integer)
    col_label = Column(String(100))
    row_label = Column(String(100))
    col_pdist_metric = Column(String(100))
    row_pdist_metric = Column(String(100))
    col_linkage_method = Column(String(100))
    row_linkage_method = Column(String(100))
    value_units = Column(String(50))
    used_ = Column(Boolean);
    comment_ = Column(Text);

    __table_args__ = (#UniqueConstraint('experiment_id','sample_name_short','time_point','component_name'),
                      UniqueConstraint('analysis_id','col_label','row_label','col_pdist_metric','row_pdist_metric','col_linkage_method','row_linkage_method','value_units'),
            )

    def __init__(self,
                row_dict_I,
                ):
        self.row_linkage_method=row_dict_I['row_linkage_method'];
        self.row_pdist_metric=row_dict_I['row_pdist_metric'];
        self.col_pdist_metric=row_dict_I['col_pdist_metric'];
        self.row_label=row_dict_I['row_label'];
        self.col_label=row_dict_I['col_label'];
        self.row_leaves=row_dict_I['row_leaves'];
        self.col_leaves=row_dict_I['col_leaves'];
        self.value=row_dict_I['value'];
        self.row_index=row_dict_I['row_index'];
        self.col_index=row_dict_I['col_index'];
        self.analysis_id=row_dict_I['analysis_id'];
        self.comment_=row_dict_I['comment_'];
        self.used_=row_dict_I['used_'];
        self.value_units=row_dict_I['value_units'];
        self.col_linkage_method=row_dict_I['col_linkage_method'];

    def __set__row__(self,analysis_id_I,
                col_index_I,
                row_index_I,
                value_I,
                col_leaves_I,
                row_leaves_I,
                col_label_I,
                row_label_I,
                col_pdist_metric_I,
                row_pdist_metric_I,
                col_linkage_method_I,
                row_linkage_method_I,
                value_units_I,
                used__I,
                comment__I):
        self.analysis_id=analysis_id_I
        self.col_index=col_index_I
        self.row_index=row_index_I
        self.value=value_I
        self.col_leaves=col_leaves_I
        self.row_leaves=row_leaves_I
        self.col_label=col_label_I
        self.row_label=row_label_I
        self.col_pdist_metric=col_pdist_metric_I
        self.row_pdist_metric=row_pdist_metric_I
        self.col_linkage_method=col_linkage_method_I
        self.row_linkage_method=row_linkage_method_I
        self.value_units = value_units_I;
        self.used_=used__I
        self.comment_=comment__I

    def __repr__dict__(self): 
        return {'id':self.id,
                'analysis_id':self.analysis_id,
            'col_index':self.col_index,
            'row_index':self.row_index,
            'value':self.value,
            'col_leaves':self.col_leaves,
            'row_leaves':self.row_leaves,
            'col_label':self.col_label,
            'row_label':self.row_label,
            'col_pdist_metric':self.col_pdist_metric,
            'row_pdist_metric':self.row_pdist_metric,
            'col_linkage_method':self.col_linkage_method,
            'row_linkage_method':self.row_linkage_method,
            'value_units':self.value_units,
            'used_':self.used_,
            'comment_':self.comment_};
    
    def __repr__json__(self):
        return json.dumps(self.__repr__dict__());