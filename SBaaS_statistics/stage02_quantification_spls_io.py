from .stage02_quantification_spls_query import stage02_quantification_spls_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
#Resources
from ddt_python.ddt_container import ddt_container
from ddt_python.ddt_container_scoresAndLoadings import ddt_container_scoresAndLoadings
from ddt_python.ddt_container_biPlotAndValidation import ddt_container_biPlotAndValidation
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable

from listDict.listDict import listDict
from python_statistics.calculate_pca import calculate_pca
import copy

class stage02_quantification_spls_io(stage02_quantification_spls_query,
                                    sbaas_template_io):
    '''
    TODO:
    7. validation: confusion matrix? (implement using a cross table)
    8. resampled: histogram
    9. compare plsda using spls to that found using pls
    10. port PCA methods to spls
    '''
    def export_dataStage02QuantificationSPLSScoresAndLoadings_js(self,analysis_id_I,axis_I=3,data_dir_I='tmp'):
        '''Export pls scores and loadings plots for axis 1 vs. 2, 1 vs 3, and 2 vs 3'''
        calculatepca = calculate_pca();
        PCs = [[1,2],[1,3],[2,3]];
        # reformat the data
        data_loadings = [];
        data_scores = [];
        data_loadings = self.get_SPlot_analysisID_dataStage02QuantificationSPLSLoadings(analysis_id_I,axis_I);        data_dict = {};
        data_loadings_dict = {}
        for d in data_loadings:
            if not d['axis'] in data_loadings_dict.keys():
                data_loadings_dict[d['axis']]=[];
            data_loadings_dict[d['axis']].append(d);
        data_scores = self.get_SPlot_analysisID_dataStage02QuantificationSPLSScores(analysis_id_I,axis_I);
        data_scores_dict = {}
        for d in data_scores:
            if not d['axis'] in data_scores_dict.keys():
                data_scores_dict[d['axis']]=[];
            data_scores_dict[d['axis']].append(d);
        data_scores_123,data_loadings_123 = {},{};
        data_scores_123,data_loadings_123 = calculatepca.extract_scoresAndLoadings_2D(
            data_scores_dict,data_loadings_dict,PCs);

        data1_keys = [
            'analysis_id',
            'response_name',
            'sample_name_short',
            'calculated_concentration_units',
            'pipeline_id',
                    ];
        data1_nestkeys = ['response_name'];
        data2_keys = [
            'analysis_id',
            'component_name',
            'component_group_name',
            'calculated_concentration_units',
            'pipeline_id',
                    ];
        data2_nestkeys = ['analysis_id'];
        data1_keymap_serieslabel = 'response_name';
        data1_keymap_featureslabel = 'sample_name_short';
        data2_keymap_serieslabel = '';
        data2_keymap_featureslabel = 'component_group_name';
        
        # dump the data to a json file
        scoresandloadings = ddt_container_scoresAndLoadings();
        scoresandloadings.make_scoresAndLoadings(
            data_scores_123,data_loadings_123,
            PCs,
            data1_keys,data1_nestkeys,
            data2_keys,data2_nestkeys,
            data1_keymap_serieslabel,data1_keymap_featureslabel,
            data2_keymap_serieslabel,data2_keymap_featureslabel,
            );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = scoresandloadings.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(scoresandloadings.get_allObjects());
    def export_dataStage02QuantificationSPLSBiPlot_js(self,analysis_id_I,axis_I=10,data_dir_I='tmp'):
        '''
        Export the bi plot for the SPLS components
        OUTPUT:
        biplot = scatterLinePlot of explained variances vs. component axis
        '''
        #get the biplot data
        biplot_O = [];
        biplot_O = self.get_rows_analysisID_dataStage02QuantificationSPLSAxis(analysis_id_I,axis_I);

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                    'axis',
                    'pipeline_id',
                    'metric_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['metric_method'];
        data1_keymap = {'xdata':'axis',
                        'ydata':'metric_value',
                        'serieslabel':'metric_method',
                        'featureslabel':'axis'};

        svgparameters={
            "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
            "svgwidth":500,"svgheight":350,
            "svgx1axislabel":"component",
            "svgy1axislabel":"variance explained",
            }

        biplotandvalidation = ddt_container_biPlotAndValidation();
        biplotandvalidation.make_biPlot(
            biplot_O,
            data1_keys,data1_nestkeys,data1_keymap,
            );
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = biplotandvalidation.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(biplotandvalidation.get_allObjects());
    def export_dataStage02QuantificationSPLSImpfeat_js(self,analysis_id_I,data_dir_I='tmp'):
        '''
        Export the SPLS important features
        OUTPUT:
        horizontal bar plot of important features
        '''
        #get the biplot data
        vip_O = [];
        vip_O = self.get_rows_analysisID_dataStage02QuantificationSPLSImpfeat(analysis_id_I);

        #initialize the ddt objects
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                    'response_name',
                    'component_name',
                    'component_group_name',
                    'pipeline_id',
                    'impfeat_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {
                        'xdata':'impfeat_value',
                        'ydata':'component_name',
                        'xdatalb':None,
                        'xdataub':None,
                        'serieslabel':'response_name',
                        'featureslabel':'component_name',
                        'tooltiplabel':'component_name'};#TODO: fix bug in tooltip

        biplotandvalidation = ddt_container_biPlotAndValidation();
        biplotandvalidation.make_impfeat(
            vip_O,
            data1_keys,data1_nestkeys,data1_keymap,
            );
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = biplotandvalidation.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(biplotandvalidation.get_allObjects());
    def export_dataStage02QuantificationSPLSHyperparameter_js(self,analysis_id_I,data_dir_I='tmp'):
        '''
        Export the hyperParameter search plots for the pls model
        OUTPUT:
        crossValidation plot = verticalBarPlot of metric scores for different cross validation parameters
        '''
        #get the validation data
        validation_O = [];
        validation_O = self.get_rows_analysisID_dataStage02QuantificationSPLSHyperparameter(analysis_id_I);

        #define the data parameters for the validation
        data1_keys = ['analysis_id',
                    'pipeline_id',
                    'pipeline_parameters',
                    'hyperparameter_id',
                    'hyperparameter_method',
                    'test_size',
                    'metric_method',
                    'crossval_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['pipeline_parameters'];
        data1_keymap = {'xdata':'pipeline_parameters',
                        'ydata':'metric_score',
                        'ydatalb':None,
                        'ydataub':None,
                        'serieslabel':'metric_method',
                        'featureslabel':'pipeline_parameters'};
        svgparameters={
            "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
            "svgwidth":500,"svgheight":350,
            "svgy1axislabel":"metric_score",
            }        

        biplotandvalidation = ddt_container_biPlotAndValidation();
        biplotandvalidation.make_hyperparameter(
            validation_O,
            data1_keys,data1_nestkeys,data1_keymap,
            );
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = biplotandvalidation.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(biplotandvalidation.get_allObjects());
    def export_dataStage02QuantificationSPLSSPlot_js(self,analysis_id_I,axis_I=3,data_dir_I='tmp'):
        '''
        Export the PLS S-plot of loadings (variable magnitude) vs. model correlation (variable reliability)
        for each component
        OUTPUT:
        scatter plot of loadings magnitude vs. loadings correlation
        '''

        # get data:
        data_loadings = [];
        data_loadings = self.get_SPlot_analysisID_dataStage02QuantificationSPLSLoadings(analysis_id_I,axis_I);
        data_dict = {};
        for d in data_loadings:
            if not d['axis'] in data_dict.keys():
                data_dict[d['axis']]=[];
            data_dict[d['axis']].append(d);                

        #initialize the ddt objects
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                      'pipeline_id',
                    'component_name',
                    'component_group_name',
                    'axis',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {
                        'xdata':'loadings',
                        'ydata':'correlations',
                        'serieslabel':'',
                        'featureslabel':'component_name'};           

        biplotandvalidation = ddt_container_biPlotAndValidation();
        biplotandvalidation.make_SPlot(
            data_loadings,data_dict,
            data1_keys,data1_nestkeys,data1_keymap,
            );
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = biplotandvalidation.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(biplotandvalidation.get_allObjects());
    def export_dataStage02QuantificationSPLSScores_js(
        self,analysis_id_I,
        axis_I=5,
        single_plot_I=False,
        absolute_value_I=True,
        data_dir_I='tmp'):
        '''Export pls scores as a bar plot and table
        Plot 1: bar plot of scores
        Table 1:  tabular display of scores
        '''
        
        query = {};
        query['where'] = [
            {"table_name":'data_stage02_quantification_spls_scores',
            'column_name':'axis',
            'value':axis_I,
            'operator':'<',
            'connector':'AND'
                        },
            #{"table_name":'data_stage02_quantification_spls_scores',
            #'column_name':'metric_method',
            #'value':'loadings',
            #'operator':'LIKE',
            #'connector':'AND'
            #            },
        ]

        #data_O = self.get_rows_analysisID_dataStage02QuantificationSPLSScores(analysis_id_I,axis_I=axis_I);
        data_O = self._get_rows_analysisID_dataStage02QuantificationSPLSScores(
            analysis_id_I,
            query_I=query,
            output_O='listDict',
            dictColumn_I=None
            )
        if absolute_value_I:
            for d in data_O:
                d['metric_value'] = abs(d['metric_value']);

        # get the dictColumn
        data_dict_O = {};
        if not single_plot_I:
            #data_dict_O = self.get_rowAxisDict_analysisID_dataStage02QuantificationSPLSScores(
            #    analysis_id_I,
            #    axis_I=axis_I);
            data_dict_O = self._get_rows_analysisID_dataStage02QuantificationSPLSScores(
                analysis_id_I,
                query_I=query,
                output_O='dictColumn',
                dictColumn_I='axis'
                )
        if absolute_value_I:
            for k,v in data_dict_O.items():
                for d in v:
                    d['metric_value'] = abs(d['metric_value']);

        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                      'pipeline_id',
                      'response_name',
                      'sample_name_short',
                      'axis',
                      'metric_method',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['sample_name_short','axis'];
        data1_keymap = {
            'xdata':'sample_name_short',
            'ydata':'axis',
            'zdata':'metric_value',
            'rowslabel':'sample_name_short',
            'columnslabel':'axis',
            'tooltipdata':'sample_name_short',
            };     
        #data2 = svg
        #if single plot, data2 = filter menu, data2, and table
        data2_keys = ['analysis_id',
                      'pipeline_id',
                      'response_name',
                      'sample_name_short',
                      'axis',
                      'metric_method',
                      'calculated_concentration_units'
                    ];
        data2_nestkeys = [
            'sample_name_short',
            #'axis'
            ];
        data2_keymap = {
            'xdata':'sample_name_short',
            'ydata':'metric_value',
            'serieslabel':'metric_method', #compare metric methods
            #'serieslabel':'pipeline_id', #compare methods
            'featureslabel':'sample_name_short',
            'tooltiplabel':'sample_name_short',
            'tooltipdata':'metric_value',
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
                svgtileheader='PLS scores',
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
    def export_dataStage02QuantificationSPLSLoadings_js(
        self,analysis_id_I,
        axis_I=5,
        single_plot_I=False,
        absolute_value_I=True,
        data_dir_I='tmp'):
        '''Export pls loadings as a bar plot and in tabular form
        Plot 1: bar plot of loadings
        Table 1:  tabular display of loadings data
        '''
        
        query = {};
        query['where'] = [
            {"table_name":'data_stage02_quantification_spls_loadings',
            'column_name':'axis',
            'value':axis_I,
            'operator':'<',
            'connector':'AND'
                        },
            #{"table_name":'data_stage02_quantification_spls_loadings',
            #'column_name':'metric_method',
            #'value':'loadings',
            #'operator':'LIKE',
            #'connector':'AND'
            #            },
        ]
        data_O = self._get_rows_analysisID_dataStage02QuantificationSPLSLoadings(
            analysis_id_I,
            query_I=query,
            output_O='listDict',
            dictColumn_I=None
            )
        #data_O = self.get_rows_analysisID_dataStage02QuantificationSPLSLoadings(analysis_id_I,axis_I=axis_I);
        if absolute_value_I:
            for d in data_O:
                d['metric_value'] = abs(d['metric_value']);

        # get the dictColumn
        data_dict_O = {};
        if not single_plot_I:
            #data_dict_O = self.get_rowAxisDict_analysisID_dataStage02QuantificationSPLSLoadings(
            #    analysis_id_I,axis_I=axis_I);
            data_dict_O = self._get_rows_analysisID_dataStage02QuantificationSPLSLoadings(
                analysis_id_I,
                query_I=query,
                output_O='dictColumn',
                dictColumn_I='axis'
                )
        if absolute_value_I:
            for k,v in data_dict_O.items():
                for d in v:
                    d['metric_value'] = abs(d['metric_value']);

        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                      'pipeline_id',
                      'component_group_name',
                      'component_name',
                      'axis',
                      'metric_method',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name','axis'];
        data1_keymap = {
            'xdata':'component_name',
            'ydata':'axis',
            'zdata':'metric_value',
            'rowslabel':'component_name',
            'columnslabel':'axis',
            'tooltipdata':'component_name',
            };     
        #data2 = svg
        #if single plot, data2 = filter menu, data2, and table
        data2_keys = ['analysis_id',
                      'pipeline_id',
                      'component_group_name',
                      'component_name',
                      'axis',
                      'metric_method',
                      'calculated_concentration_units'
                    ];
        data2_nestkeys = ['component_name'];
        data2_keymap = {
            'xdata':'component_name',
            'ydata':'metric_value',
            'serieslabel':'metric_method', #compare metric methods
            #'serieslabel':'pipeline_id', #compare methods
            'featureslabel':'component_name',
            'tooltiplabel':'component_name',
            'tooltipdata':'metric_value',
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
                svgtileheader='PLS Loadings Axis',
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

    def export_dataStage02QuantificationSPLSBiPlot_js_v1(self,analysis_id_I,axis_I=10,data_dir_I='tmp'):
        '''
        Export the bi plot for the SPLS components
        OUTPUT:
        biplot = scatterLinePlot of explained variances vs. component axis
        '''
        #get the biplot data
        biplot_O = [];
        biplot_O = self.get_rows_analysisID_dataStage02QuantificationSPLSAxis(analysis_id_I,axis_I);

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                    'axis',
                    'pipeline_id',
                    'metric_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['metric_method'];
        data1_keymap = {'xdata':'axis',
                        'ydata':'metric_value',
                        'serieslabel':'metric_method',
                        'featureslabel':'axis'};

        svgparameters={
            "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
            "svgwidth":500,"svgheight":350,
            "svgx1axislabel":"component",
            "svgy1axislabel":"variance explained",
            }
        #Also works, but without custom row/col ordering
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
            data_filtermenu=biplot_O,
            data_filtermenu_keys=data1_keys,
            data_filtermenu_nestkeys=data1_nestkeys,
            data_filtermenu_keymap=data1_keymap,
            data_svg_keys=None,
            data_svg_nestkeys=None,
            data_svg_keymap=None,
            data_table_keys=None,
            data_table_nestkeys=None,
            data_table_keymap=None,
            data_svg=None,
            data_table=None,
            svgtype='scatterlineplot2d_01',
            tabletype='responsivetable_01',
            svgx1axislabel='',
            svgy1axislabel='',
            tablekeymap = [data1_keymap],
            svgkeymap = [data1_keymap,data1_keymap],
            formtile2datamap=[0],
            tabletile2datamap=[0],
            svgtile2datamap=[0,0], #calculated on the fly
            svgfilters=None,
            svgtileheader='Biplot',
            tablefilters=None,
            tableheaders=None,
            svgparameters_I=svgparameters,
            );
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());
   