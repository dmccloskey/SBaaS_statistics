# SBaaS
from .stage02_quantification_enrichment_io import stage02_quantification_enrichment_io
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_dataPreProcessing_pairWiseTest_query import stage02_quantification_dataPreProcessing_pairWiseTest_query
from .stage02_quantification_pairWiseTest_query import stage02_quantification_pairWiseTest_query

# Resources
from python_statistics.calculate_enrichment import calculate_enrichment
from listDict.listDict import listDict
from r_statistics.r_interface import r_interface

class stage02_quantification_enrichment_execute(stage02_quantification_enrichment_io,):
    def execute_pairWiseEnrichment(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_abbreviations_1_I=[],
            sample_name_abbreviations_2_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
            component_names_mapping_I = {},
            component_group_names_mapping_I = {},
            enrichment_method_I='hypergeometric',
            enrichment_options_I={'pvalue_threshold':0.05,
                                  'pvalue_corrected_threshold':0.05,
                                  'enrichment_class_database':'iJO1366_metabolites',
                                  'use_weights':False},
            pvalue_corrected_description_I = "bonferroni",
            query_object_I = 'stage02_quantification_pairWiseTest_query',
            query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationPairWiseTest',
            r_calc_I=None,
            ):
        '''Execute an enrichment analysis
        IMPLEMENTATION:
        pvalue_corrected or pvalue is used to test for enrichment by specifying the 'pvalue_corrected_threshold' or 'pvalue_threshold' in the enrichment_options_I dict
        fold_change can also be used to test for enrichment by specifying the 'fold_change_threshold' in the enrichment_options_I dict
        By default, components_names will be used to map the data to the enrichment class
            Exceptions: topGO uses component_group_names by default
                        hypergeometric will use component_group_names if component_group_names_mapping_I is specified

        NOTES:
        multiple test_description values and multiple pvalue_corrected_description from the pairwisetest will be grouped together
        topGO does not allow specifying fold_change as a criteria for enrichment, but only allows pvalue

        INPUT:
        analysis_id_I = string, analysis id
        ...
        component_names_mapping_I = {}, mapping between sample component_names and enrichment component_names
        ...
        query_object_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_pairWiseTest_query'
        query_func_I = query method to use to select rows from the query object
            options: 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationPairWiseTest'
        '''

        print('executing enrichment from descriptiveStats...');
        
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calculateenrichment = calculate_enrichment();
        
        enrichment_O = [];

        # intantiate the query object:
        query_objects = {
                        'stage02_quantification_pairWiseTest_query':stage02_quantification_pairWiseTest_query,
                        'stage02_quantification_dataPreProcessing_pairWiseTest_query':stage02_quantification_dataPreProcessing_pairWiseTest_query,};
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance = query_object(self.session,self.engine,self.settings);
            query_instance.initialize_supportedTables();
            
        #query the data:
        data_listDict = [];
        if hasattr(query_instance, query_func_I):
            query_func = getattr(query_instance, query_func_I);
            try:
                data_listDict = query_func(analysis_id_I,
                    calculated_concentration_units_I=calculated_concentration_units_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    sample_name_abbreviations_1_I=sample_name_abbreviations_1_I,
                    sample_name_abbreviations_2_I=sample_name_abbreviations_2_I,
                    test_descriptions_I=test_descriptions_I,
                    pvalue_corrected_descriptions_I=pvalue_corrected_descriptions_I,
                    where_clause_I=where_clause_I,
                    );
            except AssertionError as e:
                print(e);
        else:
            print('query instance does not have the required method.');

        if enrichment_method_I in ['hypergeometric']:
            #get the enrichment class information:
            enrichment_classes = None;
            enrichment_classes = self.get_rows_enrichmentClassDatabase_dataStage02QuantificationEnrichmentClasses(
                enrichment_options_I['enrichment_class_database']);
            enrichment_classes_listDict = listDict(listDict_I = enrichment_classes);
            enrichment_classes_listDict.convert_listDict2DataFrame();
            enrichment_classes_listDict.set_pivotTable(
                value_label_I = 'enrichment_class_weight',
                row_labels_I = ['enrichment_class'],
                column_labels_I = ['component_name'],
                );
            enrichment_classes_listDict.pivotTable.fillna(value=0,inplace=True)
            enrichment_columns = enrichment_classes_listDict.get_columnLabels_asArray()
            enrichment_rows = enrichment_classes_listDict.get_rowLabels_asArray()
            enrichment_matrix = enrichment_classes_listDict.get_dataMatrix();
        elif enrichment_method_I in ['topGO']:
            r_calc.import_GODB(enrichment_options_I['GO_database'])
            r_calc.import_GODB(enrichment_options_I['GO_annotation_mapping'])

        #reorganize into analysis groups:
        data_analysis = {'delete':{'delete':[]}};
        for row in data_listDict:
            unique = (row['analysis_id'],
                      row['calculated_concentration_units'],
                      row['sample_name_abbreviation_1'],
                      row['sample_name_abbreviation_2'],
                      );
            if not unique in data_analysis.keys(): data_analysis[unique]=[];
            data_analysis[unique].append(row);
        del data_analysis['delete'];

        #apply the analysis to each group:
        for unique,data in data_analysis.items():
            # check for the pvalue cutoff:
            data_filtered = self._filter_enrichmentData(data,enrichment_options_I);
            if len(data_filtered.get_listDict())<1: continue;

            if enrichment_method_I in ['hypergeometric']:
                #get filtered component names:
                component_names = [];
                if component_names_mapping_I:
                    for cn in data_filtered.dataFrame['component_name'].get_values():
                        if cn in component_names_mapping_I.keys():
                            component_names.append(component_names_mapping_I[cn])
                        else:
                            print('no mapping found for ' + cn);
                    #component_names = [component_names_mapping_I[k] for k in data_filtered.dataFrame['component_name'].get_values() if k in component_names_mapping_I.keys()];
                elif component_group_names_mapping_I:
                    for cgn in data_filtered.dataFrame['component_group_name'].get_values():
                        if cgn in component_group_names_mapping_I.keys():
                            component_names.append(component_group_names_mapping_I[cgn])
                        else:
                            print('no mapping found for ' + cgn);
                    #component_names = [component_group_names_mapping_I[k] for k in data_filtered.dataFrame['component_group_name'].get_values() if k in component_group_names_mapping_I.keys()];
                else:
                    component_names = data_filtered.dataFrame['component_name'].get_values();

                #calculate the pvalues
                pvalues = calculateenrichment.calculate_enrichment_hypergeometric(
                    enrichment_matrix,
                    enrichment_rows,
                    enrichment_columns,
                    component_names,
                    use_weights_I=enrichment_options_I['use_weights']);
                #extract the data
                data_listDict = listDict(dictList_I={'pvalue':pvalues});
                data_listDict.convert_dictList2DataFrame();
                data_listDict.add_column2DataFrame('analysis_id', analysis_id_I);
                data_listDict.add_column2DataFrame('calculated_concentration_units', data[0]['calculated_concentration_units']);
                data_listDict.add_column2DataFrame('sample_name_abbreviation_1', data[0]['sample_name_abbreviation_1']);
                data_listDict.add_column2DataFrame('sample_name_abbreviation_2', data[0]['sample_name_abbreviation_2']);
                data_listDict.add_column2DataFrame('enrichment_class', enrichment_rows);
                data_listDict.add_column2DataFrame('enrichment_method', enrichment_method_I);
                data_listDict.add_column2DataFrame('enrichment_options', enrichment_options_I);
                data_listDict.add_column2DataFrame('enrichment_class_database', enrichment_options_I['enrichment_class_database']);
                data_listDict.add_column2DataFrame('test_description', enrichment_method_I);
                data_listDict.add_column2DataFrame('used_', True);
                data_listDict.add_column2DataFrame('comment_', None);

            elif enrichment_method_I in ['topGO']:
                go_ids,pvalues = self.calculate_enrichment_topGO(
                    data,
                    #data_filtered.get_listDict(), #pass in the unfiltered data!
                    enrichment_method_I,
                    enrichment_options_I,
                    r_calc);
                # Get the GO terms
                go_terms = r_calc.select_columnsByKeys_GODB(
                    GO_I=enrichment_options_I['GO_database'],
                    keys_I=go_ids,
                    columns_I=['DEFINITION', 'ONTOLOGY', 'TERM']
                    )
                assert(len(go_terms)==len(pvalues));
                #extract the data
                data_listDict = listDict(listDict_I=go_terms);
                data_listDict.convert_listDict2DataFrame();
                data_listDict.change_rowAndColumnNames(column_names_dict_I={'DEFINITION':'GO_definition', 'GOID':'GO_id', 'ONTOLOGY':'GO_ontology', 'TERM':'GO_term'});
                data_listDict.add_column2DataFrame('pvalue', pvalues);
                data_listDict.add_column2DataFrame('analysis_id', analysis_id_I);
                data_listDict.add_column2DataFrame('calculated_concentration_units', data[0]['calculated_concentration_units']);
                data_listDict.add_column2DataFrame('sample_name_abbreviation_1', data[0]['sample_name_abbreviation_1']);
                data_listDict.add_column2DataFrame('sample_name_abbreviation_2', data[0]['sample_name_abbreviation_2']);
                data_listDict.add_column2DataFrame('GO_database', enrichment_options_I['GO_database']);
                data_listDict.add_column2DataFrame('GO_annotation', enrichment_options_I['GO_annotation']);
                data_listDict.add_column2DataFrame('GO_annotation_mapping', enrichment_options_I['GO_annotation_mapping']);
                data_listDict.add_column2DataFrame('GO_annotation_id', enrichment_options_I['GO_annotation_id']);
                enrichment_method = ('%s_%s'%(enrichment_method_I,enrichment_options_I['enrichment_algorithm']))
                data_listDict.add_column2DataFrame('enrichment_method', enrichment_method);
                test_description = ('%s_%s'%(enrichment_method_I,enrichment_options_I['test_description']))
                data_listDict.add_column2DataFrame('test_description', test_description);
                data_listDict.add_column2DataFrame('enrichment_options', enrichment_options_I);
                data_listDict.add_column2DataFrame('used_', True);
            else:
                print('enrichment method not recognized.');

            if len(data_listDict.dataFrame)>1:
                # Pass 2: calculate the corrected p-values
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
                data_listDict.clear_allData();

                
        if enrichment_method_I in ['hypergeometric']:
            self.add_rows_table('data_stage02_quantification_pairWiseEnrichment',enrichment_O);
        elif enrichment_method_I in ['topGO']:
            self.add_rows_table('data_stage02_quantification_pairWiseGeneSetEnrichment',enrichment_O);

    def _filter_enrichmentData(self,data_I,enrichment_options_I):
        '''Filter the enrichment data
        INPUT:
        data_I
        enrichment_options_I
        '''

        data_listDict = listDict(listDict_I = data_I);
        data_listDict.convert_listDict2DataFrame();
        if 'pvalue_threshold' in enrichment_options_I and 'fold_change_threshold' in enrichment_options_I:
            data_filtered_tmp = data_listDict.dataFrame[(data_listDict.dataFrame.pvalue < enrichment_options_I['pvalue_threshold'])&
                                                    (abs(data_listDict.dataFrame.fold_change) > enrichment_options_I['fold_change_threshold'])
                                                    ];
            data_filtered = listDict(dataFrame_I=data_filtered_tmp);
            data_filtered.convert_dataFrame2ListDict();
        elif 'pvalue_corrected_threshold' in enrichment_options_I and 'fold_change_threshold' in enrichment_options_I:
            data_filtered_tmp = data_listDict.dataFrame[(data_listDict.dataFrame.pvalue_corrected < enrichment_options_I['pvalue_corrected_threshold'])&
                                                    (abs(data_listDict.dataFrame.fold_change) > enrichment_options_I['fold_change_threshold'])
                                                    ];      
            data_filtered = listDict(dataFrame_I=data_filtered_tmp);
            data_filtered.convert_dataFrame2ListDict();         
        elif 'pvalue_threshold' in enrichment_options_I:
            data_filtered_tmp = data_listDict.dataFrame[(data_listDict.dataFrame.pvalue < enrichment_options_I['pvalue_threshold'])];
            data_filtered = listDict(dataFrame_I=data_filtered_tmp);
            data_filtered.convert_dataFrame2ListDict();
        elif 'pvalue_corrected_threshold' in enrichment_options_I:
            data_filtered_tmp = data_listDict.dataFrame[(data_listDict.dataFrame.pvalue_corrected < enrichment_options_I['pvalue_corrected_threshold'])];
            data_filtered = listDict(dataFrame_I=data_filtered_tmp);
            data_filtered.convert_dataFrame2ListDict();
        else:
            print('no filtering threshold criteria recognized.')
            data_filtered = data_listDict;
        return data_filtered;

    def calculate_enrichment_topGO(self,
            data_I,
            enrichment_method_I,
            enrichment_options_I,
            r_calc):
        
        genes_w_pvals = {d['component_group_name']:d['pvalue_corrected'] for d in data_I};
               
        if 'pvalue_threshold' in enrichment_options_I:
            pvalue_threshold =  enrichment_options_I['pvalue_threshold']
        elif 'pvalue_corrected_threshold' in enrichment_options_I:
            pvalue_threshold =  enrichment_options_I['pvalue_corrected_threshold']
        r_calc.make_topDiffGenes(
                topDiffGenes_O = 'topDiffGenes',
                pvalue_I = enrichment_options_I['pvalue_corrected_threshold']
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

    #TODO:
    #1. combine enrichment and geneSetEnrichment
    #2. refactor to include updates in pairWiseEnrichment
    def execute_enrichment(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
            enrichment_method_I='hypergeometric',
            enrichment_options_I={'pvalue_threshold':0.05,
                                  'enrichment_class_database':'iJO1366_metabolites',
                                  'use_weights':False},
            pvalue_corrected_description_I = "bonferroni",
            query_object_descStats_I = 'stage02_quantification_dataPreProcessing_averages_query',
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingAverages',
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
        
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calculateenrichment = calculate_enrichment();
        
        enrichment_O = [];

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query,
                        };
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();
            
        #query the data:
        data_listDict = [];
        if hasattr(query_instance_descStats, query_func_descStats_I):
            query_func_descStats = getattr(query_instance_descStats, query_func_descStats_I);
            try:
                #preProcessingAverages and descStats
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
            except AssertionError as e:
                print(e);

        else:
            print('query instance does not have the required method.');

        #reorganize into analysis groups:
        data_analysis = {'delete':{'delete':[]}};
        for row in data_listDict:
            unique = (row['analysis_id'],
                      row['calculated_concentration_units'],
                      row['experiment_id'],
                      row['sample_name_abbreviation'],
                      row['time_point']);
            if not unique in data_analysis.keys(): data_analysis[unique]=[];
            data_analysis[unique].append(row);
        del data_analysis['delete'];

        if enrichment_method_I in ['hypergeometric']:
            #get the enrichment class information
            enrichment_classes = None;
            enrichment_classes = self.get_rows_enrichmentClassDatabase_dataStage02QuantificationEnrichmentClasses(
                enrichment_options_I['enrichment_class_database']);
            enrichment_classes_listDict = listDict(listDict_I = enrichment_classes);
            enrichment_classes_listDict.convert_listDict2DataFrame();
            enrichment_classes_listDict.set_pivotTable(
                value_label_I = 'enrichment_class_weight',
                row_labels_I = ['enrichment_class'],
                column_labels_I = ['component_name'],
                );
            enrichment_matrix = enrichment_classes_listDict.get_dataMatrix();

        #apply the analysis to each group:
        for unique,data in data_analysis.items():
            # check for the pvalue cutoff:
            data_filtered = self._filter_enrichmentData(data,enrichment_options_I);
            if len(data_filtered)<1: continue;

            if enrichment_method_I in ['hypergeometric']:
                #calculate the pvalues
                pvalues = self.calculate_enrichment_hypergeometric(
                    data_listDict,
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
                data_listDict = listDict(dictList_I={'pvalue':pvalues});
                data_listDict.convert_dictList2DataFrame();
                # call R
                r_calc.clear_workspace();
                r_calc.make_vectorFromList(pvalues,'pvalues');
                pvalue_corrected = r_calc.calculate_pValueCorrected(
                    'pvalues',
                    'pvalues_O',method_I = pvalue_corrected_description_I);
                # add in the corrected p-values
                data_listDict.add_column2DataFrame('pvalue_corrected', pvalue_corrected);
                data_listDict.add_column2DataFrame('pvalue_corrected_description', pvalue_corrected_description_I);
                # add in the rest of the information
                data_listDict.add_column2DataFrame('analysis_id', analysis_id_I);
                data_listDict.add_column2DataFrame('calculated_concentration_units', data[0]['calculated_concentration_units']);
                data_listDict.add_column2DataFrame('experiment_id', data[0]['experiment_id']);
                data_listDict.add_column2DataFrame('sample_name_abbreviation', data[0]['sample_name_abbreviation']);
                data_listDict.add_column2DataFrame('time_point', data[0]['time_point']);
                data_listDict.add_column2DataFrame('enrichment_options', enrichment_options_I);
                data_listDict.add_column2DataFrame('enrichment_method', enrichment_method_I);
                data_listDict.add_column2DataFrame('test_description', enrichment_method_I);
                data_listDict.add_column2DataFrame('used_', True);
                data_listDict.add_column2DataFrame('comment_', None);
                data_listDict.convert_dataFrame2ListDict();
                enrichment_O.extend(data_listDict.get_listDict());

        self.add_rows_table('data_stage02_quantification_enrichment',enrichment_O);
    def execute_geneSetEnrichment(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
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
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingAverages',
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
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        enrichment_O = [];
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();
            

        if enrichment_method_I in ['topGO']:
            r_calc.import_GODB(enrichment_options_I['GO_database'])
            r_calc.import_GODB(enrichment_options_I['GO_annotation_mapping'])
                    
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
        data_analysis = {'delete':{'delete':[]}};
        for row in data_listDict:
            unique = (row['analysis_id'],
                      row['calculated_concentration_units'],
                      row['experiment_id'],
                      row['sample_name_abbreviation'],
                      row['time_point']);
            if not unique in data_analysis.keys(): data_analysis[unique]=[];
            data_analysis[unique].append(row);
        del data_analysis['delete'];

        #apply the analysis to each group:
        for unique,data in data_analysis.items():

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
                data_listDict.add_column2DataFrame('calculated_concentration_units', data[0]['calculated_concentration_units']);
                data_listDict.add_column2DataFrame('experiment_id', data[0]['experiment_id']);
                data_listDict.add_column2DataFrame('sample_name_abbreviation', data[0]['sample_name_abbreviation']);
                data_listDict.add_column2DataFrame('time_point', data[0]['time_point']);
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