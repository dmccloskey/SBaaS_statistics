from .stage02_quantification_pairWiseTable_query import stage02_quantification_pairWiseTable_query
from .stage02_quantification_pairWiseTest_io import stage02_quantification_pairWiseTest_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
import numpy as np
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from matplotlib_utilities.matplot import matplot
from listDict.listDict import listDict

class stage02_quantification_pairWiseTest_execute(stage02_quantification_pairWiseTest_io):

    
    def execute_pairwiseTestReplicates(self,analysis_id_I,
            calculated_concentration_units_I=[],
            calculated_concentration_units_FC_I= {},
            test_description_I = "Two Sample t-test",
            ci_level_I = 0.95,
            pvalue_corrected_description_I = "bonferroni",
            redundancy_I=True,
            component_names_I=[],
            sample_name_abbreviations_I=[],
            r_calc_I=None):
        '''
        execute pairwiseTest using R and scipy

        NOTES:
        pvalue correction is performed on a per component basis
        i.e., n = len(pairwise comparisons per component)

        INPUT:
        analysis_id_I = string
        calculated_concentration_units_I = [] of strings
        calculated_concentration_units_FC_I = {'ccu_ttest':'ccu_fc'}
            specific concentration units to perform the fold-change calculation on
            i.e., fold-change cannot be accurately calculated on values that span [-inf,inf]
                (e.g., log-normalized values)
        test_description_I = string, name of the test to perform
        test_options_I = {}, options of the test
            default: 'equal_var' = True, standard independent t-test
                     'equal_var' = False, Welches t-test
        ci_level_I = float, confidence interval level (default = 0.95)
        pvalue_corrected_description_I = string, name of the pvalue adjustment method
        '''

        print('execute_pairwiseTest...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calc = calculate_interface();
        
        #quantification_pairWiseTable_query = stage02_quantification_pairWiseTable_query(self.session,self.engine,self.settings);
        #quantification_pairWiseTable_query.initialize_supportedTables();
        
        quantification_dataPreProcessing_replicates_query=stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        quantification_dataPreProcessing_replicates_query.initialize_supportedTables();

        data_pairwise_O = [];
        
        ## get concentration units
        #if calculated_concentration_units_I:
        #    calculated_concentration_units = calculated_concentration_units_I;
        #else:
        #    calculated_concentration_units = [];
        #    calculated_concentration_units = quantification_pairWiseTable_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I);
        #for cu_cnt,cu in enumerate(calculated_concentration_units):
        #    print('calculating pairwiseTest for concentration_units ' + cu);
        #    # get the component_names
        #    component_names,component_group_names = [],[];
        #    component_names,component_group_names = quantification_pairWiseTable_query.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I,cu);
        #    for cn_cnt, cn in enumerate(component_names):
        #        # get unique experiment_id/time_point/sample_name_short/sample_name_abbreviation/component_name/component_group_name
        #        # get sample_name_abbreviations and sample_name_shorts:
        #        sample_name_abbreviations_1,sample_name_abbreviations_2 = [],[];
        #        sample_name_abbreviations_1,sample_name_abbreviations_2 = quantification_pairWiseTable_query.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationPairWiseTableReplicates(
        #            analysis_id_I,cu,cn)
            
        #        # Pass 1: calculate the pairwise statistics
        #        data_O = [];
        #        for sn_1_cnt,sn_1 in enumerate(sample_name_abbreviations_1):
        #            # get the calculated concentrations in ordered by component name:
        #            data_1,data_2 = [],[];
        #            data_1,data_2 = quantification_pairWiseTable_query.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNameAndSampleNameAbbreviation_dataStage02QuantificationPairWiseTableReplicates(
        #                analysis_id_I,cu,cn,sample_name_abbreviations_1[sn_1_cnt],sample_name_abbreviations_2[sn_1_cnt]);

        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu in calculated_concentration_units:
            #get component_names
            component_names = [];
            component_names = quantification_dataPreProcessing_replicates_query.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,cu);
            if component_names_I:
                component_names = [cn for cn in component_names if cn['component_name'] in component_names_I];
            for cn in component_names:
                #get the sample_name_abbreviations
                sample_name_abbreviations = quantification_dataPreProcessing_replicates_query.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDataPreProcessingReplicates(
                    analysis_id_I,cu,cn['component_name']);
                if sample_name_abbreviations_I:
                    sample_name_abbreviations = [sna for sna in sample_name_abbreviations if sna in sample_name_abbreviations_I];
                for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                    
                    data_O=[];
                    #pass 1: calculate the pairwise statistics
                    if redundancy_I: list_2 = sample_name_abbreviations;
                    else: list_2 = sample_name_abbreviations[sna_1_cnt+1:];
                    for cnt,sna_2 in enumerate(list_2):
                        if redundancy_I: sna_2_cnt = cnt;
                        else: sna_2_cnt = sna_1_cnt+cnt+1;
                        if sna_1 != sna_2:
                            data_1,data_2 = [],[];  
                            data_1 = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNameAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
                                analysis_id_I,cu,cn['component_name'],sna_1
                                );
                            data_2 = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNameAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
                                analysis_id_I,cu,cn['component_name'],sna_2);
                            #calculate the specific test
                            if test_description_I in ["Two Sample t-test","Paired t-test"]:
                                ##split 1: R
                                ##TODO: fix p-value correction and break into individual function calls
                                #data_pairwiseTTest = {};
                                #if len(data_1)==len(data_2):
                                #    data_pairwiseTTest = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="TRUE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                                #else:
                                #    data_pairwiseTTest = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="FALSE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                                #split 2: scipy
                                if len(data_1)==len(data_2):
                                    tstat,pval = calc.calculate_pairwiseTTest(data_1, data_2);
                                else:
                                    tstat,pval = calc.calculate_twoSampleTTest(data_1, data_2, equal_var_I = True);
                            elif test_description_I in ["Welch's t-test"]:
                                tstat,pval = calc.calculate_twoSampleTTest(data_1, data_2, equal_var_I = False);
                            #elif test_description_I == "Wilcoxon-Mann-Whitney test":
                            #    #split 1: R
                            #    #TODO: fix p-value correction and break into individual function calls
                            #    data_pairwiseTTest = {};
                            #    if len(data_1)==len(data_2):
                            #        data_pairwiseTTest = r_calc.calculate_twoSampleWilcoxonRankSumTest(data_1, data_2,
                            #                            alternative_I = "two.sided",
                            #                            mu_I = 0,
                            #                            paired_I="TRUE",
                            #                            ci_level_I = 0.95, 
                            #                            padjusted_method_I = "bonferroni",
                            #                            exact_I = "NULL",
                            #                            correct_I = "TRUE",
                            #                            );
                            #    else:
                            #        data_pairwiseTTest = r_calc.calculate_twoSampleWilcoxonRankSumTest(data_1, data_2,
                            #                            alternative_I = "two.sided", 
                            #                            mu_I = 0, paired_I="FALSE", 
                            #                            ci_level_I = 0.95, 
                            #                            padjusted_method_I = "bonferroni",
                            #                            exact_I = "NULL",
                            #                            correct_I = "TRUE",
                            #                            );
                    
                            # calculate the difference
                            diff = calc.calculate_difference(data_1,data_2);
                    
                            # calculate the confidence intervals
                            mean,var,lb,ub = calc.calculate_ave_var(diff,confidence_I = ci_level_I);

                            # calculate the fold change
                            if calculated_concentration_units_FC_I:
                                # Query the original concentration values to calculate the fold change
                                data_1,data_2 = [],[];  
                                data_1 = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNameAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
                                    analysis_id_I,calculated_concentration_units_FC_I[cu],cn['component_name'],sna_1
                                    );
                                data_2 = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNameAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingReplicates(
                                    analysis_id_I,calculated_concentration_units_FC_I[cu],cn['component_name'],sna_2);
                            data_1_mean = np.array(data_1).mean();
                            data_2_mean = np.array(data_2).mean();
                            if data_1_mean < 0 or data_2_mean < 0:
                                print('negative mean found in data for component_name ' + cn['component_name']);
                                print('fold change can only be calculated on values in the domain [0,inf)');
                            foldChange = calc.calculate_foldChange(data_1_mean,data_2_mean);
                            if foldChange < 0:
                                print('negative fold_change found for component_name ' + cn['component_name']);
                                print('fold change can only be in the domain [0,inf)');


                            # add data to database
                            tmp = {'analysis_id':analysis_id_I,
                                'sample_name_abbreviation_1':sna_1,
                                'sample_name_abbreviation_2':sna_2,
                                'component_group_name':cn['component_group_name'],
                                'component_name':cn['component_name'],
                                'mean':mean,
                                'test_stat':tstat,
                                'test_description':test_description_I,
                                'pvalue':pval,
                                'ci_lb':lb,
                                'ci_ub':ub,
                                'ci_level':ci_level_I,
                                'fold_change':foldChange,
                                'calculated_calculated_concentration_units':cu,
                                'used_':True,
                                'comment_':None};
                            data_O.append(tmp);

                    if data_O:
                        # Pass 2: calculate the corrected p-values
                        data_listDict = listDict(data_O);
                        data_listDict.convert_listDict2DataFrame();
                        pvalues = data_listDict.dataFrame['pvalue'].get_values();
                        # call R
                        r_calc.clear_workspace();
                        r_calc.make_vectorFromList(pvalues,'pvalues');
                        pvalue_corrected = r_calc.calculate_pValueCorrected('pvalues','pvalues_O',method_I = pvalue_corrected_description_I);
                        # add in the corrected p-values
                        data_listDict.add_column2DataFrame('pvalue_corrected', pvalue_corrected);
                        data_listDict.add_column2DataFrame('pvalue_corrected_description', pvalue_corrected_description_I);
                        data_listDict.convert_dataFrame2ListDict();
                        data_pairwise_O.extend(data_listDict.get_listDict());

        # add data to the DB
        self.add_rows_table('data_stage02_quantification_pairWiseTest',data_pairwise_O);

    def execute_pairwiseTTest(self,analysis_id_I,
            concentration_units_I=[],
            component_names_I=[],
            redundancy_I=True,
            r_calc_I=None):
        '''execute pairwiseTTest using R
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        TODO:
        fix hard-coded values specifying the original concentration units
        '''

        print('execute_pairwiseTTest...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calc = calculate_interface();

        data_pairwise_O = [];
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
            concentration_units_original = [x.split('_glog_normalized')[0] for x in concentration_units];
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
            ## get original concentration units
            #concentration_units_original = [];
            #concentration_units_original = self.get_concentrationUnits_experimentIDAndTimePoint_dataStage01ReplicatesMI(experiment_id_I,tp);
            concentration_units_original = [x.split('_glog_normalized')[0] for x in concentration_units];
        for cu_cnt,cu in enumerate(concentration_units):
            print('calculating pairwiseTTest for concentration_units ' + cu);
            data = [];
            # get component_names:
            component_names, component_group_names = [],[];
            component_names, component_group_names = self.get_componentNames_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I, cu);
            if component_names_I:
                component_names_ind = [i for i,x in enumerate(component_names) if x in component_names_I];
                component_names_cpy = copy.copy(component_names);
                component_group_names = copy.copy(component_group_names);
                component_names = [x for i,x in enumerate(component_names) if i in component_names_ind]
                component_group_names = [x for i,x in enumerate(component_group_names) if i in component_names_ind]
            for cnt_cn,cn in enumerate(component_names):
                #print('calculating pairwiseTTest for component_names ' + cn);
                # get sample_name_abbreviations:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized(analysis_id_I,cu, cn)
                for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                    if redundancy_I: list_2 = sample_name_abbreviations;
                    else: list_2 = sample_name_abbreviations[sna_1_cnt+1:];
                    for cnt,sna_2 in enumerate(list_2):
                        if redundancy_I: sna_2_cnt = cnt;
                        else: sna_2_cnt = sna_1_cnt+cnt+1;
                        if sna_1 != sna_2:
                            #print('calculating pairwiseTTest for sample_name_abbreviations ' + sna_1 + ' vs. ' + sna_2);
                            # get data:
                            all_1,all_2 = [],[];
                            data_1,data_2 = [],[];
                            all_1,data_1 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna_1);
                            all_2,data_2 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna_2);
                            # call R
                            data_pairwiseTTest = {};
                            if len(data_1)==len(data_2):
                                data_pairwiseTTest = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="TRUE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                            else:
                                data_pairwiseTTest = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="FALSE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                            if data_pairwiseTTest is None:
                                continue;
                            # check if the values are normalized
                            if "_normalized" in cu:
                                # Query the original concentration values to calculate the fold change
                                all_1,all_2 = [],[];
                                data_1,data_2 = [],[];  
                                all_1,data_1 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage01ReplicatesMI(analysis_id_I,concentration_units_original[cu_cnt],cn,sna_1);
                                all_2,data_2 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage01ReplicatesMI(analysis_id_I,concentration_units_original[cu_cnt],cn,sna_2);
                            # calculate the fold change
                            foldChange = calc.calculate_foldChange(numpy.array(data_1).mean(),numpy.array(data_2).mean())
                            #foldChange = numpy.array(data_2).mean()/numpy.array(data_1).mean();
                            # add data to database
                            tmp = {'analysis_id':analysis_id_I,
                                'sample_name_abbreviation_1':sna_1,
                                'sample_name_abbreviation_2':sna_2,
                                'component_group_name':component_group_names[cnt_cn],
                                'component_name':cn,
                                'mean':data_pairwiseTTest['mean'],
                                'test_stat':data_pairwiseTTest['test_stat'],
                                'test_description':data_pairwiseTTest['test_description'],
                                'pvalue':data_pairwiseTTest['pvalue'],
                                'pvalue_corrected':data_pairwiseTTest['pvalue_corrected'],
                                'pvalue_corrected_description':data_pairwiseTTest['pvalue_corrected_description'],
                                'ci_lb':data_pairwiseTTest['ci_lb'],
                                'ci_ub':data_pairwiseTTest['ci_ub'],
                                'ci_level':data_pairwiseTTest['ci_level'],
                                'fold_change':foldChange,
                                'calculated_concentration_units':cu,
                                'used_':True,
                                'comment_':None};
                            data_pairwise_O.append(tmp);
        #                    row2 = data_stage02_quantification_pairWiseTest(
        #                            analysis_id_I,
        #                            sna_1,
        #                            sna_2,
        #                            component_group_names[cnt_cn],
        #                            cn,
        #                            data_pairwiseTTest['mean'],
        #                            data_pairwiseTTest['test_stat'],
        #                            data_pairwiseTTest['test_description'],
        #                            data_pairwiseTTest['pvalue'],
        #                            data_pairwiseTTest['pvalue_corrected'],
        #                            data_pairwiseTTest['pvalue_corrected_description'],
        #                            data_pairwiseTTest['ci_lb'],
        #                            data_pairwiseTTest['ci_ub'],
        #                            data_pairwiseTTest['ci_level'],
        #                            foldChange,
        #                            cu,
        #                            True,
        #                            None
        #                            );
        #                    self.session.add(row2);
        #self.session.commit();
        self.add_dataStage02QuantificationPairWiseTest(data_pairwise_O);
    def execute_pairwiseWilcoxonRankSumTest(self,analysis_id_I,
            concentration_units_I=[],
            component_names_I=[],
            redundancy_I=True,
            r_calc_I=None):
        '''execute pairwiseTTest using R
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        TODO:
        fix hard-coded values specifying the original concentration units
        '''

        print('execute_pairwiseTTest...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calc = calculate_interface();

        data_pairwise_O=[];
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
            concentration_units_original = [x.split('_glog_normalized')[0] for x in concentration_units];
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
            ## get original concentration units
            #concentration_units_original = [];
            #concentration_units_original = self.get_concentrationUnits_experimentIDAndTimePoint_dataStage01ReplicatesMI(experiment_id_I,tp);
            concentration_units_original = [x.split('_glog_normalized')[0] for x in concentration_units];
        for cu_cnt,cu in enumerate(concentration_units):
            print('calculating pairwiseTTest for concentration_units ' + cu);
            data = [];
            # get component_names:
            component_names, component_group_names = [],[];
            component_names, component_group_names = self.get_componentNames_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I, cu);
            if component_names_I:
                component_names_ind = [i for i,x in enumerate(component_names) if x in component_names_I];
                component_names_cpy = copy.copy(component_names);
                component_group_names = copy.copy(component_group_names);
                component_names = [x for i,x in enumerate(component_names) if i in component_names_ind]
                component_group_names = [x for i,x in enumerate(component_group_names) if i in component_names_ind]
            for cnt_cn,cn in enumerate(component_names):
                print('calculating pairwiseTTest for component_names ' + cn);
                # get sample_name_abbreviations:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized(analysis_id_I,cu, cn)
                for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                    if redundancy_I: list_2 = sample_name_abbreviations;
                    else: list_2 = sample_name_abbreviations[sna_1_cnt+1:];
                    for cnt,sna_2 in enumerate(list_2):
                        if redundancy_I: sna_2_cnt = cnt;
                        else: sna_2_cnt = sna_1_cnt+cnt+1;
                        if sna_1 != sna_2:
                            print('calculating pairwiseTTest for sample_name_abbreviations ' + sna_1 + ' vs. ' + sna_2);
                            # get data:
                            all_1,all_2 = [],[];
                            data_1,data_2 = [],[];
                            all_1,data_1 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna_1);
                            all_2,data_2 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna_2);
                            # call R
                            data_pairwiseTTest = {};
                            if len(data_1)==len(data_2):
                                data_pairwiseTTest = r_calc.calculate_twoSampleWilcoxonRankSumTest(data_1, data_2,
                                                    alternative_I = "two.sided",
                                                    mu_I = 0,
                                                    paired_I="TRUE",
                                                    ci_level_I = 0.95, 
                                                    padjusted_method_I = "bonferroni",
                                                    exact_I = "NULL",
                                                    correct_I = "TRUE",
                                                    );
                            else:
                                data_pairwiseTTest = r_calc.calculate_twoSampleWilcoxonRankSumTest(data_1, data_2,
                                                    alternative_I = "two.sided", 
                                                    mu_I = 0, paired_I="FALSE", 
                                                    ci_level_I = 0.95, 
                                                    padjusted_method_I = "bonferroni",
                                                    exact_I = "NULL",
                                                    correct_I = "TRUE",
                                                    );
                            # check if data was calculated
                            if data_pairwiseTTest is None:
                                continue;
                            # check if the values are normalized
                            if "_normalized" in cu:
                                # Query the original concentration values to calculate the fold change
                                all_1,all_2 = [],[];
                                data_1,data_2 = [],[];  
                                all_1,data_1 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage01ReplicatesMI(analysis_id_I,concentration_units_original[cu_cnt],cn,sna_1);
                                all_2,data_2 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage01ReplicatesMI(analysis_id_I,concentration_units_original[cu_cnt],cn,sna_2);
                            # calculate the fold change
                            foldChange = calc.calculate_foldChange(numpy.array(data_1).mean(),numpy.array(data_2).mean())
                            #foldChange = numpy.array(data_2).mean()/numpy.array(data_1).mean();
                            # add data to database
                            tmp = {'analysis_id':analysis_id_I,
                                'sample_name_abbreviation_1':sna_1,
                                'sample_name_abbreviation_2':sna_2,
                                'component_group_name':component_group_names[cnt_cn],
                                'component_name':cn,
                                'mean':data_pairwiseTTest['mean'],
                                'test_stat':data_pairwiseTTest['test_stat'],
                                'test_description':data_pairwiseTTest['test_description'],
                                'pvalue':data_pairwiseTTest['pvalue'],
                                'pvalue_corrected':data_pairwiseTTest['pvalue_corrected'],
                                'pvalue_corrected_description':data_pairwiseTTest['pvalue_corrected_description'],
                                'ci_lb':data_pairwiseTTest['ci_lb'],
                                'ci_ub':data_pairwiseTTest['ci_ub'],
                                'ci_level':data_pairwiseTTest['ci_level'],
                                'fold_change':foldChange,
                                'calculated_concentration_units':cu,
                                'used_':True,
                                'comment_':None};
                            data_pairwise_O.append(tmp);
        self.add_dataStage02QuantificationPairWiseTest(data_pairwise_O);
    def execute_volcanoPlot(self,analysis_id_I,concentration_units_I=[]):
        '''generate a volcano plot from pairwiseTest table'''

        print('execute_volcanoPlot...')
        mplot = matplot();
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02pairWiseTest(analysis_id_I);
        for cu in concentration_units:
            print('generating a volcano plot for concentration_units ' + cu);
            data = [];
            # get sample_name_abbreviations:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.get_sampleNameAbbreviations_analysisIDAndUnits_dataStage02pairWiseTest(analysis_id_I, cu)
            for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                for sna_2_cnt,sna_2 in enumerate(sample_name_abbreviations[sna_1_cnt:]):
                    if sna_1 != sna_2:
                        print('generating a volcano plot for sample_name_abbreviation ' + sna_1 + ' vs. ' + sna_2);
                        # get data:
                        data_1 = [];
                        data_1 = self.get_RDataList_analysisIDAndUnitsAndSampleNameAbbreviations_dataStage02pairWiseTest(analysis_id_I,cu,sna_1,sna_2);
                        # plot the data
                        title = sna_1 + ' vs. ' + sna_2;
                        xlabel = 'Fold Change [log2(FC)]';
                        ylabel = 'Probability [-log10(P)]';
                        x_data = [d['fold_change_log2'] for d in data_1];
                        y_data = [d['pvalue_corrected_negLog10'] for d in data_1];
                        text_labels = [t['component_group_name'] for t in data_1];
                        mplot.volcanoPlot(title,xlabel,ylabel,x_data,y_data,text_labels);
    def execute_pairwiseTTest_v1(self,experiment_id_I):
        '''execute pairwiseTTest using R'''

        print('execute_pairwiseTTest...')
        r_calc = r_interface();
        calc = calculate_interface();

        # query metabolomics data from glogNormalization
        # get time points
        time_points = [];
        time_points = self.get_timePoint_experimentID_dataStage02GlogNormalized(experiment_id_I);
        for tp in time_points:
            print('calculating pairwiseTTest for time_point ' + tp);
            data_transformed = [];
            # get concentration units...
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_experimentIDAndTimePoint_dataStage02GlogNormalized(experiment_id_I,tp);
            ## get original concentration units
            #concentration_units_original = [];
            #concentration_units_original = self.get_concentrationUnits_experimentIDAndTimePoint_dataStage01ReplicatesMI(experiment_id_I,tp);
            concentration_units_original = [x.split('_glog_normalized')[0] for x in concentration_units];
            for cu_cnt, cu in enumerate(concentration_units):
                print('calculating pairwiseTTest for concentration_units ' + cu);
                # get component_names:
                component_names, component_group_names = [],[];
                component_names, component_group_names = self.get_componentNames_experimentIDAndTimePointAndUnits_dataStage02GlogNormalized(experiment_id_I, tp, cu);
                for cnt_cn,cn in enumerate(component_names):
                    print('calculating pairwiseTTest for component_names ' + cn);
                    # get sample_name_abbreviations:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(experiment_id_I, tp, cu, cn)
                    for sna_1 in sample_name_abbreviations:
                        for sna_2 in sample_name_abbreviations:
                            print('calculating pairwiseTTest for sample_name_abbreviations ' + sna_1 + ' vs. ' + sna_2);
                            if sna_1 != sna_2:
                            # get data:
                                all_1,all_2 = [],[];
                                data_1,data_2 = [],[];
                                all_1,data_1 = self.get_RDataList_experimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(experiment_id_I,tp,cu,cn,sna_1);
                                all_2,data_2 = self.get_RDataList_experimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(experiment_id_I,tp,cu,cn,sna_2);
                                # call R
                                data_pairwiseTTest = {};
                                if len(data_1)==len(data_2):
                                    data_pairwiseTTest = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="TRUE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                                else:
                                    data_pairwiseTTest = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="FALSE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                                # Query the original concentration values to calculate the fold change
                                all_1,all_2 = [],[];
                                data_1,data_2 = [],[];  
                                all_1,data_1 = self.get_RDataList_experimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage01ReplicatesMI(experiment_id_I,tp,concentration_units_original[cu_cnt],cn,sna_1);
                                all_2,data_2 = self.get_RDataList_experimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage01ReplicatesMI(experiment_id_I,tp,concentration_units_original[cu_cnt],cn,sna_2);
                                # calculate the fold change
                                foldChange = calc.calculate_foldChange(data_1,data_2)
                                #foldChange = numpy.array(data_2).mean()/numpy.array(data_1).mean();
                                # add data to database
                                row2 = data_stage02_quantification_pairWiseTest(experiment_id_I,
                                        sna_1,sna_2,tp,tp,component_group_names[cnt_cn],cn,
                                        data_pairwiseTTest['mean'],
                                        data_pairwiseTTest['test_stat'],
                                        data_pairwiseTTest['test_description'],
                                        data_pairwiseTTest['pvalue'],
                                        data_pairwiseTTest['pvalue_corrected'],
                                        data_pairwiseTTest['pvalue_corrected_description'],
                                        data_pairwiseTTest['ci_lb'],
                                        data_pairwiseTTest['ci_ub'],
                                        data_pairwiseTTest['ci_level'],
                                        foldChange,
                                        cu,True,None);
                                self.session.add(row2);
        self.session.commit();
    def execute_volcanoPlot_v1(self,experiment_id_I):
        '''generate a volcano plot from pairwiseTest table'''

        print('execute_volcanoPlot...')
        mplot = matplot();
        # get time points
        time_points = [];
        time_points = self.get_timePoint_experimentID_dataStage02pairWiseTest(experiment_id_I);
        for tp in time_points:
            print('generating a volcano plot for time_point ' + tp);
            data_transformed = [];
            # get concentration units...
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_experimentIDAndTimePoint_dataStage02pairWiseTest(experiment_id_I,tp);
            #concentration_units = ['mM_glog_normalized']
            for cu in concentration_units:
                print('generating a volcano plot for concentration_units ' + cu);
                # get sample_name_abbreviations:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentIDAndTimePointAndUnits_dataStage02pairWiseTest(experiment_id_I, tp, cu)
                for sna_1 in sample_name_abbreviations:
                    for sna_2 in sample_name_abbreviations:
                        if sna_1 != sna_2:
                            print('generating a volcano plot for sample_name_abbreviation ' + sna_1 + ' vs. ' + sna_2);
                            # get data:
                            data_1 = [];
                            data_1 = self.get_RDataList_experimentIDAndTimePointAndUnitsAndSampleNameAbbreviations_dataStage02pairWiseTest(experiment_id_I,tp,cu,sna_1,sna_2);
                            # plot the data
                            title = sna_1 + ' vs. ' + sna_2;
                            xlabel = 'Fold Change [log2(FC)]';
                            ylabel = 'Probability [-log10(P)]';
                            x_data = [d['fold_change_log2'] for d in data_1];
                            y_data = [d['pvalue_corrected_negLog10'] for d in data_1];
                            text_labels = [t['component_group_name'] for t in data_1];
                            mplot.volcanoPlot(title,xlabel,ylabel,x_data,y_data,text_labels);