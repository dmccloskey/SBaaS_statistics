#lims
from SBaaS_LIMS.lims_experiment_postgresql_models import *
from SBaaS_LIMS.lims_sample_postgresql_models import *

from .stage02_quantification_heatmap_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_heatmap_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_heatmap':data_stage02_quantification_heatmap,
            'data_stage02_quantification_heatmap_descriptiveStats':data_stage02_quantification_heatmap_descriptiveStats,
            'data_stage02_quantification_dendrogram':data_stage02_quantification_dendrogram,
            'data_stage02_quantification_dendrogram_descriptiveStats':data_stage02_quantification_dendrogram_descriptiveStats,
                        };
        self.set_supportedTables(tables_supported);
    # query data from data_stage02_quantification_heatmap
    def get_rows_analysisID_dataStage02QuantificationHeatmap(self,analysis_id_I):
        '''Query rows from data_stage02_quantification_heatmap'''
        try:
            data = self.session.query(data_stage02_quantification_heatmap).filter(
                    data_stage02_quantification_heatmap.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_heatmap.used_).all();
            data_O = [];
            for d in data: 
                data_dict = {'analysis_id':d.analysis_id,
                    'col_index':d.col_index,
                    'row_index':d.row_index,
                    'value':d.value,
                    'col_leaves':d.col_leaves,
                    'row_leaves':d.row_leaves,
                    'col_label':d.col_label,
                    'row_label':d.row_label,
                    'col_pdist_metric':d.col_pdist_metric,
                    'row_pdist_metric':d.row_pdist_metric,
                    'col_linkage_method':d.col_linkage_method,
                    'row_linkage_method':d.row_linkage_method,
                    'value_units':d.value_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_heatmap(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_heatmap).filter(data_stage02_quantification_heatmap.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_heatmap).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_dendrogram(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_dendrogram).filter(data_stage02_quantification_dendrogram.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_dendrogram).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);

    def initialize_dataStage02_quantification_heatmap(self):
        try:
            data_stage02_quantification_heatmap.__table__.create(self.engine,True);
            data_stage02_quantification_dendrogram.__table__.create(self.engine,True);
            data_stage02_quantification_heatmap_descriptiveStats.__table__.create(self.engine,True);
            data_stage02_quantification_dendrogram_descriptiveStats.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification_heatmap(self):
        try:
            data_stage02_quantification_heatmap.__table__.drop(self.engine,True);
            data_stage02_quantification_dendrogram.__table__.drop(self.engine,True);
            data_stage02_quantification_heatmap_descriptiveStats.__table__.drop(self.engine,True);
            data_stage02_quantification_dendrogram_descriptiveStats.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);

    # query data from data_stage02_quantification_heatmap
    def get_rows_analysisID_dataStage02QuantificationHeatmapDescriptiveStats(self,analysis_id_I):
        '''Query rows from data_stage02_quantification_heatmap_descriptiveStats'''
        try:
            data = self.session.query(data_stage02_quantification_heatmap_descriptiveStats).filter(
                    data_stage02_quantification_heatmap_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_heatmap_descriptiveStats.used_).all();
            data_O = [];
            for d in data: 
                data_dict = {'analysis_id':d.analysis_id,
                    'col_index':d.col_index,
                    'row_index':d.row_index,
                    'value':d.value,
                    'col_leaves':d.col_leaves,
                    'row_leaves':d.row_leaves,
                    'col_label':d.col_label,
                    'row_label':d.row_label,
                    'col_pdist_metric':d.col_pdist_metric,
                    'row_pdist_metric':d.row_pdist_metric,
                    'col_linkage_method':d.col_linkage_method,
                    'row_linkage_method':d.row_linkage_method,
                    'value_units':d.value_units,
                    'used_':d.used_,
                    'comment_':d.comment_};
                data_O.append(data_dict);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_heatmap_descriptiveStats(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_heatmap_descriptiveStats).filter(data_stage02_quantification_heatmap_descriptiveStats.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_heatmap_descriptiveStats).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_dendrogram_descriptiveStats(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_dendrogram_descriptiveStats).filter(data_stage02_quantification_dendrogram_descriptiveStats.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_dendrogram_descriptiveStats).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    