
from .stage02_quantification_pairWiseCorrelation_io import stage02_quantification_pairWiseCorrelation_io
from .stage02_quantification_pairWiseTable_query import stage02_quantification_pairWiseTable_query
# resources
from python_statistics.calculate_correlation import calculate_correlation

class stage02_quantification_pairWiseCorrelation_execute(stage02_quantification_pairWiseCorrelation_io,
                                         stage02_quantification_pairWiseTable_query):
    def execute_pairwiseCorrelation(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            concentration_units_I=[],
            component_names_I=[],
            redundancy_I=True,
            distance_measure_I='pearson',
            value_I = 'mean'):
        '''execute pairwiseCorrelation
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        TODO:
        fix hard-coded values specifying the original concentration units
        '''

        print('execute_pairwiseCorrelation...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calc = calculate_interface();

        data_pairwise_O = [];
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu_cnt,cu in enumerate(concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
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
                print('calculating pairwiseCorrelation for component_names ' + cn);
                # get sample_name_abbreviations:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized(analysis_id_I,cu, cn)
                for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                    if redundancy_I: list_2 = sample_name_abbreviations;
                    else: list_2 = sample_name_abbreviations[sna_1+1:];
                    for cnt,sna_2 in enumerate(list_2):
                        if redundancy_I: sna_2_cnt = cnt;
                        else: sna_2_cnt = sna_1_cnt+cnt+1;
                        if sna_1 != sna_2:
                            print('calculating pairwiseCorrelation for sample_name_abbreviations ' + sna_1 + ' vs. ' + sna_2);
                            # get data:
                            all_1,all_2 = [],[];
                            data_1,data_2 = [],[];
                            all_1,data_1 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna_1);
                            all_2,data_2 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna_2);
                            # call R
                            data_pairwiseCorrelation = {};
                            if len(data_1)==len(data_2):
                                data_pairwiseCorrelation = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="TRUE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                            else:
                                data_pairwiseCorrelation = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="FALSE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                            if data_pairwiseCorrelation is None:
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
                                'mean':data_pairwiseCorrelation['mean'],
                                'test_stat':data_pairwiseCorrelation['test_stat'],
                                'test_description':data_pairwiseCorrelation['test_description'],
                                'pvalue':data_pairwiseCorrelation['pvalue'],
                                'pvalue_corrected':data_pairwiseCorrelation['pvalue_corrected'],
                                'pvalue_corrected_description':data_pairwiseCorrelation['pvalue_corrected_description'],
                                'ci_lb':data_pairwiseCorrelation['ci_lb'],
                                'ci_ub':data_pairwiseCorrelation['ci_ub'],
                                'ci_level':data_pairwiseCorrelation['ci_level'],
                                'fold_change':foldChange,
                                'calculated_concentration_units':cu,
                                'used_':True,
                                'comment_':None};
                            data_pairwise_O.append(tmp);
        self.add_dataStage02QuantificationPairWiseTest(data_pairwise_O);
    def execute_pairwiseCorrelationReplicates_fromGLogNormalized(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            sample_name_shorts_I=[],
            concentration_units_I=[],
            component_names_I=[],
            redundancy_I=True,
            distance_measure_I='pearson'):
        '''execute pairwiseCorrelation
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        '''

        print('execute_pairwiseCorrelationReplicates...')

        data_pairwise_O = [];
        calculatecorrelation = calculate_correlation();
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu_cnt,cu in enumerate(concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
            # get sample_name_abbreviations and sample_name_shorts:
            sample_name_abbreviations,sample_name_shorts = [];
            sample_name_abbreviations,sample_name_shorts = self.get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu)
            for sn_1_cnt,sn_1 in enumerate(sample_name_abbreviations):
                if redundancy_I: list_2 = sample_name_abbreviations;
                else: list_2 = sample_name_abbreviations[sn_1+1:];
                for cnt,sn_2 in enumerate(list_2):
                    if redundancy_I: sn_2_cnt = cnt;
                    else: sn_2_cnt = sn_1_cnt+cnt+1;
                    if sn_1 != sn_2:
                        print('calculating pairwiseCorrelation for sample_name_short ' + sn_1 + ' vs. ' + sn_2);
                        # get the calculated concentrations in ordered by component name:
                        data_1,data_2 = [],[];
                        data_1 = self.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02GlogNormalized(analysis_id_I,cu,sn_1);
                        data_2 = self.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02GlogNormalized(analysis_id_I,cu,sn_2);
                        # call R
                        data_pairwiseCorrelation = {};
                        if len(data_1)==len(data_2):
                            #calculate the correlation coefficient
                            if distance_measure_I=='pearson':
                                rho,pval = calculatecorrelation.calculate_correlation_pearsonr(data_1,data_2);
                            elif distance_measure_I=='spearman':
                                rho,pval = calculatecorrelation.calculate_correlation_spearmanr(data_1,data_2);
                            else:
                                print("distance measure not recognized");
                                return;
                        else:
                            print('the number of components in sn_1 and sn_2 are not equal.');
                        if data_pairwiseCorrelation is None:
                            continue;
                        # add data to database
                        tmp = {'analysis_id':analysis_id_I,
                            'sample_name_abbreviation_1':sample_name_abbreviations[sn_1_cnt],
                            'sample_name_abbreviation_2':sample_name_abbreviations[sn_2_cnt],
                            'sample_name_short_1':sn_1,
                            'sample_name_short_2':sn_2,
                            'distance_measure':distance_measure_I,
                            'correlation_coefficient':rho,
                            'pvalue':pval,
                            'pvalue_corrected':None,
                            'pvalue_corrected_description':None,
                            'calculated_concentration_units':cu,
                            'used_':True,
                            'comment_':None};
                        data_pairwise_O.append(tmp);

        #self.session.commit();
        self.add_dataStage02QuantificationPairWiseCorrelation('data_stage02_quantification_pairWiseCorrelation_replicates',data_pairwise_O);
    def execute_pairwiseCorrelationReplicates(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            sample_name_shorts_I=[],
            concentration_units_I=[],
            component_names_I=[],
            distance_measure_I='pearson'):
        '''execute pairwiseCorrelation
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        '''

        print('execute_pairwiseCorrelationReplicates...')

        data_pairwise_O = [];
        calculatecorrelation = calculate_correlation();
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
            # get sample_name_abbreviations and sample_name_shorts:
            sample_name_abbreviations_1,sample_name_shorts_1,sample_name_abbreviations_2,sample_name_shorts_2 = [],[],[],[];
            sample_name_abbreviations_1,sample_name_shorts_1,sample_name_abbreviations_2,sample_name_shorts_2 = self.get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I,cu)
            for sn_1_cnt,sn_1 in enumerate(sample_name_shorts_1):
                print('calculating pairwiseCorrelation for sample_name_short ' + sn_1 + ' vs. ' + sample_name_shorts_2[sn_1_cnt]);
                # get the calculated concentrations in ordered by component name:
                data_1,data_2 = [],[];
                data_1,data_2 = self.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I,cu,sn_1,sample_name_shorts_2[sn_1_cnt]);
                # call R
                if len(data_1)==len(data_2):
                    #calculate the correlation coefficient
                    if distance_measure_I=='pearson':
                        rho,pval = calculatecorrelation.calculate_correlation_pearsonr(data_1,data_2);
                    elif distance_measure_I=='spearman':
                        rho,pval = calculatecorrelation.calculate_correlation_spearmanr(data_1,data_2);
                    else:
                        print("distance measure not recognized");
                        return;
                else:
                    print('the number of components in sn_1 and sn_2 are not equal.');
                # add data to database
                tmp = {'analysis_id':analysis_id_I,
                    'sample_name_abbreviation_1':sample_name_abbreviations_1[sn_1_cnt],
                    'sample_name_abbreviation_2':sample_name_abbreviations_2[sn_1_cnt],
                    'sample_name_short_1':sn_1,
                    'sample_name_short_2':sample_name_shorts_2[sn_1_cnt],
                    'distance_measure':distance_measure_I,
                    'correlation_coefficient':rho,
                    'pvalue':pval,
                    'pvalue_corrected':None,
                    'pvalue_corrected_description':None,
                    'calculated_concentration_units':cu,
                    'used_':True,
                    'comment_':None};
                data_pairwise_O.append(tmp);

        #self.session.commit();
        self.add_dataStage02QuantificationPairWiseCorrelation('data_stage02_quantification_pairWiseCorrelation_replicates',data_pairwise_O);