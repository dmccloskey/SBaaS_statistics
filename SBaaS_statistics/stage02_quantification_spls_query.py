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
