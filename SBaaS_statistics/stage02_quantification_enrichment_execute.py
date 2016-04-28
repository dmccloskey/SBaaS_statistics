# SBaaS
from .stage02_quantification_enrichment_io import stage02_quantification_enrichment_io
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
# Resources
from python_calculate.calculate_enrichment import calculate_enrichment
from listDict.listDict import listDict

class stage02_quantification_enrichment_execute(stage02_quantification_enrichment_io,):
    def execute_enrichment(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                time_points_I=[],
                sample_name_abbreviations_I=[],
                component_names_I=[],
                pvalue_threshold_I = 0.05,
                pvalue_corrected_description_I = "bonferroni",
                value_I = 'mean',
                query_object_descStats_I = 'stage02_quantification_descriptiveStats_query'
                ):
        '''Execute an enrichment analysis
        INPUT:
        analysis_id_I = string, analysis id
        sample_name_abbreviations_I = list of sample_name_abbreviations
        calculated_concentration_units_I = list of concentration units
        component_names_I = list of component_names
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        '''

        print('executing enrichment from descriptiveStats...');

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        calculateenrichment = calculate_enrichment();
        
        enrichment_O = [];
        #get the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            if hasattr(query_instance, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu in calculated_concentration_units:
            print('generating a enrichment for concentration_units ' + cu);

            # get the unique experiment_id/sample_name_abbreviation/time_point
            if hasattr(query_instance, 'get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                data = query_instance_descStats.get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,cu,
                experiment_ids_I,
                sample_name_abbreviations_I,
                time_points_I);
            elif hasattr(query_instance, 'get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                data = query_instance_descStats.get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                    analysis_id_I,cu,
                experiment_ids_I,
                sample_name_abbreviations_I,
                time_points_I);
            else:
                print('query instance does not have the required method.');
            for unique_group in unique_groups.get_listDict():

                # get the data
                data = [];
                if hasattr(query_instance, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingAverages'):
                    data = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingAverages(
                        analysis_id_I,cu,unique_group['experiment_id'],unique_group['sample_name_abbreviation'],unique_group['time_point']
                        );
                elif hasattr(query_instance, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDescriptiveStats'):
                    data = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDescriptiveStats(
                        analysis_id_I,cu,unique_group['experiment_id'],unique_group['sample_name_abbreviation'],unique_group['time_point'],
                        );
                else:
                    print('query instance does not have the required method.');

                # get a list of all unique component_names
                data_listDict = listDict(listDict_I = data);
                data_listDict.convert_listDict2DataFrame();
                data_filtered = data_listDict.dataFrame[(data_listDict.dataFrame.pvalue_corrected < pvalue_threshold_I)];
                component_names = data_filtered['component_name'].unique();

                #get the enrichment class information
                enrichment_classes = None;
                enrichment_classes = self.get_rows_componentNames_dataStage02QuantificationEnrichmentClasses(component_names);
                enrichment_classes_listDict = listDict(listDict_I = enrichment_classes);
                enrichment_classes_listDict.convert_listDict2DataFrame();
                enrichment_classes_listDict.set_pivotTable(
                    value_label_I = 'enrichment_class_weight',
                    row_labels_I = ['enrichment_class'],
                    column_labels_I = ['component_name'],
                    );
                enrichment_matrix = enrichment_classes_listDict.get_dataMatrix();

                # Pass 1: calculate the enrichment
                pvalues = calculateenrichment(enrichment_matrix,component_names);

                if pvalues:
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
        self.add_rows_table('data_stage02_quantification_enrichment',enrichment_O);