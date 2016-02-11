# SBaaS
from .stage02_quantification_heatmap_io import stage02_quantification_heatmap_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
# Resources
#from .heatmap import heatmap
from python_statistics.calculate_heatmap import calculate_heatmap
import numpy
# TODO: remove after making add methods
from .stage02_quantification_heatmap_postgresql_models import *

class stage02_quantification_heatmap_execute(stage02_quantification_heatmap_io,
                                         stage02_quantification_normalization_query,
                                         stage02_quantification_analysis_query,
                                         stage02_quantification_descriptiveStats_query):
    def execute_heatmap(self, analysis_id_I,concentration_units_I=[],
                sample_name_shorts_I=[],component_names_I=[],
                row_pdist_metric_I='euclidean',row_linkage_method_I='complete',
                col_pdist_metric_I='euclidean',col_linkage_method_I='complete',
                order_componentNameBySampleNameShort_I = True,
                #order_sample_name_shorts_I=False,
                #order_component_names_I=False,
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
        #hmap = heatmap();
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiment
        heatmap_O = [];
        dendrogram_col_O = [];
        dendrogram_row_O = [];
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            print('generating a heatmap for concentration_units ' + cu);
            # get the data
            data = [];
            data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
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
            ## find unique
            #if component_names_I:
            #    component_names = [x['component_name'] for x in data if x['component_name'] in component_names_I];
            #else:
            #    component_names = [x['component_name'] for x in data];
            #component_names_unique = list(set(component_names));
            #component_names_unique.sort();
            #if sample_name_shorts_I:
            #    sample_name_shorts = [x['sample_name_short'] for x in data if x['sample_name_short'] in sample_name_shorts_I];
            #else:
            #    sample_name_shorts = [x['sample_name_short'] for x in data];
            #sample_name_short_unique = list(set(sample_name_shorts));
            #sample_name_short_unique.sort();
            ## generate the frequency matrix data structure (sample x met)
            #if order_sample_name_shorts_I:
            #    sample_name_short_unique = hmap.order_labelsFromTemplate(sample_name_short_unique,sample_name_shorts_I);
            #if order_component_names_I:
            #    component_names_unique = hmap.order_labelsFromTemplate(component_names_unique,component_names_I);
            ## generate the heatmap matrix
            #col_cnt = 0;
            #if order_componentNameBySampleNameShort_I:
            #    # order 1: met x sample
            #    data_O = numpy.zeros((len(component_names_unique),len(sample_name_short_unique)));
            #    for component_name_cnt,component_name in enumerate(component_names_unique): 
            #        for sample_name_short_cnt,sample_name_short in enumerate(sample_name_short_unique):
            #            for row in data:
            #                if row['sample_name_short'] == sample_name_short and row['component_name'] == component_name:
            #                    data_O[component_name_cnt,sample_name_short_cnt] = row['calculated_concentration'];
            #        col_cnt+=1;
            #else:
            #    # generate the frequency matrix data structure (sample x met)
            #    data_O = numpy.zeros((len(sample_name_short_unique),len(component_names_unique)));
            #    # order 2: groups each lineage by met (sample x met)
            #    for sample_name_short_cnt,sample_name_short in enumerate(sample_name_short_unique): #all lineages for sample j / met i
            #        for component_name_cnt,component_name in enumerate(component_names_unique): #all mets i for sample j
            #            for row in data:
            #                if row['sample_name_short'] == sample_name_short and row['component_name'] == component_name:
            #                    data_O[sample_name_short_cnt,component_name_cnt] = row['calculated_concentration'];
            #        col_cnt+=1;
            ## generate the clustering for the heatmap
            #heatmap_O = [];
            #dendrogram_col_O = {};
            #dendrogram_row_O = {};
            #if order_componentNameBySampleNameShort_I:
            #    heatmap_O,dendrogram_col_O,dendrogram_row_O = hmap._make_heatmap(data_O,component_names_unique,sample_name_short_unique,
            #        row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
            #        col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I);
            #else:
            #    heatmap_O,dendrogram_col_O,dendrogram_row_O = hmap._make_heatmap(data_O,sample_name_short_unique,component_names_unique,
            #        row_pdist_metric_I=row_pdist_metric_I,row_linkage_method_I=row_linkage_method_I,
            #        col_pdist_metric_I=col_pdist_metric_I,col_linkage_method_I=col_linkage_method_I);
            # add data to to the database for the heatmap
            for d in heatmap_1:
                d['analysis_id']=analysis_id_I;
                d['value_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                heatmap_O.append(d);
                #row = None;
                #row = data_stage02_quantification_heatmap(
                #    analysis_id_I,
                #    d['col_index'],
                #    d['row_index'],
                #    d['value'],
                #    d['col_leaves'],
                #    d['row_leaves'],
                #    d['col_label'],
                #    d['row_label'],
                #    d['col_pdist_metric'],
                #    d['row_pdist_metric'],
                #    d['col_linkage_method'],
                #    d['row_linkage_method'],
                #    cu,
                #    True,
                #    None
                #    );
                #self.session.add(row);
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
        #    row = None;
        #    row = data_stage02_quantification_dendrogram(
        #        analysis_id_I,
        #        dendrogram_col_O['leaves'],
        #        dendrogram_col_O['icoord'],
        #        dendrogram_col_O['dcoord'],
        #        dendrogram_col_O['ivl'],
        #        dendrogram_col_O['colors'],
        #        dendrogram_col_O['pdist_metric'],
        #        dendrogram_col_O['pdist_metric'],
        #        cu,
        #        True,
        #        None
        #        );
        #    self.session.add(row);
        #    row = None;
        #    row = data_stage02_quantification_dendrogram(
        #        analysis_id_I,
        #        dendrogram_row_O['leaves'],
        #        dendrogram_row_O['icoord'],
        #        dendrogram_row_O['dcoord'],
        #        dendrogram_row_O['ivl'],
        #        dendrogram_row_O['colors'],
        #        dendrogram_row_O['pdist_metric'],
        #        dendrogram_row_O['pdist_metric'],
        #        cu, True, None);
        #    self.session.add(row);
        #self.session.commit();
        self.add_rows_table('data_stage02_quantification_heatmap',heatmap_O);
        self.add_rows_table('data_stage02_quantification_dendrogram',dendrogram_col_O);
        self.add_rows_table('data_stage02_quantification_dendrogram',dendrogram_row_O);
    def execute_heatmap_descriptiveStats(self, analysis_id_I,concentration_units_I=[],
                sample_name_abbreviations_I=[],
                component_names_I=[],
                row_pdist_metric_I='euclidean',row_linkage_method_I='complete',
                col_pdist_metric_I='euclidean',col_linkage_method_I='complete',
                order_componentNameBySampleNameAbbreviation_I = True,
                #order_sample_name_abbreviations_I=False,
                #order_component_names_I=False,
                value_I = 'mean'):
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
        '''

        print('executing heatmap...');
        calculateheatmap = calculate_heatmap();
        #hmap = heatmap();
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiment
        heatmap_O = [];
        dendrogram_col_O = [];
        dendrogram_row_O = [];
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        for cu in concentration_units:
            print('generating a heatmap for concentration_units ' + cu);
            # get the data
            data = [];
            data = self.get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
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
        self.add_rows_table('data_stage02_quantification_dendrogram_descriptiveStats',dendrogram_col_O);
        self.add_rows_table('data_stage02_quantification_dendrogram_descriptiveStats',dendrogram_row_O);