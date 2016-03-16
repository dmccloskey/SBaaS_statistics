
from .stage02_quantification_pairWiseTable_io import stage02_quantification_pairWiseTable_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query

class stage02_quantification_pairWiseTable_execute(stage02_quantification_pairWiseTable_io,
                                         stage02_quantification_normalization_query):
    def execute_pairwiseTable(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            concentration_units_I=[],
            component_names_I=[],
            redundancy_I=True,
            value_I = 'mean'):
        '''
        execute pairwiseTable
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.

        TODO:
        ...

        '''

        print('execute_pairwiseTable...')

        data_pairwise_O = [];
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu_cnt,cu in enumerate(concentration_units):
            print('calculating pairwiseTable for concentration_units ' + cu);
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
                print('calculating pairwiseTable for component_names ' + cn);
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
                            print('calculating pairwiseTable for sample_name_abbreviations ' + sna_1 + ' vs. ' + sna_2);
                            # get data:
                            all_1,all_2 = [],[];
                            data_1,data_2 = [],[];
                            all_1,data_1 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna_1);
                            all_2,data_2 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna_2);
                            # call R
                            data_pairwiseTable = {};
                            if len(data_1)==len(data_2):
                                data_pairwiseTable = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="TRUE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                            else:
                                data_pairwiseTable = r_calc.calculate_twoSampleTTest(data_1, data_2, alternative_I = "two.sided", mu_I = 0, paired_I="FALSE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                            if data_pairwiseTable is None:
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
                                'mean':data_pairwiseTable['mean'],
                                'test_stat':data_pairwiseTable['test_stat'],
                                'test_description':data_pairwiseTable['test_description'],
                                'pvalue':data_pairwiseTable['pvalue'],
                                'pvalue_corrected':data_pairwiseTable['pvalue_corrected'],
                                'pvalue_corrected_description':data_pairwiseTable['pvalue_corrected_description'],
                                'ci_lb':data_pairwiseTable['ci_lb'],
                                'ci_ub':data_pairwiseTable['ci_ub'],
                                'ci_level':data_pairwiseTable['ci_level'],
                                'fold_change':foldChange,
                                'calculated_concentration_units':cu,
                                'used_':True,
                                'comment_':None};
                            data_pairwise_O.append(tmp);
        self.add_dataStage02QuantificationPairWiseTest(data_pairwise_O);

    def execute_pairwiseTableReplicates(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            sample_name_shorts_I=[],
            concentration_units_I=[],
            component_names_I=[],
            redundancy_I=True,):
        '''execute pairwiseTable
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        '''

        print('execute_pairwiseTableReplicates...')

        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        data_pairwise_O = [];
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            #concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
            concentration_units = dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(concentration_units):
            print('calculating pairwiseTable for concentration_units ' + cu);

            ## get component_names:
            #component_names, component_group_names = [],[];
            #component_names, component_group_names = self.get_componentNames_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I, cu);
            #if component_names_I:
            #    component_names_ind = [i for i,x in enumerate(component_names) if x in component_names_I];
            #    component_names_cpy = copy.copy(component_names);
            #    component_group_names = copy.copy(component_group_names);
            #    component_names = [x for i,x in enumerate(component_names) if i in component_names_ind]
            #    component_group_names = [x for i,x in enumerate(component_group_names) if i in component_names_ind]
            #for cnt_cn,cn in enumerate(component_names):
            #    print('calculating pairwiseTable for component_names ' + cn);

            # get sample_name_abbreviations and sample_name_shorts:
            sample_name_abbreviations,sample_name_shorts = [],[];
            #sample_name_abbreviations,sample_name_shorts = self.get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized(analysis_id_I,cu,cn)

            #TODO: add in filter for component_names when return the data from the query
            #sample_name_abbreviations,sample_name_shorts = self.get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu)
            sample_name_abbreviations,sample_name_shorts = dataPreProcessing_replicates_query.get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu)
            for sn_1_cnt,sn_1 in enumerate(sample_name_shorts):
                if redundancy_I: list_2 = sample_name_shorts;
                else: list_2 = sample_name_shorts[sn_1+1:];
                for cnt,sn_2 in enumerate(list_2):
                    if redundancy_I: sn_2_cnt = cnt;
                    else: sn_2_cnt = sn_1_cnt+cnt+1;
                    if sn_1 != sn_2:
                        print('calculating pairwiseTable for sample_name_short ' + sn_1 + ' vs. ' + sn_2);
                        # get the calculated concentrations in ordered by component name:
                        data_1,data_2 = [],[];
                        #data_1 = self.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNamesAndSampleNameShort_dataStage02GlogNormalized(analysis_id_I,cu,cn,sn_1);
                        #data_2 = self.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndComponentNamesAndSampleNameShort_dataStage02GlogNormalized(analysis_id_I,cu,cn,sn_2);
                        #data_1 = self.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02GlogNormalized(analysis_id_I,cu,sn_1);
                        #data_2 = self.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02GlogNormalized(analysis_id_I,cu,sn_2);
                        data_1 = dataPreProcessing_replicates_query.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu,sn_1);
                        data_2 = dataPreProcessing_replicates_query.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu,sn_2);

                        if len(data_1)!=len(data_2):
                            print('the number of components in sn_1 and sn_2 are not equal.');

                        #elif len(data_1)>1:
                        #    print('more than 1 value found for sn_1.');
                        #elif len(data_2)>1:
                        #    print('more than 1 value found for sn_2.');
                        # add data to database
                        #tmp = {'analysis_id':analysis_id_I,
                        #    'sample_name_abbreviation_1':sample_name_abbreviations[sn_1_cnt],
                        #    'sample_name_abbreviation_2':sample_name_abbreviations[sn_2_cnt],
                        #    'sample_name_short_1':sn_1,
                        #    'sample_name_short_2':sn_2,
                        #    'component_group_name':component_group_names[cnt_cn],
                        #    'component_name':cn,
                        #    'calculated_concentration_1':data_1[0],
                        #    'calculated_concentration_2':data_2[0],
                        #    'calculated_concentration_units':cu,
                        #    'used_':True,
                        #    'comment_':None};

                        # recorde the data
                        for d_1_cnt,d_1 in enumerate(data_1):
                            assert(d_1['component_name']==data_2[d_1_cnt]['component_name']);
                            tmp = {'analysis_id':analysis_id_I,
                                'sample_name_abbreviation_1':sample_name_abbreviations[sn_1_cnt],
                                'sample_name_abbreviation_2':sample_name_abbreviations[sn_2_cnt],
                                'sample_name_short_1':sn_1,
                                'sample_name_short_2':sn_2,
                                'component_group_name':d_1['component_group_name'],
                                'component_name':d_1['component_name'],
                                'calculated_concentration_1':d_1['calculated_concentration'],
                                'calculated_concentration_2':data_2[d_1_cnt]['calculated_concentration'],
                                'calculated_concentration_units':d_1['calculated_concentration_units'],
                                'used_':True,
                                'comment_':None};
                            data_pairwise_O.append(tmp);
        # add data to database
        self.add_dataStage02QuantificationPairWiseTable('data_stage02_quantification_pairWiseTable_replicates',data_pairwise_O);