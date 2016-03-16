# System
import json
# SBaaS
from .stage02_quantification_pairWiseTest_query import stage02_quantification_pairWiseTest_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
#SBaaS_rnasequencing
from SBaaS_rnasequencing.stage01_rnasequencing_geneExpDiff_query import stage01_rnasequencing_geneExpDiff_query

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container

class stage02_quantification_pairWiseTest_io(stage02_quantification_pairWiseTest_query,sbaas_template_io):
    def export_dataStage02QuantificationPairWiseTest_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export data for a volcano plot
        Visuals:
        1. volcano plot
        2. sample vs. sample (FC)
        3. sample vs. sample (concentration)
        4. sample vs. sample (p-value)'''
        
        #get the data for the analysis
        data_O = [];
        data_O = self.get_rows_analysisID_dataStage02pairWiseTest(analysis_id_I);
        # make the data parameters
        data1_keys = ['analysis_id','sample_name_abbreviation_1','sample_name_abbreviation_2','component_name','component_group_name','calculated_concentration_units','test_description'
                    ];
        data1_nestkeys = ['analysis_id'];
        data1_keymap = {'ydata':'pvalue_corrected_negLog10',
                        'xdata':'fold_change_log2',
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
                            "svgwidth":500,
                            "svgheight":350,
                            "svgx1axislabel":'Fold Change [log2(FC)]',
                            "svgy1axislabel":'Probability [-log10(P)]'};
        svgtileparameters_O = {'tileheader':'Volcano plot','tiletype':'svg','tileid':"tile2",'rowid':"row1",'colid':"col2",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-8"};
        svgtileparameters_O.update(svgparameters_O);
        tableparameters_O = {"tabletype":'responsivetable_01',
                    'tableid':'table1',
                    "tableclass":"table  table-condensed table-hover",
                    "tablefilters":None,
    			    'tableformtileid':'filtermenu1','tableresetbuttonid':'reset1','tablesubmitbuttonid':'submit1'};
        tabletileparameters_O = {'tileheader':'pairWiseTest','tiletype':'table','tileid':"tile3",'rowid':"row2",'colid':"col1",
            'tileclass':"panel panel-default",'rowclass':"row",'colclass':"col-sm-12"};
        tabletileparameters_O.update(tableparameters_O);
        parametersobject_O = [formtileparameters_O,svgtileparameters_O,tabletileparameters_O];
        tile2datamap_O = {"filtermenu1":[0],"tile2":[0],"tile3":[0]};
        # dump the data to a json file
        filtermenuobject_O = None;
        ddtutilities = ddt_container(parameters_I = parametersobject_O,data_I = dataobject_O,tile2datamap_I = tile2datamap_O,filtermenu_I = filtermenuobject_O);
        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = ddtutilities.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(ddtutilities.get_allObjects());

    
    #Query data from RNASequencing:
    def import_dataStage01RNASequencingGeneExpDiff(self,
                analysis_id_I,
                geneShortName2componentName_I = {},
                geneShortName2componentGroupName_I = {},
                sna2snaRNASequencing_I = {}
                ):
        '''get the the genes.fpkm_tracking data from SBaaS_rnasequencing
        INPUT:
        geneShortName2componentName_I = {}, mapping of gene_short_name to component_name
        geneShortName2componentGroupName_I = {}, mapping of gene_short_name to component_group_name
        sna2snaRNASequencing_I = {
                                'OxicEvo04Ecoli13CGlc':'OxicEvo04EcoliGlc',
                                'OxicEvo04gndEcoli13CGlc':'OxicEvo04gndEcoliGlc',
                                'OxicEvo04pgiEcoli13CGlc':'OxicEvo04pgiEcoliGlc',
                                'OxicEvo04sdhCBEcoli13CGlc':'OxicEvo04sdhCBEcoliGlc',
                                'OxicEvo04tpiAEcoli13CGlc':'OxicEvo04tpiAEcoliGlc'}
        OUTPUT:
        TODO:...
        '''
        rnasequencing_geneExpDiff_query = stage01_rnasequencing_geneExpDiff_query(self.session,self.engine,self.settings);
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        data_O = [];
        for analysis_row in analysis_rows:
            # query fpkm data:
            fpkms = [];
            if sna2snaRNASequencing_I: sample_name = sna2snaRNASequencing_I[analysis_row['sample_name_abbreviation']];
            else: sample_name = analysis_row['sample_name_abbreviation'];
            fpkms = rnasequencing_geneExpDiff_query.get_rows_experimentIDAndSampleName_dataStage01RNASequencingGenesFpkmTracking(analysis_row['experiment_id'],sample_name);
            # map the data
            for fpkm in fpkms:
                row = {};
                row['analysis_id']=analysis_id_I;
                row['experiment_id_1']=analysis_row['experiment_id_1'];
                row['experiment_id_2']=analysis_row['experiment_id_2'];
                row['sample_name_abbreviation_1']=analysis_row['sample_name_abbreviation_1'];
                row['sample_name_abbreviation_2']=analysis_row['sample_name_abbreviation_2'];
                row['time_point_1']=analysis_row['time_point_1'];
                row['time_point_2']=analysis_row['time_point_2'];
                if geneShortName2componentName_I:
                    row['component_name']=geneShortName2componentName_I[fpkm['gene_id']];
                else:
                    row['component_name']=fpkm['gene_short_name'] + '_' + fpkm['gene_id'];
                if geneShortName2componentGroupName_I:
                    row['component_group_name']=geneShortName2componentGroupName_I[fpkm['gene_short_name']];
                else:
                    row['component_group_name']=fpkm['gene_short_name'];
                
                row["imputation_method"]=None;
                row['calculated_concentration']=fpkm['test_stat'];
                row['calculated_concentration']=fpkm['p_value'];
                row['calculated_concentration']=fpkm['q_value'];
                row['calculated_concentration']='FDR';
                row['calculated_concentration']=fpkm['fold_change_log2'];
                row['calculated_concentration']=fpkm['fold_change_log2'];
                row['calculated_concentration_units']='log2(FC)';
                row['used_']=fpkm['used_']
                row['comment_']=fpkm['comment_'];                
                data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages',data_O);
   