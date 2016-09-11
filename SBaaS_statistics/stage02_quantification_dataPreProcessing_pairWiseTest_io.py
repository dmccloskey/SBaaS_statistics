# System
import json
# SBaaS
from .stage02_quantification_dataPreProcessing_pairWiseTest_query import stage02_quantification_dataPreProcessing_pairWiseTest_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
#SBaaS_rnasequencing
from SBaaS_rnasequencing.stage01_rnasequencing_geneExpDiff_query import stage01_rnasequencing_geneExpDiff_query
# SBaaS COBRA
from SBaaS_COBRA.stage02_physiology_pairWiseTest_query import stage02_physiology_pairWiseTest_query

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container

class stage02_quantification_dataPreProcessing_pairWiseTest_io(stage02_quantification_dataPreProcessing_pairWiseTest_query,sbaas_template_io):
    def export_dataStage02QuantificationDataPreProcessingPairWiseTest_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export data for a volcano plot
        Visuals:
        1. volcano plot'''
        
        #get the data for the analysis
        data_O = [];
        data_O = self.get_rows_analysisID_dataStage02QuantificationDataPreProcessingPairWiseTest(analysis_id_I);
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
                geneID2componentName_I = {},
                gene2componentGroupName_I = {},
                sna2snaRNASequencing_I = {},
                experimentID2experimentIDRNASequencing_I = {},
                fold_change_log2_threshold_I = 2,
                q_value_threshold_I = 0.05,
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
        quantification_analysis_query = stage02_quantification_analysis_query(self.session,self.engine,self.settings)
        # get the analysis information
        data_O = [];
        #get the geneExpDiff data
        experiment_ids,sample_name_abbreviations = [],[];
        experiment_ids,sample_name_abbreviations,time_points = quantification_analysis_query.get_experimentIDAndSampleNameAbbreviationAndTimePoint_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);

        for sample_name_abbreviation_cnt_1,sample_name_abbreviation_1 in enumerate(sample_name_abbreviations):

            if sna2snaRNASequencing_I: sample_name_abbreviation_1 = sna2snaRNASequencing_I[sample_name_abbreviation_1];
            else: sample_name_abbreviation_1 = sample_name_abbreviation_1;
            if experimentID2experimentIDRNASequencing_I: experiment_id_1 = experimentID2experimentIDRNASequencing_I[experiment_ids[sample_name_abbreviation_cnt_1]];
            else: experiment_id_1 = experiment_ids[sample_name_abbreviation_cnt_1];
            
            # get the geneExpDiff data
            for sample_name_abbreviation_cnt_2,sample_name_abbreviation_2 in enumerate(sample_name_abbreviations):
                if sample_name_abbreviation_cnt_1 != sample_name_abbreviation_cnt_2:
                    if sna2snaRNASequencing_I: sample_name_abbreviation_2 = sna2snaRNASequencing_I[sample_name_abbreviation_2];
                    else: sample_name_abbreviation_2 = sample_name_abbreviation_2;
                    if experimentID2experimentIDRNASequencing_I: experiment_id_2 = experimentID2experimentIDRNASequencing_I[experiment_ids[sample_name_abbreviation_cnt_2]];
                    else: experiment_id_2 = experiment_ids[sample_name_abbreviation_cnt_1];
                    geneExpDiff_tmp = [];
                    geneExpDiff_tmp = rnasequencing_geneExpDiff_query.get_rows_experimentIDsAndSampleNameAbbreviationsAndFCAndQValue_dataStage01RNASequencingGeneExpDiff(
                        experiment_id_1,experiment_id_2,sample_name_abbreviation_1,sample_name_abbreviation_2,
                        fold_change_log2_threshold_I,q_value_threshold_I);
                    # map the data
                    for fpkm in geneExpDiff_tmp:
                        row = {};
                        row['analysis_id']=analysis_id_I;
                        row['experiment_id_1']=experiment_id_1;
                        row['experiment_id_2']=experiment_id_2;
                        row['sample_name_abbreviation_1']=sample_name_abbreviation_1;
                        row['sample_name_abbreviation_2']=sample_name_abbreviation_2;
                        #row['time_point_1']=analysis_row['time_point_1'];
                        #row['time_point_2']=analysis_row['time_point_2'];
                        if geneID2componentName_I:
                            row['component_name']=geneID2componentName_I[fpkm['gene_id']];
                        else:
                            row['component_name']=fpkm['gene'] + '_' + fpkm['gene_id'];
                        if gene2componentGroupName_I:
                            row['component_group_name']=gene2componentGroupName_I[fpkm['gene']];
                        else:
                            row['component_group_name']=fpkm['gene'];
                
                        row["imputation_method"]=None;
                        row['test_stat']=fpkm['test_stat'];
                        row['test_description']='cuffdiff';
                        row['pvalue']=fpkm['p_value'];
                        row['pvalue_corrected']=fpkm['q_value'];
                        row['pvalue_corrected_description']='FDR';
                        row['mean']=fpkm['value_2']-fpkm['value_1'];
                        row['ci_level']=0.95; #assumption?
                        row['ci_lb']=None;
                        row['ci_ub']=None;
                        row['fold_change']=fpkm['fold_change_log2'];
                        row['calculated_concentration_units']='log2(FC)';
                        row['used_']=fpkm['used_']
                        row['comment_']=fpkm['comment_'];                
                        data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_pairWiseTest',data_O);
    #Query data from COBRA sampledData:
    def import_dataStage02PhysiologyPairWiseTest(self,
                analysis_id_I,
                rxn_ids_I = [],
                sample_name_abbreviations_1_I = [],
                sample_name_abbreviations_2_I = [],
                simulation_ids_1_I = [],
                simulation_ids_2_I = [],
                rxnID2componentName_I = {},
                rxnID2componentGroupName_I = {},
                snaCOBRA2sna_I = {},
                analysisID2analysisIDCOBRA_I = {},
                ):
        '''
        TODO:...
        get the sample pairWise statistics from data_stage02_physiology_pairWiseTest
        INPUT:
        TODO:...
        OUTPUT:
        TODO:...
        '''

        physiology_pairWiseTest_query = stage02_physiology_pairWiseTest_query(self.session,self.engine,self.settings);

        data_O = [];

        if analysisID2analysisIDCOBRA_I: analysis_id = analysisID2analysisIDCOBRA_I[analysis_id_I];
        else: analysis_id = analysis_id_I;

        data_tmp = [];
        data_tmp = physiology_pairWiseTest_query.get_rows_analysisID_dataStage02PhysiologyPairWiseTest(analysis_id);
        # map the data
        for fpkm in data_tmp:
            row = {};
            row['analysis_id']=analysis_id_I;
            if snaCOBRA2sna_I:
                sample_name_1=snaCOBRA2sna_I[fpkm['simulation_id_1']];
                sample_name_2=snaCOBRA2sna_I[fpkm['simulation_id_2']];
                #experiment_id=analysis_dict[snaCOBRA2sna_I[fpkm['simulation_id']]]['experiment_id'];
                #time_point=analysis_dict[snaCOBRA2sna_I[fpkm['simulation_id']]]['time_point'];
            else:
                sample_name_1=fpkm['simulation_id_1'];
                sample_name_2=fpkm['simulation_id_2'];
                #time_point=analysis_dict[fpkm['simulation_id']]['time_point'];
            if rxn_ids_I and not fpkm['rxn_id'] in rxn_ids_I: continue;
            if sample_name_abbreviations_1_I and not sample_name_1 in sample_name_abbreviations_1_I: continue;
            if sample_name_abbreviations_2_I and not sample_name_2 in sample_name_abbreviations_2_I: continue;
            if simulation_ids_1_I and not fpkm['simulation_id_1'] in simulation_ids_1_I: continue;
            if simulation_ids_2_I and not fpkm['simulation_id_2'] in simulation_ids_2_I: continue;
            row['sample_name_abbreviation_1']=sample_name_1;
            row['sample_name_abbreviation_2']=sample_name_2;
            #row['time_point']=time_point;
            #row['experiment_id']=time_point;

            row['used_']=fpkm['used_']
            row['comment_']=fpkm['comment_'];  
            if rxnID2componentName_I:
                row['component_name']=rxnID2componentName_I[fpkm['rxn_id']];
            else:
                row['component_name']=fpkm['rxn_id'];
            if rxnID2componentGroupName_I:
                row['component_group_name']=rxnID2componentGroupName_I[fpkm['rxn_id']];
            else:
                row['component_group_name']=fpkm['rxn_id'];
            row['calculated_concentration_units']=fpkm['flux_units'];

            #data_stage02_physiology_pairWiseTest map
            row['test_stat'] = fpkm['test_stat'];
            row['test_description']=fpkm['test_description'];
            row['pvalue']=fpkm['pvalue'];
            row['pvalue_corrected']=fpkm['pvalue_corrected'];
            row['pvalue_corrected_description']=fpkm['pvalue_corrected_description'];
            row['mean']=fpkm['mean'];
            row['ci_level']=fpkm['ci_level'];
            row['ci_lb']=fpkm['ci_lb'];
            row['ci_ub']=fpkm['ci_ub'];
            row['fold_change']=fpkm['fold_change']               
            data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_pairWiseTest',data_O);
    def import_dataStage02PhysiologyPairWiseTestMetabolites(self,
                analysis_id_I,
                met_ids_I = [],
                sample_name_abbreviations_1_I = [],
                sample_name_abbreviations_2_I = [],
                simulation_ids_1_I = [],
                simulation_ids_2_I = [],
                metID2componentName_I = {},
                metID2componentGroupName_I = {},
                snaCOBRA2sna_I = {},
                analysisID2analysisIDCOBRA_I = {},
                ):
        '''
        TODO:...
        get the sample pairWise statistics from data_stage02_physiology_pairWiseTest
        INPUT:
        TODO:...
        OUTPUT:
        TODO:...
        '''
        
        physiology_pairWiseTest_query = stage02_physiology_pairWiseTest_query(self.session,self.engine,self.settings);

        data_O = [];

        if analysisID2analysisIDCOBRA_I: analysis_id = analysisID2analysisIDCOBRA_I[analysis_id_I];
        else: analysis_id = analysis_id_I;

        data_tmp = [];
        data_tmp = physiology_pairWiseTest_query.get_rows_analysisID_dataStage02PhysiologyPairWiseTestMetabolites(analysis_id);
        # map the data
        for fpkm in data_tmp:
            row = {};
            row['analysis_id']=analysis_id_I;
            if snaCOBRA2sna_I:
                sample_name_1=snaCOBRA2sna_I[fpkm['simulation_id_1']];
                sample_name_2=snaCOBRA2sna_I[fpkm['simulation_id_2']];
                #experiment_id=analysis_dict[snaCOBRA2sna_I[fpkm['simulation_id']]]['experiment_id'];
                #time_point=analysis_dict[snaCOBRA2sna_I[fpkm['simulation_id']]]['time_point'];
            else:
                sample_name_1=fpkm['simulation_id_1'];
                sample_name_2=fpkm['simulation_id_2'];
                #time_point=analysis_dict[fpkm['simulation_id']]['time_point'];
            if met_ids_I and not fpkm['met_id'] in met_ids_I: continue;
            if sample_name_abbreviations_1_I and not sample_name_1 in sample_name_abbreviations_1_I: continue;
            if sample_name_abbreviations_2_I and not sample_name_2 in sample_name_abbreviations_2_I: continue;
            if simulation_ids_1_I and not fpkm['simulation_id_1'] in simulation_ids_1_I: continue;
            if simulation_ids_2_I and not fpkm['simulation_id_2'] in simulation_ids_2_I: continue;
            row['sample_name_abbreviation_1']=sample_name_1;
            row['sample_name_abbreviation_2']=sample_name_2;
            #row['time_point']=time_point;
            #row['experiment_id']=time_point;

            row['used_']=fpkm['used_']
            row['comment_']=fpkm['comment_'];  
            if metID2componentName_I:
                row['component_name']=metID2componentName_I[fpkm['met_id']];
            else:
                row['component_name']=fpkm['met_id'];
            if metID2componentGroupName_I:
                row['component_group_name']=metID2componentGroupName_I[fpkm['met_id']];
            else:
                row['component_group_name']=fpkm['met_id'];
            row['calculated_concentration_units']=fpkm['flux_units'];

            #data_stage02_physiology_pairWiseTest map
            row['test_stat'] = fpkm['test_stat'];
            row['test_description']=fpkm['test_description'];
            row['pvalue']=fpkm['pvalue'];
            row['pvalue_corrected']=fpkm['pvalue_corrected'];
            row['pvalue_corrected_description']=fpkm['pvalue_corrected_description'];
            row['mean']=fpkm['mean'];
            row['ci_level']=fpkm['ci_level'];
            row['ci_lb']=fpkm['ci_lb'];
            row['ci_ub']=fpkm['ci_ub'];
            row['fold_change']=fpkm['fold_change']               
            data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_pairWiseTest',data_O);

   