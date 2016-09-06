#SBaaS_base
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete
#SBaaS_template
from SBaaS_base.sbaas_template_query import sbaas_template_query
#postgresql_models
from .stage02_quantification_spls_postgresql_models import *
#resources
from listDict.listDict import listDict

class stage02_quantification_spls_query(sbaas_template_query,
                                       ):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_quantification_spls
        '''
        tables_supported = {
            'data_stage02_quantification_spls_scores':data_stage02_quantification_spls_scores,
            'data_stage02_quantification_spls_loadings':data_stage02_quantification_spls_loadings,
            'data_stage02_quantification_spls_loadingsResponse':data_stage02_quantification_spls_loadingsResponse,
            'data_stage02_quantification_spls_impfeat':data_stage02_quantification_spls_impfeat,
            'data_stage02_quantification_spls_pipeline':data_stage02_quantification_spls_pipeline,
            'data_stage02_quantification_spls_hyperparameter':data_stage02_quantification_spls_hyperparameter,
            #'data_stage02_quantification_spls_validation':data_stage02_quantification_spls_validation,
            'data_stage02_quantification_spls_axis':data_stage02_quantification_spls_axis,
                        };
        self.set_supportedTables(tables_supported);

    #Query rows
    def reset_dataStage02_quantification_spls(self,
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

    #Safe calls by other classes
    def get_rows_analysisID_dataStage02QuantificationSPLSPipeline(self,analysis_id_I):
        '''Query rows that are used by the analysis_id
        INPUT:
        analysis_id_I = string
        OUTPUT:
        rows_O = listDict'''
        try:
            data = self.session.query(data_stage02_quantification_spls_pipeline).filter(
                    data_stage02_quantification_spls_pipeline.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_spls_pipeline.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationSPLSPipeline(self,pipeline_id_I):
        '''Query models, methods, and parameters that are used by the pipeline_id in order
        INPUT:
        pipeline_id_I = string
        OUTPUT:
        models_O = list, pipeline models
        methods_O = list, pipeline methods
        parameters_O = list, pipeline parameters'''
        try:
            data = self.session.query(
                data_stage02_quantification_spls_pipeline.pipeline_model,
                data_stage02_quantification_spls_pipeline.pipeline_method,
                data_stage02_quantification_spls_pipeline.pipeline_parameters).filter(
                data_stage02_quantification_spls_pipeline.pipeline_id.like(pipeline_id_I),
                data_stage02_quantification_spls_pipeline.used_.is_(True)).order_by(
                data_stage02_quantification_spls_pipeline.pipeline_order).all();
            models_O,methods_O,parameters_O = [],[],[];
            if data: 
                data_i = listDict(record_I=data);
                data_i.convert_record2DataFrame();
                models_O=data_i.dataFrame['pipeline_model'].get_values();
                methods_O=data_i.dataFrame['pipeline_method'].get_values();
                parameters_O=data_i.dataFrame['pipeline_parameters'].get_values();
            return models_O,methods_O,parameters_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationSPLSAxis(self,analysis_id_I,axis_I=10):
        '''Query rows that are used by the analysis_id
        INPUT:
        analysis_id_I = string
        OUTPUT:
        rows_O = listDict'''
        try:
            data = self.session.query(data_stage02_quantification_spls_axis).filter(
                    data_stage02_quantification_spls_axis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_spls_axis.axis<=axis_I,
                    data_stage02_quantification_spls_axis.used_.is_(True)).order_by(
                    data_stage02_quantification_spls_axis.pipeline_id.asc(),
                    data_stage02_quantification_spls_axis.test_size.asc(),
                    data_stage02_quantification_spls_axis.calculated_concentration_units.asc(),
                    data_stage02_quantification_spls_axis.metric_method.asc(),
                    ).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationSPLSScores(self,analysis_id_I,axis_I=3):
        '''Query rows that are used by the analysis_id
        INPUT:
        analysis_id_I = string
        OUTPUT:
        rows_O = listDict'''
        try:
            data = self.session.query(data_stage02_quantification_spls_scores).filter(
                    data_stage02_quantification_spls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_spls_scores.axis<=axis_I,
                    data_stage02_quantification_spls_scores.used_.is_(True)).order_by(
                    data_stage02_quantification_spls_scores.pipeline_id.asc(),
                    data_stage02_quantification_spls_scores.test_size.asc(),
                    data_stage02_quantification_spls_scores.response_name.asc(),
                    data_stage02_quantification_spls_scores.sample_name_short.asc(),
                    data_stage02_quantification_spls_scores.calculated_concentration_units.asc(),
                    data_stage02_quantification_spls_scores.metric_method.asc(),
                    ).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationSPLSLoadings(self,analysis_id_I,axis_I=3):
        '''Query rows that are used by the analysis_id
        INPUT:
        analysis_id_I = string
        OUTPUT:
        rows_O = listDict'''
        try:
            data = self.session.query(data_stage02_quantification_spls_loadings).filter(
                    data_stage02_quantification_spls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_spls_loadings.axis<=axis_I,
                    data_stage02_quantification_spls_loadings.used_.is_(True)).order_by(
                    data_stage02_quantification_spls_loadings.pipeline_id.asc(),
                    data_stage02_quantification_spls_loadings.test_size.asc(),
                    data_stage02_quantification_spls_loadings.component_group_name.asc(),
                    data_stage02_quantification_spls_loadings.component_name.asc(),
                    data_stage02_quantification_spls_loadings.calculated_concentration_units.asc(),
                    data_stage02_quantification_spls_loadings.metric_method.asc(),
                    ).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationSPLSImpfeat(self,analysis_id_I):
        '''Query rows that are used by the analysis_id
        INPUT:
        analysis_id_I = string
        OUTPUT:
        rows_O = listDict'''
        try:
            data = self.session.query(data_stage02_quantification_spls_impfeat).filter(
                    data_stage02_quantification_spls_impfeat.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_spls_impfeat.used_.is_(True)).order_by(
                    data_stage02_quantification_spls_impfeat.pipeline_id.asc(),
                    data_stage02_quantification_spls_impfeat.test_size.asc(),
                    data_stage02_quantification_spls_impfeat.component_group_name.asc(),
                    data_stage02_quantification_spls_impfeat.component_name.asc(),
                    data_stage02_quantification_spls_impfeat.calculated_concentration_units.asc(),
                    data_stage02_quantification_spls_impfeat.impfeat_method.asc(),
                    ).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationSPLSHyperparameter(self,analysis_id_I):
        '''Query rows that are used by the analysis_id
        INPUT:
        analysis_id_I = string
        OUTPUT:
        rows_O = listDict'''
        try:
            data = self.session.query(data_stage02_quantification_spls_hyperparameter).filter(
                    data_stage02_quantification_spls_hyperparameter.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_spls_hyperparameter.used_.is_(True)).order_by(
                    data_stage02_quantification_spls_hyperparameter.pipeline_id.asc(),
                    data_stage02_quantification_spls_hyperparameter.test_size.asc(),
                    data_stage02_quantification_spls_hyperparameter.calculated_concentration_units.asc(),
                    data_stage02_quantification_spls_hyperparameter.hyperparameter_id.asc(),
                    data_stage02_quantification_spls_hyperparameter.hyperparameter_method.asc(),
                    data_stage02_quantification_spls_hyperparameter.metric_method.asc(),
                    data_stage02_quantification_spls_hyperparameter.crossval_method.asc(),
                    ).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowAxisDict_analysisID_dataStage02QuantificationSPLSScores(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query scores
            data_scores = self.session.query(data_stage02_quantification_spls_scores).filter(
                    data_stage02_quantification_spls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_spls_scores.axis<=axis_I,
                    data_stage02_quantification_spls_scores.used_.is_(True)).all();
            data_scores_O = {};
            for d in data_scores: 
                if not d.axis in data_scores_O.keys():
                    data_scores_O[d.axis]=[];
                data_scores_O[d.axis].append(d.__repr__dict__());
            return data_scores_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowAxisDict_analysisID_dataStage02QuantificationSPLSLoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_spls_loadings).filter(
                    data_stage02_quantification_spls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_spls_loadings.axis<=axis_I,
                    data_stage02_quantification_spls_loadings.used_.is_(True)).all();
            data_loadings_O = {};
            for d in data_loadings: 
                if not d.axis in data_loadings_O.keys():
                    data_loadings_O[d.axis]=[];
                data_loadings_O[d.axis].append(d.__repr__dict__());
            return data_loadings_O;
        except SQLAlchemyError as e:
            print(e);

    def _get_rows_analysisID_dataStage02QuantificationSPLSLoadings(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_spls_loadings
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_spls_loadings'];
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
            {"table_name":tables[0],
            'column_name':'axis',
            'value':5,
            'operator':'<',
            'connector':'AND'
                },
	    ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'pipeline_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'test_size',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'calculated_concentration_units',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_group_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'axis',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'metric_method',
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
    def _get_rows_analysisID_dataStage02QuantificationSPLSScores(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_spls_scores
        INPUT:
        analysis_id_I = string
        query_I = {}, query block changes or additions
        output_O = string
        dictColumn_I = string
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_spls_scores'];
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
            {"table_name":tables[0],
            'column_name':'axis',
            'value':5,
            'operator':'<',
            'connector':'AND'
                },
	    ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'pipeline_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'test_size',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'calculated_concentration_units',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'response_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_short',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'axis',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'metric_method',
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
    def get_SPlot_analysisID_dataStage02QuantificationSPLSLoadings(self,analysis_id_I,axis_I=3):
        '''
        Custom query to stack loadings and correlations as seperate rows
        INPUT:
        analysis_id_I
        axis_I
        OUTPUT:
        data_O
        '''
        try:
            cmd = '''SELECT data_stage02_quantification_spls_loadings.analysis_id, 
            data_stage02_quantification_spls_loadings.pipeline_id, 
            data_stage02_quantification_spls_loadings.test_size, 
            data_stage02_quantification_spls_loadings.calculated_concentration_units, 
            data_stage02_quantification_spls_loadings.component_group_name, 
            data_stage02_quantification_spls_loadings.component_name, 
            data_stage02_quantification_spls_loadings.axis, 
            max(CASE WHEN metric_method = 'loadings' THEN metric_value END) AS loadings, 
            max(CASE WHEN metric_method = 'correlations' THEN metric_value END) AS correlations 
            FROM data_stage02_quantification_spls_loadings 
            WHERE "data_stage02_quantification_spls_loadings".analysis_id LIKE '%s' 
            AND "data_stage02_quantification_spls_loadings".used_ IS true 
            AND "data_stage02_quantification_spls_loadings".axis <= %s 
            GROUP BY "data_stage02_quantification_spls_loadings".analysis_id, 
            "data_stage02_quantification_spls_loadings".pipeline_id, 
            "data_stage02_quantification_spls_loadings".test_size, 
            "data_stage02_quantification_spls_loadings".calculated_concentration_units, 
            "data_stage02_quantification_spls_loadings".component_group_name, 
            "data_stage02_quantification_spls_loadings".component_name, 
            "data_stage02_quantification_spls_loadings".axis 
            ORDER BY "data_stage02_quantification_spls_loadings".pipeline_id ASC, 
            "data_stage02_quantification_spls_loadings".test_size ASC, 
            "data_stage02_quantification_spls_loadings".calculated_concentration_units ASC, 
            "data_stage02_quantification_spls_loadings".component_group_name ASC, 
            "data_stage02_quantification_spls_loadings".component_name ASC, 
            "data_stage02_quantification_spls_loadings".axis ASC'''%(analysis_id_I,axis_I);
            
            result = self.session.execute(cmd);
            data = result.fetchall();
            data_O = [dict(d) for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    def get_SPlot_analysisID_dataStage02QuantificationSPLSScores(self,analysis_id_I,axis_I=3):
        '''
        Custom query to stack scores and Yscores as seperate columns
        INPUT:
        analysis_id_I
        axis_I
        OUTPUT:
        data_O
        '''
        try:
            cmd = '''SELECT data_stage02_quantification_spls_scores.analysis_id, 
            data_stage02_quantification_spls_scores.pipeline_id, 
            data_stage02_quantification_spls_scores.test_size, 
            data_stage02_quantification_spls_scores.calculated_concentration_units, 
            data_stage02_quantification_spls_scores.response_name, 
            data_stage02_quantification_spls_scores.sample_name_short, 
            data_stage02_quantification_spls_scores.axis, 
            max(CASE WHEN metric_method = 'scores' THEN metric_value END) AS score, 
            max(CASE WHEN metric_method = 'Yscores' THEN metric_value END) AS yscore 
            FROM data_stage02_quantification_spls_scores 
            WHERE "data_stage02_quantification_spls_scores".analysis_id LIKE '%s' 
            AND "data_stage02_quantification_spls_scores".used_ IS true 
            AND "data_stage02_quantification_spls_scores".axis <= %s 
            GROUP BY "data_stage02_quantification_spls_scores".analysis_id, 
            "data_stage02_quantification_spls_scores".pipeline_id, 
            "data_stage02_quantification_spls_scores".test_size, 
            "data_stage02_quantification_spls_scores".calculated_concentration_units, 
            "data_stage02_quantification_spls_scores".response_name, 
            "data_stage02_quantification_spls_scores".sample_name_short, 
            "data_stage02_quantification_spls_scores".axis 
            ORDER BY "data_stage02_quantification_spls_scores".pipeline_id ASC, 
            "data_stage02_quantification_spls_scores".test_size ASC, 
            "data_stage02_quantification_spls_scores".calculated_concentration_units ASC, 
            "data_stage02_quantification_spls_scores".response_name ASC, 
            "data_stage02_quantification_spls_scores".sample_name_short ASC, 
            "data_stage02_quantification_spls_scores".axis ASC'''%(analysis_id_I,axis_I);
            
            result = self.session.execute(cmd);
            data = result.fetchall();
            data_O = [dict(d) for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);


