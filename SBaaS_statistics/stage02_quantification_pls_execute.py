
from .stage02_quantification_pls_io import stage02_quantification_pls_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict
import copy

class stage02_quantification_pls_execute(stage02_quantification_pls_io):
    #TODO:
    #1. refactor into execute_plsHyperparameter
    #2. refactor into execute_pls
    def execute_plsda(self,
            analysis_id_I,
            concentration_units_I=[],
            r_calc_I=None,
            pls_model_I = 'PLS-DA',
            response_I = None,
            factor_I= "sample_name_abbreviation",
            ncomp = 5,
            Y_add = "NULL",
            scale = "TRUE",
            #validation = "LOO",
            validation = "CV",
            segments = 10,
            method = "cppls",
            stripped = "FALSE",
            lower = 0.5,
            upper = 0.5, 
            trunc_pow = "FALSE", 
            weights = "NULL",
            p_method = "fdr",
            nperm = 999,
            query_object_descStats_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            ):
        '''execute pls using R
        INPUT:
        analysis_id_I
        experiment_ids_I
        concentration_units_I
        r_calc_I
        PLS INPUT:

        '''

        print('execute_plsda...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query,
                        'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        descStats_replicate_keys = ['median','iq_1','iq_3','min','max']
        
        data_scores_O = [];
        data_loadings_O = [];
        data_validation_O = [];
        data_vip_O = [];
        data_coefficients_O = [];
        data_loadings_factors_O = [];
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            #concentration_units = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu in concentration_units:
            print('calculating pls for concentration_units ' + cu);
            data = [];
            # get data:
            #data = quantification_dataPreProcessing_replicates_query.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            if hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates'):
                data = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                data_tmp = [];
                data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
                for d in data_tmp:
                    for i,k in enumerate(descStats_replicate_keys):
                        tmp = copy.copy(d);
                        tmp['calculated_concentration']=tmp[k];
                        tmp['sample_name_short']='%s_%s'%(tmp['sample_name_abbreviation'],i);
                        data.append(tmp);
            elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                data_tmp = [];
                data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
                for d in data_tmp:
                    for i,k in enumerate(descStats_replicate_keys):
                        tmp = copy.copy(d);
                        tmp['calculated_concentration']=tmp[k];
                        tmp['sample_name_short']='%s_%s'%(tmp['sample_name_abbreviation'],i);
            else:
                print('query instance does not have the required method.');
            
            # will need to refactor in the future...
            if type(data)==type(listDict()):
                data.convert_dataFrame2ListDict()
                data = data.get_listDict();
            # call R
            data_scores,data_loadings = [],[];
            #TODO: add option parameters
            #data_scores,data_loadings = r_calc.calculate_plsda_mixomics(data);
            #data_scores,data_loadings = r_calc.calculate_oplsda_ropl(data);
            data_scores,data_loadings,data_perf,data_vip,data_coefficients,data_loadings_factors = r_calc.calculate_mvr(
                data,
                pls_model_I=pls_model_I,
                response_I=response_I,
                factor_I=factor_I,
                ncomp=ncomp,
                Y_add=Y_add,
                scale=scale,
                validation=validation,
                segments=segments,
                method=method,
                stripped=stripped,
                lower=lower,
                upper=upper,
                trunc_pow=trunc_pow,
                weights=weights,
                p_method=p_method,
                nperm=nperm);
            # add data to database
            for d in data_scores[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_scores_O.append(d);
            for d in data_loadings[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_loadings_O.append(d);
            for d in data_perf[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_validation_O.append(d);
            for d in data_vip[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_vip_O.append(d);
            for d in data_coefficients[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_coefficients_O.append(d);
            for d in data_loadings_factors[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_loadings_factors_O.append(d);
        # add data to the database
        self.add_rows_table('data_stage02_quantification_pls_scores',data_scores_O);
        self.add_rows_table('data_stage02_quantification_pls_loadings',data_loadings_O);
        self.add_rows_table('data_stage02_quantification_pls_validation',data_validation_O);
        self.add_rows_table('data_stage02_quantification_pls_vip',data_vip_O);
        self.add_rows_table('data_stage02_quantification_pls_coefficients',data_coefficients_O);
        self.add_rows_table('data_stage02_quantification_pls_loadingsResponse',data_loadings_factors_O);

    def execute_SUSplot(self,analysis_id_1_I,analysis_id_2_I):
        '''Generate the data for a SUS (shared and unique structures) plot

        INPUT:
        analysis_id_1_I = two-factor pls model (control vs. condition 1)
        analysis_id_2_I = two-factor pls model (control vs. condition 2)
        OUTPUT
        for each component:
            x = correlation of feature i from analysis_id_1
            y = correlation of feature j from analysis_id_2
        '''
        pass;