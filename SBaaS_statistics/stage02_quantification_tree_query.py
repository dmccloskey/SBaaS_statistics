#SBaaS_base
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete
#SBaaS_template
from SBaaS_base.sbaas_template_query import sbaas_template_query
#postgresql_models
from .stage02_quantification_tree_postgresql_models import *
#resources
from listDict.listDict import listDict

class stage02_quantification_tree_query(sbaas_template_query,
                                       ):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_quantification_tree
        '''
        tables_supported = {
            #'data_stage02_quantification_tree_impfeat':data_stage02_quantification_tree_impfeat,
            #'data_stage02_quantification_tree_responseClassification':data_stage02_quantification_tree_responseClassification,
            'data_stage02_quantification_tree_pipeline':data_stage02_quantification_tree_pipeline,
            #'data_stage02_quantification_tree_hyperparameter':data_stage02_quantification_tree_hyperparameter,
            #'data_stage02_quantification_tree_validation':data_stage02_quantification_tree_validation,
                        };
        self.set_supportedTables(tables_supported);

    #Query rows
    def get_rows_dataStage02QuantificationTree(self,
                tables_I,
                query_I,
                output_O,
                dictColumn_I=None):
        """get rows by analysis ID from data_stage02_quantification_tree"""
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
    def add_dataStage02QuantificationTree(self,table_I,data_I):
        '''add rows of data_stage02_quantification_tree'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryinsert = sbaas_base_query_insert(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryinsert.add_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);
    def update_dataStage02QuantificationTree(self,table_I,data_I):
        '''update rows of data_stage02_quantification_tree'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryupdate = sbaas_base_query_update(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryupdate.update_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);

    def initialize_dataStage02_quantification_tree(self,
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
    def drop_dataStage02_quantification_tree(self,
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
    def reset_dataStage02_quantification_tree(self,
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
    def get_rows_analysisID_dataStage02QuantificationTreePipeline(self,analysis_id_I):
        '''Query rows that are used by the analysis_id'''
        try:
            data = self.session.query(data_stage02_quantification_tree_pipeline).filter(
                    data_stage02_quantification_tree_pipeline.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_tree_pipeline.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationTreePipeline(self,pipeline_id_I):
        '''Query rows that are used by the pipeline_id in order'''
        try:
            data = self.session.query(
                data_stage02_quantification_tree_pipeline.pipeline_model,
                data_stage02_quantification_tree_pipeline.pipeline_method,
                data_stage02_quantification_tree_pipeline.pipeline_parameters).filter(
                data_stage02_quantification_tree_pipeline.pipeline_id.like(pipeline_id_I),
                data_stage02_quantification_tree_pipeline.used_.is_(True)).order_by(
                data_stage02_quantification_tree_pipeline.pipeline_order).all();
            models_O,methods_O,parameters_O = [],[],[];
            if data: 
                data_i = listDict(record_I=data);
                data_i.convert_record2DataFrame();
                models_O=data_i.dataFame['pipeline_model'].get_values();
                methods_O=data_i.dataFame['pipeline_method'].get_values();
                parameters_O=data_i.dataFame['pipeline_parameters'].get_values();
            return models_O,methods_O,parameters_O;
        except SQLAlchemyError as e:
            print(e);
