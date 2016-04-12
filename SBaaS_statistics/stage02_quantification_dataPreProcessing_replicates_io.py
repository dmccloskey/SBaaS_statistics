# System
import json
# SBaaS
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
#Resources:
from listDict.listDict import listDict
#SBaaS_rnasequencing
from SBaaS_rnasequencing.stage01_rnasequencing_genesFpkmTracking_query import stage01_rnasequencing_genesFpkmTracking_query
#SBaaS_quantification
from SBaaS_quantification.stage01_quantification_replicates_query import stage01_quantification_replicates_query
from SBaaS_quantification.stage01_quantification_replicatesMI_query import stage01_quantification_replicatesMI_query
from SBaaS_quantification.stage01_quantification_physiologicalRatios_query import stage01_quantification_physiologicalRatios_query

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
                row['calculated_concentration_units']='FPKM';
                row['used_']=fpkm['used_']
                row['comment_']=fpkm['comment_'];                
                data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);

    #Query data from quantification:    
    def import_dataStage01QuantificationReplicates(self,
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