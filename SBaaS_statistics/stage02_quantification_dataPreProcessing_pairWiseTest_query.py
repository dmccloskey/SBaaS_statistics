#SBaaS
from .stage02_quantification_analysis_postgresql_models import *
from .stage02_quantification_dataPreProcessing_pairWiseTest_postgresql_models import *
#Resources
from math import log

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_dataPreProcessing_pairWiseTest_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_dataPreProcessing_pairWiseTest':data_stage02_quantification_dataPreProcessing_pairWiseTest,
                            'data_stage02_quantification_dataPreProcessing_pairWiseTest_im':data_stage02_quantification_dataPreProcessing_pairWiseTest_im,
                            'data_stage02_quantification_dataPreProcessing_pairWiseTest_mv':data_stage02_quantification_dataPreProcessing_pairWiseTest_mv,
                        };
        self.set_supportedTables(tables_supported);
    def get_rows_analysisID_dataStage02QuantificationDataPreProcessingPairWiseTest(self, analysis_id_I):
        """get data from analysis ID"""
        try:
            data = self.session.query(data_stage02_quantification_dataPreProcessing_pairWiseTest).filter(
                    data_stage02_quantification_dataPreProcessing_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_dataPreProcessing_pairWiseTest.used_.is_(True)).order_by(
                    data_stage02_quantification_dataPreProcessing_pairWiseTest.analysis_id.asc(),
                    data_stage02_quantification_dataPreProcessing_pairWiseTest.calculated_concentration_units.asc(),
                    data_stage02_quantification_dataPreProcessing_pairWiseTest.sample_name_abbreviation_1.asc(),
                    data_stage02_quantification_dataPreProcessing_pairWiseTest.sample_name_abbreviation_2.asc(),
                    data_stage02_quantification_dataPreProcessing_pairWiseTest.component_group_name.asc()).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['sample_name_abbreviation_1'] = d.sample_name_abbreviation_1;
                data_1['sample_name_abbreviation_2'] = d.sample_name_abbreviation_2;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['test_stat'] = d.test_stat;
                data_1['test_description'] = d.test_description;
                try:
                    data_1['pvalue_negLog10'] = -log(d.pvalue,10);
                except ValueError as e:
                    print(e);
                    print('substituting 0 pvalue for 1e-12');
                    data_1['pvalue_negLog10'] = -log(1e-12,10);
                try:
                    data_1['pvalue_corrected_negLog10'] = -log(d.pvalue_corrected,10);
                except ValueError as e:
                    print(e);
                    print('substituting 0 pvalue for 1e-12');
                    data_1['pvalue_negLog10'] = -log(1e-12,10);
                data_1['pvalue_corrected_description'] = d.pvalue_corrected_description;
                data_1['mean'] = d.mean;
                data_1['ci_lb'] = d.ci_lb;
                data_1['ci_ub'] = d.ci_ub;
                data_1['ci_level'] = d.ci_level;
                try:
                    data_1['fold_change_log2'] = log(d.fold_change,2);
                except ValueError as e:
                    print(e);
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_1['used_'] = d.used_;
                data_1['comment_'] = d.comment_;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def reset_stage02_quantification_dataPreProcessing_pairWiseTest(self,
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

    def get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingPairWiseTest(
        self,analysis_id_I,
        calculated_concentration_units_I=[],
        component_names_I=[],
        component_group_names_I=[],
        sample_name_abbreviations_1_I=[],
        sample_name_abbreviations_2_I=[],
        time_points_I=[],
        experiment_ids_I=[],
        test_descriptions_I=[],
        pvalue_corrected_descriptions_I=[],
        where_clause_I=None,
        ):
        '''Query rows from data_stage02_quantification_dataPreProcessing_pairWiseTest
        INPUT:
        analysis_id_I = string
        ... = list or comma seperate string
        where_clause_I = formatted clause to add at the end
        OUTPUT:
        rows_O = listDict
        '''
        try:
            cmd = '''SELECT "data_stage02_quantification_dataPreProcessing_pairWiseTest"."id", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."analysis_id", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."sample_name_abbreviation_1", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."sample_name_abbreviation_2", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."component_group_name", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."component_name", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."test_stat", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."test_description", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."pvalue", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."pvalue_corrected", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."pvalue_corrected_description", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."mean", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."ci_lb", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."ci_ub", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."ci_level", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."fold_change", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."calculated_concentration_units", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."used_", 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."comment_" ''';
            cmd+= 'FROM "data_stage02_quantification_dataPreProcessing_pairWiseTest" ';
            analysis_ids = self.convert_list2string(analysis_id_I);
            cmd+= '''WHERE "data_stage02_quantification_dataPreProcessing_pairWiseTest".analysis_id =ANY 
                ('{%s}'::character varying[]) '''%(analysis_ids);
            cmd+= '''AND "data_stage02_quantification_dataPreProcessing_pairWiseTest".used_ ''';
            if calculated_concentration_units_I:
                cmd_q = "AND calculated_concentration_units =ANY ('{%s}'::text[]) " %(self.convert_list2string(calculated_concentration_units_I));
                cmd+=cmd_q;
            if sample_name_abbreviations_1_I:
                cmd_q = "AND sample_name_abbreviation_1 =ANY ('{%s}'::text[]) " %(self.convert_list2string(component_names_I));
                cmd+=cmd_q;
            if sample_name_abbreviations_2_I:
                cmd_q = "AND sample_name_abbreviation_2 =ANY ('{%s}'::text[]) " %(self.convert_list2string(component_names_I));
                cmd+=cmd_q;
            if component_names_I:
                cmd_q = "AND component_name =ANY ('{%s}'::text[]) " %(self.convert_list2string(component_names_I));
                cmd+=cmd_q;
            if component_group_names_I:
                cmd_q = "AND component_group_name =ANY ('{%s}'::text[]) " %(self.convert_list2string(component_group_names_I));
                cmd+=cmd_q;
            if test_descriptions_I:
                cmd_q = "AND test_description =ANY ('{%s}'::text[]) " %(self.convert_list2string(test_descriptions_I));
                cmd+=cmd_q;
            if pvalue_corrected_descriptions_I:
                cmd_q = "AND pvalue_corrected_descriptions =ANY ('{%s}'::text[]) " %(self.convert_list2string(pvalue_corrected_descriptions_I));
                cmd+=cmd_q;
            if where_clause_I:
                cmd += "AND %s " %(where_clause_I);
            cmd+= '''ORDER BY "data_stage02_quantification_dataPreProcessing_pairWiseTest"."analysis_id" ASC, 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."calculated_concentration_units" ASC, 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."sample_name_abbreviation_1" ASC, 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."sample_name_abbreviation_2" ASC, 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."component_group_name" ASC, 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."component_name" ASC,
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."test_description" ASC, 
                "data_stage02_quantification_dataPreProcessing_pairWiseTest"."pvalue_corrected_description" ASC ''';
            result = self.session.execute(cmd);
            data = result.fetchall();
            data_O = [dict(d) for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);

