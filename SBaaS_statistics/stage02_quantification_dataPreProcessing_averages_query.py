from SBaaS_base.sbaas_base import sbaas_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

from .stage02_quantification_dataPreProcessing_replicates_postgresql_models import *

class stage02_quantification_dataPreProcessing_replicates_query(sbaas_template_query,
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
    def initialize_stage02_quantification_dataPreProcessing_replicates(self,
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
    def drop_stage02_quantification_dataPreProcessing_replicates(self,
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
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def delete_rows_analysisIDAndCalculatedConcentrationUnitsAndCalculatedConcentrationValueAndOperator_dataStage02QuantificationDataPreProcessingAverages(self,
            analysis_id_I,
            calculated_concentration_units_I,
            value_I,operator_I,
            warn_I=True):
        '''delete rows from data_stage02_quantification_dataPreProcessing_averages
        INPUT:
        analysis_id_I = string,
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

    # get unique values based on a json type query
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
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def getGroup_analysisIDAndExperimentIDAndSampleNameShortAndTimePoint_analysisIDAndCalculatedConcentrationUnits_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
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
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDAndSampleNameShortAndTimePoint_dataStage02QuantificationDataPreProcessingAverages(self,
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
    
    def getGroup_analysisIDAndExperimentIDAndSampleNameShortAndTimePointAndComponentNameArray_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
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
            for d in data:
                add_row = True
                if calculated_concentration_units_I and not d.calculated_concentration_units in calculated_concentration_units_I:
                    add_row = False;
                elif experiment_ids_I and not d.experiment_id in experiment_ids_I:
                    add_row = False;
                elif sample_name_abbreviations_I and not d.sample_name_abbreviation in sample_name_abbreviations_I:
                    add_row = False;
                elif time_points_I and not d.time_point in time_points_I:
                    add_row = False;
                if add_row:
                    data_O.append({
                    'analysis_id':d.analysis_id,
                    'calculated_concentration_units':d.calculated_concentration_units,
                    'experiment_id':d.calculated_concentration_units,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    'time_point':d.time_point,
                    })
            return data_O;
        except SQLAlchemyError as e:
            print(e);
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
            for d in data:
                add_row = True
                if calculated_concentration_units_I and not d.calculated_concentration_units in calculated_concentration_units_I:
                    add_row = False;
                elif experiment_ids_I and not d.experiment_id in experiment_ids_I:
                    add_row = False;
                elif sample_name_abbreviations_I and not d.sample_name_abbreviation in sample_name_abbreviations_I:
                    add_row = False;
                elif time_points_I and not d.time_point in time_points_I:
                    add_row = False;
                if add_row:
                    data_O.append({
                    'analysis_id':d.analysis_id,
                    'calculated_concentration_units':d.calculated_concentration_units,
                    'experiment_id':d.experiment_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    'time_point':d.time_point,
                    })
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
            data_O=[];
            for d in data:
                data_O.append(d.__repr__dict__())
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
            sample_name_abbreviation_O = [];
            for d in data: 
                sample_name_abbreviation_O.append(d.sample_name_abbreviation);
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
            for d in data:
                add_row = True
                if experiment_ids_I and not d.experiment_id in experiment_ids_I:
                    add_row = False;
                elif sample_name_abbreviations_I and not d.sample_name_abbreviation in sample_name_abbreviations_I:
                    add_row = False;
                elif time_points_I and not d.time_point in time_points_I:
                    add_row = False;
                if add_row:
                    data_O.append({
                    'analysis_id':d.analysis_id,
                    'calculated_concentration_units':d.calculated_concentration_units,
                    'experiment_id':d.experiment_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    'time_point':d.time_point,
                    })
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    #Querys to be called by other classes
    def get_allCalculatedConcentrations_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages(self, analysis_id_I,concentration_units_I):
        """get all calculated_calculated concentrations by analysis_id and calculated_concentration_units from analysis ID"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration).filter(
                    data_stage02_quantification_dataPreProcessing_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_dataPreProcessing_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_averages.calculated_concentration.asc()).all();
            data_O = [];
            for d in data: 
                data_O.append(d.calculated_concentration);
            return data_O;
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
    def getCount_experimentIDAndSampleNameShortAndTimePoint_analysisID_dataStage02QuantificationDataPreProcessingAverages(self, analysis_id_I):
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
    def getCount_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,
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
    def getCount_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndImputationMethodAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(self,analysis_id_I,
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
            data_O = [];
            for d in data: 
                data_O.append(d.__repr__dict__());
            return data_O;
        except SQLAlchemyError as e:
            print(e);
