from .stage02_quantification_analysis_postgresql_models import *
#SBaaS base
from SBaaS_base.postgresql_methods import postgresql_methods
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete
from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_analysis_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_quantification_analysis
        '''
        tables_supported = {'data_stage02_quantification_analysis':data_stage02_quantification_analysis,
                            'data_stage02_quantification_analysis_pipeline':data_stage02_quantification_analysis_pipeline,
                            'data_stage02_quantification_analysis_connection':data_stage02_quantification_analysis_connection,
                            'data_stage02_quantification_analysis_group':data_stage02_quantification_analysis_group,
                            'data_stage02_quantification_analysis_diagnostics':data_stage02_quantification_analysis_diagnostics,
                            'data_stage02_quantification_analysis_partitions':data_stage02_quantification_analysis_partitions,
                        };
        self.set_supportedTables(tables_supported);
    # data_stage02_quantification_analysis
    # query rows from data_stage02_quantification_analysis
    def get_experimentIDAndSampleNameAbbreviationAndTimePoint_analysisID_dataStage02QuantificationAnalysis(self,analysis_id_I):
        '''Query experiment_id, sample_name_abbreviation and time_point that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_analysis.time_point).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_analysis.time_point).order_by(
                    data_stage02_quantification_analysis.experiment_id.asc(),
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc(),
                    data_stage02_quantification_analysis.time_point.asc()).all();
            experiment_id_O = []
            sample_name_abbreviation_O = []
            time_point_O = []
            if data: 
                for d in data:
                    experiment_id_O.append(d.experiment_id);
                    sample_name_abbreviation_O.append(d.sample_name_abbreviation); 
                    time_point_O.append(d.time_point);               
            return  experiment_id_O,sample_name_abbreviation_O,time_point_O;
        except SQLAlchemyError as e:
            print(e);
    def get_experimentIDAndSampleNameShortAndTimePoint_analysisID_dataStage02QuantificationAnalysis(self,analysis_id_I):
        '''Query Query experiment_id, sample_name_short and time_point that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_short,
                    data_stage02_quantification_analysis.time_point).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_short,
                    data_stage02_quantification_analysis.time_point).order_by(
                    data_stage02_quantification_analysis.experiment_id.asc(),
                    data_stage02_quantification_analysis.sample_name_short.asc(),
                    data_stage02_quantification_analysis.time_point.asc()).all();
            experiment_id_O = []
            sample_name_short_O = []
            time_point_O = []
            if data: 
                for d in data:
                    experiment_id_O.append(d.experiment_id);
                    sample_name_short_O.append(d.sample_name_short); 
                    time_point_O.append(d.time_point);               
            return  experiment_id_O,sample_name_short_O,time_point_O;
        except SQLAlchemyError as e:
            print(e);
    def get_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndSampleNameAbbreviation_dataStage02QuantificationAnalysis(self,
            analysis_id_I,
            sample_name_abbreviation_I):
        '''Query experiment_id, sample_name_short and time_point that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_short,
                    data_stage02_quantification_analysis.time_point).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_analysis.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_short,
                    data_stage02_quantification_analysis.time_point).order_by(
                    data_stage02_quantification_analysis.experiment_id.asc(),
                    data_stage02_quantification_analysis.sample_name_short.asc(),
                    data_stage02_quantification_analysis.time_point.asc()).all();
            experiment_id_O = []
            sample_name_short_O = []
            time_point_O = []
            if data: 
                for d in data:
                    experiment_id_O.append(d.experiment_id);
                    sample_name_short_O.append(d.sample_name_short); 
                    time_point_O.append(d.time_point);               
            return  experiment_id_O,sample_name_short_O,time_point_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_analysisIDAndExperimentIDAndSampleNameAbbreviation_dataStage02QuantificationAnalysis(self,
            analysis_id_I,
            experiment_id_I,
            sample_name_abbreviation_I):
        '''Query time_point that are used from the analysis'''
        try:
            data = self.session.query(
                    data_stage02_quantification_analysis.time_point).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_analysis.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.time_point).order_by(
                    data_stage02_quantification_analysis.time_point.asc()).all();
            time_point_O = [d.time_point for d in data]           
            return  time_point_O;
        except SQLAlchemyError as e:
            print(e);

    #SPLIT 2:
    def reset_dataStage02_quantification_analysis(self,
            tables_I = ['data_stage02_quantification_analysis'],
            analysis_id_I = None,
            warn_I=True):
        try:
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
    def reset_dataStage02_quantification_analysis_diagnostics(self,
            tables_I = ['data_stage02_quantification_analysis_diagnostics'],
            pipeline_id_I = None,
            warn_I=True):
        try:
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                query = {};
                query['delete_from'] = [{'table_name':table}];
                query['where'] = [{
                        'table_name':table,
                        'column_name':'pipeline_id',
                        'value':pipeline_id_I,
		                'operator':'LIKE',
                        'connector':'AND'
                        }
	                ];
                table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
                query = querydelete.make_queryFromString(table_model,query);
                querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);
    def _get_rows_analysisID_dataStage02QuantificationAnalysis(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_analysis
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_analysis'];
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
            if k not in query.items():
                query[k]=[];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def _get_rows_analysisID_dataStage02QuantificationAnalysisGroup(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_analysis_group
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_analysis_group'];
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
            'column_name':'analysis_group_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'order':'ASC',
            },
        ];

        #additional blocks
        for k,v in query_I.items():
            if k not in query.items():
                query[k]=[];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def _get_rows_connectionID_dataStage02QuantificationAnalysisConnection(self,
                connection_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by connection_id from data_stage02_quantification_analysis_connection
        INPUT:
        connection_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_analysis_connection'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'connection_id',
            'value':connection_id_I,
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
            'column_name':'connection_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'connection_order',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'execute_object',
            'order':'ASC',
            },
        ];

        #additional blocks
        for k,v in query_I.items():
            if k not in query.items():
                query[k]=[];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def _get_rows_pipelineID_dataStage02QuantificationAnalysisPipeline(self,
                pipeline_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by pipeline_id from data_stage02_quantification_analysis_pipeline
        INPUT:
        pipeline_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_analysis_pipeline'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'pipeline_id',
            'value':pipeline_id_I,
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
            'column_name':'pipeline_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'pipeline_order',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'connection_id',
            'order':'ASC',
            },
        ];

        #additional blocks
        for k,v in query_I.items():
            if k not in query.items():
                query[k]=[];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def _get_rows_analysisID_dataStage02QuantificationAnalysisPartitions(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_analysis_partitions
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        EXAMPLE:
        analysis2Partitions = {};
        analysis2Partitions = _get_rows_analysisID_dataStage02QuantificationAnalysisPartitions(
            analysis_id_I='',
            query_I={},
            output_O='dictColumn',
            dictColumn_I='analysis_id',
        )
        '''

        tables = ['data_stage02_quantification_analysis_partitions'];
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
            'column_name':'analysis_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'partition_id',
            'order':'ASC',
            },
        ];

        #additional blocks
        for k,v in query_I.items():
            if k not in query.items():
                query[k]=[];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def _get_rows_analysisIDs_dataStage02QuantificationAnalysisPartitions(self,
                analysis_ids_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_analysis_partitions
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        EXAMPLE:
        analysis2Partitions = {};
        analysis2Partitions = _get_rows_analysisID_dataStage02QuantificationAnalysisPartitions(
            analysis_id_I='',
            query_I={},
            output_O='dictColumn',
            dictColumn_I='analysis_id',
        )
        '''

        tables = ['data_stage02_quantification_analysis_partitions'];
        # get the listDict data
        data_O = [];
        query = {};
        analysis_ids_str = "('{%s}'::text[])"%self.convert_list2string(analysis_ids_I);
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'partition_column',
            'value':'analysis_id',
            'operator':'=',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'partition_value',
            'value':analysis_ids_str,
            'operator':'=ANY',
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
            'column_name':'partition_column',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'partition_value',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'partition_id',
            'order':'ASC',
            },
        ];

        #additional blocks
        for k,v in query_I.items():
            if k not in query.items():
                query[k]=[];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def drop_dataStage02QuantificationAnalysisTablePartitions(
        self,
        schema_I='public',
        table_name_I='',
        analysis_ids_I=[],
        verbose_I=True,
        ):
        '''drop table partitions by analysis_id
        INPUT:
        schema_I = string
        tablen_name_I = string
        analysis_ids_I = [] of strings

        '''

        #get the partition ids for the analysis_ids
        rows = self._get_rows_analysisIDs_dataStage02QuantificationAnalysisPartitions(
            analysis_ids_I,query_I={},
            output_O='listDict',dictColumn_I=None
            )
        partition_ids = [r['partition_id'] for r in rows];
        #drop the tables
        pg_methods = postgresql_methods();
        pg_methods.drop_tablePartitions(
            self.session,
            schema_I=schema_I,
            table_name_I=table_name_I,
            partition_ids_I=partition_ids,
            verbose_I=verbose_I,
            )

    #SPLIT 1:   
    def get_rows_analysisID_dataStage02QuantificationAnalysis(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_analysis).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.used_.is_(True)).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
   

