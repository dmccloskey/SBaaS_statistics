# System
import json
# SBaaS
from .stage02_quantification_correlation_query import stage02_quantification_correlation_query
from .stage02_quantification_correlation_dependencies import stage02_quantification_correlation_dependencies
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container
from numpy import isnan

class stage02_quantification_correlation_io(stage02_quantification_correlation_query,
                                            stage02_quantification_correlation_dependencies,
                                            sbaas_template_io):
    def import_dataStage02QuantificationCorrelationProfile_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02QuantificationCorrelationProfile(data.data);
        data.clear_data();

    def import_dataStage02QuantificationCorrelationProfile_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02QuantificationCorrelationProfile(data.data);
        data.clear_data();
        
    def import_dataStage02QuantificationCorrelationTrend_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02QuantificationCorrelationTrend(data.data);
        data.clear_data();

    def import_dataStage02QuantificationCorrelationTrend_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02QuantificationCorrelationTrend(data.data);
        data.clear_data();
        
    def import_dataStage02QuantificationCorrelationPattern_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02QuantificationCorrelationPattern(data.data);
        data.clear_data();

    def import_dataStage02QuantificationCorrelationPattern_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02QuantificationCorrelationPattern(data.data);
        data.clear_data();

    def export_dataStage02QuantificationCorrelationProfile_js(self, analysis_id_I,data_dir_I='tmp'):
        '''Export Profile to js
        Plots:
        1. vertical bar chart
        2. scatter-line plot of the profile
        '''
        
        data_O = [];
        #get the data
        data_tmp = [];
        data_tmp = self.get_rows_analysisID_dataStage02QuantificationCorrelationProfile(analysis_id_I);
        #remove any NaNs
        for d in data_tmp:
            if not isnan(d['correlation_coefficient']):
                d['sample_name_abbreviations']='-'.join(d['sample_name_abbreviations']);
                data_O.append(d);

        #get the profiles
        profiles = [];
        profiles = self.get_profiles_analysisID_dataStage02QuantificationCorrelationProfile(analysis_id_I);
        profiles_O = [];
        profiles_O = self.convert_profileStr2DataList(profiles);

        # dump chart parameters to a js files
        data1_keys = ['sample_name_abbreviations',
                    'profile_match',
                    'profile_match_description',
                    #'component_match',
                    #'component_match_units',
                    'distance_measure',
                    'component_name',
                    'component_group_name',
                    'component_profile',
                    'pvalue',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {'xdata':'correlation_coefficient',
                        'ydata':'component_name',
                        'serieslabel':'profile_match',
                        'featureslabel':'component_name'
                        };
        data2_keys = ['profile_match',
                    ];
        data2_nestkeys = ['profile_match'];
        data2_keymap = {'xdata':'profile_index',
                        'ydata':'profile_int',
                        'serieslabel':'profile_match',
                        'featureslabel':''
                        };
        # make the data object
        dataobject_O = [{"data":data_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys},
                        {"data":profiles_O,"datakeys":data2_keys,"datanestkeys":data2_nestkeys},];
        # make the tile parameter objects
        # tile 1: form (row 1, col1)
        formtileparameters_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-4"};
        formparameters_O = {'htmlid':'filtermenuform1',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit1','text':'submit'},"formresetbuttonidtext":{'id':'reset1','text':'reset'},"formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters_O.update(formparameters_O);
        # tile 2: vertical bars plot of the flux_difference (row 1, col 2)
        svgparameters1_O = {"svgtype":'horizontalbarschart2d_01',"svgkeymap":[data1_keymap],
                            'svgid':'svg1',
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 50, 'left': 250 },
                            "svgwidth":350,"svgheight":900,
                            "svgx1axislabel":"Correlation coefficient","svgy1axislabel":"component_name",
    						'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
        svgtileparameters1_O = {'tileheader':'Correlating profiles','tiletype':'svg','tileid':"tile1",'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
        svgtileparameters1_O.update(svgparameters1_O);
        # tile 3: vertical bars plot of the flux_difference (row 2, col 2)
        svgparameters2_O = {"svgtype":'scatterlineplot2d_01',"svgkeymap":[data2_keymap,data2_keymap],
                            'svgid':'svg2',
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 50, 'left': 50 },
                            "svgwidth":350,"svgheight":350,
                            "svgx1axislabel":"index","svgy1axislabel":"profile",
    						'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
        svgtileparameters2_O = {'tileheader':'Profile','tiletype':'svg','tileid':"tile2",'rowid':"row2",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-6"};
        svgtileparameters2_O.update(svgparameters2_O);
        # tile 4: table of data (row 3, col 1)
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tablefilters":None,
                    "tableclass":"table  table-condensed table-hover",
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'Profile matches','tiletype':'table','tileid':"tile3",'rowid':"row3",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O = [formtileparameters_O,
                              svgtileparameters1_O,
                              svgtileparameters2_O,
                              tabletileparameters_O];
        tile2datamap_O = {"filtermenu1":[0],
                          "tile1":[0],
                          "tile2":[1,1],
                          "tile3":[0]};
        # dump the data to a json file
        data_str = 'var ' + 'data' + ' = ' + json.dumps(dataobject_O) + ';';
        parameters_str = 'var ' + 'parameters' + ' = ' + json.dumps(parametersobject_O) + ';';
        tile2datamap_str = 'var ' + 'tile2datamap' + ' = ' + json.dumps(tile2datamap_O) + ';';
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = None);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());

    def export_dataStage02QuantificationCorrelationTrend_js(self, analysis_id_I,data_dir_I='tmp'):
        '''Export Trend to js
        Plots:
        1. vertical bar chart
        2. scatter-line plot of the trend
        '''
        
        data_O = [];
        #get the data
        data_tmp = [];
        data_tmp = self.get_rows_analysisID_dataStage02QuantificationCorrelationTrend(analysis_id_I);
        #remove any NaNs
        for d in data_tmp:
            if not isnan(d['correlation_coefficient']):
                d['sample_name_abbreviations']='-'.join(d['sample_name_abbreviations']);
                data_O.append(d);

        #get the trends
        trends = [];
        trends = self.get_trends_analysisID_dataStage02QuantificationCorrelationTrend(analysis_id_I);
        trends_O = [];
        trends_O = self.convert_trendStr2DataList(trends);

        # dump chart parameters to a js files
        data1_keys = ['sample_name_abbreviations',
                    'trend_match',
                    'trend_match_description',
                    #'component_match',
                    #'component_match_units',
                    'distance_measure',
                    'component_name',
                    'component_group_name',
                    'component_trend',
                    'pvalue',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {'xdata':'correlation_coefficient',
                        'ydata':'component_name',
                        'serieslabel':'trend_match',
                        'featureslabel':'component_name'
                        };
        data2_keys = ['trend_match',
                    ];
        data2_nestkeys = ['trend_match'];
        data2_keymap = {'xdata':'trend_index',
                        'ydata':'trend_int',
                        'serieslabel':'trend_match',
                        'featureslabel':''
                        };
        # make the data object
        dataobject_O = [{"data":data_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys},
                        {"data":trends_O,"datakeys":data2_keys,"datanestkeys":data2_nestkeys},];
        # make the tile parameter objects
        # tile 1: form (row 1, col1)
        formtileparameters_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-4"};
        formparameters_O = {'htmlid':'filtermenuform1',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit1','text':'submit'},"formresetbuttonidtext":{'id':'reset1','text':'reset'},"formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters_O.update(formparameters_O);
        # tile 2: vertical bars plot of the flux_difference (row 1, col 2)
        svgparameters1_O = {"svgtype":'horizontalbarschart2d_01',"svgkeymap":[data1_keymap],
                            'svgid':'svg1',
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 50, 'left': 250 },
                            "svgwidth":350,"svgheight":900,
                            "svgx1axislabel":"Correlation coefficient","svgy1axislabel":"component_name",
    						'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
        svgtileparameters1_O = {'tileheader':'Correlating trends','tiletype':'svg','tileid':"tile1",'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
        svgtileparameters1_O.update(svgparameters1_O);
        # tile 3: vertical bars plot of the flux_difference (row 2, col 2)
        svgparameters2_O = {"svgtype":'scatterlineplot2d_01',"svgkeymap":[data2_keymap,data2_keymap],
                            'svgid':'svg2',
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 50, 'left': 50 },
                            "svgwidth":350,"svgheight":350,
                            "svgx1axislabel":"index","svgy1axislabel":"trend",
    						'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
        svgtileparameters2_O = {'tileheader':'Trend','tiletype':'svg','tileid':"tile2",'rowid':"row2",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-6"};
        svgtileparameters2_O.update(svgparameters2_O);
        # tile 4: table of data (row 3, col 1)
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tablefilters":None,
                    "tableclass":"table  table-condensed table-hover",
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'Trend matches','tiletype':'table','tileid':"tile3",'rowid':"row3",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O = [formtileparameters_O,
                              svgtileparameters1_O,
                              svgtileparameters2_O,
                              tabletileparameters_O];
        tile2datamap_O = {"filtermenu1":[0],
                          "tile1":[0],
                          "tile2":[1,1],
                          "tile3":[0]};
        # dump the data to a json file
        data_str = 'var ' + 'data' + ' = ' + json.dumps(dataobject_O) + ';';
        parameters_str = 'var ' + 'parameters' + ' = ' + json.dumps(parametersobject_O) + ';';
        tile2datamap_str = 'var ' + 'tile2datamap' + ' = ' + json.dumps(tile2datamap_O) + ';';
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = None);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());

    def export_dataStage02QuantificationCorrelationPattern_js(self, analysis_id_I,data_dir_I='tmp'):
        '''Export Pattern to js
        Plots:
        1. vertical bar chart
        2. scatter-line plot of the pattern
        '''
        
        data_O = [];
        #get the data
        data_tmp = [];
        data_tmp = self.get_rows_analysisID_dataStage02QuantificationCorrelationPattern(analysis_id_I);
        #remove any NaNs
        for d in data_tmp:
            if not isnan(d['correlation_coefficient']):
                d['sample_name_abbreviations']='-'.join(d['sample_name_abbreviations']);
                data_O.append(d);

        #get the patterns
        patterns = [];
        patterns = self.get_patterns_analysisID_dataStage02QuantificationCorrelationPattern(analysis_id_I);
        patterns_O = [];
        patterns_O = self.convert_patternStr2DataList(patterns);

        # dump chart parameters to a js files
        data1_keys = ['sample_name_abbreviations',
                    'pattern_match',
                    'pattern_match_description',
                    #'component_match',
                    #'component_match_units',
                    'distance_measure',
                    'component_name',
                    'component_group_name',
                    'component_pattern',
                    'pvalue',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {'xdata':'correlation_coefficient',
                        'ydata':'component_name',
                        'serieslabel':'pattern_match',
                        'featureslabel':'component_name'
                        };
        data2_keys = ['pattern_match',
                    ];
        data2_nestkeys = ['pattern_match'];
        data2_keymap = {'xdata':'pattern_index',
                        'ydata':'pattern_int',
                        'serieslabel':'pattern_match',
                        'featureslabel':''
                        };
        # make the data object
        dataobject_O = [{"data":data_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys},
                        {"data":patterns_O,"datakeys":data2_keys,"datanestkeys":data2_nestkeys},];
        # make the tile parameter objects
        # tile 1: form (row 1, col1)
        formtileparameters_O = {'tileheader':'Filter menu','tiletype':'html','tileid':"filtermenu1",'rowid':"row1",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-4"};
        formparameters_O = {'htmlid':'filtermenuform1',"htmltype":'form_01',"formsubmitbuttonidtext":{'id':'submit1','text':'submit'},"formresetbuttonidtext":{'id':'reset1','text':'reset'},"formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters_O.update(formparameters_O);
        # tile 2: vertical bars plot of the flux_difference (row 1, col 2)
        svgparameters1_O = {"svgtype":'horizontalbarschart2d_01',"svgkeymap":[data1_keymap],
                            'svgid':'svg1',
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 50, 'left': 250 },
                            "svgwidth":350,"svgheight":900,
                            "svgx1axislabel":"Correlation coefficient","svgy1axislabel":"component_name",
    						'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
        svgtileparameters1_O = {'tileheader':'Correlating patterns','tiletype':'svg','tileid':"tile1",'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
        svgtileparameters1_O.update(svgparameters1_O);
        # tile 3: vertical bars plot of the flux_difference (row 2, col 2)
        svgparameters2_O = {"svgtype":'scatterlineplot2d_01',"svgkeymap":[data2_keymap,data2_keymap],
                            'svgid':'svg2',
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 50, 'left': 50 },
                            "svgwidth":350,"svgheight":350,
                            "svgx1axislabel":"index","svgy1axislabel":"pattern",
    						'svgformtileid':'filtermenu1','svgresetbuttonid':'reset1','svgsubmitbuttonid':'submit1'};
        svgtileparameters2_O = {'tileheader':'Pattern','tiletype':'svg','tileid':"tile2",'rowid':"row2",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-6"};
        svgtileparameters2_O.update(svgparameters2_O);
        # tile 4: table of data (row 3, col 1)
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tablefilters":None,
                    "tableclass":"table  table-condensed table-hover",
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'Pattern matches','tiletype':'table','tileid':"tile3",'rowid':"row3",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O = [formtileparameters_O,
                              svgtileparameters1_O,
                              svgtileparameters2_O,
                              tabletileparameters_O];
        tile2datamap_O = {"filtermenu1":[0],
                          "tile1":[0],
                          "tile2":[1,1],
                          "tile3":[0]};
        # dump the data to a json file
        data_str = 'var ' + 'data' + ' = ' + json.dumps(dataobject_O) + ';';
        parameters_str = 'var ' + 'parameters' + ' = ' + json.dumps(parametersobject_O) + ';';
        tile2datamap_str = 'var ' + 'tile2datamap' + ' = ' + json.dumps(tile2datamap_O) + ';';
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = None);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());