
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_pairWiseCorrelation_io import stage02_quantification_pairWiseCorrelation_io
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
# resources
from python_statistics.calculate_correlation import calculate_correlation
from listDict.listDict import listDict
import numpy as np

class stage02_quantification_pairWiseCorrelation_execute(stage02_quantification_pairWiseCorrelation_io):
    def execute_pairwiseCorrelationAverages_v01(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            calculated_concentration_units_I=[],
            component_names_I=[],
            pvalue_corrected_description_I = "bonferroni",
            redundancy_I=True,
            distance_measure_I='pearson',
            value_I = 'mean',
            r_calc_I=None,
            query_object_descStats_I = 'stage02_quantification_dataPreProcessing_averages_query'):
        '''execute pairwiseCorrelation
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        '''

        print('execute_pairwiseCorrelation...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        data_pairwise_O = [];
        calculatecorrelation = calculate_correlation();
        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations=[];
                if hasattr(query_instance_descStats, 'get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                    sample_name_abbreviations = query_instance_descStats.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,cu);
                elif hasattr(query_instance_descStats, 'get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                    sample_name_abbreviations = query_instance_descStats.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                    analysis_id_I,cu);
                else:
                    print('query instance does not have the required method.');
            for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                    
                data_O=[];
                #pass 1: calculate the pairwise correlations
                if redundancy_I: list_2 = sample_name_abbreviations;
                else: list_2 = sample_name_abbreviations[sna_1_cnt+1:];
                for cnt,sna_2 in enumerate(list_2):
                    if redundancy_I: sna_2_cnt = cnt;
                    else: sna_2_cnt = sna_1_cnt+cnt+1;

                    # get the calculated concentrations ordered by component name:
                    data_1,data_2 = [],[];
                    if hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages'):
                        data_1 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(
                            analysis_id_I,cu,sna_1);
                        data_2 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(
                            analysis_id_I,cu,sna_2);
                    elif hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats'):
                        data_1 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats(
                            analysis_id_I,cu,sna_1);
                        data_2 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats(
                            analysis_id_I,cu,sna_2);
                    else:
                        print('query instance does not have the required method.');

                    #extract out the values 
                    #TODO: incorporate into the actual query
                    data_1 = [d[value_I] for d in data_1]
                    data_2 = [d[value_I] for d in data_2]

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

                    #check for nan in rho
                    if np.isnan(rho): rho = 0.0;

                    # add data to database
                    tmp = {'analysis_id':analysis_id_I,
                        'value_name':value_I,
                        'sample_name_abbreviation_1':sna_1,
                        'sample_name_abbreviation_2':sna_2,
                        'distance_measure':distance_measure_I,
                        'correlation_coefficient':rho,
                        'pvalue':pval,
                        'calculated_concentration_units':cu,
                        'used_':True,
                        'comment_':None};
                    data_O.append(tmp)
                
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

        self.add_rows_table('data_stage02_quantification_pairWiseCorrelation',data_pairwise_O);
    def execute_pairwiseCorrelationFeaturesAverages_v01(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            calculated_concentration_units_I=[],
            component_names_I=[],
            pvalue_corrected_description_I = "bonferroni",
            redundancy_I=True,
            distance_measure_I='pearson',
            value_I = 'mean',
            r_calc_I=None,
            query_object_descStats_I = 'stage02_quantification_dataPreProcessing_averages_query'):
        '''execute pairwiseCorrelation
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        '''

        print('execute_pairwiseCorrelation...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        data_pairwise_O = [];
        calculatecorrelation = calculate_correlation();
        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
            component_names,component_group_names = [],[];
            if hasattr(query_instance_descStats, 'get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                component_names,component_group_names = query_instance_descStats.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
            elif hasattr(query_instance_descStats, 'get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                component_names,component_group_names = query_instance_descStats.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
            else:
                print('query instance does not have the required method.');
            #if component_names_I:
            #    component_names = component_names_I;
            for cn_1_cnt,cn_1 in enumerate(component_names):
                    
                data_O=[];
                #pass 1: calculate the pairwise correlations
                if redundancy_I: list_2 = component_names;
                else: list_2 = component_names[cn_1_cnt+1:];
                for cnt,cn_2 in enumerate(list_2):
                    if redundancy_I: cn_2_cnt = cnt;
                    else: cn_2_cnt = cn_1_cnt+cnt+1;
                    
                    data_1,data_2 = [],[];
                    if hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages'):
                        data_1 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDataPreProcessingAverages(
                            analysis_id_I,cu,cn_1);
                        data_2 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDataPreProcessingAverages(
                            analysis_id_I,cu,cn_2);
                    elif hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats'):
                        data_1 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDescriptiveStats(
                            analysis_id_I,cu,cn_1);
                        data_2 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDescriptiveStats(
                            analysis_id_I,cu,cn_2);
                    else:
                        print('query instance does not have the required method.');
                        
                    #extract out the values 
                    #TODO: incorporate into the actual query
                    data_1 = [d[value_I] for d in data_1];
                    data_2 = [d[value_I] for d in data_2];

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

                    #check for nan in rho
                    if np.isnan(rho): rho = 0.0;

                    # add data to database
                    tmp = {'analysis_id':analysis_id_I,
                        'value_name':value_I,
                        'component_name_1':cn_1,
                        'component_name_2':cn_2,
                        'component_group_name_1':component_group_names[cn_1_cnt],
                        'component_group_name_2':component_group_names[cn_2_cnt],
                        'distance_measure':distance_measure_I,
                        'correlation_coefficient':rho,
                        'pvalue':pval,
                        'calculated_concentration_units':cu,
                        'used_':True,
                        'comment_':None};
                    data_O.append(tmp)
                
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

        self.add_rows_table('data_stage02_quantification_pairWiseCorrelationFeatures',data_pairwise_O);
    def execute_pairwiseCorrelationReplicates(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            sample_name_shorts_I=[],
            calculated_concentration_units_I=[],
            component_names_I=[],
            pvalue_corrected_description_I = "bonferroni",
            redundancy_I=True,
            distance_measure_I='pearson',
            r_calc_I=None):
        '''execute pairwiseCorrelation
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        '''

        print('execute_pairwiseCorrelationReplicates...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        #quantification_pairWiseTable_query = stage02_quantification_pairWiseTable_query(self.session,self.engine,self.settings);
        #quantification_pairWiseTable_query.initialize_supportedTables();
        
        quantification_dataPreProcessing_replicates_query=stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        quantification_dataPreProcessing_replicates_query.initialize_supportedTables();

        data_pairwise_O = [];
        calculatecorrelation = calculate_correlation();
        # query metabolomics data from glogNormalization
        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            #calculated_concentration_units = quantification_pairWiseTable_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I);
            calculated_concentration_units = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
            # get sample_name_abbreviations and sample_name_shorts:
            sample_name_abbreviations,sample_name_shorts=[],[];
            sample_name_abbreviations,sample_name_shorts=quantification_dataPreProcessing_replicates_query.get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,cu);
            #sample_name_abbreviations_1,sample_name_shorts_1,sample_name_abbreviations_2,sample_name_shorts_2 = [],[],[],[];
            #sample_name_abbreviations_1,sample_name_shorts_1,sample_name_abbreviations_2,sample_name_shorts_2 = quantification_pairWiseTable_query.get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I,cu)
            #for sn_1_cnt,sn_1 in enumerate(sample_name_shorts_1):
            for sna_1_cnt,sna_1 in enumerate(sample_name_shorts):
                    
                data_O=[];
                #pass 1: calculate the pairwise correlations
                if redundancy_I: list_2 = sample_name_shorts;
                else: list_2 = sample_name_shorts[sna_1_cnt+1:];
                for cnt,sna_2 in enumerate(list_2):
                    if redundancy_I: sna_2_cnt = cnt;
                    else: sna_2_cnt = sna_1_cnt+cnt+1;
                    #print('calculating pairwiseCorrelation for sample_name_short ' + sn_1 + ' vs. ' + sample_name_shorts_2[sn_1_cnt]);
                    # get the calculated concentrations ordered by component name:
                    data_1,data_2 = [],[];
                    data_1 = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationDataPreProcessingReplicates(
                        analysis_id_I,cu,sample_name_shorts[sna_1_cnt]);
                    data_2 = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationDataPreProcessingReplicates(
                        analysis_id_I,cu,sample_name_shorts[sna_2_cnt]);
                    #data_1,data_2 = quantification_pairWiseTable_query.get_calculatedConcentrations_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I,cu,sn_1,sample_name_shorts_2[sn_1_cnt]);
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
                        'sample_name_abbreviation_1':sample_name_abbreviations[sna_1_cnt],
                        'sample_name_abbreviation_2':sample_name_abbreviations[sna_2_cnt],
                        'sample_name_short_1':sample_name_shorts[sna_1_cnt],
                        'sample_name_short_2':sample_name_shorts[sna_2_cnt],
                        'distance_measure':distance_measure_I,
                        'correlation_coefficient':rho,
                        'pvalue':pval,
                        'calculated_concentration_units':cu,
                        'used_':True,
                        'comment_':None};
                    data_O.append(tmp)
               
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

        self.add_rows_table('data_stage02_quantification_pairWiseCorrelation_replicates',data_pairwise_O);

    ###refactored:    
    def execute_pairwiseCorrelationFeaturesAverages(self,analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
            pvalue_corrected_description_I = "bonferroni",
            redundancy_I=True,
            distance_measure_I='pearson',
            value_I = 'mean',
            r_calc_I=None,
            query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats'):
        '''execute pairwiseCorrelation
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        '''

        print('execute_pairwiseCorrelation...')

        # instantiate dependent objects
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calculatecorrelation = calculate_correlation();

        # instantiate the output list
        data_pairwise_O = [];

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        #query the data:
        data_listDict = [];
        if hasattr(query_instance_descStats, query_func_descStats_I):
            query_func_descStats = getattr(query_instance_descStats, query_func_descStats_I);
            data_listDict = query_func_descStats(analysis_id_I,
                calculated_concentration_units_I=calculated_concentration_units_I,
                component_names_I=component_names_I,
                component_group_names_I=component_group_names_I,
                sample_name_abbreviations_I=sample_name_abbreviations_I,
                time_points_I=time_points_I,
                experiment_ids_I=experiment_ids_I,
                test_descriptions_I=test_descriptions_I,
                pvalue_corrected_descriptions_I=pvalue_corrected_descriptions_I,
                where_clause_I=where_clause_I,
                );
        else:
            print('query instance does not have the required method.');

        #reorganize into analysis groups:
        calculated_concentration_units = list(set([c['calculated_concentration_units'] for c in data_listDict]));
        calculated_concentration_units.sort();
        component_names = list(set([c['component_name'] for c in data_listDict]));
        component_names.sort();
        data_analysis = {'':{'':[]}};
        for row in data_listDict:
            cu = row['calculated_concentration_units']
            cn = row['component_name']
            if not cu in data_analysis.keys(): data_analysis[cu]={};
            if not cn in data_analysis[cu].keys(): data_analysis[cu][cn]=[];
            data_analysis[cu][cn].append(row);
        del data_analysis[''];

        #apply the analysis to each unique dimension
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
            for cn_1_cnt,cn_1 in enumerate(component_names):                    
                data_O=[];
                #pass 1: calculate the pairwise correlations
                if redundancy_I: list_2 = component_names;
                else: list_2 = component_names[cn_1_cnt+1:];
                for cnt,cn_2 in enumerate(list_2):
                    if redundancy_I: cn_2_cnt = cnt;
                    else: cn_2_cnt = cn_1_cnt+cnt+1;
                    
                    data_1,data_2 = [],[];
                    data_1 = data_analysis[cu][cn_1];
                    data_2 = data_analysis[cu][cn_2];                        
                    #extract out the values 
                    data_1 = [d[value_I] for d in data_1];
                    data_2 = [d[value_I] for d in data_2];

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

                    #check for nan in rho
                    if np.isnan(rho):
                        rho = 0.0;
                    if np.isnan(pval):
                        pval = 0.0;

                    # add data to database
                    tmp = {'analysis_id':analysis_id_I,
                        'value_name':value_I,
                        'component_name_1':cn_1,
                        'component_name_2':cn_2,
                        'component_group_name_1':data_analysis[cu][cn_1][0]['component_group_name'],
                        'component_group_name_2':data_analysis[cu][cn_2][0]['component_group_name'],
                        'distance_measure':distance_measure_I,
                        'correlation_coefficient':rho,
                        'pvalue':pval,
                        'calculated_concentration_units':cu,
                        'used_':True,
                        'comment_':None};
                    data_O.append(tmp)
                
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

        self.add_rows_table('data_stage02_quantification_pairWiseCorrelationFeatures',data_pairwise_O);
    def execute_pairwiseCorrelationAverages(self,analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
            pvalue_corrected_description_I = "bonferroni",
            redundancy_I=True,
            distance_measure_I='pearson',
            value_I = 'mean',
            r_calc_I=None,
            query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats'):
        '''execute pairwiseCorrelation
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        '''

        print('execute_pairwiseCorrelation...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calculatecorrelation = calculate_correlation();

        data_pairwise_O = [];

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        #query the data:
        data_listDict = [];
        if hasattr(query_instance_descStats, query_func_descStats_I):
            query_func_descStats = getattr(query_instance_descStats, query_func_descStats_I);
            data_listDict = query_func_descStats(analysis_id_I,
                calculated_concentration_units_I=calculated_concentration_units_I,
                component_names_I=component_names_I,
                component_group_names_I=component_group_names_I,
                sample_name_abbreviations_I=sample_name_abbreviations_I,
                time_points_I=time_points_I,
                experiment_ids_I=experiment_ids_I,
                test_descriptions_I=test_descriptions_I,
                pvalue_corrected_descriptions_I=pvalue_corrected_descriptions_I,
                where_clause_I=where_clause_I,
                );
        else:
            print('query instance does not have the required method.');

        #reorganize into analysis groups:
        calculated_concentration_units = list(set([c['calculated_concentration_units'] for c in data_listDict]));
        calculated_concentration_units.sort();
        sample_name_abbreviations = list(set([c['sample_name_abbreviation'] for c in data_listDict]));
        sample_name_abbreviations.sort();
        data_analysis = {'':{'':[]}};
        for row in data_listDict:
            cu = row['calculated_concentration_units']
            sna = row['sample_name_abbreviation']
            if not cu in data_analysis.keys(): data_analysis[cu]={};
            if not sna in data_analysis[cu].keys(): data_analysis[cu][sna]=[];
            data_analysis[cu][sna].append(row);
        del data_analysis[''];

        #apply the analysis to each unique dimension
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
            for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                    
                data_O=[];
                #pass 1: calculate the pairwise correlations
                if redundancy_I: list_2 = sample_name_abbreviations;
                else: list_2 = sample_name_abbreviations[sna_1_cnt+1:];
                for cnt,sna_2 in enumerate(list_2):
                    if redundancy_I: sna_2_cnt = cnt;
                    else: sna_2_cnt = sna_1_cnt+cnt+1;
                    
                    data_1,data_2 = [],[];
                    data_1 = data_analysis[cu][sna_1];
                    data_2 = data_analysis[cu][sna_2];                        
                    #extract out the values 
                    data_1 = [d[value_I] for d in data_1];
                    data_2 = [d[value_I] for d in data_2];

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
                        
                    if np.isnan(rho):
                        rho = 0.0;
                    if np.isnan(pval):
                        pval = 0.0;

                    # add data to database
                    tmp = {'analysis_id':analysis_id_I,
                        'value_name':value_I,
                        'sample_name_abbreviation_1':sna_1,
                        'sample_name_abbreviation_2':sna_2,
                        'distance_measure':distance_measure_I,
                        'correlation_coefficient':rho,
                        'pvalue':pval,
                        'calculated_concentration_units':cu,
                        'used_':True,
                        'comment_':None};
                    data_O.append(tmp)
                
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

        self.add_rows_table('data_stage02_quantification_pairWiseCorrelation',data_pairwise_O);