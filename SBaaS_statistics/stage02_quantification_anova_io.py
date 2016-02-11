# System
import json
# SBaaS
from .stage02_quantification_anova_query import stage02_quantification_anova_query
from .stage02_quantification_anova_dependencies import stage02_quantification_anova_dependencies
from SBaaS_base.sbaas_template_io import sbaas_template_io
from ddt_python.ddt_container import ddt_container
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class stage02_quantification_anova_io(stage02_quantification_anova_query,
                                      stage02_quantification_anova_dependencies,
                                      sbaas_template_io):
    
    def export_dataStage02QuantificationAnova_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export data for an anova plot'''
        
        #get the data for the analysis
        data_O = [];
        data_O = self.get_rows_analysisID_dataStage02QuantificationAnova(analysis_id_I);
        #reformat the data for anova plot
        data_O = self.format_dataAnovaPlot(data_O);
        # make the data parameters
        data1_keys = ['analysis_id',
                      'component_name',
                      'component_index',
                      'component_group_name',
                      'calculated_concentration_units',
                      'test_description'
                    ];
        data1_nestkeys = ['analysis_id'];
        data1_keymap = {'ydata':'pvalue_negLog10',
                        'xdata':'component_index',
                        'serieslabel':'',
                        'featureslabel':'component_group_name'};
        # make the data object
        dataobject_O = [{"data":data_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys}];
        # make the tile parameter objects
        formtileparameters_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-4"};
        formparameters_O = {'htmlid':'filtermenuform1',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit1','text':'submit'},"formresetbuttonidtext":{'id':'reset1','text':'reset'},"formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters_O.update(formparameters_O);
        svgparameters_O = {"svgtype":'volcanoplot2d_01',
                           "svgkeymap":[data1_keymap],
                            'svgid':'svg1',
                            "svgmargin":{ 'top': 50, 'right': 50, 'bottom': 50, 'left': 50 },
                            "svgwidth":500,"svgheight":350,
                            "svgx1axislabel":'Component index',
                            "svgy1axislabel":'Probability [-log10(P)]'};
        svgtileparameters_O = {'tileheader':'ANOVA','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
        svgtileparameters_O.update(svgparameters_O);
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tablefilters":None,
                    "tableclass":"table  table-condensed table-hover",
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'ANOVA','tiletype':'table','tileid':"tile3",'rowid':"row2",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O = [formtileparameters_O,svgtileparameters_O,tabletileparameters_O];
        tile2datamap_O = {"filtermenu1":[0],"tile2":[0],"tile3":[0]};
        # dump the data to a json file
        data_str = 'var ' + 'data' + ' = ' + json.dumps(dataobject_O) + ';';
        parameters_str = 'var ' + 'parameters' + ' = ' + json.dumps(parametersobject_O) + ';';
        tile2datamap_str = 'var ' + 'tile2datamap' + ' = ' + json.dumps(tile2datamap_O) + ';';
        #
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = None);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());
   