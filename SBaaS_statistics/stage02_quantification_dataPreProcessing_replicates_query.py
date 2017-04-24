#SBaaS base classes
from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete
#SBaaS base templates
from SBaaS_base.sbaas_template_query import sbaas_template_query
#postgresql objects
from .stage02_quantification_dataPreProcessing_replicates_postgresql_models import *
from .stage02_quantification_analysis_postgresql_models import * #required for sample_name_abbreviation joins
#resources
import pandas as pd
from listDict.listDict import listDict

class stage02_quantification_dataPreProcessing_replicates_query(sbaas_template_query,
                                       ):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for data_stage02_quantification_dataPreProcessing_replicates
        '''
        tables_supported = {'data_stage02_quantification_dataPreProcessing_replicates':data_stage02_quantification_dataPreProcessing_replicates,
                            'data_stage02_quantification_dataPreProcessing_replicates_mv':data_stage02_quantification_dataPreProcessing_replicates_mv,
                            'data_stage02_quantification_dataPreProcessing_replicates_im':data_stage02_quantification_dataPreProcessing_replicates_im,
                        };
        self.set_supportedTables(tables_supported);

    #Query rows
    def get_rows_dataStage02QuantificationDataPreProcessingReplicates(self,
                tables_I,
                query_I,
                output_O,
                dictColumn_I=None):
        """get rows by analysis ID from data_stage02_quantification_dataPreProcessing_replicates"""
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
    def reset_stage02_quantification_dataPreProcessing_replicates(self,
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
    def get_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_replicates'];
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
            'column_name':'experiment_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_short',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'time_point',
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
    def get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_replicates'];
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
            'column_name':'calculated_concentration_units',
            'value':calculated_concentration_units_I,
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
            'column_name':'experiment_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_short',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'time_point',
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
    def getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                column_name_I = 'analysis_id',
                aggregate_function_I='count',
                aggregate_label_I='count_1',
                query_I={},
                output_O='scalar',
                dictColumn_I=None):
        '''Query row count by analysis_id from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string
        column_name_I = string
        aggregate_function_I = name of the aggregate function to call on the column
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_replicates'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [
            {"table_name":tables[0],
             "column_name":column_name_I,
             'aggregate_function':aggregate_function_I,
             'label':aggregate_label_I,
             }
            ];
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

        #additional query blocks
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

    #Delete rows
    def delete_rows_analysisIDAndCalculatedConcentrationUnitsAndCalculatedConcentrationValueAndOperator_dataStage02QuantificationDataPreProcessingReplicates(self,
            analysis_id_I,
            calculated_concentration_units_I,
            value_I,operator_I,
            warn_I=True):
        '''delete rows from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string,
        value_I = float,
        operator_I = string, e.g. "="
        OUTPUT:
        '''
        try:
            table = 'data_stage02_quantification_dataPreProcessing_replicates';
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            query = {};
            query['delete_from'] = [{'table_name':table}];
            query['where'] = [{
                    'table_name':table,
                    'column_name':'analysis_id',
                    'value':analysis_id_I,
		            'operator':'LIKE',
                    'connector':'AND'
                    },{
                    'table_name':table,
                    'column_name':'calculated_concentration',
                    'value':value_I,
		            'operator':operator_I,
                    'connector':'AND'
                    },
                    {"table_name":table,
                    'column_name':'calculated_concentration_units',
                    'value':calculated_concentration_units_I,
                    'operator':'LIKE',
                    'connector':'AND'
                    },
	            ];
            table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
            query = querydelete.make_queryFromString(table_model,query);
            querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);
    def delete_rows_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDataPreProcessingReplicates(self,
            analysis_id_I,
            calculated_concentration_units_I,
            component_name_I,
            warn_I=True):
        '''delete rows from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string,
        calculated_concentration_units_I = string,
        component_name_I = string,
        OUTPUT:
        '''
        try:
            table = 'data_stage02_quantification_dataPreProcessing_replicates';
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            query = {};
            query['delete_from'] = [{'table_name':table}];
            query['where'] = [{
                    'table_name':table,
                    'column_name':'analysis_id',
                    'value':analysis_id_I,
		            'operator':'LIKE',
                    'connector':'AND'
                    },
                    {"table_name":table,
                    'column_name':'calculated_concentration_units',
                    'value':calculated_concentration_units_I,
                    'operator':'LIKE',
                    'connector':'AND'
                    },{
                    'table_name':table,
                    'column_name':'component_name',
                    'operator':'LIKE',
		            'value':component_name_I,
                    'connector':'AND'
                    },
	            ];
            table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
            query = querydelete.make_queryFromString(table_model,query);
            querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);
    def delete_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDAndTimePointAndSampleNameShortAndComponentName_dataStage02QuantificationDataPreProcessingReplicates(self,
            analysis_id_I,
            calculated_concentration_units_I,
            experiment_id_I,
            time_point_I,
            sample_name_short_I,
            component_name_I,
            warn_I=True):
        '''delete rows from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string,
        calculated_concentration_units_I = string,
        experiment_id_I = string,
        time_point_I = string,
        sample_name_short_I = string,
        component_name_I = string,
        OUTPUT:
        '''
        try:
            table = 'data_stage02_quantification_dataPreProcessing_replicates';
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            query = {};
            query['delete_from'] = [{'table_name':table}];
            query['where'] = [{
                    'table_name':table,
                    'column_name':'analysis_id',
                    'value':analysis_id_I,
		            'operator':'LIKE',
                    'connector':'AND'
                    },
                    {"table_name":table,
                    'column_name':'calculated_concentration_units',
                    'value':calculated_concentration_units_I,
                    'operator':'LIKE',
                    'connector':'AND'
                    },{
                    'table_name':table,
                    'column_name':'experiment_id',
                    'operator':'LIKE',
		            'value':experiment_id_I,
                    'connector':'AND'
                    },{
                    'table_name':table,
                    'column_name':'time_point',
                    'operator':'LIKE',
		            'value':time_point_I,
                    'connector':'AND'
                    },{
                    'table_name':table,
                    'column_name':'sample_name_short',
                    'operator':'LIKE',
		            'value':sample_name_short_I,
                    'connector':'AND'
                    },{
                    'table_name':table,
                    'column_name':'component_name',
                    'operator':'LIKE',
		            'value':component_name_I,
                    'connector':'AND'
                    },
	            ];
            table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
            query = querydelete.make_queryFromString(table_model,query);
            querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);
    def delete_rows_experimentIDAndSampleNameShortAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
            data_I,
            warn_I=False):
        '''delete rows from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        data_I = listDict
        OUTPUT:
        '''
        querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        if data_I:
            for d in data_I:
                try:
                    table = 'data_stage02_quantification_dataPreProcessing_replicates';
                    query = {};
                    query['delete_from'] = [{'table_name':table}];
                    query['where'] = [
                            {
                            'table_name':table,
                            'column_name':'experiment_id',
                            'value':d['experiment_id'],
		                    'operator':'LIKE',
                            'connector':'AND'
                            },{
                            'table_name':table,
                            'column_name':'time_point',
                            'value':d['time_point'],
		                    'operator':'LIKE',
                            'connector':'AND'
                            },{
                            'table_name':table,
                            'column_name':'sample_name_short',
                            'value':d['sample_name_short'],
		                    'operator':'LIKE',
                            'connector':'AND'
                            },{
                            'table_name':table,
                            'column_name':'component_name',
                            'value':d['component_name'],
		                    'operator':'LIKE',
                            'connector':'AND'
                            },{
                            'table_name':table,
                            'column_name':'calculated_concentration_units',
                            'value':d['calculated_concentration_units'],
		                    'operator':'LIKE',
                            'connector':'AND'
                            },
	                    ];
                    table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
                    query = querydelete.make_queryFromString(table_model,query);
                    querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
                except Exception as e:
                    print(e);

    # get unique values based on a json type query
    def getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_replicates'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [
            {"table_name":tables[0],
             "column_name":'component_name',
             },
             {"table_name":tables[0],
             "column_name":'component_group_name',
             },
            ];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'calculated_concentration_units',
            'value':calculated_concentration_units_I,
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
        query['group_by'] = [
            {"table_name":tables[0],
            'column_name':'component_name',
            },
            {"table_name":tables[0],
            'column_name':'component_group_name',
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
        ];

        #additional blocks
        for k,v in query_I.items():
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def getGroup_analysisIDAndExperimentIDAndSampleNameShortAndTimePoint_analysisIDAndCalculatedConcentrationUnits_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_replicates'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [
            {"table_name":tables[0],
             "column_name":'analysis_id',
             },
             {"table_name":tables[0],
             "column_name":'experiment_id',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_short',
             },
             {"table_name":tables[0],
             "column_name":'time_point',
             },
            ];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'calculated_concentration_units',
            'value':calculated_concentration_units_I,
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
        query['group_by'] = [
            {"table_name":tables[0],
             "column_name":'analysis_id',
             },
             {"table_name":tables[0],
             "column_name":'experiment_id',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_short',
             },
             {"table_name":tables[0],
             "column_name":'time_point',
             },
        ];
        query['order_by'] = [
            {"table_name":tables[0],
             "column_name":'analysis_id',
            'order':'ASC',
             },
             {"table_name":tables[0],
             "column_name":'experiment_id',
            'order':'ASC',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_short',
            'order':'ASC',
             },
             {"table_name":tables[0],
             "column_name":'time_point',
            'order':'ASC',
             },
        ];

        #additional blocks
        for k,v in query_I.items():
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDAndSampleNameShortAndTimePoint_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_id_I,
                sample_name_short_I,
                time_point_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_replicates'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [
            {"table_name":tables[0],
             "column_name":'component_name',
             },
             {"table_name":tables[0],
             "column_name":'component_group_name',
             },
            ];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'calculated_concentration_units',
            'value':calculated_concentration_units_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'experiment_id',
            'value':experiment_id_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'sample_name_short',
            'value':sample_name_short_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'time_point',
            'value':time_point_I,
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
        query['group_by'] = [
            {"table_name":tables[0],
            'column_name':'component_name',
            },
            {"table_name":tables[0],
            'column_name':'component_group_name',
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
        ];

        #additional blocks
        for k,v in query_I.items():
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    
    def getGroup_analysisIDAndExperimentIDAndSampleNameShortAndTimePointAndComponentNameArray_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_replicates'];
        # get the listDict data
        data_O = [];
        query_cmd = 'SELECT analysis_id, experiment_id, sample_name_short, time_point, ';
        query_cmd += ('array(select component_name from "%s" group by component_name) ' %(tables[0]));
        query_cmd += ('FROM "%s" ' %(tables[0]));
        query_cmd += ("WHERE analysis_id LIKE '%s' " %(analysis_id_I));
        query_cmd += ("AND calculated_concentration_units LIKE '%s'" %(calculated_concentration_units_I));
        query_cmd += 'GROUP BY analysis_id, experiment_id, sample_name_short, time_point;';
        
        try:
            queryselect = sbaas_base_query_select(self.session,self.engine,self.settings);
            data_tmp = queryselect.execute_select(query_cmd);
            data_O = queryselect.convert_listKeyedTuple2ListDict(data_tmp);
        except Exception as e:
            print(e);

        return data_O;   

    #Joins with data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_replicates
    def get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndSampleNameShortsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_analysis.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                data_stage02_quantification_analysis.time_point,
                ).filter(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_analysis.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                data_stage02_quantification_analysis.time_point).order_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                data_stage02_quantification_analysis.sample_name_abbreviation.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
                data_stage02_quantification_analysis.time_point.asc()).all();
            data_O=[];
            #for d in data:
            #    add_row = True
            #    if calculated_concentration_units_I and not d.calculated_concentration_units in calculated_concentration_units_I:
            #        add_row = False;
            #    elif experiment_ids_I and not d.experiment_id in experiment_ids_I:
            #        add_row = False;
            #    elif sample_name_abbreviations_I and not d.sample_name_abbreviation in sample_name_abbreviations_I:
            #        add_row = False;
            #    elif time_points_I and not d.time_point in time_points_I:
            #        add_row = False;
            #    if add_row:
            #        data_O.append({
            #        'analysis_id':d.analysis_id,
            #        'calculated_concentration_units':d.calculated_concentration_units,
            #        'experiment_id':d.calculated_concentration_units,
            #        'sample_name_abbreviation':d.sample_name_abbreviation,
            #        'sample_name_short':d.sample_name_short,
            #        'time_point':d.time_point,
            #        })
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'time_point':time_points_I,
                                           'calculated_concentration_units':calculated_concentration_units_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_analysis.sample_name_abbreviation,
                data_stage02_quantification_analysis.time_point,
                ).filter(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_analysis.sample_name_abbreviation,
                data_stage02_quantification_analysis.time_point).order_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                data_stage02_quantification_analysis.sample_name_abbreviation.asc(),
                data_stage02_quantification_analysis.time_point.asc()).all();
            data_O=[];
            #for d in data:
            #    add_row = True
            #    if calculated_concentration_units_I and not d.calculated_concentration_units in calculated_concentration_units_I:
            #        add_row = False;
            #    elif experiment_ids_I and not d.experiment_id in experiment_ids_I:
            #        add_row = False;
            #    elif sample_name_abbreviations_I and not d.sample_name_abbreviation in sample_name_abbreviations_I:
            #        add_row = False;
            #    elif time_points_I and not d.time_point in time_points_I:
            #        add_row = False;
            #    if add_row:
            #        data_O.append({
            #        'analysis_id':d.analysis_id,
            #        'calculated_concentration_units':d.calculated_concentration_units,
            #        'experiment_id':d.experiment_id,
            #        'sample_name_abbreviation':d.sample_name_abbreviation,
            #        'time_point':d.time_point,
            #        })
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'time_point':time_points_I,
                                           'calculated_concentration_units':calculated_concentration_units_I,
                                           });
            return data_O;
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrationUnitsAndExperimentIDs_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                ).filter(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,).order_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc()).all();
            data_O=[];
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                           'calculated_concentration_units':calculated_concentration_units_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePointsAndComponentNames_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                component_names_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_analysis.sample_name_abbreviation,
                data_stage02_quantification_analysis.time_point,
                data_stage02_quantification_dataPreProcessing_replicates.component_name,
                data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                ).filter(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_analysis.sample_name_abbreviation,
                data_stage02_quantification_analysis.time_point,
                data_stage02_quantification_dataPreProcessing_replicates.component_name,
                data_stage02_quantification_dataPreProcessing_replicates.component_group_name,).order_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                data_stage02_quantification_analysis.sample_name_abbreviation.asc(),
                data_stage02_quantification_analysis.time_point.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.component_name.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.component_group_name.asc(),).all();
            data_O=[];
            #for d in data:
            #    add_row = True
            #    if calculated_concentration_units_I and not d.calculated_concentration_units in calculated_concentration_units_I:
            #        add_row = False;
            #    elif experiment_ids_I and not d.experiment_id in experiment_ids_I:
            #        add_row = False;
            #    elif sample_name_abbreviations_I and not d.sample_name_abbreviation in sample_name_abbreviations_I:
            #        add_row = False;
            #    elif time_points_I and not d.time_point in time_points_I:
            #        add_row = False;
            #    if add_row:
            #        data_O.append({
            #        'analysis_id':d.analysis_id,
            #        'calculated_concentration_units':d.calculated_concentration_units,
            #        'experiment_id':d.calculated_concentration_units,
            #        'sample_name_abbreviation':d.sample_name_abbreviation,
            #        'sample_name_short':d.sample_name_short,
            #        'time_point':d.time_point,
            #        })
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'time_point':time_points_I,
                                           'calculated_concentration_units':calculated_concentration_units_I,
                                           'component_name':component_names_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsAndSampleNameAbbreviations_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],):
        """get analysis_id, experiment_id, sample_name_abbreviation, sample_name_short, time_point, component_name, component_group_name,
        calculated_concentration, and calculated_concentration units from data_stage02_quantification_dataPreProcessing_replicates
        and from data_stage02_quantification_analysis
        INPUT:
        analysis_id
        OPTIONAL INPUT:
        calculated_concentration_units_I
        experiment_ids_I
        sample_name_abbreviations_I
        time_points_I
        """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).all();
            data_O = [];
            #for d in data:
            #    add_row = True
            #    if experiment_ids_I and not d.experiment_id in experiment_ids_I:
            #        add_row = False;
            #    elif sample_name_abbreviations_I and not d.sample_name_abbreviation in sample_name_abbreviations_I:
            #        add_row = False;
            #    elif sample_name_shorts_I and not d.sample_name_short in sample_name_shorts_I:
            #        add_row = False;
            #    elif component_names_I and not d.component_name in component_names_I:
            #        add_row = False;
            #    elif component_group_names_I and not d.component_group_name in component_group_names_I:
            #        add_row = False;
            #    elif time_points_I and not d.time_point in time_points_I:
            #        add_row = False;
            #    if add_row:
            #        data_O.append({
            #        'analysis_id':d.analysis_id,
            #        'calculated_concentration_units':d.calculated_concentration_units,
            #        'experiment_id':d.calculated_concentration_units,
            #        'sample_name_abbreviation':d.sample_name_abbreviation,
            #        'sample_name_short':d.sample_name_short,
            #        'time_point':d.time_point,
            #        'component_group_name':d.component_group_name,
            #        'component_name':d.component_name,
            #        'calculated_concentration':d.calculated_concentration,
            #        })
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'calculated_concentration_units':calculated_concentration_units_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'sample_name_short':sample_name_shorts_I,
                                           'component_name':component_names_I,
                                           'component_group_name':component_group_names_I,
                                           'time_point':time_points_I,
                                           });
                data_O.convert_dataFrame2ListDict();
            return data_O.get_listDict();
        except SQLAlchemyError as e:
            print(e);
    def get_rowsAndSampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                sample_name_abbreviation_I,
                experiment_ids_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],):
        """get analysis_id, experiment_id, sample_name_abbreviation, sample_name_short, time_point, component_name, component_group_name,
        calculated_concentration, and calculated_concentration units from data_stage02_quantification_dataPreProcessing_replicates
        and from data_stage02_quantification_analysis by analysis_id, calculated_concentration_units, and sample_name_abbreviation
        INPUT:
        analysis_id_I
        calculated_concentration_units_I
        sample_name_abbreviation_I
        OPTIONAL INPUT:
        experiment_ids_I
        sample_name_abbreviations_I
        time_points_I
        """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).all();
            data_O = [];
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                           'sample_name_short':sample_name_shorts_I,
                                           'component_name':component_names_I,
                                           'component_group_name':component_group_names_I,
                                           'time_point':time_points_I,
                                           });
                data_O.convert_dataFrame2ListDict();
            return data_O.get_listDict();
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,calculated_concentration_units_I,
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],):
        """get analysis_id, experiment_id, sample_name_abbreviation, sample_name_short, time_point, component_name, component_group_name,
        calculated_concentration, and calculated_concentration units from data_stage02_quantification_dataPreProcessing_replicates
        and from data_stage02_quantification_analysis
        INPUT:
        analysis_id
        calculated_concentration_units
        OPTIONAL INPUT:
        experiment_ids_I
        sample_name_abbreviations_I
        time_points_I
        """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).all();
            data_O = [];
            #for d in data:
            #    add_row = True
            #    if experiment_ids_I and not d.experiment_id in experiment_ids_I:
            #        add_row = False;
            #    elif sample_name_abbreviations_I and not d.sample_name_abbreviation in sample_name_abbreviations_I:
            #        add_row = False;
            #    elif sample_name_shorts_I and not d.sample_name_short in sample_name_shorts_I:
            #        add_row = False;
            #    elif component_names_I and not d.component_name in component_names_I:
            #        add_row = False;
            #    elif component_group_names_I and not d.component_group_name in component_group_names_I:
            #        add_row = False;
            #    elif time_points_I and not d.time_point in time_points_I:
            #        add_row = False;
            #    if add_row:
            #        data_O.append({
            #        'analysis_id':d.analysis_id,
            #        'calculated_concentration_units':d.calculated_concentration_units,
            #        'experiment_id':d.calculated_concentration_units,
            #        'sample_name_abbreviation':d.sample_name_abbreviation,
            #        'sample_name_short':d.sample_name_short,
            #        'time_point':d.time_point,
            #        'component_group_name':d.component_group_name,
            #        'component_name':d.component_name,
            #        'calculated_concentration':d.calculated_concentration,
            #        })
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'sample_name_short':sample_name_shorts_I,
                                           'component_name':component_names_I,
                                           'component_group_name':component_group_names_I,
                                           'time_point':time_points_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataFrame_analysisIDAndCalculatedConcentrationUnitsAndComponentNames_dataStage02DataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                component_name_I,
                experiment_ids_I = [],
                time_points_I = [],
                sample_name_abbreviations_I = [],
                sample_name_shorts_I = []
                ):
        """get data from analysis ID and experiment ID and time point and concentration_units and component name and sample name abbreviation"""
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.like(component_name_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).order_by(

                    #    .group_by(
                    #data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    #data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    #data_stage02_quantification_analysis.sample_name_abbreviation,
                    #data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    #data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    #data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    #data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    #data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    #data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,)
                        
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.asc(),).all();
            data_O = [];
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'sample_name_short':sample_name_shorts_I,
                                           'time_point':time_points_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataList_analysisIDAndExperimentIDAndTimePointAndCalculatedConcentrationUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02DataPreProcessingReplicates(self,
                analysis_id_I,
                experiment_id_I,
                time_point_I,
                concentration_units_I,
                component_name_I,
                sample_name_abbreviation_I):
        """get data from analysis ID and experiment ID and time point and concentration_units and component name and sample name abbreviation"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                    data_stage02_quantification_dataPreProcessing_replicates.used_,
                    data_stage02_quantification_dataPreProcessing_replicates.comment_).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_analysis.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.like(time_point_I),
                    data_stage02_quantification_analysis.time_point.like(time_point_I),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.like(component_name_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point,
                    data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                    data_stage02_quantification_dataPreProcessing_replicates.component_name,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                    data_stage02_quantification_dataPreProcessing_replicates.used_,
                    data_stage02_quantification_dataPreProcessing_replicates.comment_).all();
            data_O = [];
            concentrations_O = [];
            #for d in data: 
            #    concentrations_O.append(d.calculated_concentration);
            #    data_1 = {};
            #    data_1['analysis_id'] = d.analysis_id;
            #    data_1['experiment_id'] = d.experiment_id;
            #    data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
            #    data_1['sample_name_short'] = d.sample_name_short;
            #    data_1['time_point'] = d.time_point;
            #    data_1['component_group_name'] = d.component_group_name;
            #    data_1['component_name'] = d.component_name;
            #    data_1['calculated_concentration'] = d.calculated_concentration;
            #    data_1['calculated_concentration_units'] = d.calculated_concentration_units;
            #    data_1['used_'] = d.used_;
            #    data_1['comment_'] = d.comment_;
            #    data_O.append(data_1);
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                concentrations_O = data_O.dataFrame['calculated_concentration'].get_values();
            return data_O,concentrations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNameAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
        self, analysis_id_I,calculated_concentration_units_I,component_name_I,sample_name_abbreviation_I):
        """get all calculated_calculated concentrations by analysis_id, calculated_concentration_units, component_name, sample_name_abbreviation"""
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.like(component_name_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_analysis.sample_name_short.like(data_stage02_quantification_dataPreProcessing_replicates.sample_name_short),
                    data_stage02_quantification_analysis.time_point.like(data_stage02_quantification_dataPreProcessing_replicates.time_point),
                    data_stage02_quantification_analysis.experiment_id.like(data_stage02_quantification_dataPreProcessing_replicates.experiment_id),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration.asc()).all();
            data_O = [d.calculated_concentration for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_id_I,
                sample_name_abbreviation_I,
                time_point_I,
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates
                ).filter(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(experiment_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.time_point.like(time_point_I),
                data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).order_by(
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.component_name.asc(),
                ).all();
            data_O=[d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDs_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_id_I,
                sample_name_abbreviations_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            #data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates
            #    ).filter(
            #    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
            #    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
            #    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(experiment_id_I),
            #    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).order_by(
            #    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
            #    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
            #    data_stage02_quantification_dataPreProcessing_replicates.component_name.asc(),
            #    ).all();
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration,
                data_stage02_quantification_dataPreProcessing_replicates.imputation_method,
                data_stage02_quantification_dataPreProcessing_replicates.component_group_name,
                data_stage02_quantification_dataPreProcessing_replicates.component_name,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_analysis.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                data_stage02_quantification_dataPreProcessing_replicates.time_point,
                ).filter(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(experiment_id_I),
                data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).all();
            #data_O=[d.__repr__dict__() for d in data];
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'time_point':time_points_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self, analysis_id_I,calculated_concentration_units_I):
        """get sample_name_abbreviation and sample_name_short by analysis_id, calculated_concentration_units from data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(data_stage02_quantification_analysis.sample_name_abbreviation,
                                      data_stage02_quantification_analysis.sample_name_short).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_analysis.sample_name_short).order_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc(),
                    data_stage02_quantification_analysis.sample_name_short.asc()).all();
            sample_name_abbreviation_O = [];
            sample_name_short_O = [];
            for d in data: 
                sample_name_abbreviation_O.append(d.sample_name_abbreviation);
                sample_name_short_O.append(d.sample_name_short);
            return sample_name_abbreviation_O,sample_name_short_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
        self, analysis_id_I,calculated_concentration_units_I):
        """get sample_name_abbreviation and sample_name_short by analysis_id, calculated_concentration_units, component_name from data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(data_stage02_quantification_analysis.sample_name_abbreviation,).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation,).order_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc(),).all();
            sample_name_abbreviation_O = [d.sample_name_abbreviation for d in data];
            return sample_name_abbreviation_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDataPreProcessingReplicates(
        self, analysis_id_I,calculated_concentration_units_I,component_name_I):
        """get sample_name_abbreviation and sample_name_short by analysis_id, calculated_concentration_units, component_name from data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(data_stage02_quantification_analysis.sample_name_abbreviation,).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.like(component_name_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation,).order_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc(),).all();
            sample_name_abbreviation_O = [d.sample_name_abbreviation for d in data];
            return sample_name_abbreviation_O;
        except SQLAlchemyError as e:
            print(e);
    
    def get_analysisIDAndExperimentIDsAndSampleNameShortsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_ids_I=[],
                sample_name_shorts_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_replicates"""
        try:
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                data_stage02_quantification_dataPreProcessing_replicates.time_point,
                ).filter(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id,
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                data_stage02_quantification_dataPreProcessing_replicates.time_point).order_by(
                data_stage02_quantification_dataPreProcessing_replicates.analysis_id.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
                data_stage02_quantification_dataPreProcessing_replicates.time_point.asc()).all();
            data_O=[];
            for d in data:
                add_row = True
                if experiment_ids_I and not d.experiment_id in experiment_ids_I:
                    add_row = False;
                elif sample_name_shorts_I and not d.sample_name_short in sample_name_shorts_I:
                    add_row = False;
                elif time_points_I and not d.time_point in time_points_I:
                    add_row = False;
                if add_row:
                    data_O.append({
                    'analysis_id':d.analysis_id,
                    'calculated_concentration_units':d.calculated_concentration_units,
                    'experiment_id':d.experiment_id,
                    'sample_name_short':d.sample_name_short,
                    'time_point':d.time_point,
                    })
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    #Querys to be called by other classes
    def get_allCalculatedConcentrations_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingReplicates(self, analysis_id_I,concentration_units_I):
        """get all calculated_calculated concentrations by analysis_id and calculated_concentration_units"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration.isnot(None)).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration.asc()).all();
            data_O = [];
            for d in data: 
                data_O.append(d.calculated_concentration);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationDataPreProcessingReplicates(
        self, analysis_id_I,calculated_concentration_units_I,sample_name_short_I):
        """get all calculated_calculated concentrations by analysis_id, calculated_concentration_units, sample_name_short"""
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(sample_name_short_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.asc()).all();
            data_O = [d.calculated_concentration for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self, analysis_id_I):
        """query calculated_concentration_units by analysis id from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d.calculated_concentration_units);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrationUnits_analysisIDAndImputationMethod_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                imputation_method_I):
        """query calculated_concentration_units from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        OUTPUT:
        """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.imputation_method.like(imputation_method_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d.calculated_concentration_units);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_imputationMethods_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                ):
        """query imputation_methods from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        OUTPUT:
        """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.imputation_method,
                    #data_stage02_quantification_dataPreProcessing_replicates.imputation_options
                    ).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.imputation_method,
                    #data_stage02_quantification_dataPreProcessing_replicates.imputation_options
                    ).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.imputation_method.asc()).all();
            imputation_method_O = [];
            #imputation_options_O = [];
            for d in data: 
                imputation_method_O.append(d.imputation_method);
                #imputation_options_O.append(d.imputation_options);
            return imputation_method_O;
            #return imputation_method_O,imputation_options_O;
        except SQLAlchemyError as e:
            print(e);   
    def getCount_componentNames_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self, analysis_id_I):
        """query row count of unique component_names by analysis id from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.component_name).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.component_name).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);
    def getCount_componentNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I):
        """query row count of unique component_names from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.component_name).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.component_name).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);
    def getCount_componentNames_analysisIDAndImputationMethodAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                imputation_method_I,
                calculated_concentration_units_I):
        """query row count of unique component_names from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.component_name).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.imputation_method.like(imputation_method_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.component_name).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);   
    def getCount_experimentIDAndSampleNameShortAndTimePoint_analysisID_dataStage02QuantificationDataPreProcessingReplicates(self, analysis_id_I):
        """query row count of unique experiment_id/sample_name_short/time_point by analysis id from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);
    def getCount_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I):
        """query row count of unique experiment_id/sample_name_short/time_point from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);   
    def getCount_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndImputationMethodAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,analysis_id_I,
                imputation_method_I,
                calculated_concentration_units_I):
        """query row count of unique experiment_id/sample_name_short/time_point from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.imputation_method.like(imputation_method_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);  
    def getCount_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,analysis_id_I,
                component_name_I,
                calculated_concentration_units_I):
        """query row count of unique experiment_id/sample_name_short/time_point from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.like(component_name_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id,
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short,
                    data_stage02_quantification_dataPreProcessing_replicates.time_point).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.experiment_id.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.asc(),
                    data_stage02_quantification_dataPreProcessing_replicates.time_point.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationDataPreProcessingReplicates(self, analysis_id_I,calculated_concentration_units_I,sample_name_short_I):
        """get rows by analysis_id, calculated_concentration_units, and sample_name_short from data_stage02_quantification_dataPreProcessing_replicates"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_replicates).filter(
                    data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(sample_name_short_I),
                    data_stage02_quantification_dataPreProcessing_replicates.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_replicates.component_name.asc()).all();
            data_O = [];
            for d in data: 
                data_O.append(d.__repr__dict__());
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    #update methods
    def setUsed2False_experimentIDAndSampleNameShortAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,data_I):
        '''update rows of data_stage02_quantification_dataPreProcessing_replicates'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_dataPreProcessing_replicates).filter(
                            data_stage02_quantification_dataPreProcessing_replicates.experiment_id.like(d['experiment_id']),
                            data_stage02_quantification_dataPreProcessing_replicates.sample_name_short.like(d['sample_name_short']),
                            data_stage02_quantification_dataPreProcessing_replicates.time_point.like(d['time_point']),
                            data_stage02_quantification_dataPreProcessing_replicates.component_name.like(d['component_name']),
                            data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(d['calculated_concentration_units']),).update(
                            {
                            'used_':False,},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def setUsed2False_analysisIDAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self,data_I):
        '''update rows of data_stage02_quantification_dataPreProcessing_replicates'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_dataPreProcessing_replicates).filter(
                            data_stage02_quantification_dataPreProcessing_replicates.analysis_id.like(d['analysis_id']),
                            data_stage02_quantification_dataPreProcessing_replicates.component_name.like(d['component_name']),
                            data_stage02_quantification_dataPreProcessing_replicates.calculated_concentration_units.like(d['calculated_concentration_units']),).update(
                            {
                            'used_':False,},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
            
    ##refactored
    def get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates(
        self,analysis_id_I,
        calculated_concentration_units_I=[],
        component_names_I=[],
        component_group_names_I=[],
        sample_name_shorts_I=[],
        sample_name_abbreviations_I=[],
        time_points_I=[],
        experiment_ids_I=[],
        imputation_methods_I=[],
        pvalue_corrected_descriptions_I=[],
        where_clause_I=None,
        ):
        '''Query rows from data_stage02_quantification_dataPreProcessing_replicates
        INPUT:
        analysis_id_I = list or comma seperated string
        ... = list or comma seperate string
        where_clause_I = formatted clause to add at the end
        OUTPUT:
        rows_O = listDict
        '''
        try:
            cmd = '''SELECT "data_stage02_quantification_dataPreProcessing_replicates"."id", 
                "data_stage02_quantification_dataPreProcessing_replicates"."analysis_id", 
                "data_stage02_quantification_dataPreProcessing_replicates"."experiment_id", 
                "data_stage02_quantification_analysis"."sample_name_abbreviation", 
                "data_stage02_quantification_dataPreProcessing_replicates"."sample_name_short", 
                "data_stage02_quantification_dataPreProcessing_replicates"."time_point", 
                "data_stage02_quantification_dataPreProcessing_replicates"."component_group_name", 
                "data_stage02_quantification_dataPreProcessing_replicates"."component_name", 
                "data_stage02_quantification_dataPreProcessing_replicates"."imputation_method", 
                "data_stage02_quantification_dataPreProcessing_replicates"."calculated_concentration", 
                "data_stage02_quantification_dataPreProcessing_replicates"."calculated_concentration_units", 
                "data_stage02_quantification_dataPreProcessing_replicates"."used_", 
                "data_stage02_quantification_dataPreProcessing_replicates"."comment_" ''';
            cmd+= '''FROM "data_stage02_quantification_dataPreProcessing_replicates", 
                "data_stage02_quantification_analysis" ''';
            #cmd+= '''WHERE "data_stage02_quantification_dataPreProcessing_replicates".analysis_id LIKE '%s' '''%(analysis_id_I);
            analysis_ids = self.convert_list2string(analysis_id_I);
            cmd+= '''WHERE "data_stage02_quantification_dataPreProcessing_replicates".analysis_id =ANY 
                ('{%s}'::character varying[]) '''%(analysis_ids);
            cmd+= '''AND "data_stage02_quantification_dataPreProcessing_replicates".used_ ''';
            cmd+= '''AND "data_stage02_quantification_dataPreProcessing_replicates".analysis_id LIKE "data_stage02_quantification_analysis".analysis_id  
                AND "data_stage02_quantification_dataPreProcessing_replicates".experiment_id LIKE "data_stage02_quantification_analysis".experiment_id  
                AND "data_stage02_quantification_dataPreProcessing_replicates".time_point LIKE "data_stage02_quantification_analysis".time_point  
                AND "data_stage02_quantification_dataPreProcessing_replicates".sample_name_short LIKE "data_stage02_quantification_analysis".sample_name_short  '''
            if calculated_concentration_units_I:
                cmd_q = '''AND "data_stage02_quantification_dataPreProcessing_replicates".calculated_concentration_units =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(calculated_concentration_units_I));
                cmd+=cmd_q;
            if sample_name_shorts_I:
                cmd_q = '''AND "data_stage02_quantification_dataPreProcessing_replicates".sample_name_short =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(sample_name_shorts_I));
                cmd+=cmd_q;
            if sample_name_abbreviations_I:
                cmd_q = '''AND "data_stage02_quantification_analysis".sample_name_abbreviation =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(sample_name_abbreviations_I));
                cmd+=cmd_q;
            if component_names_I:
                cmd_q = '''AND "data_stage02_quantification_dataPreProcessing_replicates".component_name =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(component_names_I));
                cmd+=cmd_q;
            if component_group_names_I:
                cmd_q = '''AND "data_stage02_quantification_dataPreProcessing_replicates".component_group_name =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(component_group_names_I));
                cmd+=cmd_q;
            if time_points_I:
                cmd_q = '''AND "data_stage02_quantification_dataPreProcessing_replicates".time_point =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(time_points_I));
                cmd+=cmd_q;
            if experiment_ids_I:
                cmd_q = '''AND "data_stage02_quantification_dataPreProcessing_replicates".experiment_id =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(experiment_ids_I));
                cmd+=cmd_q;
            if imputation_methods_I:
                cmd_q = '''AND "data_stage02_quantification_dataPreProcessing_replicates".imputation_method =ANY ('{%s}'::text[]) ''' %(self.convert_list2string(imputation_methods_I));
                cmd+=cmd_q;
            if where_clause_I:
                cmd += '''AND %s ''' %(where_clause_I);
            cmd+= '''ORDER BY "data_stage02_quantification_dataPreProcessing_replicates"."analysis_id" ASC, 
                "data_stage02_quantification_dataPreProcessing_replicates"."calculated_concentration_units" ASC, 
                "data_stage02_quantification_dataPreProcessing_replicates"."experiment_id" ASC, 
                "data_stage02_quantification_dataPreProcessing_replicates"."time_point" ASC, 
                "data_stage02_quantification_analysis"."sample_name_abbreviation" ASC, 
                "data_stage02_quantification_dataPreProcessing_replicates"."sample_name_short" ASC, 
                "data_stage02_quantification_dataPreProcessing_replicates"."component_group_name" ASC, 
                "data_stage02_quantification_dataPreProcessing_replicates"."component_name" ASC,
                "data_stage02_quantification_dataPreProcessing_replicates"."imputation_method" ASC ''';
            result = self.session.execute(cmd);
            data = result.fetchall();
            data_O = [dict(d) for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);