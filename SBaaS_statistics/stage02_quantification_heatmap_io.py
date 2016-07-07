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
                    ##will break stratify
                    #n['component_name']=n['name']
                    #n.pop('name')
                    data_row_O.append(n);
                else:
                    #n['sample_name']=n['name']
                    #n.pop('name')
                    data_col_O.append(n);


        # dump the data to a json file
        data1_keys = [
            'analysis_id','pdist_metric','linkage_method','value_units',
            ]
        data1_nestkeys = [
            'analysis_id'
            ];
        data2_keys = [
            'analysis_id','pdist_metric','linkage_method','value_units',
            ]
        data2_nestkeys = [
            'analysis_id'
            ];
        ddtheatmap = ddt_container_heatmap();
        ddtheatmap.make_container_dendrogram(data_col_O,data_row_O,
            svgcolorcategory='blue2gold64RBG',
            svgcolordomain='min,max');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtheatmap.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtheatmap.get_allObjects());
    def export_dataStage02QuantificationDendrogramDescriptiveStats_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export data as a dendrogram'''

        data_col_O = [];
        data_row_O = [];
        #get the dendrogram data for the analysis
        data_tmp = self.get_rows_analysisID_dataStage02QuantificationDendrogramDescriptiveStats(analysis_id_I);

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
                    ##will break stratify
                    #n['component_name']=n['name']
                    #n.pop('name')
                    data_row_O.append(n);
                else:
                    #n['sample_name']=n['name']
                    #n.pop('name')
                    data_col_O.append(n);


        # dump the data to a json file
        data1_keys = [
            'analysis_id','pdist_metric','linkage_method','value_units',
            ]
        data1_nestkeys = [
            'analysis_id'
            ];
        data2_keys = [
            'analysis_id','pdist_metric','linkage_method','value_units',
            ]
        data2_nestkeys = [
            'analysis_id'
            ];
        ddtheatmap = ddt_container_heatmap();
        ddtheatmap.make_container_dendrogram(data_col_O,data_row_O,
            svgcolorcategory='blue2gold64RBG',
            svgcolordomain='min,max');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtheatmap.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtheatmap.get_allObjects());
   