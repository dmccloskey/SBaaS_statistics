#SBaaS_base
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete
#SBaaS_template
from SBaaS_base.sbaas_template_query import sbaas_template_query
#postgresql_models
from .stage02_quantification_enrichment_postgresql_models import *
#resources
from listDict.listDict import listDict

class stage02_quantification_enrichment_query(sbaas_template_query,
                                       ):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_quantification_enrichment
        '''
        tables_supported = {
            'data_stage02_quantification_enrichment':data_stage02_quantification_enrichment,
            'data_stage02_quantification_enrichmentClasses':data_stage02_quantification_enrichmentClasses,
            'data_stage02_quantification_geneSetEnrichment':data_stage02_quantification_geneSetEnrichment,
                        };
        self.set_supportedTables(tables_supported);

    #Reset rows
    def reset_dataStage02_quantification_enrichment(self,
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

    #Query rows:
    def get_rows_analysisID_dataStage02QuantificationGeneSetEnrichment(self,
                analysis_id_I = [],
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        
        # get the listDict data
        data_O = [];
        tables = ['data_stage02_quantification_geneSetEnrichment'];

        # make the query
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'used_',
            'value':'true',
            'operator':'IS',
            'connector':'AND'
                },
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            'operator':'LIKE',
            'connector':'AND'
                },
	    ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'"GO_term"',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'enrichment_method',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'test_description',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_abbreviation',
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

    def get_rows_componentNames_dataStage02QuantificationEnrichmentClasses(self,
                component_names_I = [],
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_enrichmentClasses
        INPUT:
        analysis_id_I = string
        component_names_I = list of component_names,
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''
        # get the listDict data
        data_O = [];
        tables = ['data_stage02_quantification_enrichmentClasses'];

        # make the query
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        component_names_str = ','.join(component_names_I);
        component_names_query = ("('{%s}'::text[])" %(component_names_str))
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'used_',
            'value':'true',
            'operator':'IS',
            'connector':'AND'
                },
            {"table_name":tables[0],
            'column_name':'component_name',
            'value':'true',
            'operator':'=ANY',
            'connector':'AND'
                },
	    ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'enrichment_class',
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

    #Safe calls by other classes
    def get_rows_analysisID_dataStage02QuantificationEnrichmentPipeline(self,analysis_id_I):
        '''Query rows that are used by the analysis_id
        INPUT:
        analysis_id_I = string
        OUTPUT:
        rows_O = listDict'''
        try:
            data = self.session.query(data_stage02_quantification_enrichment_pipeline).filter(
                    data_stage02_quantification_enrichment_pipeline.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_enrichment_pipeline.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationEnrichmentPipeline(self,pipeline_id_I):
        '''Query models, methods, and parameters that are used by the pipeline_id in order
        INPUT:
        pipeline_id_I = string
        OUTPUT:
        models_O = list, pipeline models
        methods_O = list, pipeline methods
        parameters_O = list, pipeline parameters'''
        try:
            data = self.session.query(
                data_stage02_quantification_enrichment_pipeline.pipeline_model,
                data_stage02_quantification_enrichment_pipeline.pipeline_method,
                data_stage02_quantification_enrichment_pipeline.pipeline_parameters).filter(
                data_stage02_quantification_enrichment_pipeline.pipeline_id.like(pipeline_id_I),
                data_stage02_quantification_enrichment_pipeline.used_.is_(True)).order_by(
                data_stage02_quantification_enrichment_pipeline.pipeline_order).all();
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
