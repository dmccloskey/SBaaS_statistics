#sbaas
from .stage02_quantification_histogram_query import stage02_quantification_histogram_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
#sbaas models
from .stage02_quantification_histogram_postgresql_models import *
#sbaas lims
#biologicalMaterial_geneReference

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container

class stage02_quantification_histogram_io(stage02_quantification_histogram_query,sbaas_template_io):

    def import_dataStage02QuantificationHistogram_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02QuantificationHistogram(data.data);
        data.clear_data();

    def import_dataStage02QuantificationHistogram_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02QuantificationHistogram(data.data);
        data.clear_data();

    def export_dataStage02QuantificationHistogram_js(self,analysis_id_I,single_plot_I=False,data_dir_I="tmp"):
        '''export data_stage02_quantification_histogram to js file
        Visualization: histogram of bins for each feature
        '''

        #get the table data
        data_table_O = [];
        data_table_O = self.get_rows_analysisID_dataStage02QuantificationHistogram(analysis_id_I);
        #get the data as a dictionary for each feature
        data_dict_O = {};
        data_dict_O = self.get_rowsAsFeaturesDict_analysisID_dataStage02QuantificationHistogram(analysis_id_I);
        
        # initialize the ddt objects
        dataobject_O = [];
        parametersobject_O = [];
        tile2datamap_O = {};
        
        # visualization parameters
        data1_keys = ['feature_id',
                      'feature_units',
                      'bin',
                      ];
        data1_nestkeys = [
            'bin'
            ];
        data1_keymap = {
                'xdata':'bin',
                'ydata':'frequency',
                'serieslabel':'feature_id',
                'featureslabel':'bin',
                'ydatalb':None,
                'ydataub':None};

        # make the tile parameter objects
        # tile 0: form
        formtileparameters_O = {
            'tileheader':'Filter menu',
            'tiletype':'html',
            'tileid':"filtermenu1",
            'rowid':"row1",
            'colid':"col1",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-12"};
        formparameters_O = {
            'htmlid':'filtermenuform1',
            'htmltype':'form_01',
            "formsubmitbuttonidtext":{'id':'submit1','text':'submit'},
            "formresetbuttonidtext":{'id':'reset1','text':'reset'},
            "formupdatebuttonidtext":{'id':'update1','text':'update'}
            };
        formtileparameters_O.update(formparameters_O);

        dataobject_O.append({"data":data_table_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys});
        parametersobject_O.append(formtileparameters_O);
        tile2datamap_O.update({"filtermenu1":[0]});

        # tile 1-n features: histogram
        if not single_plot_I:
            rowcnt = 1;
            colcnt = 1;
            cnt = 0;
            for k,v in data_dict_O.items():
                svgtileid = "tilesvg"+str(cnt);
                svgid = 'svg'+str(cnt);
                iter=cnt+1; #start at 1
                if (cnt % 2 == 0): 
                    rowcnt = rowcnt+1;#even 
                    colcnt = 1;
                else:
                    colcnt = colcnt+1;
                # make the svg object
                svgparameters1_O = {
                    "svgtype":'verticalbarschart2d_01',
                    "svgkeymap":[data1_keymap],
                    'svgid':'svg'+str(cnt),
                    "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                    "svgwidth":350,
                    "svgheight":250,
                    "svgy1axislabel":"frequency"            
                        };
                svgtileparameters1_O = {
                    'tileheader':'Histogram',
                    'tiletype':'svg',
                    'tileid':svgtileid,
                    'rowid':"row"+str(rowcnt),
                    'colid':"col"+str(colcnt),
                    'tileclass':"panel panel-default",
                    'rowclass':"row",
                    'colclass':"col-sm-6"};
                dataobject_O.append({"data":v,"datakeys":data1_keys,"datanestkeys":data1_nestkeys});
                svgtileparameters1_O.update(svgparameters1_O);
                parametersobject_O.append(svgtileparameters1_O);
                tile2datamap_O.update({svgtileid:[iter]});
                #tile2datamap_O["filtermenu1"].append(iter);
                cnt+=1;
        else:
            cnt = 0;
            svgtileid = "tilesvg"+str(cnt);
            svgid = 'svg'+str(cnt);
            rowcnt = 2;
            colcnt = 1;
            # make the svg object
            svgparameters1_O = {
                "svgtype":'verticalbarschart2d_01',
                "svgkeymap":[data1_keymap],
                'svgid':'svg'+str(cnt),
                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                "svgwidth":350,
                "svgheight":250,
                "svgy1axislabel":"frequency"            
                    };
            svgtileparameters1_O = {
                'tileheader':'Histogram',
                'tiletype':'svg',
                'tileid':svgtileid,
                'rowid':"row"+str(rowcnt),
                'colid':"col"+str(colcnt),
                'tileclass':"panel panel-default",
                'rowclass':"row",
                'colclass':"col-sm-6"};
            svgtileparameters1_O.update(svgparameters1_O);
            parametersobject_O.append(svgparameters1_O);
            tile2datamap_O.update({svgtileid:[1]});
            #tile2datamap_O["filtermenu1"].append(1);
            
        # make the table object
        tableparameters1_O = {
            "tabletype":'responsivetable_01',
            'tableid':'table1',
            "tablefilters":None,
            "tableclass":"table  table-condensed table-hover",
    		'tableformtileid':'tile1',
            };
        tabletileparameters1_O = {
            'tileheader':'Histogram',
            'tiletype':'table',
            'tileid':"tabletile1",
            'rowid':"row"+str(rowcnt+1),
            'colid':"col1",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-12"
            };
        tabletileparameters1_O.update(tableparameters1_O);

        dataobject_O.append({"data":data_table_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys});
        parametersobject_O.append(tabletileparameters1_O);
        tile2datamap_O.update({"tabletile1":[0]})

        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = None);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());