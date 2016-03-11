# System
import json
# SBaaS
from .stage02_quantification_pairWiseTable_query import stage02_quantification_pairWiseTable_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable

class stage02_quantification_pairWiseTable_io(stage02_quantification_pairWiseTable_query,sbaas_template_io):
    def stage02_quantification_pairWiseTable_scatterPlot_js(self,):
        '''pairwise scatter plot'''
        pass;
    def stage02_quantification_pairWiseTableReplicates_scatterPlot_js(self,analysis_id_I,
                        query_I=None,
                        single_plot_I=False,
                        data_dir_I='tmp'):
        '''pairwise scatter plot
        '''

        data_O = self.get_rows_analysisID_dataStage02QuantificationPairWiseTableReplicates(analysis_id_I,
                query_I = query_I);

        # get the dictColumn
        data_dict_O = {};
        if not single_plot_I:
            dictColumn = 'sample_name_short_1';
            data_dict_O = self.get_rows_analysisID_dataStage02QuantificationPairWiseTableReplicates(
                analysis_id_I,
                query_I = query_I,
                output_O='dictColumn',
                dictColumn_I=dictColumn);
        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                      'sample_name_short_1',
                      'sample_name_short_2',
                      'component_name',
                      'component_group_name',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name','sample_name_short_1'];
        data1_keymap = {
            'xdata':'',
            'ydata':'',
            'zdata':'',
            'rowslabel':'',
            'columnslabel':'',
            'tooltipdata':'',
            };     
        #data2 = svg
        #if single plot, data2 = filter menu, data2, and table
        data2_keys = ['analysis_id',
                      'sample_name_short_1',
                      'sample_name_short_2',
                      'component_name',
                      'component_group_name',
                      'calculated_concentration_units'
                    ];
        data2_nestkeys = ['component_name'];
        data2_keymap = {
            'xdata':'calculated_concentration_1',
            'ydata':'calculated_concentration_2',
            #'serieslabel':'singular_value_index',
            'serieslabel':'calculated_concentration_units',
            'featureslabel':'component_name',
            #'tooltiplabel':'component_name',
            };
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        if not single_plot_I:
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
                svgtype='pcaplot2d_scores_01',
                tabletype='responsivetable_01',
                svgx1axislabel='',
                svgy1axislabel='',
                tablekeymap = [data1_keymap],
                svgkeymap = [], #calculated on the fly
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=[], #calculated on the fly
                svgfilters=None,
                svgtileheader='Pair-wise scatter plot',
                tablefilters=None,
                tableheaders=None
                );
        else:
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
                data_svg=None,
                data_table=None,
                svgtype='pcaplot2d_scores_01',
                tabletype='responsivetable_01',
                svgx1axislabel='',
                svgy1axislabel='',
                tablekeymap = [data1_keymap],
                svgkeymap = [data2_keymap],
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=[0], #calculated on the fly
                svgfilters=None,
                svgtileheader='Pair-wise scatter plot',
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
   