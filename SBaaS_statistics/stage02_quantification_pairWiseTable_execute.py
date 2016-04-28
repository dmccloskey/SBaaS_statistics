
from .stage02_quantification_pairWiseTable_io import stage02_quantification_pairWiseTable_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query

class stage02_quantification_pairWiseTable_execute(stage02_quantification_pairWiseTable_io):
    def execute_pairwiseTableAverages(self,analysis_id_I,
            sample_name_abbreviations_I=[],
            calculated_concentration_units_I=[],
            component_names_I=[],
            redundancy_I=True,
            value_I = 'mean',
            query_object_descStats_I = 'stage02_quantification_descriptiveStats_query'):
        '''
        execute pairwiseTable
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'

        '''

        print('execute_pairwiseTable...')
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        data_pairwise_O = [];
        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            if hasattr(query_instance, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
            # get sample_name_abbreviations and sample_name_shorts:
            if sample_name_abbreviations_I:
                sample_name_abbreviations = sample_name_abbreviations_I;
            else:
                sample_name_abbreviations=[];
                if hasattr(query_instance, 'get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                    calculated_concentration_units = query_instance_descStats.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,cu);
                elif hasattr(query_instance, 'get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                    calculated_concentration_units = query_instance_descStats.get_sampleNameAbbreviations_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
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
                    if sna_1 != sna_2:

                        # get the calculated concentrations ordered by component name:
                        data_1,data_2 = [],[];
                        if hasattr(query_instance, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages'):
                            data_1 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(
                                analysis_id_I,cu,sna_1);
                            data_2 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDataPreProcessingAverages(
                                analysis_id_I,cu,sna_2);
                        elif hasattr(query_instance, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats'):
                            data_1 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats(
                                analysis_id_I,cu,sna_1);
                            data_2 = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats(
                                analysis_id_I,cu,sna_2);
                        else:
                            print('query instance does not have the required method.');

                        if len(data_1)!=len(data_2):
                            print('the number of components in sn_1 and sn_2 are not equal.');

                        # recorde the data
                        for d_1_cnt,d_1 in enumerate(data_1):
                            assert(d_1['component_name']==data_2[d_1_cnt]['component_name']);
                            tmp = {'analysis_id':analysis_id_I,
                                'component_group_name':d_1['component_group_name'],
                                'component_name':d_1['component_name'],
                                'value_name':value_I,
                                'sample_name_abbreviation_1':sna_1,
                                'sample_name_abbreviation_2':sna_2,
                                'value_1':d_1[value_I],
                                'value_2':data_2[d_1_cnt][value_I],
                                'calculated_concentration_units':cu,
                                'used_':True,
                                'comment_':None};
                            data_pairwise_O.append(tmp)
        # add data to database
        self.add_rows_table('data_stage02_quantification_pairWiseTable',data_pairwise_O);

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

        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu_cnt,cu in enumerate(concentration_units):
            print('calculating pairwiseTable for concentration_units ' + cu);

            # get sample_name_abbreviations and sample_name_shorts:
            sample_name_abbreviations,sample_name_shorts = [],[];
            #TODO: add in filter for component_names when return the data from the query
            sample_name_abbreviations,sample_name_shorts = dataPreProcessing_replicates_query.get_sampleNameAbbreviationsAndSampleNameShorts_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu)
            for sn_1_cnt,sn_1 in enumerate(sample_name_shorts):
                if redundancy_I: list_2 = sample_name_shorts;
                else: list_2 = sample_name_shorts[sn_1_cnt+1:];
                for cnt,sn_2 in enumerate(list_2):
                    if redundancy_I: sn_2_cnt = cnt;
                    else: sn_2_cnt = sn_1_cnt+cnt+1;
                    if sn_1 != sn_2:
                        # get the calculated concentrations in ordered by component name:
                        data_1,data_2 = [],[];
                        data_1 = dataPreProcessing_replicates_query.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu,sn_1);
                        data_2 = dataPreProcessing_replicates_query.get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameShort_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu,sn_2);

                        if len(data_1)!=len(data_2):
                            print('the number of components in sn_1 and sn_2 are not equal.');

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
        self.add_rows_table('data_stage02_quantification_pairWiseTable_replicates',data_pairwise_O);