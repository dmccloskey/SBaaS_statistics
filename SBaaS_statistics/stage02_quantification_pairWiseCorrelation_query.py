﻿#SBaaS
from .stage02_quantification_pairWiseCorrelation_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_pairWiseCorrelation_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {
            'data_stage02_quantification_pairWiseCorrelation':data_stage02_quantification_pairWiseCorrelation,
            'data_stage02_quantification_pairWiseCorrelation_replicates':data_stage02_quantification_pairWiseCorrelation_replicates,
            #'data_stage02_quantification_pairWiseCorrelationFeatures':data_stage02_quantification_pairWiseCorrelationFeatures,
            'data_stage02_quantification_pairWiseCorrFeaturesAndConditions':data_stage02_quantification_pairWiseCorrFeaturesAndConditions,
            'data_stage02_quantification_pairWiseCorrFeatures_replicates':data_stage02_quantification_pairWiseCorrFeatures_replicates,
            #'data_stage02_quantification_pairWiseCorrelationCrossUnits':data_stage02_quantification_pairWiseCorrelationCrossUnits,
            #'data_stage02_quantification_pairWiseCorrFeaturesCrossUnits':data_stage02_quantification_pairWiseCorrFeaturesCrossUnits,
            'statistics_pairWiseCorrFeat':statistics_pairWiseCorrFeat,
                        };
        self.set_supportedTables(tables_supported);

    def get_rows_analysisID_dataStage02QuantificationPairWiseCorrelation(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_pairWiseCorrelation
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_pairWiseCorrelation'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            #'value':self.convert_string2StringString(analysis_id_I),
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
            'column_name':'calculated_concentration_units_1',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'calculated_concentration_units_2',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_abbreviation_1',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_abbreviation_2',
            'order':'ASC',
            },
        ];
        #additional blocks
        for k,v in query_I.items():
            if not k in query.keys():
                query[k] = [];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def get_rows_dataStage02QuantificationPairWiseCorrelation(self,
                tables_I,
                query_I,
                output_O,
                dictColumn_I=None):
        """get rows by analysis ID from data_stage02_quantification_pairWiseCorrelation"""
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
    def get_rows_analysisID_dataStage02QuantificationPairWiseCorrelationFeatures(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_pairWiseCorrelationFeatures
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_pairWiseCorrelationFeatures'];
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
            'column_name':'calculated_concentration_units',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_name_1',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_name_2',
            'order':'ASC',
            },
        ];
        #additional blocks
        for k,v in query_I.items():
            if not k in query.keys():
                query[k] = [];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;

    def reset_dataStage02_quantification_pairWiseCorrelation(self,
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
                        #'value':self.convert_string2StringString(analysis_id_I),
		                'operator':'LIKE',
                        'connector':'AND'
                        }
	                ];
                table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
                query = querydelete.make_queryFromString(table_model,query);
                querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);

    def get_rows_analysisID_dataStage02QuantificationPairWiseCorrelationReplicates(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_pairWiseCorrelation_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_pairWiseCorrelation_replicates'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            #'value':self.convert_string2StringString(analysis_id_I),
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
            'column_name':'calculated_concentration_units',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_short_1',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_short_2',
            'order':'ASC',
            },
        ];
        #additional blocks
        for k,v in query_I.items():
            if not k in query.keys():
                query[k] = [];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;