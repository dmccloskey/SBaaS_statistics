# System
import json
# SBaaS
from .stage02_quantification_opls_query import stage02_quantification_opls_query
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container
from ddt_python.ddt_container_scoresAndLoadings import ddt_container_scoresAndLoadings
from ddt_python.ddt_container_biPlotAndValidation import ddt_container_biPlotAndValidation
from listDict.listDict import listDict
from python_statistics.calculate_pca import calculate_pca

class stage02_quantification_opls_io(stage02_quantification_opls_query):
    def export_dataStage02QuantificationOPLSScoresAndLoadings_js(self,analysis_id_I,axis_I=3,data_dir_I='tmp'):
        '''Export pls scores and loadings plots for axis 1 vs. 2, 1 vs 3, and 2 vs 3'''
        calculatepca = calculate_pca();
        PCs = [[1,2],[1,3],[2,3]];
        # get data:
        data_scores,data_loadings = [],[];
        data_scores,data_loadings = self.get_RExpressionData_analysisID_dataStage02QuantificationOPLSScoresLoadings(analysis_id_I,axis_I);
        # reformat the data
        data_scores_123,data_loadings_123 = [],[];
        data_scores = self.get_rowAxisDict_analysisID_dataStage02QuantificationOPLSScores(analysis_id_I,axis_I)
        data_loadings = self.get_rowAxisDict_analysisID_dataStage02QuantificationOPLSLoadings(analysis_id_I,axis_I)
        data_scores_123,data_loadings_123 = {},{};
        data_scores_123,data_loadings_123 = calculatepca.extract_scoresAndLoadings_2D(data_scores,data_loadings,PCs);

        data1_keys = [
            'analysis_id',
            'response_name',
            'sample_name_short',
            'calculated_concentration_units',
            #'pls_model',
            #'pls_method'
                    ];
        data1_nestkeys = ['response_name'];
        data2_keys = [
            'analysis_id',
            'component_name',
            'component_group_name',
            'calculated_concentration_units'
                    ];
        data2_nestkeys = ['analysis_id'];
        data1_keymap_serieslabel = 'response_name';
        data1_keymap_featureslabel = 'sample_name_short';
        data2_keymap_serieslabel = '';
        data2_keymap_featureslabel = 'component_group_name';
        
        # dump the data to a json file
        scoresandloadings = ddt_container_scoresAndLoadings();
        scoresandloadings.make_scoresAndLoadings(
            data_scores_123,data_loadings_123,
            PCs,
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
    def export_dataStage02QuantificationOPLSBiPlotAndValidation_js(self,analysis_id_I,data_dir_I='tmp'):
        '''
        Export the bi plot for the PLS components and validation plots for the pls model
        OUTPUT:
        biplot = scatterLinePlot of explained variances vs. component axis
        crossValidation plot = verticalBarPlot of MSEP, R2, and Q2 for increasing numbers of component axis
        OUTPUT TODO:
        permutation plot = p-value of permutation test
        '''
        #get the biplot data
        biplot_O = [];
        biplot_tmp = self.get_biPlotData_analysisID_dataStage02QuantificationOPLSScores(analysis_id_I);
        listdict = listDict(biplot_tmp);
        biplot_O = listdict.convert_listDict2ListDictValues(
            value_key_name_I = 'var_value',
            value_label_name_I = 'var_label',
            value_labels_I=['var_proportion','var_cumulative']);
        #get the validation data
        validation_O = [];
        validation_tmp = self.get_rows_analysisID_dataStage02QuantificationOPLSValidation(analysis_id_I);
        listdict = listDict(validation_tmp);
        validation_O = listdict.convert_listDict2ListDictValues(
            value_key_name_I = 'metric_value',
            value_label_name_I = 'metric_label',
            value_labels_I=['pls_msep','pls_rmsep','pls_r2','pls_r2x','pls_q2']);

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                    'axis',
                    'var_label',
                    'pls_model',
                    'pls_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['var_label'];
        data1_keymap = {'xdata':'axis',
                        'ydata':'var_value',
                        'serieslabel':'var_label',
                        'featureslabel':'axis'};
        #define the data parameters for the validation
        data2_keys = ['analysis_id',
                    'pls_model',
                    'pls_method',
                    'metric_label',
                    'crossValidation_ncomp',
                    'crossValidation_method',
                    'calculated_concentration_units'
                    ];
        data2_nestkeys = ['crossValidation_ncomp'];
        data2_keymap = {'xdata':'crossValidation_ncomp',
                        'ydata':'metric_value',
                        'ydatalb':None,
                        'ydataub':None,
                        'serieslabel':'metric_label',
                        'featureslabel':'crossValidation_ncomp'};

        biplotandvalidation = ddt_container_biPlotAndValidation();
        biplotandvalidation.make_biPlotAndValidation(
            biplot_O,validation_O,
            data1_keys,data1_nestkeys,data1_keymap,
            data2_keys,data2_nestkeys,data2_keymap,
            );

        # export the data
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = biplotandvalidation.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(biplotandvalidation.get_allObjects());
    def export_dataStage02QuantificationOPLSVIPs_js(self,analysis_id_I,data_dir_I='tmp'):
        '''
        Export the PLS VIPs
        OUTPUT:
        horizontal bar plot of VIPs
        '''
        #get the biplot data
        vip_O = [];
        vip_O = self.get_rows_analysisID_dataStage02QuantificationOPLSVIP(analysis_id_I);
        #vip_O = self.get_VIPs_analysisID_dataStage02QuantificationOPLSLoadings(analysis_id_I);

        #initialize the ddt objects
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                    'response_name',
                    'component_name',
                    'component_group_name',
                    'pls_model',
                    'pls_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {
                        'xdata':'pls_vip',
                        'ydata':'component_name',
                        'xdatalb':None,
                        'xdataub':None,
                        'serieslabel':'response_name',
                        'featureslabel':'component_name'};
        dataobject_O.append({"data":vip_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys});

        #form 1: vip
        formtileparameters1_O = {
            'tileheader':'VIP filter menu',
            'tiletype':'html',
            'tileid':"filtermenu1",
            'rowid':"row1",
            'colid':"col1",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-4"};
        formparameters1_O = {
            'htmlid':'filtermenuform1',
            "htmltype":'form_01',
            "formsubmitbuttonidtext":{'id':'submit1','text':'submit'},
            "formresetbuttonidtext":{'id':'reset1','text':'reset'},
            "formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters1_O.update(formparameters1_O);
        parametersobject_O.append(formtileparameters1_O);
        tile2datamap_O.update({"filtermenu1":[0]});
        filtermenuobject_O.append(
            {"filtermenuid":"filtermenu1",
             "filtermenuhtmlid":"filtermenuform1",
            "filtermenusubmitbuttonid":"submit1",
            "filtermenuresetbuttonid":"reset1",
            "filtermenuupdatebuttonid":"update1"})

        #svg 1: vip
        svgparameters1_O = {
            "svgtype":'horizontalbarschart2d_01',
            "svgkeymap":[data1_keymap],
            'svgid':'svg1',
            "svgmargin":{ 'top': 50, 'right': 350, 'bottom': 50, 'left': 50 },
            "svgwidth":450,"svgheight":900,
            "svgx1axislabel":"vip_value",
            "svgy1axislabel":"component_name",
    		'svgformtileid':'filtermenu1',
            };
        svgtileparameters1_O = {
            'tileheader':'VIP components',
            'tiletype':'svg',
            'tileid':"tile1",
            'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-6"};
        svgtileparameters1_O.update(svgparameters1_O);
        parametersobject_O.append(svgtileparameters1_O);
        tile2datamap_O.update({"tile1":[0]});

        #table 1: vip
        tableparameters1_O = {
            "tabletype":'responsivetable_01',
            'tableid':'table2',
            "tablefilters":None,
            "tableheaders":None,
            "tableclass":"table  table-condensed table-hover",
    		};
        tabletileparameters1_O = {
            'tileheader':'VIP components',
            'tiletype':'table',
            'tileid':"tile2",
            'rowid':"row2",
            'colid':"col1",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-12"};
        tabletileparameters1_O.update(tableparameters1_O);
        parametersobject_O.append(tabletileparameters1_O);
        tile2datamap_O.update({"tile2":[0]});

        # export the data
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = filtermenuobject_O);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());
    def export_dataStage02QuantificationOPLSCoefficients_js(self,analysis_id_I,data_dir_I='tmp'):
        '''
        Export the PLS Coefficientss
        OUTPUT:
        horizontal bar plot of Coefficientss
        '''
        #get the biplot data
        vip_O = [];
        vip_O = self.get_rows_analysisID_dataStage02QuantificationOPLSCoefficients(analysis_id_I);
        #vip_O = self.get_Coefficientss_analysisID_dataStage02QuantificationOPLSLoadings(analysis_id_I);

        #initialize the ddt objects
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                    'response_name',
                    'component_name',
                    'component_group_name',
                    'pls_model',
                    'pls_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {
                        'xdata':'pls_coefficients',
                        'ydata':'component_name',
                        'xdatalb':None,
                        'xdataub':None,
                        'serieslabel':'response_name',
                        'featureslabel':'component_name'};
        dataobject_O.append({"data":vip_O,"datakeys":data1_keys,"datanestkeys":data1_nestkeys});

        #form 1: vip
        formtileparameters1_O = {
            'tileheader':'Coefficients filter menu',
            'tiletype':'html',
            'tileid':"filtermenu1",
            'rowid':"row1",
            'colid':"col1",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-4"};
        formparameters1_O = {
            'htmlid':'filtermenuform1',
            "htmltype":'form_01',
            "formsubmitbuttonidtext":{'id':'submit1','text':'submit'},
            "formresetbuttonidtext":{'id':'reset1','text':'reset'},
            "formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters1_O.update(formparameters1_O);
        parametersobject_O.append(formtileparameters1_O);
        tile2datamap_O.update({"filtermenu1":[0]});
        filtermenuobject_O.append(
            {"filtermenuid":"filtermenu1",
             "filtermenuhtmlid":"filtermenuform1",
            "filtermenusubmitbuttonid":"submit1",
            "filtermenuresetbuttonid":"reset1",
            "filtermenuupdatebuttonid":"update1"})

        #svg 1: vip
        svgparameters1_O = {
            "svgtype":'horizontalbarschart2d_01',
            "svgkeymap":[data1_keymap],
            'svgid':'svg1',
            "svgmargin":{ 'top': 50, 'right': 350, 'bottom': 50, 'left': 50 },
            "svgwidth":450,"svgheight":900,
            "svgx1axislabel":"regressioin_coefficient",
            "svgy1axislabel":"component_name",
    		'svgformtileid':'filtermenu1',
            };
        svgtileparameters1_O = {
            'tileheader':'Regression coefficients',
            'tiletype':'svg',
            'tileid':"tile1",
            'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-6"};
        svgtileparameters1_O.update(svgparameters1_O);
        parametersobject_O.append(svgtileparameters1_O);
        tile2datamap_O.update({"tile1":[0]});

        #table 1: vip
        tableparameters1_O = {
            "tabletype":'responsivetable_01',
            'tableid':'table2',
            "tablefilters":None,
            "tableheaders":None,
            "tableclass":"table  table-condensed table-hover",
    		};
        tabletileparameters1_O = {
            'tileheader':'Coefficients components',
            'tiletype':'table',
            'tileid':"tile2",
            'rowid':"row2",
            'colid':"col1",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-12"};
        tabletileparameters1_O.update(tableparameters1_O);
        parametersobject_O.append(tabletileparameters1_O);
        tile2datamap_O.update({"tile2":[0]});

        # export the data
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = filtermenuobject_O);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());
    def export_dataStage02QuantificationOPLSSPlot_js(self,analysis_id_I,axis_I=3,data_dir_I='tmp'):
        '''
        Export the PLS S-plot of loadings (variable magnitude) vs. model correlation (variable reliability)
        for each component
        OUTPUT:
        horizontal bar plot of Coefficientss
        '''
        # get data:
        data_loadings = [];
        data_loadings = self.get_rows_analysisID_dataStage02QuantificationOPLSLoadings(analysis_id_I,axis_I);
        data_dict = {};
        data_dict = self.get_rowAxisDict_analysisID_dataStage02QuantificationOPLSLoadings(analysis_id_I,axis_I);

        #initialize the ddt objects
        # make the tile objects
        parametersobject_O = [];
        tile2datamap_O = {};
        filtermenuobject_O = [];
        dataobject_O = [];

        # define the data parameters for the biplot:
        data1_keys = ['analysis_id',
                    'component_name',
                    'component_group_name',
                    'pls_model',
                    'pls_method',
                    'calculated_concentration_units'
                    ];
        data1_nestkeys = ['component_name'];
        data1_keymap = {
                        'xdata':'loadings',
                        'ydata':'correlations',
                        'serieslabel':'',
                        'featureslabel':'component_name'};
        dataobject_O.append({"data":data_loadings,"datakeys":data1_keys,"datanestkeys":data1_nestkeys});

        #form 1: vip
        formtileparameters1_O = {
            'tileheader':'S-Plot filter menu',
            'tiletype':'html',
            'tileid':"filtermenu1",
            'rowid':"row1",
            'colid':"col1",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-4"};
        formparameters1_O = {
            'htmlid':'filtermenuform1',
            "htmltype":'form_01',
            "formsubmitbuttonidtext":{'id':'submit1','text':'submit'},
            "formresetbuttonidtext":{'id':'reset1','text':'reset'},
            "formupdatebuttonidtext":{'id':'update1','text':'update'}};
        formtileparameters1_O.update(formparameters1_O);
        parametersobject_O.append(formtileparameters1_O);
        tile2datamap_O.update({"filtermenu1":[0]});
        filtermenuobject_O.append(
            {"filtermenuid":"filtermenu1",
             "filtermenuhtmlid":"filtermenuform1",
            "filtermenusubmitbuttonid":"submit1",
            "filtermenuresetbuttonid":"reset1",
            "filtermenuupdatebuttonid":"update1"})

        #svg 1-ncomps: extraction out the S-plot for each component
        for i in range(axis_I):
            axis = i+1;
            svgid = 'svg'+str(axis);
            colid = 'col'+str(axis+1);
            tileid = 'tile'+str(axis);
            svgparameters1_O = {
                "svgtype":'volcanoplot2d_01',
                "svgkeymap":[data1_keymap],
                'svgid':'svg1',
                "svgmargin":{ 'top': 50, 'right': 150, 'bottom': 50, 'left': 50 },
                "svgwidth":400,"svgheight":350,
                "svgx1axislabel":"loadings" + str(axis),
                "svgy1axislabel":"correlations" + str(axis),
                };
            svgtileparameters1_O = {
                'tileheader':'S-Plot',
                'tiletype':'svg',
                'tileid':tileid,
                'rowid':"row1",
                'colid':colid,
                'tileclass':"panel panel-default",
                'rowclass':"row",
                'colclass':"col-sm-6"};
            svgtileparameters1_O.update(svgparameters1_O);
            parametersobject_O.append(svgtileparameters1_O);
            tile2datamap_O.update({tileid:[axis]});
            dataobject_O.append({"data":data_dict[axis],"datakeys":data1_keys,"datanestkeys":data1_nestkeys});

        #table 1: vip
        tableparameters1_O = {
            "tabletype":'responsivetable_01',
            'tableid':'table2',
            "tablefilters":None,
            "tableheaders":None,
            "tableclass":"table  table-condensed table-hover",
    		};
        tabletileparameters1_O = {
            'tileheader':'S-Plot',
            'tiletype':'table',
            'tileid':'tile'+str(axis+1),
            'rowid':"row2",
            'colid':"col1",
            'tileclass':"panel panel-default",
            'rowclass':"row",
            'colclass':"col-sm-12"};
        tabletileparameters1_O.update(tableparameters1_O);
        parametersobject_O.append(tabletileparameters1_O);
        tile2datamap_O.update({'tile'+str(axis+1):[0]});

        # export the data
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = filtermenuobject_O);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());

    def export_dataStage02QuantificationOPLSScores_js(self,analysis_id_I,axis_I=3,data_dir_I='tmp'):
        '''Export pls scores as a bar plot and table
        Plot 1: bar plot of scores
        Table 1:  tabular display of loadings
        TODO:
        '''

        # get data:
        data_scores,data_loadings = [],[];
        data_scores,data_loadings = self.get_RExpressionData_analysisID_dataStage02QuantificationOPLSScoresLoadings(analysis_id_I,axis_I);
        
        data1_keys = [
            'analysis_id',
            'response_name',
            'sample_name_short',
            'calculated_concentration_units',
            #'pls_model',
            #'pls_method'
                    ];
        data1_nestkeys = ['response_name'];

        data2_keys = [
            'analysis_id',
            'component_name',
            'component_group_name',
            'calculated_concentration_units'
                    ];
        data2_nestkeys = ['analysis_id'];

        # dump the data to a json file
        scoresandloadings = ddt_container_scoresAndLoadings();
        scoresandloadings.make_scoresAndLoadings(
            data_scores_123,data_loadings_123,
            PCs,
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

    def export_dataStage02QuantificationOPLSLoadings_js(self,analysis_id_I,axis_I=3,data_dir_I='tmp'):
        '''Export pls loadings as a bar plot and in tabular form
        Plot 1: bar plot of loadings
        Table 1:  tabular display of loadings data
        TODO:
        '''

        # get data:
        data_scores,data_loadings = [],[];
        data_scores,data_loadings = self.get_RExpressionData_analysisID_dataStage02QuantificationOPLSScoresLoadings(analysis_id_I,axis_I);
        
        data1_keys = [
            'analysis_id',
            'response_name',
            'sample_name_short',
            'calculated_concentration_units',
            #'pls_model',
            #'pls_method'
                    ];
        data1_nestkeys = ['response_name'];

        data2_keys = [
            'analysis_id',
            'component_name',
            'component_group_name',
            'calculated_concentration_units'
                    ];
        data2_nestkeys = ['analysis_id'];

        # dump the data to a json file
        scoresandloadings = ddt_container_scoresAndLoadings();
        scoresandloadings.make_scoresAndLoadings(
            data_scores_123,data_loadings_123,
            PCs,
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