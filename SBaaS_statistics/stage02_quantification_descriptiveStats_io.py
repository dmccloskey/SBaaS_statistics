# System
import json
# SBaaS
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container

class stage02_quantification_descriptiveStats_io(stage02_quantification_descriptiveStats_query,
                                                 stage02_quantification_analysis_query,
                                         stage02_quantification_normalization_query,
                                                 sbaas_template_io):
    def export_dataStage02QuantificationDescriptiveStats_js(self,analysis_id_I,plot_points_I=True,vertical_I=True,data_dir_I='tmp'):
        '''Export data for a box and whiskers plot
        INPUT:
        analysis_id_I = string,
        plot_points_I = boolean, default=False, raw data points will not be plotted on the same plot
        vertical_I = boolean, default=True, orient the boxes vertical as opposed to horizontal
        '''
        quantification_dataPreProcessing_replicates_query=stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);

        #get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        #get the data for the analysis
        if plot_points_I:
        #get the replicate data for the analysis
            data_points_O = [];
            data_points_O = quantification_dataPreProcessing_replicates_query.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            #data_points_O = self.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02GlogNormalized(analysis_id_I);
            data_O = [];
            data_O = self.get_rows_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        else:
            data_O = [];
            data_O = self.get_rows_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];
        # dump chart parameters to a js files
        data1_keys = ['analysis_id',
                      'experiment_id',
                      'sample_name_abbreviation',
                      'component_name',
                      'component_group_name',
                      'time_point',
                      'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data2_keys = ['analysis_id',
                      'experiment_id',
                      'sample_name_abbreviation',
                      'sample_name_short',
                      'component_group_name',
                      'component_name',
                      'time_point',
                      'calculated_concentration_units'
                    ];
        data2_nestkeys = ['component_name'];
        if vertical_I:
            data1_keymap = {'xdata':'component_name',
                        'ydatamean':'mean',
                        'ydatalb':'ci_lb',
                        'ydataub':'ci_ub',
                        'ydatamin':'min',
                        'ydatamax':'max',
                        'ydataiq1':'iq_1',
                        'ydataiq3':'iq_3',
                        'ydatamedian':'median',
                        'serieslabel':'sample_name_abbreviation',
                        'featureslabel':'component_name'};
            data2_keymap = {'xdata':'component_name',
                        'ydata':'calculated_concentration',
                        'serieslabel':'sample_name_abbreviation',
                        'featureslabel':'sample_name_short'};
        else:
            data1_keymap = {'ydata':'component_name',
                        'xdata':'mean',
                        'xdatamean':'mean',
                        'xdatalb':'ci_lb',
                        'xdataub':'ci_ub',
                        'xdatamin':'min',
                        'xdatamax':'max',
                        'xdataiq1':'iq_1',
                        'xdataiq3':'iq_3',
                        'xdatamedian':'median',
                        'serieslabel':'sample_name_abbreviation',
                        'featureslabel':'component_name'};
            data2_keymap = {'ydata':'component_name',
                        'xdata':'calculated_concentration',
                        'serieslabel':'sample_name_abbreviation',
                        'featureslabel':'sample_name_short'};

        # make the data object
        dataobject_O.append({"data":data_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys});

        # make the tile parameter objects
        formtileparameters_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-4"};
        formparameters_O = {'htmlid':'filtermenuform1',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit1','text':'submit'},"formresetbuttonidtext":{'id':'reset1','text':'reset'},"formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters_O.update(formparameters_O);
        parametersobject_O.append(formtileparameters_O);
        if plot_points_I:
            tile2datamap_O.update({"filtermenu1":[1]});
        else:
            tile2datamap_O.update({"filtermenu1":[0]});
        
        #make the svg object
        if plot_points_I and vertical_I:
            dataobject_O.append({"data":data_points_O,"datakeys":data2_keys,"datanestkeys":data2_nestkeys});
            svgparameters_O = {"svgtype":'boxandwhiskersplot2d_02',
                               "svgkeymap":[data1_keymap,data2_keymap],
                                'svgid':'svg1',
                                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                                "svgwidth":500,"svgheight":350,
                                "svgx1axislabel":"component_group_name",
                                "svgy1axislabel":"concentration",
                                "svgdata2pointsradius":5.0,
    						    };
            svgtileparameters_O = {'tileheader':'Custom box and whiskers plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
            svgtileparameters_O.update(svgparameters_O);
            parametersobject_O.append(svgtileparameters_O);
            tile2datamap_O.update({"tile2":[0,1]});
        elif not plot_points_I and vertical_I:
            svgparameters_O = {"svgtype":'boxandwhiskersplot2d_01',
                               "svgkeymap":[data1_keymap],
                                'svgid':'svg1',
                                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                                "svgwidth":500,"svgheight":350,
                                "svgx1axislabel":"component_group_name","svgy1axislabel":"concentration",
    						    'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
            svgtileparameters_O = {'tileheader':'Custom box and whiskers plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
            svgtileparameters_O.update(svgparameters_O);
            parametersobject_O.append(svgtileparameters_O);
            tile2datamap_O.update({"tile2":[0]});
        elif plot_points_I and not vertical_I:
            dataobject_O.append({"data":data_points_O,"datakeys":data2_keys,"datanestkeys":data2_nestkeys});
            svgparameters_O = {"svgtype":'horizontalBoxAndWhiskersPlot2d_02',
                               "svgkeymap":[data1_keymap,data2_keymap],
                                'svgid':'svg1',
                                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                                "svgwidth":500,"svgheight":350,
                                "svgx1axislabel":"concentration",
                                "svgy1axislabel":"component_group_name",
                                "svgdata2pointsradius":5.0,
    						    };
            svgtileparameters_O = {'tileheader':'Custom box and whiskers plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
            svgtileparameters_O.update(svgparameters_O);
            parametersobject_O.append(svgtileparameters_O);
            tile2datamap_O.update({"tile2":[0,1]});
        elif not plot_points_I and not vertical_I:
            svgparameters_O = {"svgtype":'horizontalBoxAndWhiskersPlot2d_01',
                               "svgkeymap":[data1_keymap],
                                'svgid':'svg1',
                                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                                "svgwidth":500,"svgheight":350,
                                "svgx1axislabel":"concentration",
                                "svgy1axislabel":"component_group_name",
    						    'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
            svgtileparameters_O = {'tileheader':'Custom box and whiskers plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
                'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
            svgtileparameters_O.update(svgparameters_O);
            parametersobject_O.append(svgtileparameters_O);
            tile2datamap_O.update({"tile2":[0]});

        #make the table object
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tablefilters":None,
                    "tableclass":"table  table-condensed table-hover",
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'descriptiveStats','tiletype':'table','tileid':"tile3",'rowid':"row2",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O.append(tabletileparameters_O);
        tile2datamap_O.update({"tile3":[0]});

        # dump the data to a json file
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = filtermenuobject_O);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());
   