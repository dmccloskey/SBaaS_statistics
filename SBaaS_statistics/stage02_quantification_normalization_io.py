# System
import json
# SBaaS
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container_table import ddt_container_table
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable
from listDict.listDict import listDict

class stage02_quantification_normalization_io(stage02_quantification_normalization_query,
                                                   stage02_quantification_analysis_query,
                                                   sbaas_template_io):
    def export_data_stage02_quantification_glogNormalized_csv(self, analysis_id_I, filename_O,
                        experiment_id_I='%',
                        sample_name_short_I='%',
                        time_point_I='%',
                        component_name_I='%',
                        calculated_concentration_units_I='%'):
        '''export data_stage02_quantification_glogNormalized to .csv'''

        data = [];
        data = self.get_rows_unique_dataStage02GlogNormalized(analysis_id_I,
                        experiment_id_I,
                        sample_name_short_I,
                        time_point_I,
                        component_name_I,
                        calculated_concentration_units_I);
        if data:
            # write data to file
            export = base_exportData(data);
            export.write_dict2csv(filename_O);
    def export_dataStage02QuantificationGlogNormalized_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export a tabular representation of the data
        INPUT:
        analysis_id_I = string,
        '''

        #get the data for the analysis
        data_points_O = [];
        data_points_O = self.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02GlogNormalized(analysis_id_I);

        # dump chart parameters to a js files
        data1_keys = ['analysis_id',
                      'experiment_id',
                      'sample_name_abbreviation',
                      'sample_name_short',
                      'component_group_name',
                      'component_name',
                      'time_point',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {'xdata':'component_name',
                        'ydata':'calculated_concentration',
                        'serieslabel':'sample_name_abbreviation',
                        'featureslabel':'component_name'};

        ddttable = ddt_container_table()
        ddttable.make_container_table(data_points_O,data1_keys,data1_nestkeys,data1_keymap,tabletype='responsivecrosstable_01');

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddttable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddttable.get_allObjects());
    def export_dataStage02QuantificationGlogNormalizedCrossTable_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export a heatmap and cross-table representation of the data
        PLOTS:
        1. cross-table
        INPUT:
        analysis_id_I = string,
        '''

        #get the data for the analysis
        data_points_O = [];
        data_points_O = self.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02GlogNormalized(analysis_id_I);
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];

        # dump chart parameters to a js files
        data1_keys = ['analysis_id',
                      'experiment_id',
                      'sample_name_abbreviation',
                      'sample_name_short',
                      'component_group_name',
                      'component_name',
                      'time_point',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name','sample_name_short']; #rows,columns
        data1_keymap = {
            'xdata':'sample_name_short',
            'ydata':'component_name',
            'zdata':'calculated_concentration',
            'rowslabel':'component_name',
            'columnslabel':'sample_name_short',};
        
        ddttable = ddt_container_table()
        ddttable.make_container_table(data_points_O,data1_keys,data1_nestkeys,data1_keymap,tabletype='responsivecrosstable_01');

        # dump the data to a json file
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddttable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddttable.get_allObjects());
    def export_dataStage02QuantificationGlogNormalizedPairWiseReplicates_js(self, analysis_id_I,calculated_concentration_units_I=None, data_dir_I='tmp'):
        '''
        pairwise scatter plot of replicate data
        '''
        data_O = [];
        if calculated_concentration_units_I:
            data_O = self.get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02GlogNormalized(analysis_id_I,calculated_concentration_units_I);
        else:
            data_O = self.get_rows_analysisID_dataStage02GlogNormalized(analysis_id_I);
        # reorganize the data
        listdict = listDict(data_O);
        data_O,columnValueHeader_O = listdict.convert_listDict2ColumnGroupListDict(
                    value_labels_I = ['calculated_concentration',],
                    column_labels_I = ['experiment_id','sample_name_short','time_point','calculated_concentration_units'],
                    feature_labels_I = ['component_name','component_group_name'],
                    na_str_I=0.0,
                    columnValueConnector_str_I='_',
                    );
        # make the tile object
        #data1 = filtermenu/table
        data1_keymap_table = {
            'xdata':'',
            'ydata':'',
            'zdata':'',
            'rowslabel':'',
            'columnslabel':'',
            };     
        #data2 = svg
        #if single plot, data2 = filter menu, data2, and table
        data1_keys = ['component_name','component_group_name','experiment_id','sample_name_short','time_point','calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap_svg = [];
        svgtype = [];
        svgtile2datamap = [];
        data_svg_keymap = [];
        for cnt1,column1 in enumerate(columnValueHeader_O):
            for cnt2,column2 in enumerate(columnValueHeader_O[cnt1+1:]):
                keymap = {
                'xdata':column1,
                'ydata':column2,
                'serieslabel':'',
                'featureslabel':'component_name',
                'tooltipdata':'component_name',
                };
                data1_keymap_svg.append([keymap]);
                data_svg_keymap.append(keymap);
                svgtype.append('pcaplot2d_scores_01');
                svgtile2datamap.append([0]);

        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
                data_filtermenu=data_O,
                data_filtermenu_keys=data1_keys,
                data_filtermenu_nestkeys=data1_nestkeys,
                data_filtermenu_keymap=data1_keymap_table,
                data_svg_keys=data1_keys,
                data_svg_nestkeys=data1_nestkeys,
                data_svg_keymap=data_svg_keymap,
                data_table_keys=data1_keys,
                data_table_nestkeys=data1_nestkeys,
                data_table_keymap=data1_keymap_table,
                data_svg=None,
                data_table=None,
                svgtype=svgtype,
                tabletype='responsivetable_01',
                svgx1axislabel='',
                svgy1axislabel='',
                tablekeymap = [data1_keymap_table],
                svgkeymap = data1_keymap_svg,
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=svgtile2datamap,
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