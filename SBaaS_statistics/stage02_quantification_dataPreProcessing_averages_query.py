from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete
#SBaaS template
from SBaaS_base.sbaas_template_query import sbaas_template_query
#SBaaS tables
from .stage02_quantification_dataPreProcessing_averages_postgresql_models import *
#resources
from listDict.listDict import listDict
from math import sqrt

class stage02_quantification_dataPreProcessing_averages_query(sbaas_template_query,
                                       ):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for data_stage02_quantification_dataPreProcessing_averages
        '''
        tables_supported = {'data_stage02_quantification_dataPreProcessing_averages':data_stage02_quantification_dataPreProcessing_averages,
                            'data_stage02_quantification_dataPreProcessing_averages_mv':data_stage02_quantification_dataPreProcessing_averages_mv,
                            'data_stage02_quantification_dataPreProcessing_averages_im':data_stage02_quantification_dataPreProcessing_averages_im,
                        };
        self.set_supportedTables(tables_supported);

    #Query rows
    def get_rows_dataStage02QuantificationDataPreProcessingAverages(self,
                tables_I,
                query_I,
                output_O,
                dictColumn_I=None):
        """get rows by analysis ID from data_stage02_quantification_dataPreProcessing_averages"""
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
    def add_dataStage02QuantificationDataPreProcessingAverages(self,table_I,data_I):
        '''add rows of data_stage02_quantification_dataPreProcessing_averages'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryinsert = sbaas_base_query_insert(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryinsert.add_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);
    def update_dataStage02QuantificationDataPreProcessingAverages(self,table_I,data_I):
        '''update rows of data_stage02_quantification_dataPreProcessing_averages'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryupdate = sbaas_base_query_update(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryupdate.update_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);
    def initialize_stage02_quantification_dataPreProcessing_averages(self,
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
    def drop_stage02_quantification_dataPreProcessing_averages(self,
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
    def reset_stage02_quantification_dataPreProcessing_averages(self,
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
    def get_rows_analysisID_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_averages'];
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
            'column_name':'sample_name_abbreviation',
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
    def get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_averages'];
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
            'column_name':'sample_name_abbreviation',
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
    def getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                column_name_I = 'analysis_id',
                aggregate_function_I='count',
                aggregate_label_I='count_1',
                query_I={},
                output_O='scalar',
                dictColumn_I=None):
        '''Query row count by analysis_id from data_stage02_quantification_dataPreProcessing_averages
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

        tables = ['data_stage02_quantification_dataPreProcessing_averages'];
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
    def delete_rows_analysisIDAndCalculatedConcentrationUnitsAndFeatureValueAndOperator_dataStage02QuantificationDataPreProcessingAverages(self,
            analysis_id_I,
            calculated_concentration_units_I,
            feature_I,
            value_I,operator_I,
            warn_I=True):
        '''delete rows from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string,
        feature_I = string, column name
        value_I = float,
        operator_I = string, e.g. "="
        OUTPUT:
        '''
        try:
            table = 'data_stage02_quantification_dataPreProcessing_averages';
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
                    'column_name':feature_I,
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
    def delete_rows_analysisIDAndCalculatedConcentrationUnitsAndComponentNames_dataStage02QuantificationDataPreProcessingAverages(self,
            analysis_id_I,
            calculated_concentration_units_I,
            component_names_I,
            warn_I=True):
        '''delete rows from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string,
        component_names_I = [] of string
        OUTPUT:
        '''
        try:
            table = 'data_stage02_quantification_dataPreProcessing_averages';
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            
            query = {};
            query['delete_from'] = [{'table_name':table}];
                    
            names_str = ','.join(component_names_I);
            names_query = ("('{%s}'::text[])" %(names_str))

            query['where'] = [{
                    'table_name':table,
                    'column_name':'analysis_id',
                    'value':analysis_id_I,
		            'operator':'LIKE',
                    'connector':'AND'
                    },{
                    'table_name':table,
                    'column_name':'component_name',
                    'value':names_query,
                    'operator':'=ANY',
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

    # get unique values based on a json type query
    def getGroup_componentNameAndCount_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_averages'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [
            {"table_name":tables[0],
             "column_name":'component_name',
             },
             {"table_name":tables[0],
             "column_name":'component_name',
             'aggregate_function':'count',
             'label':'count_1',
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
        ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'component_name',
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
    def getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_averages'];
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
    def getGroup_analysisIDAndExperimentIDAndSampleNameAbbreviationAndTimePoint_analysisIDAndCalculatedConcentrationUnits_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_averages'];
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
             "column_name":'sample_name_abbreviation',
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
             "column_name":'sample_name_abbreviation',
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
             "column_name":'sample_name_abbreviation',
            'order':'ASC',
             },
             {"table_name":tables[0],
             "column_name":'time_point',
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
    def getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDAndSampleNameAbbreviationAndTimePoint_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_id_I,
                sample_name_abbreviation_I,
                time_point_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_averages'];
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
            'column_name':'sample_name_abbreviation',
            'value':sample_name_abbreviation_I,
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
    
    def getGroup_analysisIDAndExperimentIDAndSampleNameAbbreviationAndTimePointAndComponentNameArray_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_dataPreProcessing_averages'];
        # get the listDict data
        data_O = [];
        query_cmd = 'SELECT analysis_id, experiment_id, sample_name_abbreviation, time_point, ';
        query_cmd += ('array(select component_name from "%s" group by component_name) ' %(tables[0]));
        query_cmd += ('FROM "%s" ' %(tables[0]));
        query_cmd += ("WHERE analysis_id LIKE '%s' " %(analysis_id_I));
        query_cmd += ("AND calculated_concentration_units LIKE '%s'" %(calculated_concentration_units_I));
        query_cmd += 'GROUP BY analysis_id, experiment_id, sample_name_abbreviation, time_point;';
        
        try:
            queryselect = sbaas_base_query_select(self.session,self.engine,self.settings);
            data_tmp = queryselect.execute_select(query_cmd);
            data_O = queryselect.convert_listKeyedTuple2ListDict(data_tmp);
        except Exception as e:
            print(e);

        return data_O;   

    #Joins with data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_averages
    def get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_averages"""
        try:
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id,
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_averages.time_point,
                ).filter(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id,
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_averages.time_point).order_by(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id.asc(),
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.asc(),
                data_stage02_quantification_dataPreProcessing_averages.experiment_id.asc(),
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc(),
                data_stage02_quantification_dataPreProcessing_averages.time_point.asc()).all();
            data_O=[];
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'calculated_concentration_units':calculated_concentration_units_I,
                                           'time_point':time_points_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                component_names_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_averages"""
        try:
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id,
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_averages.time_point,
                ).filter(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id,
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_averages.time_point).order_by(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id.asc(),
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.asc(),
                data_stage02_quantification_dataPreProcessing_averages.experiment_id.asc(),
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc(),
                data_stage02_quantification_dataPreProcessing_averages.time_point.asc()).all();
            data_O=[];
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'component_name':component_names_I,
                                           'calculated_concentration_units':calculated_concentration_units_I,
                                           'time_point':time_points_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_id_I,
                sample_name_abbreviation_I,
                time_point_I,
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_averages"""
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages
                ).filter(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_dataPreProcessing_averages.experiment_id.like(experiment_id_I),
                data_stage02_quantification_dataPreProcessing_averages.time_point.like(time_point_I),
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc(),
                data_stage02_quantification_dataPreProcessing_averages.component_name.asc(),
                ).all();
            data_O=[d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePointsAndComponentName_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_id_I,
                sample_name_abbreviation_I,
                time_point_I,
                component_name_I
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_averages"""
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages
                ).filter(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_dataPreProcessing_averages.experiment_id.like(experiment_id_I),
                data_stage02_quantification_dataPreProcessing_averages.time_point.like(time_point_I),
                data_stage02_quantification_dataPreProcessing_averages.component_name.like(component_name_I),
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc(),
                data_stage02_quantification_dataPreProcessing_averages.component_name.asc(),
                ).all();
            data_O=[d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,calculated_concentration_units_I,
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],):
        """get analysis_id, experiment_id, sample_name_abbreviation, time_point, component_name, component_group_name,
        [descriptive_statistics], and calculated_concentration units from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id
        calculated_concentration_units
        OPTIONAL INPUT:
        experiment_ids_I
        sample_name_abbreviations_I
        time_points_I
        """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).all();
            data_O = [];
            if data:
                data_O = listDict(listDict_I=[d.__repr__dict__() for d in data]);
                data_O.convert_listDict2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'component_name':component_names_I,
                                           'component_group_name':component_group_names_I,
                                           'time_point':time_points_I,
                                           });
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self, analysis_id_I,calculated_concentration_units_I):
        """get sample_name_abbreviation and sample_name_abbreviation by analysis_id, calculated_concentration_units from data_stage02_quantification_dataPreProcessing_averages"""
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc()).all();
            sample_name_abbreviation_O = [d.sample_name_abbreviation for d in data];
            return sample_name_abbreviation_O;
        except SQLAlchemyError as e:
            print(e);
    
    def get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_dataPreProcessing_averages"""
        try:
            data = self.session.query(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id,
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_averages.time_point,
                ).filter(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id,
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units,
                data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                data_stage02_quantification_dataPreProcessing_averages.time_point).order_by(
                data_stage02_quantification_dataPreProcessing_averages.analysis_id.asc(),
                data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.asc(),
                data_stage02_quantification_dataPreProcessing_averages.experiment_id.asc(),
                data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc(),
                data_stage02_quantification_dataPreProcessing_averages.time_point.asc()).all();
            data_O=[];
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'time_point':time_points_I,
                                           });
                data_O.convert_dataFrame2ListDict();
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_means_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(
        self, analysis_id_I,calculated_concentration_units_I,sample_name_abbreviation_I):
        """get all means ordered by component_name ASC and by analysis_id, calculated_concentration_units, sample_name_abbreviation
        """
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_averages.mean).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name.asc()).all();
            data_O = [d.mean for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_means_analysisIDAndCalculatedConcentrationUnitsAndComponentNameAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(
        self, analysis_id_I,calculated_concentration_units_I,component_name_I,sample_name_abbreviation_I):
        """get all means concentrations by analysis_id, calculated_concentration_units, component_name, sample_name_abbreviation"""
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_averages.mean).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.component_name.like(component_name_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration.asc()).all();
            data_O = [d.mean for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    #Querys to be called by other classes
    def get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all mean values by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.mean).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.mean).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.mean);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allMedians_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all median values by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.median).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.mean).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.median);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allCVs_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all CVs by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.cv).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.cv).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.cv);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(self, analysis_id_I):
        """query calculated_concentration_units by analysis id from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d.calculated_concentration_units);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrationUnits_analysisIDAndImputationMethod_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                imputation_method_I):
        """query calculated_concentration_units from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        OUTPUT:
        """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.imputation_method.like(imputation_method_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d.calculated_concentration_units);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_imputationMethods_analysisID_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                ):
        """query imputation_methods from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        OUTPUT:
        """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.imputation_method,
                    ).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.imputation_method,
                    ).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.imputation_method.asc()).all();
            imputation_method_O = [];
            for d in data: 
                imputation_method_O.append(d.imputation_method);
            return imputation_method_O;
        except SQLAlchemyError as e:
            print(e);   
    def getCount_componentNames_analysisID_dataStage02QuantificationDataPreProcessingAverages(self, analysis_id_I):
        """query row count of unique component_names by analysis id from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.component_name).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);
    def getCount_componentNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I):
        """query row count of unique component_names from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.component_name).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);
    def getCount_componentNames_analysisIDAndImputationMethodAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                imputation_method_I,
                calculated_concentration_units_I):
        """query row count of unique component_names from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.component_name).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.imputation_method.like(imputation_method_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);   
    def getCount_experimentIDAndSampleNameAbbreviationAndTimePoint_analysisID_dataStage02QuantificationDataPreProcessingAverages(self, analysis_id_I):
        """query row count of unique experiment_id/sample_name_abbreviation/time_point by analysis id from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_averages.time_point).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_averages.time_point).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.experiment_id.asc(),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc(),
                    data_stage02_quantification_dataPreProcessing_averages.time_point.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);
    def getCount_experimentIDAndSampleNameAbbreviationAndTimePoint_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                analysis_id_I,
                calculated_concentration_units_I):
        """query row count of unique experiment_id/sample_name_abbreviation/time_point from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_averages.time_point).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_averages.time_point).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.experiment_id.asc(),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc(),
                    data_stage02_quantification_dataPreProcessing_averages.time_point.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);   
    def getCount_experimentIDAndSampleNameAbbreviationAndTimePoint_analysisIDAndImputationMethodAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,analysis_id_I,
                imputation_method_I,
                calculated_concentration_units_I):
        """query row count of unique experiment_id/sample_name_abbreviation/time_point from """
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_averages.time_point).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.imputation_method.like(imputation_method_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.experiment_id,
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_averages.time_point).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.experiment_id.asc(),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc(),
                    data_stage02_quantification_dataPreProcessing_averages.time_point.asc()).count();
            return data;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(self, analysis_id_I,calculated_concentration_units_I,sample_name_abbreviation_I):
        """get rows by analysis_id, calculated_concentration_units, and sample_name_abbreviation from data_stage02_quantification_dataPreProcessing_averages"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_averages).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDataPreProcessingAverages(self, analysis_id_I,calculated_concentration_units_I,component_name_I):
        """get rows by analysis_id, calculated_concentration_units, and component_name from data_stage02_quantification_dataPreProcessing_averages"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_averages).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.component_name.like(component_name_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
      
    # query sample_names from data_stage02_quantification_descriptiveStats
    def get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingAverages(self,analysis_id_I):
        '''Querry sample_name_abbreviations that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_averages.time_point).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation,
                    data_stage02_quantification_dataPreProcessing_averages.time_point).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.time_point.asc(),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            time_points_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
                    time_points_O.append(d.time_point);
            return sample_name_abbreviations_O,time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # query component_names from data_stage02_quantification_descriptiveStats
    def get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,analysis_id_I,calculated_concentration_units_I):
        '''Query component_names and component_group_names that are used by analysis_id and calculated_concentration_units'''
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages.component_name,
                                      data_stage02_quantification_dataPreProcessing_averages.component_group_name).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).group_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name,
                    data_stage02_quantification_dataPreProcessing_averages.component_group_name).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.component_name.asc()).all();
            component_name_O = [];
            component_group_name_O = [];
            if data: 
                for d in data:
                    component_name_O.append(d.component_name);
                    component_group_name_O.append(d.component_group_name);
            return component_name_O,component_group_name_O;
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage02_quantification_descriptiveStats
    def get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                                analysis_id_I,
                                sample_name_abbreviation_I,
                                component_name_I,
                                calculated_concentration_units_I):
        '''Query data by sample_name_abbreviation, component_name, and calculated_concentration_units that are used for the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_dataPreProcessing_averages.component_name.like(component_name_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).all();
            mean,stdev,ci_lb,ci_ub,calculated_concentration_units = None,None,None,None,None;
            if len(data)>1:
                print('More than 1 row found');
            if data: 
                for d in data:
                    mean=d.mean;
                    if d.var and not d.var is None: stdev=sqrt(d.var);
                    else: stdev=0.0;
                    ci_lb=d.ci_lb;
                    ci_ub=d.ci_ub;
                    calculated_concentration_units=d.calculated_concentration_units;
            return mean,stdev,ci_lb,ci_ub,calculated_concentration_units;
        except SQLAlchemyError as e:
            print(e);
    def get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
                                analysis_id_I,
                                sample_name_abbreviation_I,
                                time_point_I,
                                component_name_I,
                                calculated_concentration_units_I):
        '''Querry data by sample_name_abbreviation, component_name, and calculated_concentration_units that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_averages).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_dataPreProcessing_averages.time_point.like(time_point_I),
                    data_stage02_quantification_dataPreProcessing_averages.component_name.like(component_name_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).all();
            mean,stdev,ci_lb,ci_ub,calculated_concentration_units = None,None,None,None,None;
            if len(data)>1:
                print('More than 1 row found');
            if data: 
                for d in data:
                    mean=d.mean;
                    if d.var and not d.var is None: stdev=sqrt(d.var);
                    else: stdev=0.0;
                    ci_lb=d.ci_lb;
                    ci_ub=d.ci_ub;
                    calculated_concentration_units=d.calculated_concentration_units;
            return mean,stdev,ci_lb,ci_ub,calculated_concentration_units;
        except SQLAlchemyError as e:
            print(e);
