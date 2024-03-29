﻿# SBaaS
from .stage02_quantification_heatmap_io import stage02_quantification_heatmap_io
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query

# Resources
#from .heatmap import heatmap
from python_statistics.calculate_heatmap import calculate_heatmap
from listDict.listDict import listDict

class stage02_quantification_heatmap_execute(stage02_quantification_heatmap_io,):
    def execute_heatmap(self, analysis_id_I,calculated_concentration_units_I=[],
                sample_name_shorts_I=[],component_names_I=[],
                row_pdist_metric_I='euclidean',row_linkage_method_I='complete',
                col_pdist_metric_I='euclidean',col_linkage_method_I='complete',
                order_componentNameBySampleNameShort_I = True,
                order_sample_name_shorts_I=False,
                order_component_names_I=False,
            experiment_ids_I = [],
            time_points_I = [],
            sample_name_abbreviations_I = [],
            component_group_names_I = [],
            where_clause_I = None,
            query_object_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates',
            includeAll_calculatedConcentrationUnits_I=False,
                ):
        '''Execute hierarchical cluster on row and column data corresponding
        INPUT:
        analysis_id_I = string, analysis id
        sample_name_shorts_I = list of sample_name_shorts
        concentration_units_I = list of concentration units
        component_names_I = list of component_names
        observable_only_I = include only observable reactions
        order_componentNameBySampleNameShort_I = if True, rows will represent the concentrations and columns will represent the sample_name_short
                           if False, rows will represent the sample_name_shorts and columns will represent the concentrations
        order_sample_name_shorts_I = if True, order of the sample_name_shorts will be kept
        order_component_names_I = if True, order of the component_names will be kept
        '''

        print('executing heatmap...');
        calculateheatmap = calculate_heatmap();

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance = query_object(self.session,self.engine,self.settings);
            query_instance.initialize_supportedTables();

        heatmap_O = [];
        dendrogram_col_O = [];
        dendrogram_row_O = [];
        
        #query the data:
        data_listDict = [];
        if hasattr(query_instance, query_func_I):
            query_func = getattr(query_instance, query_func_I);
            try:
                data_listDict = query_func(analysis_id_I,
                    calculated_concentration_units_I=calculated_concentration_units_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    sample_name_shorts_I=sample_name_shorts_I,
                    sample_name_abbreviations_I=sample_name_abbreviations_I,
                    time_points_I=time_points_I,
                    experiment_ids_I=experiment_ids_I,
                    where_clause_I=where_clause_I,
                    );
            except AssertionError as e:
                print(e);
        else:
            print('query instance does not have the required method.');

        #reorganize into analysis groups:
        calculated_concentration_units = list(set([c['calculated_concentration_units'] for c in data_listDict]));
        calculated_concentration_units.sort();
        data_analysis = {'_del_':[]};
        for row in data_listDict:
            if includeAll_calculatedConcentrationUnits_I:
                cu = ','.join(calculated_concentration_units);
            else:
                cu = row['calculated_concentration_units']
            if not cu in data_analysis.keys(): data_analysis[cu]=[];
            data_analysis[cu].append(row);
        del data_analysis['_del_'];

        #apply the analysis to each group
        for cu in calculated_concentration_units:
            print('generating a heatmap for concentration_units ' + cu);
            # get the data
            data = data_analysis[cu];
            # generate the clustering for the heatmap
            heatmap_1 = [];
            dendrogram_col_1 = {};
            dendrogram_row_1 = {};
            if order_componentNameBySampleNameShort_I:
                heatmap_1,dendrogram_col_1,dendrogram_row_1 = calculateheatmap.make_heatmap(data,
                    'component_name','sample_name_short','calculated_concentration',
                    row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
                    col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I,
                    filter_rows_I=component_names_I,
                    filter_columns_I=sample_name_shorts_I,
                    order_rowsFromTemplate_I=component_names_I,
                    order_columnsFromTemplate_I=sample_name_shorts_I,);
            else:
                heatmap_1,dendrogram_col_1,dendrogram_row_1 = calculateheatmap.make_heatmap(data,
                    'sample_name_short','component_name','calculated_concentration',
                    row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
                    col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I,
                    filter_rows_I=sample_name_shorts_I,
                    filter_columns_I=component_names_I,
                    order_rowsFromTemplate_I=sample_name_shorts_I,
                    order_columnsFromTemplate_I=component_names_I,);
            # add data to to the database for the heatmap
            for d in heatmap_1:
                d['analysis_id']=analysis_id_I;
                d['value_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                heatmap_O.append(d);
            # add data to the database for the dendrograms
            #if dendrogram_col_1['leaves'].__sizeof__() < 8191:
            dendrogram_col_1['analysis_id']=analysis_id_I;
            dendrogram_col_1['value_units']=cu;
            dendrogram_col_1['used_']=True;
            dendrogram_col_1['comment_']=None;
            dendrogram_col_O.append(dendrogram_col_1);
            #if dendrogram_row_1['leaves'].__sizeof__() < 8191:
            dendrogram_row_1['analysis_id']=analysis_id_I;
            dendrogram_row_1['value_units']=cu;
            dendrogram_row_1['used_']=True;
            dendrogram_row_1['comment_']=None;
            dendrogram_row_O.append(dendrogram_row_1);
        self.add_rows_table('data_stage02_quantification_heatmap',heatmap_O);
        self.add_rows_table('data_stage02_quantification_dendrogram',dendrogram_col_O);
        self.add_rows_table('data_stage02_quantification_dendrogram',dendrogram_row_O);
    def execute_heatmap_descriptiveStats(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                sample_name_abbreviations_I=[],
                component_names_I=[],
                row_pdist_metric_I='euclidean',row_linkage_method_I='complete',
                col_pdist_metric_I='euclidean',col_linkage_method_I='complete',
                order_componentNameBySampleNameAbbreviation_I = True,
                order_sample_name_abbreviations_I=False,
                order_component_names_I=False,
                value_I = 'mean',
            includeAll_calculatedConcentrationUnits_I=False,
            component_group_names_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
                query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats',
                convert_idCoord2DistanceAndNode_I = False
                ):
        '''Execute hierarchical cluster on row and column data corresponding
        INPUT:
        analysis_id_I = string, analysis id
        sample_name_abbreviations_I = list of sample_name_abbreviations
        concentration_units_I = list of concentration units
        component_names_I = list of component_names
        observable_only_I = include only observable reactions
        order_componentNameBySampleNameAbbreviation_I = if True, rows will represent the concentrations and columns will represent the sample_name_abbreviation
                           if False, rows will represent the sample_name_abbreviations and columns will represent the concentrations
        order_sample_name_abbreviations_I = if True, order of the sample_name_abbreviations will be kept
        order_component_names_I = if True, order of the component_names will be kept
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        convert_idCoord2DistanceAndNode_I = boolean, if True, convert from i/dcoord to distance/node
        '''

        print('executing heatmap from descriptiveStats...');

        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        calculateheatmap = calculate_heatmap();
        heatmap_O = [];
        dendrogram_col_O = [];
        dendrogram_row_O = [];
        
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
        data_analysis = {'_del_':[]};
        for row in data_listDict:
            if includeAll_calculatedConcentrationUnits_I:
                cu = ','.join(calculated_concentration_units);
            else:
                cu = row['calculated_concentration_units']
            if not cu in data_analysis.keys(): data_analysis[cu]=[];
            data_analysis[cu].append(row);
        del data_analysis['_del_'];

        for cu in calculated_concentration_units:
            print('generating a heatmap for concentration_units ' + cu);

            # generate the clustering for the heatmap
            heatmap_1 = [];
            dendrogram_col_1 = {};
            dendrogram_row_1 = {};
            if order_componentNameBySampleNameAbbreviation_I:
                heatmap_1,dendrogram_col_1,dendrogram_row_1 = calculateheatmap.make_heatmap(data_analysis[cu],
                    'component_name','sample_name_abbreviation',value_I,
                    row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
                    col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I,
                    filter_rows_I=component_names_I,
                    filter_columns_I=sample_name_abbreviations_I,
                    order_rowsFromTemplate_I=component_names_I,
                    order_columnsFromTemplate_I=sample_name_abbreviations_I,);
            else:
                heatmap_1,dendrogram_col_1,dendrogram_row_1 = calculateheatmap.make_heatmap(data_analysis[cu],
                    'sample_name_abbreviation','component_name',value_I,
                    row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
                    col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I,
                    filter_rows_I=sample_name_abbreviations_I,
                    filter_columns_I=component_names_I,
                    order_rowsFromTemplate_I=sample_name_abbreviations_I,
                    order_columnsFromTemplate_I=component_names_I,);
            # add data to to the database for the heatmap
            for d in heatmap_1:
                d['analysis_id']=analysis_id_I;
                d['value_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                heatmap_O.append(d);
            # add data to the database for the dendrograms
            if dendrogram_col_1 and not dendrogram_col_1 is None:
                dendrogram_col_1['analysis_id']=analysis_id_I;
                dendrogram_col_1['value_units']=cu;
                dendrogram_col_1['used_']=True;
                dendrogram_col_1['comment_']=None;
                dendrogram_col_O.append(dendrogram_col_1);
            if dendrogram_row_1 and not dendrogram_row_1 is None:
                dendrogram_row_1['analysis_id']=analysis_id_I;
                dendrogram_row_1['value_units']=cu;
                dendrogram_row_1['used_']=True;
                dendrogram_row_1['comment_']=None;
                dendrogram_row_O.append(dendrogram_row_1);
        if heatmap_O: self.add_rows_table('data_stage02_quantification_heatmap_descriptiveStats',heatmap_O);
        if dendrogram_col_O: self.add_rows_table('data_stage02_quantification_dendrogram_descriptiveStats',dendrogram_col_O);
        if dendrogram_row_O: self.add_rows_table('data_stage02_quantification_dendrogram_descriptiveStats',dendrogram_row_O);

    ##DEPRECATED
    def execute_heatmap_v1(self, analysis_id_I,calculated_concentration_units_I=[],
                sample_name_shorts_I=[],component_names_I=[],
                row_pdist_metric_I='euclidean',row_linkage_method_I='complete',
                col_pdist_metric_I='euclidean',col_linkage_method_I='complete',
                order_componentNameBySampleNameShort_I = True,
                order_sample_name_shorts_I=False,
                order_component_names_I=False,
                ):
        '''Execute hierarchical cluster on row and column data corresponding
        INPUT:
        analysis_id_I = string, analysis id
        sample_name_shorts_I = list of sample_name_shorts
        concentration_units_I = list of concentration units
        component_names_I = list of component_names
        observable_only_I = include only observable reactions
        order_componentNameBySampleNameShort_I = if True, rows will represent the concentrations and columns will represent the sample_name_short
                           if False, rows will represent the sample_name_shorts and columns will represent the concentrations
        order_sample_name_shorts_I = if True, order of the sample_name_shorts will be kept
        order_component_names_I = if True, order of the component_names will be kept
        '''

        print('executing heatmap...');
        calculateheatmap = calculate_heatmap();
        quantification_dataPreProcessing_replicates_query=stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);

        # query metabolomics data from the experiment
        heatmap_O = [];
        dendrogram_col_O = [];
        dendrogram_row_O = [];
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu in calculated_concentration_units:
            print('generating a heatmap for concentration_units ' + cu);
            # get the data
            data = [];
            data = quantification_dataPreProcessing_replicates_query.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            # will need to refactor in the future...
            if type(data)==type(listDict()):
                data.convert_dataFrame2ListDict()
                data = data.get_listDict();
            # generate the clustering for the heatmap
            heatmap_1 = [];
            dendrogram_col_1 = {};
            dendrogram_row_1 = {};
            if order_componentNameBySampleNameShort_I:
                heatmap_1,dendrogram_col_1,dendrogram_row_1 = calculateheatmap.make_heatmap(data,
                    'component_name','sample_name_short','calculated_concentration',
                    row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
                    col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I,
                    filter_rows_I=component_names_I,
                    filter_columns_I=sample_name_shorts_I,
                    order_rowsFromTemplate_I=component_names_I,
                    order_columnsFromTemplate_I=sample_name_shorts_I,);
            else:
                heatmap_1,dendrogram_col_1,dendrogram_row_1 = calculateheatmap.make_heatmap(data,
                    'sample_name_short','component_name','calculated_concentration',
                    row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
                    col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I,
                    filter_rows_I=sample_name_shorts_I,
                    filter_columns_I=component_names_I,
                    order_rowsFromTemplate_I=sample_name_shorts_I,
                    order_columnsFromTemplate_I=component_names_I,);
            # add data to to the database for the heatmap
            for d in heatmap_1:
                d['analysis_id']=analysis_id_I;
                d['value_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                heatmap_O.append(d);
            # add data to the database for the dendrograms
            #if dendrogram_col_1['leaves'].__sizeof__() < 8191:
            dendrogram_col_1['analysis_id']=analysis_id_I;
            dendrogram_col_1['value_units']=cu;
            dendrogram_col_1['used_']=True;
            dendrogram_col_1['comment_']=None;
            dendrogram_col_O.append(dendrogram_col_1);
            #if dendrogram_row_1['leaves'].__sizeof__() < 8191:
            dendrogram_row_1['analysis_id']=analysis_id_I;
            dendrogram_row_1['value_units']=cu;
            dendrogram_row_1['used_']=True;
            dendrogram_row_1['comment_']=None;
            dendrogram_row_O.append(dendrogram_row_1);
        self.add_rows_table('data_stage02_quantification_heatmap',heatmap_O);
        self.add_rows_table('data_stage02_quantification_dendrogram',dendrogram_col_O);
        self.add_rows_table('data_stage02_quantification_dendrogram',dendrogram_row_O);
    def execute_heatmap_descriptiveStats_v1(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                sample_name_abbreviations_I=[],
                component_names_I=[],
                row_pdist_metric_I='euclidean',row_linkage_method_I='complete',
                col_pdist_metric_I='euclidean',col_linkage_method_I='complete',
                order_componentNameBySampleNameAbbreviation_I = True,
                order_sample_name_abbreviations_I=False,
                order_component_names_I=False,
                value_I = 'mean',
                query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
                #testing...does not seem to have any benefit...
                export_dendrogram_I = False,
                convert_idCoord2DistanceAndNode_I = False
                ):
        '''Execute hierarchical cluster on row and column data corresponding
        INPUT:
        analysis_id_I = string, analysis id
        sample_name_abbreviations_I = list of sample_name_abbreviations
        concentration_units_I = list of concentration units
        component_names_I = list of component_names
        observable_only_I = include only observable reactions
        order_componentNameBySampleNameAbbreviation_I = if True, rows will represent the concentrations and columns will represent the sample_name_abbreviation
                           if False, rows will represent the sample_name_abbreviations and columns will represent the concentrations
        order_sample_name_abbreviations_I = if True, order of the sample_name_abbreviations will be kept
        order_component_names_I = if True, order of the component_names will be kept
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        export_dendrogram_I = boolean, if True, the dendrogram will be exported
        convert_idCoord2DistanceAndNode_I = boolean, if True, convert from i/dcoord to distance/node
        '''

        print('executing heatmap from descriptiveStats...');

        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        calculateheatmap = calculate_heatmap();
        # query metabolomics data from the experiment
        heatmap_O = [];
        dendrogram_col_O = [];
        dendrogram_row_O = [];
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu in calculated_concentration_units:
            print('generating a heatmap for concentration_units ' + cu);
            # get the data
            data = [];
            if hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                data = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
            elif hasattr(query_instance_descStats, 'get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                data = query_instance_descStats.get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
            else:
                print('query instance does not have the required method.');
            # generate the clustering for the heatmap
            heatmap_1 = [];
            dendrogram_col_1 = {};
            dendrogram_row_1 = {};
            if order_componentNameBySampleNameAbbreviation_I:
                heatmap_1,dendrogram_col_1,dendrogram_row_1 = calculateheatmap.make_heatmap(data,
                    'component_name','sample_name_abbreviation',value_I,
                    row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
                    col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I,
                    filter_rows_I=component_names_I,
                    filter_columns_I=sample_name_abbreviations_I,
                    order_rowsFromTemplate_I=component_names_I,
                    order_columnsFromTemplate_I=sample_name_abbreviations_I,);
            else:
                heatmap_1,dendrogram_col_1,dendrogram_row_1 = calculateheatmap.make_heatmap(data,
                    'sample_name_abbreviation','component_name',value_I,
                    row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
                    col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I,
                    filter_rows_I=sample_name_abbreviations_I,
                    filter_columns_I=component_names_I,
                    order_rowsFromTemplate_I=sample_name_abbreviations_I,
                    order_columnsFromTemplate_I=component_names_I,);
            # add data to to the database for the heatmap
            for d in heatmap_1:
                d['analysis_id']=analysis_id_I;
                d['value_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                heatmap_O.append(d);
            # add data to the database for the dendrograms
            dendrogram_col_1['analysis_id']=analysis_id_I;
            dendrogram_col_1['value_units']=cu;
            dendrogram_col_1['used_']=True;
            dendrogram_col_1['comment_']=None;
            dendrogram_col_O.append(dendrogram_col_1);
            dendrogram_row_1['analysis_id']=analysis_id_I;
            dendrogram_row_1['value_units']=cu;
            dendrogram_row_1['used_']=True;
            dendrogram_row_1['comment_']=None;
            dendrogram_row_O.append(dendrogram_row_1);
        self.add_rows_table('data_stage02_quantification_heatmap_descriptiveStats',heatmap_O);
        #Testing direct export of dendrogram
        if export_dendrogram_I:
            self.export_dataStage02QuantificationDendrogramDescriptiveStats_js(
                analysis_id_I,
                data_I=[dendrogram_col_O[0],dendrogram_row_O[0]]
                );
        else:
            self.add_rows_table('data_stage02_quantification_dendrogram_descriptiveStats',dendrogram_col_O);
            self.add_rows_table('data_stage02_quantification_dendrogram_descriptiveStats',dendrogram_row_O);
        #self.add_rows_table('data_stage02_quantification_dendrogram_descriptiveStats',dendrogram_col_O);
        #self.add_rows_table('data_stage02_quantification_dendrogram_descriptiveStats',dendrogram_row_O);