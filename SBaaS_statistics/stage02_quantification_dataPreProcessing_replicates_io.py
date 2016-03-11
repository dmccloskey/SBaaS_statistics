# System
import json
# SBaaS
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
#SBaaS_rnasequencing
from SBaaS_rnasequencing.stage01_rnasequencing_genesFpkmTracking_query import stage01_rnasequencing_genesFpkmTracking_query

class stage02_quantification_dataPreProcessing_replicates_io(stage02_quantification_dataPreProcessing_replicates_query,
                                    sbaas_template_io #abstract io methods
                                    ):
    
    #Query data from RNASequencing:
    def import_dataStage01RNASequencingGenesFpkmTracking(self,
                analysis_id_I,
                geneShortName2componentName_I = {},
                geneShortName2componentGroupName_I = {},
                snsPreProcessing2snRNASequencing_I = {}
                ):
        '''get the the genes.fpkm_tracking data from SBaaS_rnasequencing
        INPUT:
        geneShortName2componentName_I = {}, mapping of gene_short_name to component_name
        geneShortName2componentGroupName_I = {}, mapping of gene_short_name to component_group_name
        sns2snRNASequencing_I = {
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
            if snsPreProcessing2snRNASequencing_I: sample_name = snsPreProcessing2snRNASequencing_I[analysis_row['sample_name_short']];
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