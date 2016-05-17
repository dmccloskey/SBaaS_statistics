# System
import json
import copy
# SBaaS
from .stage02_quantification_pca_query import stage02_quantification_pca_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container_scoresAndLoadings import ddt_container_scoresAndLoadings
from ddt_python.ddt_container_biPlotAndValidation import ddt_container_biPlotAndValidation
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable
from listDict.listDict import listDict
from python_statistics.calculate_pca import calculate_pca

class stage02_quantification_pca_io(stage02_quantification_pca_query,sbaas_template_io):
    def export_dataStage02QuantificationPCAScoresAndLoadings_js(self,analysis_id_I,axis_I=3,data_dir_I='tmp'):
        '''Export pca scores and loadings plots for axis 1 vs. 2, 1 vs 3, and 2 vs 3'''

        calculatepca = calculate_pca();
        PCs = [[1,2],[1,3],[2,3]];

        # get the data
        data_scores = self.get_rowAxisDict_analysisID_dataStage02QuantificationPCAScores(analysis_id_I,axis_I)
        data_loadings = self.get_rowAxisDict_analysisID_dataStage02QuantificationPCALoadings(analysis_id_I,axis_I)
        data_scores_123,data_loadings_123 = {},{};
        data_scores_123,data_loadings_123 = calculatepca.extract_scoresAndLoadings_2D(data_scores,data_loadings,PCs);

        # make the tile objects      
        data1_keys = ['analysis_id',
                      'sample_name_abbreviation',
                      'sample_name_short',
                      'calculated_concentration_units',
                      'pca_model',
                      'pca_method',
                      'pca_options'
                    ];
        data1_nestkeys = ['sample_name_abbreviation'];
        data2_keys = ['analysis_id',
                      'component_name',
                      'component_group_name',
                      'calculated_concentration_units',
                      'pca_model',
                      'pca_method',
                      'pca_options'
            ];
        data2_nestkeys = ['analysis_id']; #scatter plot
        #data2_nestkeys = ['component_group_name']; #vertical bars plot
        data1_keymap_serieslabel = 'sample_name_abbreviation';
        data1_keymap_featureslabel = 'sample_name_short';
        data1_keymap_tooltiplabel = 'sample_name_short';
        data2_keymap_serieslabel = 'analysis_id';
        data2_keymap_featureslabel = 'component_group_name';
        data2_keymap_tooltiplabel = 'component_group_name';
        
        # dump the data to a json file
        scoresandloadings = ddt_container_scoresAndLoadings();
        scoresandloadings.make_scoresAndLoadings(
            data_scores_123,data_loadings_123,
            PCs,
            data1_keys,data1_nestkeys,
            data2_keys,data2_nestkeys,
            data1_keymap_serieslabel,data1_keymap_featureslabel,
            data2_keymap_serieslabel,data2_keymap_featureslabel,
            data1_keymap_tooltiplabel = data1_keymap_featureslabel,
            data2_keymap_tooltiplabel = data2_keymap_featureslabel,
            );
        
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = scoresandloadings.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(scoresandloadings.get_allObjects());
    def export_dataStage02QuantificationPCABiPlotAndValidation_js(self,analysis_id_I,data_dir_I='tmp'):
        '''
        Export the bi plot for the PCA components and validation plots for the pca model
        OUTPUT:
        biplot = scatterLinePlot of explained variances vs. component axis
        crossValidation plot = verticalBarPlot of MSEP, R2, and Q2 for increasing numbers of component axis
        OUTPUT TODO:
        permutation plot = p-value of permutation test
        '''

        #get the biplot data
        biplot_O = [];
        biplot_tmp = self.get_biPlotData_analysisID_dataStage02QuantificationPCAScores(analysis_id_I);
        listdict = listDict(biplot_tmp);
        biplot_O = listdict.convert_listDict2ListDictValues(
            value_key_name_I = 'var_value',
            value_label_name_I = 'var_label',
            value_labels_I=['var_proportion','var_cumulative']);
        #get the validation data
        validation_O = [];
        validation_tmp = self.get_rows_analysisID_dataStage02QuantificationPCAValidation(analysis_id_I);
        listdict = listDict(validation_tmp);
        validation_O = listdict.convert_listDict2ListDictValues(
            value_key_name_I = 'metric_value',
            value_label_name_I = 'metric_label',
            value_labels_I=['pca_msep','pca_rmsep','pca_r2','pca_q2']);

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                    'axis',
                    'var_label',
                    'pca_model',
                    'pca_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['var_label'];
        data1_keymap = {'xdata':'axis',
                        'ydata':'var_value',
                        'serieslabel':'var_label',
                        'featureslabel':'axis'};
        #define the data parameters for the validation
        data2_keys = ['analysis_id',
                    'pca_model',
                    'pca_method',
                    'metric_label',
                    'crossValidation_ncomp',
                    'crossValidation_method',
                    'calculated_concentration_units'
                    ];
        data2_nestkeys = ['crossValidation_ncomp'];
        data2_keymap = {'xdata':'crossValidation_ncomp',
                        'ydata':'metric_value',
                        'ydatalb':None,
                        'ydataub':None,
                        'serieslabel':'metric_label',
                        'featureslabel':'crossValidation_ncomp'};


        biplotandvalidation = ddt_container_biPlotAndValidation();
        biplotandvalidation.make_biPlotAndValidation(
            biplot_O,validation_O,
            data1_keys,data1_nestkeys,data1_keymap,
            data2_keys,data2_nestkeys,data2_keymap,
            );

        # export the data
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = biplotandvalidation.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(biplotandvalidation.get_allObjects());

    def export_dataStage02QuantificationPCAScores_js(
        self,analysis_id_I,
        axis_I=5,
        single_plot_I=False,
        absolute_value_I=True,
        data_dir_I='tmp'):
        '''Export pls scores as a bar plot and table
        Plot 1: bar plot of scores
        Table 1:  tabular display of scores
        TODO: copy/paste from loadings
        '''

        data_O = self.get_rows_analysisID_dataStage02QuantificationPCAScores(analysis_id_I,axis_I=axis_I);
        if absolute_value_I:
            for d in data_O:
                d['score'] = abs(d['score']);

        # get the dictColumn
        data_dict_O = {};
        if not single_plot_I:
            data_dict_O = self.get_rowAxisDict_analysisID_dataStage02QuantificationPCAScores(
                analysis_id_I,axis_I=axis_I);
        if absolute_value_I:
            for k,v in data_dict_O.items():
                for d in v:
                    d['score'] = abs(d['score']);

        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                      'sample_name_abbreviation',
                      'axis',
                      'sample_name_short',
                      'pca_method',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['sample_name_short','axis'];
        data1_keymap = {
            'xdata':'sample_name_short',
            'ydata':'axis',
            'zdata':'score',
            'rowslabel':'sample_name_short',
            'columnslabel':'axis',
            'tooltipdata':'sample_name_short',
            };     
        #data2 = svg
        #if single plot, data2 = filter menu, data2, and table
        data2_keys = ['analysis_id',
                      'sample_name_abbreviation',
                      'axis',
                      'sample_name_short',
                      'pls_method',
                      'calculated_concentration_units'
                    ];
        data2_nestkeys = [
            'sample_name_short',
            #'axis'
            ];
        data2_keymap = {
            'xdata':'sample_name_short',
            'ydata':'score',
            #'serieslabel':'axis',
            'serieslabel':'sample_name_abbreviation',
            'featureslabel':'sample_name_short',
            'tooltiplabel':'sample_name_short',
            'tooltipdata':'score',
            };
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
                data_filtermenu=data_O,
                data_filtermenu_keys=data1_keys,
                data_filtermenu_nestkeys=data1_nestkeys,
                data_filtermenu_keymap=data1_keymap,
                data_svg_keys=data2_keys,
                data_svg_nestkeys=data2_nestkeys,
                data_svg_keymap=data2_keymap,
                data_table_keys=None,
                data_table_nestkeys=None,
                data_table_keymap=None,
                data_svg=data_dict_O,
                data_table=None,
                svgtype='verticalbarschart2d_01',
                tabletype='responsivetable_01',
                svgx1axislabel='',
                svgy1axislabel='',
                tablekeymap = [data1_keymap],
                svgkeymap = [], #calculated on the fly
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=[], #calculated on the fly
                svgfilters=None,
                svgtileheader='PCA scores',
                tablefilters=None,
                tableheaders=None
                );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());
    
    def export_dataStage02QuantificationPCALoadings_js(
        self,analysis_id_I,
        axis_I=5,
        single_plot_I=False,
        absolute_value_I=True,
        data_dir_I='tmp'):
        '''Export pca loadings as a bar plot and in tabular form
        Plot 1: bar plot of loadings
        Table 1:  tabular display of loadings data

        TODO:
        convert get_rows_... query to use of listDict as in SVD
        '''

        data_O = self.get_rows_analysisID_dataStage02QuantificationPCALoadings(analysis_id_I,axis_I=axis_I);
        if absolute_value_I:
            for d in data_O:
                d['loadings'] = abs(d['loadings']);

        # get the dictColumn
        data_dict_O = {};
        if not single_plot_I:
            data_dict_O = self.get_rowAxisDict_analysisID_dataStage02QuantificationPCALoadings(
                analysis_id_I,axis_I=axis_I);
        if absolute_value_I:
            for k,v in data_dict_O.items():
                for d in v:
                    d['loadings'] = abs(d['loadings']);

        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                      'component_group_name',
                      'axis',
                      'component_name',
                      'pca_method',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name','axis'];
        data1_keymap = {
            'xdata':'component_name',
            'ydata':'axis',
            'zdata':'loadings',
            'rowslabel':'component_name',
            'columnslabel':'axis',
            'tooltipdata':'component_name',
            };     
        #data2 = svg
        #if single plot, data2 = filter menu, data2, and table
        data2_keys = ['analysis_id',
                      'component_group_name',
                      'axis',
                      'component_name',
                      'pca_method',
                      'calculated_concentration_units'
                    ];
        data2_nestkeys = ['component_name'];
        data2_keymap = {
            'xdata':'component_name',
            'ydata':'loadings',
            #'serieslabel':'axis',
            'serieslabel':'pca_method',
            'featureslabel':'component_name',
            'tooltiplabel':'component_name',
            'tooltipdata':'loadings',
            };
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
                data_filtermenu=data_O,
                data_filtermenu_keys=data1_keys,
                data_filtermenu_nestkeys=data1_nestkeys,
                data_filtermenu_keymap=data1_keymap,
                data_svg_keys=data2_keys,
                data_svg_nestkeys=data2_nestkeys,
                data_svg_keymap=data2_keymap,
                data_table_keys=None,
                data_table_nestkeys=None,
                data_table_keymap=None,
                data_svg=data_dict_O,
                data_table=None,
                svgtype='verticalbarschart2d_01',
                tabletype='responsivetable_01',
                svgx1axislabel='',
                svgy1axislabel='',
                tablekeymap = [data1_keymap],
                svgkeymap = [], #calculated on the fly
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=[], #calculated on the fly
                svgfilters=None,
                svgtileheader='PCA loadings',
                tablefilters=None,
                tableheaders=None
                );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());
   