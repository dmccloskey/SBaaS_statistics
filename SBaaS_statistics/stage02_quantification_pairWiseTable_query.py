#SBaaS
from .stage02_quantification_pairWiseTable_postgresql_models import *
#SBaaS_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete
#SBaaS_template
from SBaaS_base.sbaas_template_query import sbaas_template_query
#Resources
import numpy as np

class stage02_quantification_pairWiseTable_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_pairWiseTable':data_stage02_quantification_pairWiseTable,
                            'data_stage02_quantification_pairWiseTable_replicates':data_stage02_quantification_pairWiseTable_replicates,
                            'data_stage02_quantification_pairWiseTableFeatures':data_stage02_quantification_pairWiseTableFeatures,
                            'data_stage02_quantification_pairWiseTableCrossUnits':data_stage02_quantification_pairWiseTableCrossUnits,
                            'data_stage02_quantification_pairWiseTableFeaturesCrossUnits':data_stage02_quantification_pairWiseTableFeaturesCrossUnits,
                        };
        self.set_supportedTables(tables_supported);
        
    #Query rows from data_stage02_quantification_pairWiseTable_replicates
    def get_rows_analysisID_dataStage02QuantificationPairWiseTable(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_pairWiseTable
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_pairWiseTable'];
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
    def get_rows_dataStage02QuantificationPairWiseTable(self,
                tables_I,
                query_I,
                output_O,
                dictColumn_I=None):
        """get rows by analysis ID from data_stage02_quantification_pairWiseTable"""
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
    def add_dataStage02QuantificationPairWiseTable(self,table_I,data_I):
        '''add rows of data_stage02_quantification_pairWiseTable'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryinsert = sbaas_base_query_insert(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryinsert.add_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);
    def update_dataStage02QuantificationPairWiseTable(self,table_I,data_I):
        '''update rows of data_stage02_quantification_pairWiseTable'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryupdate = sbaas_base_query_update(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryupdate.update_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);

    def initialize_dataStage02_quantification_pairWiseTable(self,
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
    def drop_dataStage02_quantification_pairWiseTable(self,
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
    def reset_dataStage02_quantification_pairWiseTable(self,
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

    ##Query unique data from data_stage02_quantification_pairWiseTable_replicates
    def get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationPairWiseTableReplicates(self, analysis_id_I):
        """get concentration_units by analysis_id from data_stage02_quantification_pairWiseTable_replicates"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_units).filter(
                    data_stage02_quantification_pairWiseTable_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTable_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_units).order_by(
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationPairWiseTableReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                ):
        """get component_name and component_group_name by analysis_id, calculated_concentration_unit"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTable_replicates.component_name,
                    data_stage02_quantification_pairWiseTable_replicates.component_group_name).filter(
                    data_stage02_quantification_pairWiseTable_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_pairWiseTable_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTable_replicates.component_name,
                    data_stage02_quantification_pairWiseTable_replicates.component_group_name).order_by(
                    data_stage02_quantification_pairWiseTable_replicates.component_name.asc(),
                    data_stage02_quantification_pairWiseTable_replicates.component_group_name.asc()).all();
            component_name_O = [];
            component_group_name_O = [];
            for d in data: 
                component_name_O.append(d.component_name);
                component_group_name_O.append(d.component_group_name);
            return component_name_O,component_group_name_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationPairWiseTableReplicates(self, analysis_id_I,concentration_units_I):
        """get sample_name_abbreviation and sample_name_short by analysis_id, calculated_concentration_units"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1,
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2,
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_short_1,
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_short_2).filter(
                    data_stage02_quantification_pairWiseTable_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pairWiseTable_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1,
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2,
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_short_1,
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_short_2).order_by(
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1.asc(),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_short_1.asc(),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2.asc(),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_short_2.asc()).all();
            sample_name_abbreviation_1_O = [];
            sample_name_abbreviation_2_O = [];
            sample_name_short_1_O = [];
            sample_name_short_2_O = [];
            for d in data: 
                sample_name_abbreviation_1_O.append(d.sample_name_abbreviation_1);
                sample_name_short_1_O.append(d.sample_name_short_1);
                sample_name_abbreviation_2_O.append(d.sample_name_abbreviation_2);
                sample_name_short_2_O.append(d.sample_name_short_2);
            return sample_name_abbreviation_1_O,sample_name_short_1_O,sample_name_abbreviation_2_O,sample_name_short_2_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationPairWiseTableReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                component_name_I,
                ):
        """get sample_name_abbreviation and sample_name_short by analysis_id, calculated_concentration_units, component_name"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1,
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2,).filter(
                    data_stage02_quantification_pairWiseTable_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTable_replicates.component_name.like(component_name_I),
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1!=data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2,
                    data_stage02_quantification_pairWiseTable_replicates.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1,
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2,).order_by(
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1.asc(),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2.asc(),).all();
            sample_name_abbreviation_1_O = [d.sample_name_abbreviation_1 for d in data];
            sample_name_abbreviation_2_O = [d.sample_name_abbreviation_2 for d in data];
            return sample_name_abbreviation_1_O,sample_name_abbreviation_2_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationPairWiseTableReplicates(self, analysis_id_I,concentration_units_I,sample_name_short_1_I,sample_name_short_2_I):
        """get calculated_calculated concentrations by analysis_id, calculated_concentration_units, and sample_name_short_1/_2"""
        try:
            data = self.session.query(
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_1,
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_2).filter(
                    data_stage02_quantification_pairWiseTable_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_short_1.like(sample_name_short_1_I),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_short_2.like(sample_name_short_2_I),
                    data_stage02_quantification_pairWiseTable_replicates.used_.is_(True)).order_by(
                    data_stage02_quantification_pairWiseTable_replicates.component_name.asc()).all();
            data_1_O = [];
            data_2_O = [];
            for d in data: 
                data_1_O.append(d.calculated_concentration_1);
                data_2_O.append(d.calculated_concentration_2);
            return data_1_O,data_2_O;
        except SQLAlchemyError as e:
            print(e);
    def get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNameAndSampleNameAbbreviation_dataStage02QuantificationPairWiseTableReplicates(
            self, analysis_id_I,calculated_concentration_units_I,component_name_I,sample_name_abbreviation_1_I,sample_name_abbreviation_2_I):
        """get calculated_calculated concentrations by analysis_id, calculated_concentration_units, component_name, and sample_name_abbreviation_1/_2"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_1,
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_2).filter(
                    data_stage02_quantification_pairWiseTable_replicates.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTable_replicates.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_pairWiseTable_replicates.component_name.like(component_name_I),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1.like(sample_name_abbreviation_1_I),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2.like(sample_name_abbreviation_2_I),
                    data_stage02_quantification_pairWiseTable_replicates.used_.is_(True)).order_by(
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_1.asc(),
                    data_stage02_quantification_pairWiseTable_replicates.sample_name_abbreviation_2.asc()).all();
            nvalues = int(np.sqrt(len(data)));
            rvalues = range(len(data))
            # data 2 unique is the first n values; data 1 unique is every nvalue
            data_1_O = [data[i].calculated_concentration_1 for i in rvalues[0::nvalues]];
            #data_1_O = [data[i].calculated_concentration_1 for i in range(len(data)) if i % nvalues == 0];
            data_2_O = [data[i].calculated_concentration_2 for i in range(nvalues)];
            return data_1_O,data_2_O;
        except SQLAlchemyError as e:
            print(e);

    #Query rows from data_stage02_quantification_pairWiseTable_replicates
    def get_rows_analysisID_dataStage02QuantificationPairWiseTableReplicates(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_pairWiseTable_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_pairWiseTable_replicates'];
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

    #Query groups from data_stage02_quantification_pairWiseTable_replicates
    def getGroup_analysisIDAndSampleNameShortAndSampleNameAbbreviationAndComponentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationPairWiseTableReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_pairWiseTable_replicates
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_pairWiseTable_replicates'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [
            {"table_name":tables[0],
             "column_name":'analysis_id',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_short_1',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_short_2',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_abbreviation_1',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_abbreviation_2',
             },
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
             "column_name":'analysis_id',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_short_1',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_short_2',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_abbreviation_1',
             },
             {"table_name":tables[0],
             "column_name":'sample_name_abbreviation_2',
             },
            {"table_name":tables[0],
             "column_name":'component_name',
             },
             {"table_name":tables[0],
             "column_name":'component_group_name',
             },
        ];
        query['order_by'] = [
            {"table_name":tables[0],
             "column_name":'analysis_id',
            'order':'ASC',
             },
             {"table_name":tables[0],
             "column_name":'component_name',
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