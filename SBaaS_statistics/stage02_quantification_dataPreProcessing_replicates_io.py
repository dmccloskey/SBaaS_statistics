# System
import json
# SBaaS
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
#Resources:
from listDict.listDict import listDict
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
#SBaaS_rnasequencing
from SBaaS_rnasequencing.stage01_rnasequencing_genesFpkmTracking_query import stage01_rnasequencing_genesFpkmTracking_query
from SBaaS_rnasequencing.stage01_rnasequencing_genesCountTable_query import stage01_rnasequencing_genesCountTable_query
#SBaaS_quantification
from SBaaS_quantification.stage01_quantification_replicates_query import stage01_quantification_replicates_query
from SBaaS_quantification.stage01_quantification_replicatesMI_query import stage01_quantification_replicatesMI_query
from SBaaS_quantification.stage01_quantification_physiologicalRatios_query import stage01_quantification_physiologicalRatios_query
#DDT
from ddt_python.ddt_container_table import ddt_container_table

class stage02_quantification_dataPreProcessing_replicates_io(stage02_quantification_dataPreProcessing_replicates_query,
                                    sbaas_template_io #abstract io methods
                                    ):
    
    #Query data from RNASequencing:
    def import_dataStage01RNASequencingGenesFpkmTracking(self,
                analysis_id_I,
                geneShortName2componentName_I = {},
                geneShortName2componentGroupName_I = {},
                sns2snsRNASequencing_I = {}
                ):
        '''get the the genes.fpkm_tracking data from SBaaS_rnasequencing
        INPUT:
        geneShortName2componentName_I = {}, mapping of gene_short_name to component_name
        geneShortName2componentGroupName_I = {}, mapping of gene_short_name to component_group_name
        sns2snsRNASequencing_I = {
                                'OxicEvo04Ecoli13CGlc':'OxicEvo04EcoliGlc',
                                'OxicEvo04gndEcoli13CGlc':'OxicEvo04gndEcoliGlc',
                                'OxicEvo04pgiEcoli13CGlc':'OxicEvo04pgiEcoliGlc',
                                'OxicEvo04sdhCBEcoli13CGlc':'OxicEvo04sdhCBEcoliGlc',
                                'OxicEvo04tpiAEcoli13CGlc':'OxicEvo04tpiAEcoliGlc'}
        OUTPUT:
        '''
        rnasequencing_genesFpkmTracking_query = stage01_rnasequencing_genesFpkmTracking_query(self.session,self.engine,self.settings);
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        data_O = [];
        for analysis_row in analysis_rows:
            # query fpkm data:
            fpkms = [];
            if sns2snsRNASequencing_I: sample_name = sns2snsRNASequencing_I[analysis_row['sample_name_short']];
            else: sample_name = analysis_row['sample_name_short'];
            fpkms = rnasequencing_genesFpkmTracking_query.get_rows_experimentIDAndSampleName_dataStage01RNASequencingGenesFpkmTracking(analysis_row['experiment_id'],sample_name);
            # map the data
            for fpkm in fpkms:
                row = {};
                row['analysis_id']=analysis_id_I;
                row['experiment_id']=analysis_row['experiment_id'];
                row['sample_name_short']=analysis_row['sample_name_short'];
                row['time_point']=analysis_row['time_point'];
                if geneShortName2componentName_I:
                    row['component_name']=geneShortName2componentName_I[fpkm['gene_id']];
                else:
                    row['component_name']=fpkm['gene_short_name'] + '_' + fpkm['gene_id'];
                if geneShortName2componentGroupName_I:
                    row['component_group_name']=geneShortName2componentGroupName_I[fpkm['gene_short_name']];
                else:
                    row['component_group_name']=fpkm['gene_short_name'];
                
                row["imputation_method"]=None;
                row['calculated_concentration']=fpkm['FPKM'];
                #row['calculated_concentration_units']='FPKM'+"_"+fpkm['normalization_method'];
                row['calculated_concentration_units']='FPKM';
                row['used_']=fpkm['used_']
                row['comment_']=fpkm['comment_'];                
                data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);
    def import_dataStage01RNASequencingGenesCountTable(self,
                analysis_id_I,
                geneShortName2componentName_I = {},
                geneShortName2componentGroupName_I = {},
                snsRNASequencing2sns_I = {},
                analysisID2analysisIDRNASequencing_I = {},
                geneShortNames_I=[]
                ):
        '''get the the genes.fpkm_tracking data from SBaaS_rnasequencing
        INPUT:
        geneShortName2componentName_I = {}, mapping of gene_short_name to component_name
        geneShortName2componentGroupName_I = {}, mapping of gene_short_name to component_group_name
        snsRNASequencing2sns_I = {
                                'OxicEvo04Ecoli13CGlc':'OxicEvo04EcoliGlc',
                                'OxicEvo04gndEcoli13CGlc':'OxicEvo04gndEcoliGlc',
                                'OxicEvo04pgiEcoli13CGlc':'OxicEvo04pgiEcoliGlc',
                                'OxicEvo04sdhCBEcoli13CGlc':'OxicEvo04sdhCBEcoliGlc',
                                'OxicEvo04tpiAEcoli13CGlc':'OxicEvo04tpiAEcoliGlc'}
        analysisID2analysisIDRNASequencing = {}, mapping of statistics analysis ID to RNAseq analysis ID
        geneShortNames_I = list of gene_short_names to include
        OUTPUT:
        '''
        rnasequencing_genesCountTable_query = stage01_rnasequencing_genesCountTable_query(self.session,self.engine,self.settings);
        data_O = [];
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        sns2tp = {r['sample_name_short']:r['time_point'] for r in analysis_rows};
        # query fpkm data:
        if analysisID2analysisIDRNASequencing_I: analysis_id=analysisID2analysisIDRNASequencing_I[analysis_id_I]
        else: analysis_id=analysis_id_I;
        fpkms = [];
        fpkms = rnasequencing_genesCountTable_query.get_rows_analysisID_dataStage01RNASequencingGenesCountTable(analysis_id);
        # map the data
        for fpkm in fpkms:
            if geneShortNames_I and not fpkm['gene_short_name'] in geneShortNames_I: continue
            row = {};
            row['analysis_id']=analysis_id;
            row['experiment_id']=fpkm['experiment_id'];
            if snsRNASequencing2sns_I: sample_name = snsRNASequencing2sns_I[fpkm['sample_name']];
            else: sample_name = fpkm['sample_name'];
            row['sample_name_short']=sample_name;

            row['time_point']=sns2tp[sample_name];

            if geneShortName2componentName_I:
                row['component_name']=geneShortName2componentName_I[fpkm['gene_id']];
            else:
                row['component_name']=fpkm['gene_short_name'] + '_' + fpkm['gene_id'];
            if geneShortName2componentGroupName_I:
                row['component_group_name']=geneShortName2componentGroupName_I[fpkm['gene_short_name']];
            else:
                row['component_group_name']=fpkm['gene_short_name'];
                
            row["imputation_method"]=None;
            row['calculated_concentration']=fpkm['value'];
            row['calculated_concentration_units']=fpkm['value_units']+'_cuffnorm';
            row['used_']=fpkm['used_']
            row['comment_']=fpkm['comment_'];                
            data_O.append(row);
        # add data to the DB
        if data_O: self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);

    #Query data from quantification:    
    def import_dataStage01QuantificationReplicates(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                componentName2componentName_I = {},
                componentGroupName2componentGroupName_I = {},
                sns2sns_I = {}
                ):
        '''
        INPUT:
        OUTPUT:
        '''
        quantification_replicates_query = stage01_quantification_replicates_query(self.session,self.engine,self.settings);
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiments
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            experiment_ids = list(set([row['experiment_id'] for row in analysis_rows]));
            calculated_concentration_units = [];
            for experiment_id in experiment_ids:
                calculated_concentration_units_tmp = []
                calculated_concentration_units_tmp = quantification_replicates_query.get_calculatedConcentrationUnits_experimentID_dataStage01Replicates(experiment_id);
                calculated_concentration_units.extend(calculated_concentration_units_tmp)
            calculated_concentration_units = list(set(calculated_concentration_units));
        for cu in calculated_concentration_units:
            print('getting data for concentration_units ' + cu);
            data_O = [];
            # get all of the samples in the simulation
            for analysis_row in analysis_rows:
                data_tmp = [];
                data_tmp = quantification_replicates_query.get_rows_experimentIDAndSampleNameShortAndTimePointAndCalculatedConcentrationUnits_dataStage01Replicates(
                    analysis_row['experiment_id'], analysis_row['sample_name_short'], analysis_row['time_point'], cu);
                #split 2:
                data_listDict = listDict();
                data_listDict.set_listDict(data_tmp);
                data_listDict.convert_listDict2DataFrame();
                data_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_listDict.dataFrame['id'] = None;
                data_listDict.add_column2DataFrame("imputation_method",None);
                data_listDict.convert_dataFrame2ListDict();
                data_O.extend(data_listDict.get_listDict());
                ##split 1:
                #for row in data_tmp:
                #    row['analysis_id']=analysis_id_I;
                #    row['id']=None;
                #    row["imputation_method"]=None;
                #    data_O.append(row);
            # add data to the DB every calculated concentration unit to avoid a massive transaction
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);   
    def import_dataStage01QuantificationReplicatesMI(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                componentName2componentName_I = {},
                componentGroupName2componentGroupName_I = {},
                sns2sns_I = {}
                ):
        '''get the the genes.fpkm_tracking data from SBaaS_rnasequencing
        INPUT:
        OUTPUT:
        '''
        quantification_replicatesMI_query = stage01_quantification_replicatesMI_query(self.session,self.engine,self.settings);
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiments
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            experiment_ids = list(set([row['experiment_id'] for row in analysis_rows]));
            calculated_concentration_units = [];
            for experiment_id in experiment_ids:
                calculated_concentration_units_tmp = []
                calculated_concentration_units_tmp = quantification_replicatesMI_query.get_calculatedConcentrationUnits_experimentID_dataStage01ReplicatesMI(experiment_id);
                calculated_concentration_units.extend(calculated_concentration_units_tmp)
            calculated_concentration_units = list(set(calculated_concentration_units));
        for cu in calculated_concentration_units:
            print('getting data for concentration_units ' + cu);
            data_O = [];
            # get all of the samples in the simulation
            for analysis_row in analysis_rows:
                data_tmp = [];
                data_tmp = quantification_replicatesMI_query.get_rows_experimentIDAndSampleNameShortAndTimePointAndCalculatedConcentrationUnits_dataStage01ReplicatesMI(
                    analysis_row['experiment_id'], analysis_row['sample_name_short'], analysis_row['time_point'], cu);
                #split 2:
                data_listDict = listDict();
                data_listDict.set_listDict(data_tmp);
                data_listDict.convert_listDict2DataFrame();
                data_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_listDict.dataFrame['id'] = None;
                data_listDict.convert_dataFrame2ListDict();
                data_O.extend(data_listDict.get_listDict());
                ##split 1:
                #for row in data_tmp:
                #    row['analysis_id']=analysis_id_I;
                #    row['id']=None;
                #    row["imputation_method"]=None;
                #    data_O.append(row);
            # add data to the DB every calculated concentration unit to avoid a massive transaction
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O); 
    def import_dataStage01QuantificationPhysiologicalRatios(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                componentName2componentName_I = {},
                componentGroupName2componentGroupName_I = {},
                sns2sns_I = {}
                ):
        '''get the the genes.fpkm_tracking data from SBaaS_rnasequencing
        INPUT:
        OUTPUT:
        '''
        quantification_physiologicalRatios_query = stage01_quantification_physiologicalRatios_query(self.session,self.engine,self.settings);
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiments

        data_O = [];
        # get all of the samples in the simulation
        for analysis_row in analysis_rows:
            data_tmp = [];
            data_tmp = quantification_physiologicalRatios_query.get_rows_experimentIDAndSampleNameShortAndTimePoint_dataStage01PhysiologicalRatiosReplicates(
                analysis_row['experiment_id'], analysis_row['sample_name_short'], analysis_row['time_point']);
            #split 2:
            data_listDict = listDict();
            data_listDict.set_listDict(data_tmp);
            data_listDict.convert_listDict2DataFrame();
            data_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
            data_listDict.add_column2DataFrame("imputation_method",None);
            data_listDict.add_column2DataFrame("calculated_concentration_units",'ratio');
            data_listDict.change_rowAndColumnNames(
                column_names_dict_I={'physiologicalratio_id':'component_name',
                    'physiologicalratio_value':'calculated_concentration',
                    #'physiologicalratio_description':'comment_'
                    })
            data_listDict.convert_dataFrame2ListDict();
            data_O.extend(data_listDict.get_listDict());
            ##split 1:
            #for row in data_tmp:
            #    row['analysis_id']=analysis_id_I;
            #    row['id']=None;
            #    row["imputation_method"]=None;
            #    data_O.append(row);
        # add data to the DB every calculated concentration unit to avoid a massive transaction
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);

    #Updates from file:
    def import_setUsed2False_experimentIDAndSampleNameShortAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.setUsed2False_experimentIDAndSampleNameShortAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(data.data);
        data.clear_data();
    def import_delete_rows_experimentIDAndSampleNameShortAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.delete_rows_experimentIDAndSampleNameShortAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(data.data);
        data.clear_data();

    #Visualization
    def export_dataStage02QuantificationDataPreProcessingReplicates_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export a tabular representation of the data
        INPUT:
        analysis_id_I = string,
        '''

        #get the data for the analysis
        data_points_O = [];
        data_points_O = self.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);

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
    def export_dataStage02QuantificationDataPreProcessingReplicatesCrossTable_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export a heatmap and cross-table representation of the data
        PLOTS:
        1. cross-table
        INPUT:
        analysis_id_I = string,
        '''

        #get the data for the analysis
        data_points_O = [];
        data_points_O = self.get_rowsAndSampleNameAbbreviations_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
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