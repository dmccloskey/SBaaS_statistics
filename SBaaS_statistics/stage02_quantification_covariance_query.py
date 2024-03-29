from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

from .stage02_quantification_covariance_postgresql_models import *

class stage02_quantification_covariance_query(sbaas_template_query,
                                       ):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_quantification_covariance
        '''
        tables_supported = {'data_stage02_quantification_covariance_samples':data_stage02_quantification_covariance_samples,
                        'data_stage02_quantification_covariance_features':data_stage02_quantification_covariance_features,
                        'data_stage02_quantification_covariance_samples_mahalanobis':data_stage02_quantification_covariance_samples_mahalanobis,
                        'data_stage02_quantification_covariance_features_mahalanobis':data_stage02_quantification_covariance_features_mahalanobis,
                        'data_stage02_quantification_covariance_samples_score':data_stage02_quantification_covariance_samples_score,
                        'data_stage02_quantification_covariance_features_score':data_stage02_quantification_covariance_features_score,
                        };
        self.set_supportedTables(tables_supported);

    #Query rows
    def get_rows_dataStage02QuantificationCovariance(self,
                tables_I,
                query_I,
                output_O,
                dictColumn_I=None):
        """get rows by analysis ID from data_stage02_quantification_covariance"""
        data_O = [];
        try:
            table_model = self.convert_tableStringList2SqlalchemyModelDict(tables_I);
            queryselect = sbaas_base_query_select(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            query = queryselect.make_queryFromString(table_model,query_I);
            data_O = queryselect.get_rows_sqlalchemyModel(
                query_I=query,
                output_O=output_O,
                dictColumn_I=dictColumn_I);
        except Exception as e:
            print(e);
        return data_O;
    def add_dataStage02QuantificationCovariance(self,table_I,data_I):
        '''add rows of data_stage02_quantification_covariance'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryinsert = sbaas_base_query_insert(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryinsert.add_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);
    def update_dataStage02QuantificationCovariance(self,table_I,data_I):
        '''update rows of data_stage02_quantification_covariance'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryupdate = sbaas_base_query_update(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryupdate.update_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);

    def initialize_dataStage02_quantification_covariance(self,
            tables_I = [],):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            queryinitialize = sbaas_base_query_initialize(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                model_I = self.convert_tableString2SqlalchemyModel(table);
                queryinitialize.initialize_table_sqlalchemyModel(model_I);
        except Exception as e:
            print(e);
    def drop_dataStage02_quantification_covariance(self,
            tables_I = [],):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            querydrop = sbaas_base_query_drop(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                model_I = self.convert_tableString2SqlalchemyModel(table);
                querydrop.drop_table_sqlalchemyModel(model_I);
        except Exception as e:
            print(e);
    def reset_dataStage02_quantification_covariance(self,
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
    def get_rows_analysisID_dataStage02QuantificationCovarianceSamplesMahalanobis(self,
                analysis_id_I,
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_covariance_samples_mahalanobis
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_covariance_samples_mahalanobis'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'used_',
            'value':'true',
            'operator':'IS',
            'connector':'AND'
                },
	    ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'sample_name_short',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_abbreviation',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'covariance_method',
            'order':'ASC',
            },
        ];
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def get_rows_analysisID_dataStage02QuantificationCovarianceFeaturesMahalanobis(self,
                analysis_id_I,
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_covariance_features_mahalanobis
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_covariance_features_mahalanobis'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'used_',
            'value':'true',
            'operator':'IS',
            'connector':'AND'
                },
	    ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'component_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_group_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'covariance_method',
            'order':'ASC',
            },
        ];
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;