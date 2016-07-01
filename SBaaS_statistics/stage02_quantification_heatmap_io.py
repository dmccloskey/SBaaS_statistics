# System
import json
# SBaaS
from .stage02_quantification_heatmap_query import stage02_quantification_heatmap_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container_heatmap import ddt_container_heatmap
from python_statistics.calculate_heatmap import calculate_heatmap
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable

class stage02_quantification_heatmap_io(stage02_quantification_heatmap_query,sbaas_template_io):
    def export_dataStage02QuantificationHeatmap_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export data as a heatmap'''

        #get the heatmap data for the analysis
        data_O = self.get_rows_analysisID_dataStage02QuantificationHeatmap(analysis_id_I);

        # dump the data to a json file
        ddtheatmap = ddt_container_heatmap();
        ddtheatmap.make_container_heatmap(data_O,
            svgcolorcategory='blue2gold64RBG',
            svgcolordomain='min,0,max');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtheatmap.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtheatmap.get_allObjects());

    def export_dataStage02QuantificationHeatmapDescriptiveStats_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export data as a heatmap'''

        #get the heatmap data for the analysis
        data_O = self.get_rows_analysisID_dataStage02QuantificationHeatmapDescriptiveStats(analysis_id_I);

        # dump the data to a json file
        ddtheatmap = ddt_container_heatmap();
        ddtheatmap.make_container_heatmap(data_O,
            svgcolorcategory='blue2gold64RBG',
            svgcolordomain='min,max');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtheatmap.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtheatmap.get_allObjects());

    def export_dataStage02QuantificationDendrogram_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export data as a dendrogram'''

        data_col_O = [];
        data_row_O = [];
        #get the dendrogram data for the analysis
        data_tmp = self.get_rows_analysisID_dataStage02QuantificationDendrogram(analysis_id_I);

        #convert from i/dcoord to distance/node
        for i,d in enumerate(data_tmp):
            nodes = [];
            if i%2==0:
                #component_names
                heatmap = calculate_heatmap(
                    dendrogram_row_I=d)
                nodes = heatmap.convert_idCoord2NodeDistance_dendrogramRow();
            else:                
                heatmap = calculate_heatmap(
                    dendrogram_col_I=d)
                nodes = heatmap.convert_idCoord2NodeDistance_dendrogramCol();
            for n in nodes:
                n['analysis_id']=d['analysis_id']
                n['pdist_metric']=d['pdist_metric']
                n['linkage_method']=d['linkage_method']
                n['value_units']=d['value_units']
                if i%2==0:
                    data_row_O.append(n);
                else:
                    data_col_O.append(n);


        # dump the data to a json file
        # make the data parameters
        data1_keys = [
                    'analysis_id','pdist_metric','linkage_method','value_units',
                    ];
        data1_nestkeys = [
            'analysis_id',
                          ];
        data1_keymap = {'xdata':'',
                        'ydata':'distance',
                        'serieslabel':'color',
                        'featureslabel':'name'};
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
                data_filtermenu=data_row_O,
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
                svgtype='radialdendrogram2d_01',
                #svgtype='treelayout2d_01',
                #svgtype='forcelayout2d_01',
                tabletype='responsivetable_01',
                svgx1axislabel='',
                svgy1axislabel='',
                tablekeymap = [data1_keymap],
                svgkeymap = [data1_keymap],
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=[0],
                svgfilters=None,
                svgtileheader='BioCyc Regulation',
                tablefilters=None,
                tableheaders=None,
                svgparameters_I= {
                            "svgmargin":{ 'top': 100, 'right': 100, 'bottom': 100, 'left': 100 },
                            "svgwidth":500,
                            "svgheight":500,
                            "svgduration":750,
                            "svgradius":250,
                            "datalastchild":'name',
                            'colclass':"col-sm-12"
                            }
                );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());
   