# System
import json
import copy
# SBaaS
from .stage02_quantification_covariance_query import stage02_quantification_covariance_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable
from ddt_python.ddt_container_scoresAndLoadings import ddt_container_scoresAndLoadings
from listDict.listDict import listDict
from python_statistics.calculate_covariance import calculate_covariance

class stage02_quantification_covariance_io(stage02_quantification_covariance_query,
                                    sbaas_template_io #abstract io methods
                                    ):
    def export_dataStage02QuantificationCovarianceSamples_js(self,analysis_id_I,
                        single_plot_I=False,
                        data_dir_I='tmp'):
        '''Export Covariance V matrix
        Plot = Bar plot
        Table
        '''

        
        data_O = self.get_rows_analysisID_dataStage02QuantificationCovarianceSamples(analysis_id_I);

        #TODO:
        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                      'component_group_name',
                      'singular_value_index',
                      'component_name',
                      'covariance_method',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name','singular_value_index'];
        data1_keymap = {
            'xdata':'component_name',
            'ydata':'singular_value_index',
            'zdata':'v_matrix',
            'rowslabel':'component_name',
            'columnslabel':'singular_value_index',
            'tooltipdata':'component_name',
            };     
        #data2 = svg
        #if single plot, data2 = filter menu, data2, and table
        data2_keys = ['analysis_id',
                      'component_group_name',
                      'singular_value_index',
                      'component_name',
                      'covariance_method',
                      'calculated_concentration_units'
                    ];
        data2_nestkeys = ['component_name'];
        data2_keymap = {
            'xdata':'component_name',
            'ydata':'v_matrix',
            #'serieslabel':'singular_value_index',
            'serieslabel':'covariance_method',
            'featuresslabel':'component_name',
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
                svgtileheader='Covariance V matrix',
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
    def export_dataStage02QuantificationCovarianceFeatures_js(self,analysis_id_I,
                        single_plot_I=False,
                        absolute_value_I=True,
                        data_dir_I='tmp'):
        '''Export Covariance U matrix
        Plot = Bar plot or scatter plot
        Table
        '''

        data_O = self.get_rows_analysisID_dataStage02QuantificationCovarianceFeatures(
            analysis_id_I,
            output_O='listDict',
            dictColumn_I=None);
        if absolute_value_I:
            for d in data_O:
                d['u_matrix'] = abs(d['u_matrix']);

        # get the dictColumn
        data_dict_O = {};
        if not single_plot_I:
            dictColumn = 'singular_value_index';
            #data_dict_O = self.get_rows_dataStage02QuantificationCovariance(
            data_dict_O = self.get_rows_analysisID_dataStage02QuantificationCovarianceU(
                analysis_id_I,
                output_O='dictColumn',
                dictColumn_I=dictColumn);
        if absolute_value_I:
            for k,v in data_dict_O.items():
                for d in v:
                    d['u_matrix'] = abs(d['u_matrix']);

        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                      'sample_name_abbreviation',
                      'sample_name_short',
                      'singular_value_index',
                      'covariance_method',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['sample_name_short','singular_value_index'];
        data1_keymap = {
            'xdata':'sample_name_short',
            'ydata':'singular_value_index',
            'zdata':'u_matrix',
            'rowslabel':'sample_name_short',
            'columnslabel':'singular_value_index',
            'tooltipdata':'sample_name_short',
            };     
        #data2 = svg
        #if single plot, data2 = filter menu, data2, and table
        data2_keys = ['analysis_id',
                      'sample_name_abbreviation',
                      'sample_name_short',
                      'singular_value_index',
                      'covariance_method',
                      'calculated_concentration_units'
                    ];
        data2_nestkeys = ['sample_name_short'];
        data2_keymap = {
            'xdata':'sample_name_short',
            'ydata':'u_matrix',
            #'serieslabel':'singular_value_index',
            'serieslabel':'covariance_method',
            'featuresslabel':'sample_name_short',
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
                svgtileheader='Covariance U matrix',
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
    #TODO:
    def export_dataStage02QuantificationCovarianceScoresAndLoadingsAndMethods_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export covariance scores and loadings plots for axis 1 vs. 2, 1 vs 3, and 2 vs 3'''

        calculatecovariance = calculate_covariance();
        PCs = [[1,1],[2,2],[3,3]];
        methods = [['covariance','robustSvd'],['covariance','robustSvd'],['covariance','robustSvd']];

        # get the data for the V matrix
        dictColumn = 'singular_value_index';
        data_v = self.get_rows_analysisID_dataStage02QuantificationCovarianceSamples(analysis_id_I,
            output_O='dictColumn',
            dictColumn_I=dictColumn);

        # get the U data
        data_u = [];
        tables = ['data_stage02_quantification_covariance_u'];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':self.convert_string2StringString(analysis_id_I),
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'used_',
            'value':'true',
            'operator':'IS',
            'connector':'AND'
                },
            {"table_name":tables[0],
            'column_name':'singular_value_index',
            'value':4,
            'operator':'<',
            'connector':'AND'
                },
	    ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'singular_value_index',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'covariance_method',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_short',
            'order':'ASC',
            },
        ];
        dictColumn = 'singular_value_index';
        data_u = self.get_rows_analysisID_dataStage02QuantificationCovarianceU(
            analysis_id_I,
            output_O='dictColumn',
            dictColumn_I=dictColumn);
        
        data_u_123,data_v_123,PCs_O = {},{},[];
        data_u_123,data_v_123,PCs_O = calculatecovariance.extract_UAndVMatrices_2D_byPCAndMethod(
            data_u,data_v,PCs,methods,
            score_column_I = 'u_matrix',
            loadings_column_I = 'v_matrix',
            method_column_I='covariance_method');

        # make the tile objects      
        data1_keys = ['analysis_id',
                      'sample_name_abbreviation',
                      'sample_name_short',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['sample_name_abbreviation'];
        data2_keys = ['analysis_id',
                      'component_name',
                      'component_group_name',
                      'calculated_concentration_units'
            ];
        data2_nestkeys = ['analysis_id'];
        data1_keymap_serieslabel = 'sample_name_abbreviation';
        data1_keymap_featureslabel = 'sample_name_short';
        data2_keymap_serieslabel = '';
        data2_keymap_featureslabel = 'component_group_name';
        
        # dump the data to a json file
        scoresandloadings = ddt_container_scoresAndLoadings();
        scoresandloadings.make_scoresAndLoadings(
            data_u_123,data_v_123,
            PCs_O,
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