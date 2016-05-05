# SBaaS
from .stage02_quantification_enrichment_io import stage02_quantification_enrichment_io
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
# Resources
from python_statistics.calculate_enrichment import calculate_enrichment
from listDict.listDict import listDict
from r_statistics.r_interface import r_interface

class stage02_quantification_enrichment_execute(stage02_quantification_enrichment_io,):
    def execute_enrichment(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                time_points_I=[],
                sample_name_abbreviations_I=[],
                component_names_I=[],
                enrichment_method_I='hypergeometric',
                enrichment_options_I={'pvalue_threshold':0.05},
                pvalue_threshold_I = 0.05,
                pvalue_corrected_description_I = "bonferroni",
                value_I = 'mean',
                query_object_descStats_I = 'stage02_quantification_dataPreProcessing_averages_query',
                r_calc_I=None,
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
            
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calculateenrichment = calculate_enrichment();

        if enrichment_method_I in ['hypergeometric']:
            #get the enrichment class information
            enrichment_classes = None;
            #enrichment_classes = self.get_rows_componentNames_dataStage02QuantificationEnrichmentClasses(component_names);
            enrichment_classes_listDict = listDict(listDict_I = enrichment_classes);
            enrichment_classes_listDict.convert_listDict2DataFrame();
            enrichment_classes_listDict.set_pivotTable(
                value_label_I = 'enrichment_class_weight',
                row_labels_I = ['enrichment_class'],
                column_labels_I = ['component_name'],
                );
            enrichment_matrix = enrichment_classes_listDict.get_dataMatrix();

        
        enrichment_O = [];
        #get the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu in calculated_concentration_units:
            print('generating a enrichment for concentration_units ' + cu);

            # get the unique experiment_id/sample_name_abbreviation/time_point
            if hasattr(query_instance_descStats, 'get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                unique_groups = query_instance_descStats.get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,cu,
                experiment_ids_I,
                sample_name_abbreviations_I,
                time_points_I);
            elif hasattr(query_instance_descStats, 'get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                unique_groups = query_instance_descStats.get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                    analysis_id_I,cu,
                experiment_ids_I,
                sample_name_abbreviations_I,
                time_points_I);
            else:
                print('query instance does not have the required method.');
            for unique_group in unique_groups.get_listDict():

                # get the data
                data = [];
                if hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingAverages'):
                    data = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingAverages(
                        analysis_id_I,cu,unique_group['experiment_id'],unique_group['sample_name_abbreviation'],unique_group['time_point']
                        );
                elif hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDescriptiveStats'):
                    data = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDescriptiveStats(
                        analysis_id_I,cu,unique_group['experiment_id'],unique_group['sample_name_abbreviation'],unique_group['time_point'],
                        );
                else:
                    print('query instance does not have the required method.');

                # check for the pvalue cutoff:
                data_listDict = listDict(listDict_I = data);
                data_listDict.convert_listDict2DataFrame();
                data_filtered = data_listDict.dataFrame[(data_listDict.dataFrame.pvalue_corrected < enrichment_options_I['pvalue_threshold'])];
                if len(data_filtered)<1: continue;
                data_listDict.dataFrame['pvalue_corrected'].fillna(1.0, inplace=True)
                data_listDict.convert_dataFrame2ListDict()

                if enrichment_method_I in ['hypergeometric']:
                    pvalues = self.calculate_enrichment_hypergeometric(
                        data_filtered,
                        enrichment_matrix,
                        enrichment_method_I,
                        enrichment_options_I);
                else:
                    print('enrichment method not recognized.');

                #NOTES:
                #p-value adjustment is not needed
                # see https://www.bioconductor.org/packages/3.3/bioc/vignettes/topGO/inst/doc/topGO.pdf
                # section 6.2 for a discussion
                if pvalues:
                    # Pass 2: calculate the corrected p-values
                    data_listDict = listDict(data_O);
                    data_listDict.convert_listDict2DataFrame();
                    pvalues = data_listDict.dataFrame['pvalue'].get_values();
                    # call R
                    r_calc.clear_workspace();
                    r_calc.make_vectorFromList(pvalues,'pvalues');
                    pvalue_corrected = r_calc.calculate_pValueCorrected(
                        'pvalues',
                        'pvalues_O',method_I = pvalue_corrected_description_I);
                    # add in the corrected p-values
                    data_listDict.add_column2DataFrame('pvalue_corrected', pvalue_corrected);
                    data_listDict.add_column2DataFrame('pvalue_corrected_description', pvalue_corrected_description_I);
                    data_listDict.convert_dataFrame2ListDict();
                    enrichment_O.extend(data_listDict.get_listDict());


        self.add_rows_table('data_stage02_quantification_enrichment',enrichment_O);

    def calculate_enrichment_hypergeometric(self,
            data_I,
            enrichment_matrix_I,
            enrichment_method_I,
            enrichment_options_I,
                ):
        
        # get a list of all unique component_names
        data_listDict = listDict(listDict_I = data_I);
        data_listDict.convert_listDict2DataFrame();
        data_filtered = data_listDict.dataFrame[(data_listDict.dataFrame.pvalue_corrected < enrichment_options_I['pvalue_threshold'])];
        component_names = data_I['component_name'].unique();

        # Pass 1: calculate the enrichment
        pvalues_O = calculateenrichment(enrichment_matrix,component_names);
        return pvalues_O;

    def execute_geneSetEnrichment(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                time_points_I=[],
                sample_name_abbreviations_I=[],
                component_names_I=[],
                enrichment_method_I='topGO',
                enrichment_options_I={
                    'pvalue_threshold':0.05,
                    'GO_database':'GO.db',
                    'enrichment_algorithm':'classic','test_description':'fisher',
                    'GO_ontology':"BP",'GO_annotation':"annFUN.org",
                    'GO_annotation_mapping':"org.EcK12.eg.db",
                    'GO_annotation_id' :'alias'},
                pvalue_corrected_description_I = "bonferroni",
                query_object_descStats_I = 'stage02_quantification_dataPreProcessing_averages_query',
                r_calc_I=None
                ):
        '''Execute a gene set enrichment analysis using R
        INPUT:
        analysis_id_I = string, analysis id
        sample_name_abbreviations_I = list of sample_name_abbreviations
        calculated_concentration_units_I = list of concentration units
        component_names_I = list of component_names
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'

        USAGE FOR topGO:
        enrichment_method_I='topGO'
        enrichment_options_I={
            'pvalue_threshold':0.05,
            'value':'mean',
            'value_operator':"<",
            'value_threshold':0,
            'GO_database':'GO.db',
            'enrichment_algorithm':'classic','test_description':'fisher',
            'GO_ontology':"BP",'GO_annotation':"annFUN.org",
            'GO_annotation_mapping':"org.EcK12.eg.db",
            'GO_annotation_id' :'alias'}
        '''

        print('executing enrichment from descriptiveStats...');

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();
            
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();

        if enrichment_method_I in ['topGO']:
            r_calc.import_GODB(enrichment_options_I['GO_database'])
            r_calc.import_GODB(enrichment_options_I['GO_annotation_mapping'])
                    
        enrichment_O = [];
        #get the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu in calculated_concentration_units:
            print('generating a enrichment for concentration_units ' + cu);

            # get the unique experiment_id/sample_name_abbreviation/time_point
            if hasattr(query_instance_descStats, 'get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                unique_groups = query_instance_descStats.get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,cu,
                experiment_ids_I,
                sample_name_abbreviations_I,
                time_points_I);
            elif hasattr(query_instance_descStats, 'get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                unique_groups = query_instance_descStats.get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                    analysis_id_I,cu,
                experiment_ids_I,
                sample_name_abbreviations_I,
                time_points_I);
            else:
                print('query instance does not have the required method.');
            for unique_group in unique_groups.get_listDict():

                # get the data
                data = [];
                if hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingAverages'):
                    data = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingAverages(
                        analysis_id_I,cu,unique_group['experiment_id'],unique_group['sample_name_abbreviation'],unique_group['time_point']
                        );
                elif hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDescriptiveStats'):
                    data = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDescriptiveStats(
                        analysis_id_I,cu,unique_group['experiment_id'],unique_group['sample_name_abbreviation'],unique_group['time_point'],
                        );
                else:
                    print('query instance does not have the required method.');

                # check for the pvalue cutoff:
                data_listDict = listDict(listDict_I = data);
                data_listDict.convert_listDict2DataFrame();
                ##Testing adding in a FC direction
                #if 'pvalue_threshold' in enrichment_options_I.keys() and 'value_operator' in enrichment_options_I.keys()\
                #    and 'value_operator'=='>':
                #    data_filtered = data_listDict.dataFrame[
                #        (data_listDict.dataFrame.pvalue_corrected < enrichment_options_I['pvalue_threshold'])&
                #        (data_listDict.dataFrame['value'] > enrichment_options_I['value_threshold'])];
                #    enrichment_direction = '>';
                #elif 'pvalue_threshold' in enrichment_options_I.keys() and 'value_operator' in enrichment_options_I.keys()\
                #    and 'value_operator'=='<':
                #    data_filtered = data_listDict.dataFrame[
                #        (data_listDict.dataFrame.pvalue_corrected < enrichment_options_I['pvalue_threshold'])&
                #        (data_listDict.dataFrame['value'] < enrichment_options_I['value_threshold'])];
                #    enrichment_direction = '<';
                #elif 'pvalue_threshold' in enrichment_options_I.keys():
                #    data_filtered = data_listDict.dataFrame[
                #        (data_listDict.dataFrame.pvalue_corrected < enrichment_options_I['pvalue_threshold'])
                #        ];
                #    enrichment_direction = 'None';
                if 'pvalue_threshold' in enrichment_options_I.keys():
                    data_filtered = data_listDict.dataFrame[
                        (data_listDict.dataFrame.pvalue_corrected < enrichment_options_I['pvalue_threshold'])
                        ];
                if len(data_filtered)<1: continue;
                data_listDict.dataFrame['pvalue_corrected'].fillna(1.0, inplace=True)
                data_listDict.convert_dataFrame2ListDict()

                # perform GSA
                if enrichment_method_I in ['topGO']:
                    go_ids,pvalues = self.calculate_enrichment_topGO(
                        data_listDict.get_listDict(),
                        enrichment_method_I,
                        enrichment_options_I,
                        r_calc);
                else:
                    print('enrichment method not recognized.');

                # Get the GO terms
                go_terms = r_calc.select_columnsByKeys_GODB(
                    GO_I=enrichment_options_I['GO_database'],
                    keys_I=go_ids,
                    columns_I=['DEFINITION', 'ONTOLOGY', 'TERM']
                    )
                assert(len(go_terms)==len(pvalues));

                data_listDict = listDict(listDict_I=go_terms);
                data_listDict.convert_listDict2DataFrame();
                data_listDict.change_rowAndColumnNames(column_names_dict_I={'DEFINITION':'GO_definition', 'GOID':'GO_id', 'ONTOLOGY':'GO_ontology', 'TERM':'GO_term'});
                data_listDict.add_column2DataFrame('pvalue', pvalues);
                data_listDict.add_column2DataFrame('analysis_id', analysis_id_I);
                data_listDict.add_column2DataFrame('calculated_concentration_units', cu);
                data_listDict.add_column2DataFrame('experiment_id', unique_group['experiment_id']);
                data_listDict.add_column2DataFrame('sample_name_abbreviation', unique_group['sample_name_abbreviation']);
                data_listDict.add_column2DataFrame('time_point', unique_group['time_point']);
                data_listDict.add_column2DataFrame('GO_database', enrichment_options_I['GO_database']);
                data_listDict.add_column2DataFrame('GO_annotation', enrichment_options_I['GO_annotation']);
                data_listDict.add_column2DataFrame('GO_annotation_mapping', enrichment_options_I['GO_annotation_mapping']);
                data_listDict.add_column2DataFrame('GO_annotation_id', enrichment_options_I['GO_annotation_id']);
                enrichment_method = ('%s_%s'%(enrichment_method_I,enrichment_options_I['enrichment_algorithm']))
                data_listDict.add_column2DataFrame('enrichment_method', enrichment_method);
                test_description = ('%s_%s'%(enrichment_method_I,enrichment_options_I['test_description']))
                data_listDict.add_column2DataFrame('test_description', test_description);
                enrichment_options = {'pvalue_threshold':enrichment_options_I['pvalue_threshold']};
                data_listDict.add_column2DataFrame('enrichment_options', enrichment_options);
                #data_listDict.add_column2DataFrame('enrichment_direction', enrichment_direction);
                data_listDict.add_column2DataFrame('used_', True);

                if pvalues.any():
                    # Pass 2: calculate the corrected p-values
                    # call R
                    r_calc.clear_workspace();
                    r_calc.make_vectorFromList(pvalues,'pvalues');
                    pvalue_corrected = r_calc.calculate_pValueCorrected(
                        'pvalues',
                        'pvalues_O',method_I = pvalue_corrected_description_I);
                    # add in the corrected p-values
                    data_listDict.add_column2DataFrame('pvalue_corrected', pvalue_corrected);
                    data_listDict.add_column2DataFrame('pvalue_corrected_description', pvalue_corrected_description_I);
                    data_listDict.convert_dataFrame2ListDict();
                    enrichment_O.extend(data_listDict.get_listDict());

        self.add_rows_table('data_stage02_quantification_geneSetEnrichment',enrichment_O);

    def calculate_enrichment_topGO(self,
            data_I,
            enrichment_method_I,
            enrichment_options_I,
            r_calc):
        
        genes_w_pvals = {d['component_group_name']:d['pvalue_corrected'] for d in data_I};

        r_calc.make_topDiffGenes(
                topDiffGenes_O = 'topDiffGenes',
                pvalue_I = enrichment_options_I['pvalue_threshold']
                )
                
        r_calc.make_namedVectorFromDict(
            dict_I = genes_w_pvals,
            namedVector_O = 'genes_w_pvals'
            );

        #required if 'annot':"annFUN.gene2GO"
        #gene_to_go,go_to_gene = r_calc.parse_go_map_file(enrichment_classes,genes_w_pvalus);
        #r_calc.make_namedVectorFromDict(
        #    dict_I = gene_to_go,
        #    namedVector_O = 'gene_to_go'
        #    );

        r_calc.make_topGOdata(
            topDiffdata_O = 'topGOdata_O',
            ontology = enrichment_options_I['GO_ontology'],
            annot = enrichment_options_I['GO_annotation'],
            mapping =  enrichment_options_I['GO_annotation_mapping'],
            ID = enrichment_options_I['GO_annotation_id'],
            geneSel = "topDiffGenes",
            allGenes = "genes_w_pvals",
            nodeSize = 10,
            )
                    
        r_calc.calculate_enrichment_topGO(
            topGOresult_O = 'result',
            topDiffdata_I = 'topGOdata_O',
            algorithm = enrichment_options_I['enrichment_algorithm'],
            statistic = enrichment_options_I['test_description'],
            );

        go_ids, pvals = r_calc.extract_scores_topGO(
                topGOresult_I = 'result',
                topGOscores_O = 'scores',
                );

        ##OPTIONAL: get sub children
        #for go_id in go_ids:
        #    go_children = r_calc.get_go_children(go_id, enrichment_options_I['ontology'])

        #get the corresponding go description for each go id
        #enrichment_options_I['enrichment_class_database']

        return go_ids, pvals;

                
                
               