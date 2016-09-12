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
        tables_supported = {
            'data_stage02_quantification_heatmap':data_stage02_quantification_heatmap,
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
    def get_rows_analysisID_dataStage02QuantificationDendrogram(self,analysis_id_I):
        '''Query rows from data_stage02_quantification_dendrogram'''
        try:
            data = self.session.query(data_stage02_quantification_dendrogram).filter(
                    data_stage02_quantification_dendrogram.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dendrogram.used_).all();
            data_O = [d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_heatmap(self,
            tables_I = [],
            analysis_id_I = None,
            warn_I=True):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                query = {};
                query['delete_from'] = [{'table_name':table}];
                query['where'] = [{
                        'table_name':table,
                        'column_name':'analysis_id',
                        'value':analysis_id_I,
		                'operator':'LIKE',
                        'connector':'AND'
                        }
	                ];
                table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
                query = querydelete.make_queryFromString(table_model,query);
                querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
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
    def get_rows_analysisID_dataStage02QuantificationDendrogramDescriptiveStats(self,analysis_id_I):
        '''Query rows from data_stage02_quantification_dendrogram_descriptiveStats'''
        try:
            data = self.session.query(data_stage02_quantification_dendrogram_descriptiveStats).filter(
                    data_stage02_quantification_dendrogram_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dendrogram_descriptiveStats.used_).all();
            data_O = [d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    