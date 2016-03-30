# System
import json
# SBaaS
from .stage02_quantification_pairWiseCorrelation_query import stage02_quantification_pairWiseCorrelation_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container
from listDict.listDict import listDict
from ddt_python.ddt_container_heatmap import ddt_container_heatmap
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable

class stage02_quantification_pairWiseCorrelation_io(stage02_quantification_pairWiseCorrelation_query,sbaas_template_io):

    def export_dataStage02QuantificationPairWiseCorrelation_js(self,):
        '''table of correlations'''
        pass;

    def export_dataStage02QuantificationPairWiseCorrelationReplicates_heatmap_js(self,
                analysis_id_I,
                query_I={},
                data_dir_I='tmp'
                ):
        '''export a chord diagram
        INPUT:
        analysis_id_I = string
        query_I = {} of additional SQL query operators
        data_dir_I
        OUTPUT:
        '''

        #get the data
        data = [];        
        data_O = self.get_rows_analysisID_dataStage02QuantificationPairWiseCorrelationReplicates(analysis_id_I,
                query_I = query_I);
        data_O_listDict = listDict();
        data_O_listDict.set_listDict(data_O);
        data_O_listDict.convert_listDict2DataFrame();
        data_O_listDict.make_dummyIndexColumn('row_index','sample_name_short_1');
        data_O_listDict.make_dummyIndexColumn('col_index','sample_name_short_2');
        data_O_listDict.make_dummyIndexColumn('row_leaves','sample_name_short_1');
        data_O_listDict.make_dummyIndexColumn('col_leaves','sample_name_short_2');
        data_O_listDict.convert_dataFrame2ListDict();
        data_O = data_O_listDict.get_listDict();
        # make the tile objects  
        #data1 = filter menu and table  
        data1_keys = [
            'analysis_id',
            'sample_name_short_1',
            'sample_name_short_2',
            'row_index',
            'col_index',
            'row_leaves',
            'col_leaves',
            'calculated_concentration_units',
            'distance_measure'
            ]
        data1_nestkeys = [
            'sample_name_short_1',
            'sample_name_short_2'
            ];
        data1_keymap = {
            'xdata':'row_index',
            'ydata':'col_index',
            'zdata':'correlation_coefficient',
            'rowslabel':'sample_name_short_1',
            'columnslabel':'sample_name_short_2',
            'rowsindex':'row_index',
            'columnsindex':'col_index',
            'rowsleaves':'row_index',
            'columnsleaves':'col_index'
            };  

        #svgparameters={
        #        'svgcellsize':18,
        #        'svgmargin':{ 'top': 200, 'right': 50, 'bottom': 100, 'left': 200 },
        #        'svgcolorscale':'quantile',
        #        'svgcolorcategory':'blue2gold64RBG',
        #        'svgcolordomain':[0,1],
        #        'svgcolordatalabel':'correlation_coefficient',
        #        'svgdatalisttileid':'tile1'}
        
        #nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        #nsvgtable.make_filterMenuAndChart2dAndTable(
        #    data_filtermenu=data_O,
        #    data_filtermenu_keys=data1_keys,
        #    data_filtermenu_nestkeys=data1_nestkeys,
        #    data_filtermenu_keymap=data1_keymap,
        #    data_svg_keys=None,
        #    data_svg_nestkeys=None,
        #    data_svg_keymap=None,
        #    data_table_keys=None,
        #    data_table_nestkeys=None,
        #    data_table_keymap=None,
        #    data_svg=None,
        #    data_table=None,
        #    svgtype='heatmap2d_01',
        #    tabletype='responsivecrosstable_01',
        #    svgx1axislabel='',
        #    svgy1axislabel='',
        #    tablekeymap = [data1_keymap],
        #    svgkeymap = [data1_keymap],
        #    formtile2datamap=[0],
        #    tabletile2datamap=[0],
        #    svgtile2datamap=[0], #calculated on the fly
        #    svgfilters=None,
        #    svgtileheader='heatmap',
        #    svgparameters_I=svgparameters,
        #    tablefilters=None,
        #    tableheaders=None
        #    );

        #if data_dir_I=='tmp':
        #    filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        #elif data_dir_I=='data_json':
        #    data_json_O = nsvgtable.get_allObjects_js();
        #    return data_json_O;
        #with open(filename_str,'w') as file:
        #    file.write(nsvgtable.get_allObjects());

        # dump the data to a json file
        ddtheatmap = ddt_container_heatmap();
        ddtheatmap.make_container_heatmap(data_O,
            svgcolorcategory='blue2gold64RBG',
            svgcolordomain=[0,1],
            data1_keymap=data1_keymap,
            data1_keys=data1_keys,
            data1_nestkeys=data1_nestkeys,
            svgparameters_I={'svgcolordatalabel':'correlation_coefficient'}
            );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtheatmap.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtheatmap.get_allObjects());
   