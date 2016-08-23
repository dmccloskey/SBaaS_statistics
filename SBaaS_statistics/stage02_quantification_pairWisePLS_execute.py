
from .stage02_quantification_pairWisePLS_io import stage02_quantification_pairWisePLS_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict
import copy

class stage02_quantification_pairWisePLS_execute(stage02_quantification_pairWisePLS_io,):
    #TODO:
    #1. refactor into execute_plsHyperparameter
    #2. refactor into execute_pls
    def execute_pairWise_plsda(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            sample_name_abbreviation_control_I=None,
            calculated_concentration_units_I=[],
            component_names_I=[],
                    redundancy_I=False,
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
        '''execute a pairwise pls using R
        INPUT:
        analysis_id_I
        concentration_units_I
        r_calc_I
        PLS INPUT:

        '''

        print('execute_plsda...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        
        data_scores_O = [];
        data_loadings_O = [];
        data_validation_O = [];
        data_vip_O = [];
        data_coefficients_O = [];
        data_loadings_factors_O = [];

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
        data_pairwise_O = [];
        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            #concentration_units = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwisePls for concentration_units ' + cu);
            # get sample_name_abbreviations:
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations=[];
                #sample_name_abbreviations=quantification_dataPreProcessing_replicates_query.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                #    analysis_id_I,cu);
                if hasattr(query_instance_descStats, 'get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates'):
                    sample_name_abbreviations = query_instance_descStats.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
                elif hasattr(query_instance_descStats, 'get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                    sample_name_abbreviations = query_instance_descStats.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
                elif hasattr(query_instance_descStats, 'get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                    sample_name_abbreviations = query_instance_descStats.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
                else:
                    print('query instance does not have the required method.');
            #if sample_name_abbreviation_control_I:
            #    sample_name_abbreviations_1 = [sna for sna in [sample_name_abbreviation_control_I]];
            #    if len(sample_name_abbreviations_1)<1:
            #        print(sample_name_abbreviation_control_I + ' not found.');
            #        return;
            #    sample_name_abbreviations_2 = [sna for sna in sample_name_abbreviations if sna != sample_name_abbreviation_control_I];
            #else:
            #    sample_name_abbreviations_1 = sample_name_abbreviations;
            #    sample_name_abbreviations_2 = sample_name_abbreviations;

            for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):

                if redundancy_I: list_2 = sample_name_abbreviations;
                else: list_2 = sample_name_abbreviations[sna_1_cnt+1:];
                for cnt,sna_2 in enumerate(list_2):
                    if redundancy_I: sna_2_cnt = cnt;
                    else: sna_2_cnt = sna_1_cnt+cnt+1;
                    print('calculating pairwisePls for sample_name_abbreviations ' + sna_1 + ' vs. ' + sna_2);

                    response_name_pair = [sna_1,sna_2]

                    # get data:
                    data_1,data_2 = [],[];
                    #data_1 = quantification_dataPreProcessing_replicates_query.get_rowsAndSampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
                    #    analysis_id_I,cu,sna_1);
                    #data_2 = quantification_dataPreProcessing_replicates_query.get_rowsAndSampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
                    #    analysis_id_I,cu,sna_2);
                    if hasattr(query_instance_descStats, 'get_rowsAndSampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates'):
                        data_1 = query_instance_descStats.get_rowsAndSampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
                            analysis_id_I,cu,sna_1);
                        data_2 = query_instance_descStats.get_rowsAndSampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
                            analysis_id_I,cu,sna_2);
                        data_1.extend(data_2);
                    elif hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats'):
                        data_1_tmp = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats(
                            analysis_id_I,cu,sna_1);
                        data_2_tmp = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats(
                            analysis_id_I,cu,sna_2);
                        if type(data_1_tmp)==type(listDict()):
                            data_1_tmp.convert_dataFrame2ListDict()
                            data_1_tmp = data_1_tmp.get_listDict();
                        if type(data_2_tmp)==type(listDict()):
                            data_2_tmp.convert_dataFrame2ListDict()
                            data_2_tmp = data_2_tmp.get_listDict();
                        data_1_tmp.extend(data_2_tmp);
                        for d in data_1_tmp:
                            for i,k in enumerate(descStats_replicate_keys):
                                tmp = copy.copy(d);
                                tmp['calculated_concentration']=tmp[k];
                                tmp['sample_name_short']='%s_%s'%(tmp['sample_name_abbreviation'],i);
                                data_1.append(tmp);
                    elif hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages'):
                        data_1_tmp = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(
                            analysis_id_I,cu,sna_1);
                        data_2_tmp = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(
                            analysis_id_I,cu,sna_2);
                        if type(data_1_tmp)==type(listDict()):
                            data_1_tmp.convert_dataFrame2ListDict()
                            data_1_tmp = data_1_tmp.get_listDict();
                        if type(data_2_tmp)==type(listDict()):
                            data_2_tmp.convert_dataFrame2ListDict()
                            data_2_tmp = data_2_tmp.get_listDict();
                        data_1_tmp.extend(data_2_tmp);
                        for d in data_1_tmp:
                            for i,k in enumerate(descStats_replicate_keys):
                                tmp = copy.copy(d);
                                tmp['calculated_concentration']=tmp[k];
                                tmp['sample_name_short']='%s_%s'%(tmp['sample_name_abbreviation'],i);
                                data_1.append(tmp);
                    else:
                        print('query instance does not have the required method.');

                    # call R
                    #TODO: add option parameters
                    data_scores,data_loadings,data_perf,data_vip,data_coefficients,data_loadings_factors = r_calc.calculate_mvr(
                        data_1,
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
                        d['response_name_pair']=response_name_pair;
                        data_scores_O.append(d);
                    for d in data_loadings[:]:
                        d['analysis_id']=analysis_id_I;
                        d['calculated_concentration_units']=cu;
                        d['used_']=True;
                        d['comment_']=None;
                        d['response_name_pair']=response_name_pair;
                        data_loadings_O.append(d);
                    for d in data_perf[:]:
                        d['analysis_id']=analysis_id_I;
                        d['calculated_concentration_units']=cu;
                        d['used_']=True;
                        d['comment_']=None;
                        d['response_name_pair']=response_name_pair;
                        data_validation_O.append(d);
                    for d in data_vip[:]:
                        d['analysis_id']=analysis_id_I;
                        d['calculated_concentration_units']=cu;
                        d['used_']=True;
                        d['comment_']=None;
                        d['response_name_pair']=response_name_pair;
                        data_vip_O.append(d);
                    for d in data_coefficients[:]:
                        d['analysis_id']=analysis_id_I;
                        d['calculated_concentration_units']=cu;
                        d['used_']=True;
                        d['comment_']=None;
                        d['response_name_pair']=response_name_pair;
                        data_coefficients_O.append(d);
                    for d in data_loadings_factors[:]:
                        d['analysis_id']=analysis_id_I;
                        d['calculated_concentration_units']=cu;
                        d['used_']=True;
                        d['comment_']=None;
                        d['response_name_pair']=response_name_pair;
                        data_loadings_factors_O.append(d);
        # add data to the database
        self.add_rows_table('data_stage02_quantification_pairWisePLS_scores',data_scores_O);
        self.add_rows_table('data_stage02_quantification_pairWisePLS_loadings',data_loadings_O);
        self.add_rows_table('data_stage02_quantification_pairWisePLS_validation',data_validation_O);
        self.add_rows_table('data_stage02_quantification_pairWisePLS_vip',data_vip_O);
        self.add_rows_table('data_stage02_quantification_pairWisePLS_coefficients',data_coefficients_O);
        self.add_rows_table('data_stage02_quantification_pairWisePLS_loadingsResponse',data_loadings_factors_O);