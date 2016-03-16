# System
import json
# SBaaS
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# SBaaS_resequencing
from SBaaS_resequencing.stage01_resequencing_mutationsAnnotated_query import stage01_resequencing_mutationsAnnotated_query
from sequencing_analysis.genome_diff import genome_diff
#SBaaS_rnasequencing
from SBaaS_rnasequencing.stage01_rnasequencing_geneExpDiff_query import stage01_rnasequencing_geneExpDiff_query
# Resources
from python_statistics.calculate_interface import calculate_interface

class stage02_quantification_dataPreProcessing_replicates_io(stage02_quantification_dataPreProcessing_replicates_query,
                                    sbaas_template_io #abstract io methods
                                    ):
    #Query data from Requencing:
    def import_dataStage01ResequencingMutationsAnnotated(self,
                                                        
                mutationID2componentName_I = {},
                mutationGenes2componentGroupName_I = {},
                sna2snRequencing_I = {}
                ):
        '''get the mutation_frequency data from SBaaS_resequencing
        INPUT:
        mutationID2componentName_I = {}, mapping of gene_short_name to component_name
        mutationGenes2componentGroupName_I = {}, mapping of gene_short_name to component_group_name
        sna2snRequencing_I = {
                                'OxicEvo04Ecoli13CGlc':'OxicEvo04EcoliGlc',
                                'OxicEvo04gndEcoli13CGlc':'OxicEvo04gndEcoliGlc',
                                'OxicEvo04pgiEcoli13CGlc':'OxicEvo04pgiEcoliGlc',
                                'OxicEvo04sdhCBEcoli13CGlc':'OxicEvo04sdhCBEcoliGlc',
                                'OxicEvo04tpiAEcoli13CGlc':'OxicEvo04tpiAEcoliGlc'}
        OUTPUT:
        TODO:...
        '''
        resequencing_mutationsAnnotated_query = stage01_resequencing_mutationsAnnotated_query(self.session,self.engine,self.settings);
        genomediff = genome_diff();
        calc = calculate_interface();
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        data_O = [];
        for analysis_row in analysis_rows:
            # query mutation_frequency data:
            mutation_frequencies = [];
            if sna2snRequencing_I: sample_name = sna2snRequencing_I[analysis_row['sample_name_abbreviation']];
            else: sample_name = analysis_row['sample_name_abbreviation'];
            mutation_frequencies = resequencing_mutationsAnnotated_query.get_mutations_experimentIDAndSampleName_dataStage01ResequencingMutationsAnnotated(analysis_row['experiment_id'],sample_name);
            # map the data
            for mutation_frequency in mutation_frequencies:
                row = {};
                row['analysis_id']=analysis_id_I;
                row['experiment_id']=analysis_row['experiment_id'];
                row['time_point']=analysis_row['time_point'];
                row["imputation_method"]=None;
                row['used_']=mutation_frequency['used_']
                row['comment_']=mutation_frequency['comment_'];  
                #sample name mapping
                row['sample_name_abbreviation']=analysis_row['sample_name_abbreviation'];
                #component mapping                
                mutation_id = genomediff._make_mutationID(
                    mutation_frequency['mutation_genes,mutation_frequency'],
                    mutation_frequency['mutation_type,mutation_frequency'],
                    mutation_frequency['mutation_position']
                    );
                mutation_genes = genomediff._make_mutationGenesStr(mutation_frequency['mutation_genes'])
                if mutationID2componentName_I:
                    row['component_name']=mutationID2componentName_I[mutation_id];
                else:
                    row['component_name']=mutation_id;
                if mutationGenes2componentGroupName_I:
                    row['component_group_name']=mutationGenes2componentGroupName_I[mutation_genes];
                else:
                    row['component_group_name']=mutation_genes;
                row['calculated_concentration_units']='Frequency';
                #descriptive statistics map
                data_mean,data_median = mutation_frequency['mutation_frequency'],mutation_frequency['mutation_frequency'];
                data_var = 0.2;
                if data_mean:
                    data_cv = sqrt(data_var)/data_mean*100;
                    data_lb = data_mean - sqrt(data_var)
                    data_ub = data_mean + sqrt(data_var)
                else:
                    data_cv = None;
                    data_lb = None;
                    data_ub = None;
                row['test_stat']=None;
                row['test_description']=None;
                row['pvalue']=None;
                row['pvalue_corrected']=None;
                row['pvalue_corrected_description']=None;
                row['mean']=mean;
                row['var']=var;
                row['cv']=data_cv;
                row['n']=1;
                row['ci_lb']=data_lb;
                row['ci_ub']=data_ub;
                row['ci_level']=0.95;
                row['min']=None;
                row['max']=None;
                row['median']=median;
                row['iq_1']=None;
                row['iq_3']=None;              
                data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages',data_O);
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
        sna2snaRNASequencing_I = {}
        OUTPUT:
        TODO:...
        '''
        rnasequencing_geneExpDiff_query = stage01_rnasequencing_geneExpDiff_query(self.session,self.engine,self.settings);
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # get the # of replicates per sample_name_abbreviation
        sample_name_dict = {};
        #sample_name_dict = self.(analysis_id_I);

        data_O = [];
        for sample_name_abbreviation_cnt_1,sample_name_abbreviation_1 in enumerate(sample_name_abbreviations):
            for sample_name_abbreviation_cnt_2,sample_name_abbreviation_2 in enumerate(sample_name_abbreviations):
                if sample_name_abbreviation_cnt_1 != sample_name_abbreviation_cnt_2:
                    # query geneExpDiff data:
                    if sna2snaRNASequencing_I: sample_name = sna2snaRNASequencing_I[analysis_row['sample_name_abbreviation']];
                    else: sample_name = analysis_row['sample_name_abbreviation'];
                    geneExpDiff_tmp = [];
                    geneExpDiff_tmp = self.get_rows_experimentIDsAndSampleNameAbbreviations_dataStage01RNASequencingGeneExpDiff(experiment_ids[sample_name_abbreviation_cnt_1],experiment_ids[sample_name_abbreviation_cnt_2],sample_name_abbreviation_1,sample_name_abbreviation_2);
                    # map the data
                    for fpkm in geneExpDiff_tmp:
                        row = {};
                        row['analysis_id']=analysis_id_I;
                        row['experiment_id']=('%s/%s' %(analysis_row_1['experiment_id']),analysis_row_2['experiment_id']);
                        row['time_point']=('%s/%s' %(analysis_row_1['time_point_1']),analysis_row_2['time_point']);
                        row['sample_name_abbreviation']=('%s/%s' %(analysis_row_1['sample_name_abbreviation']),analysis_row_2['sample_name_abbreviation']);
                        row['used_']=fpkm['used_']
                        row['comment_']=fpkm['comment_'];  
                        if geneShortName2componentName_I:
                            row['component_name']=geneShortName2componentName_I[fpkm['gene_id']];
                        else:
                            row['component_name']=fpkm['gene_short_name'] + '_' + fpkm['gene_id'];
                        if geneShortName2componentGroupName_I:
                            row['component_group_name']=geneShortName2componentGroupName_I[fpkm['gene_short_name']];
                        else:
                            row['component_group_name']=fpkm['gene_short_name'];
                        row['calculated_concentration_units']='log2(FC)';
                        #descriptive statistics map
                        data_mean,data_median = fpkm['fold_change_log2'],fpkm['fold_change_log2'];
                        data_var = None;
                        data_cv = None;
                        data_lb = None;
                        data_ub = None;
                        row['test_stat']=fpkm['test_stat'];
                        row['test_description']='cuffdiff';
                        row['pvalue']=fpkm['p_value'];
                        row['pvalue_corrected']=fpkm['q_value'];
                        row['pvalue_corrected_description']='FDR';
                        row['mean']=mean;
                        row['var']=var;
                        row['cv']=data_cv;
                        row['n']=1;
                        row['ci_lb']=data_lb;
                        row['ci_ub']=data_ub;
                        row['ci_level']=0.95;
                        row['min']=None;
                        row['max']=None;
                        row['median']=median;
                        row['iq_1']=None;
                        row['iq_3']=None;                 
                        data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages',data_O);