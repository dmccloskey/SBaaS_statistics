# System
import json
# SBaaS
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# SBaaS_resequencing
from SBaaS_resequencing.stage01_resequencing_gd_query import stage01_resequencing_gd_query
from sequencing_analysis.genome_diff import genome_diff
#SBaaS_rnasequencing
from SBaaS_rnasequencing.stage01_rnasequencing_geneExpDiff_query import stage01_rnasequencing_geneExpDiff_query
# Resources
from python_statistics.calculate_interface import calculate_interface
import numpy as np
from math import sqrt

class stage02_quantification_dataPreProcessing_averages_io(stage02_quantification_dataPreProcessing_averages_query,
                                    sbaas_template_io #abstract io methods
                                    ):
    #Query data from Requencing:
    def import_dataStage01ResequencingMutationsAnnotated(self,
                analysis_id_I,   
                mutationID2componentName_I = {},
                mutationGenes2componentGroupName_I = {},
                sna2snRequencing_I = {},
                frequency_threshold_I = 0.1,
                frequency_var_I = 0.01,
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
        frequency_threshold_I = float, lower limit of mutation frequency
        frequency_var_I = float, estimated variation of mutation frequency calls
        OUTPUT:
 
        '''
        resequencing_gd_query = stage01_resequencing_gd_query(self.session,self.engine,self.settings);
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
            mutation_frequencies = resequencing_gd_query.get_mutations_experimentIDAndSampleName_dataStage01ResequencingMutationsAnnotated(analysis_row['experiment_id'],sample_name);
            # map the data
            for mutation_frequency in mutation_frequencies:
                if mutation_frequency['mutation_frequency']<frequency_threshold_I: continue;
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
                    mutation_frequency['mutation_genes'],
                    mutation_frequency['mutation_type'],
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
                data_var = frequency_var_I;
                if data_mean:
                    data_cv = sqrt(data_var)/data_mean*100;
                    data_lb = data_mean - sqrt(data_var);
                    if data_lb < 0.: data_lb = 0.;
                    data_ub = data_mean + sqrt(data_var)
                    if data_ub > 1.: data_ub = 1.0;
                else:
                    data_cv = None;
                    data_lb = None;
                    data_ub = None;
                row['test_stat']=None;
                row['test_description']=None;
                row['pvalue']=0.;
                row['pvalue_corrected']=0.;
                row['pvalue_corrected_description']=None;
                row['mean']=data_mean;
                row['var']=data_var;
                row['cv']=data_cv;
                row['n']=1;
                row['ci_lb']=data_lb;
                row['ci_ub']=data_ub;
                row['ci_level']=0.95;
                row['min']=None;
                row['max']=None;
                row['median']=data_median;
                row['iq_1']=None;
                row['iq_3']=None;              
                data_O.append(row);
        # remove any duplicates
        #TODO: refactor data_stage01_resequencing_mutationsAnnotated to remove duplicate rows
        data_db = [];
        unique_constraint = set();
        for row in data_O:
            unique_str = ','.join([row['component_name'],row['sample_name_abbreviation'],\
                row['experiment_id'],row['time_point'],row['analysis_id'],\
                row['calculated_concentration_units']])
            if not unique_str in unique_constraint:
                unique_constraint.add(unique_str);
                data_db.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages',data_db);
    #Query data from RNASequencing:
    def import_dataStage01RNASequencingGeneExpDiffFpkmTracking(self,
                analysis_id_I,
                geneID2componentName_I = {},
                gene2componentGroupName_I = {},
                snaRNASequencing2sna_I = {},
                analysisID2analysisIDRNASequencing_I = {},
                n_I=2,ci_level_I=0.95

                ):
        '''get the the genes.fpkm_tracking data from SBaaS_rnasequencing
        INPUT:
        geneID2componentName_I = {}, mapping of gene_short_name to component_name
        gene2componentGroupName_I = {}, mapping of gene_short_name to component_group_name
        snaRNASequencing2sna_I = {}
        OUTPUT:
        TODO:...
        '''
        quantification_analysis_query = stage02_quantification_analysis_query(self.session,self.engine,self.settings);
        rnasequencing_geneExpDiff_query = stage01_rnasequencing_geneExpDiff_query(self.session,self.engine,self.settings);
        data_O = [];
        # query geneExpDiffFpkmTracking data:
        if analysisID2analysisIDRNASequencing_I: analysis_id = analysisID2analysisIDRNASequencing_I[analysis_id_I];
        else: analysis_id = analysis_id_I;
        geneExpDiff_tmp = [];
        geneExpDiff_tmp = rnasequencing_geneExpDiff_query.get_rows_analysisID_dataStage01RNASequencingGeneExpDiffFpkmTracking(
            analysis_id);
        # map the data
        for fpkm in geneExpDiff_tmp:
            row = {};
            row['analysis_id']=analysis_id_I;
            row['experiment_id']=fpkm['experiment_id'];
            if snaRNASequencing2sna_I:
                sample_name=snaRNASequencing2sna_I['sample_name_abbreviation'];
            else:
                sample_name=fpkm['sample_name_abbreviation'];
            row['sample_name_abbreviation']=sample_name;
            #query the time-point from the analysis table
            time_point = quantification_analysis_query.get_timePoint_analysisIDAndExperimentIDAndSampleNameAbbreviation_dataStage02QuantificationAnalysis(analysis_id_I,fpkm['experiment_id'],sample_name);
            row['time_point']=time_point[0];
            row['used_']=fpkm['used_']
            row['comment_']=fpkm['comment_'];  
            if geneID2componentName_I:
                row['component_name']=geneID2componentName_I[fpkm['gene_id']];
            else:
                row['component_name']=fpkm['gene_short_name'] + '_' + fpkm['gene_id'];
            if gene2componentGroupName_I:
                row['component_group_name']=gene2componentGroupName_I[fpkm['gene_short_name']];
            else:
                row['component_group_name']=fpkm['gene_short_name'];
            #row['calculated_concentration_units']='FPKM_cuffdiff'+"_"+fpkm['normalization_method'];
            row['calculated_concentration_units']='FPKM_cuffdiff';
            #descriptive statistics map
            if fpkm['FPKM_status'] == 'OK': row['test_stat'] = 1;
            else: row['test_stat'] = 0;
            row['test_description']='cuffdiff';
            row['pvalue']=None;
            row['pvalue_corrected']=None;
            row['pvalue_corrected_description']=None;
            row['mean']=fpkm['FPKM'];
            
            # assuming the ci_level is 0.95
            row['ci_level']=ci_level_I;
            #TODO: move to stats module
            # assuming the stdev ~= stdErr
            #TODO: query the # of samples used
            stdev = (fpkm['FPKM_conf_hi']-fpkm['FPKM_conf_lo'])/3.92; # 95% CI only
            var = np.sqrt(stdev);
            if fpkm['FPKM']: cv = stdev/fpkm['FPKM']*100;
            else: cv = 0;
            row['var']=var;
            row['cv']=cv;
            row['n']=n_I;
            row['ci_lb']=fpkm['FPKM_conf_lo'];
            row['ci_ub']=fpkm['FPKM_conf_hi'];
            row['min']=None;
            row['max']=None;
            row['median']=None;
            row['iq_1']=None;
            row['iq_3']=None;                 
            data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages',data_O);
        
    #TODO: move to pairwisetest?
    def import_dataStage01RNASequencingGeneExpDiff_(self,
                analysis_id_I,
                geneID2componentName_I = {},
                gene2componentGroupName_I = {},
                sna2snaRNASequencing_I = {}
                ):
        '''get the the genes.fpkm_tracking data from SBaaS_rnasequencing
        INPUT:
        geneID2componentName_I = {}, mapping of gene_short_name to component_name
        gene2componentGroupName_I = {}, mapping of gene_short_name to component_group_name
        sna2snaRNASequencing_I = {}
        OUTPUT:
        TODO:...
        '''
        rnasequencing_geneExpDiff_query = stage01_rnasequencing_geneExpDiff_query(self.session,self.engine,self.settings);
        # get the analysis information
        analysis_rows = [];
        analysis_rows = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
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
                        row['experiment_id']=('%s/%s' %(analysis_row_2['experiment_id']),analysis_row_1['experiment_id']);
                        row['time_point']=('%s/%s' %(analysis_row_2['time_point']),analysis_row_1['time_point']);
                        row['sample_name_abbreviation']=('%s/%s' %(analysis_row_2['sample_name_abbreviation']),analysis_row_1['sample_name_abbreviation']);
                        row['used_']=fpkm['used_']
                        row['comment_']=fpkm['comment_'];  
                        if geneID2componentName_I:
                            row['component_name']=geneID2componentName_I[fpkm['gene_id']];
                        else:
                            row['component_name']=fpkm['gene'] + '_' + fpkm['gene_id'];
                        if gene2componentGroupName_I:
                            row['component_group_name']=gene2componentGroupName_I[fpkm['gene']];
                        else:
                            row['component_group_name']=fpkm['gene'];
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
                        row['n']=None;
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

    def import_dataStage01RNASequencingGeneExpDiff_foldChange(self,
                analysis_id_I,
                geneID2componentName_I = {},
                gene2componentGroupName_I = {},
                sna2snaRNASequencing_I = {},
                experimentID2experimentIDRNASequencing_I = {},
                sample_name_abbreviations_base_I = [],
                experiment_ids_base_I = [],
                add_self_vs_self_I = True,
                fold_change_log2_threshold_I = 2,
                q_value_threshold_I = 0.05,
                ):
        '''
        get the the genes.fpkm_tracking data from SBaaS_rnasequencing

        USE CASE:
        1. pull out a single differential expression experiment
            i.e., set(sample_name_abbreviation) = [sna_1,sna_2]
        2. pull out multiple differential expression experiments using exp_1, sna_1 as the comparison
            i.e., set(sample_name_abbreviation) = [sna_1,sna_2,...]
            the user must ensure the following:
                a. that the base exp/sna case is consistant accross all samples
                    when designing the analysis
                b. and that the base exp/sna case is the only base case in geneExpDiff
                c. if b in not true, the user can explicity enforce a particular base case

        INPUT:
        geneID2componentName_I = {}, mapping of rnasequencing gene_id to component_name
        gene2componentGroupName_I = {}, mapping of rnasequencing gene_short_name to component_group_name
        sna2snaRNASequencing_I = {}, mapping of sample_name_abbreviation to rnasequencing sample_name_abbreviation
        experimentID2experimentIDRNASequencing_I = {}, mapping of experiment_id to rnasequencing experiment_id
        analysisID2analysisIDRNASequencing_I = {}, analysis_id to rnasequencing analysis_id
        sample_name_abbreviations_base_I = [], sample_name_abbreviations to use as the base
        experiment_ids_base_I = [], experiment_ids to use as the base
        fold_change_log2_threshold_I = float, fold change values above which will be included
        q_value_threshold_I = float, correct pvalues above which will be included

        OUTPUT:
        TODO:...
        '''
        rnasequencing_geneExpDiff_query = stage01_rnasequencing_geneExpDiff_query(self.session,self.engine,self.settings);
        rnasequencing_geneExpDiff_query.initialize_supportedTables();

        data_O = [];
        #get the geneExpDiff data
        experiment_ids,sample_name_abbreviations = [],[];
        experiment_ids,sample_name_abbreviations,time_points = self.get_experimentIDAndSampleNameAbbreviationAndTimePoint_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);

        for sample_name_abbreviation_cnt_1,sample_name_abbreviation_1 in enumerate(sample_name_abbreviations):

            # enforce a particular experiment_id/sample_name_abbreviation base
            if not sample_name_abbreviation_1 in sample_name_abbreviations_base_I: continue;
            if not experiment_ids[sample_name_abbreviation_cnt_1] in experiment_ids_base_I: continue;

            if sna2snaRNASequencing_I: sample_name_abbreviation_1 = sna2snaRNASequencing_I[sample_name_abbreviation_1];
            else: sample_name_abbreviation_1 = sample_name_abbreviation_1;
            if experimentID2experimentIDRNASequencing_I: experiment_id_1 = experimentID2experimentIDRNASequencing_I[experiment_ids[sample_name_abbreviation_cnt_1]];
            else: experiment_id_1 = experiment_ids[sample_name_abbreviation_cnt_1];
            
            # get the geneExpDiff data
            unique_componentNamesAndComponentGroupNames = set();

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
                        row['experiment_id']=experiment_id_2;
                        row['time_point']=time_points[sample_name_abbreviation_cnt_2];
                        row['sample_name_abbreviation']=sample_name_abbreviation_2;
                        row['used_']=fpkm['used_']
                        row['comment_']=fpkm['comment_'];  
                        if geneID2componentName_I:
                            row['component_name']=geneID2componentName_I[fpkm['gene_id']];
                        else:
                            row['component_name']=fpkm['gene'] + '_' + fpkm['gene_id'];
                        if gene2componentGroupName_I:
                            row['component_group_name']=gene2componentGroupName_I[fpkm['gene']];
                        else:
                            row['component_group_name']=fpkm['gene'];

                        unique_componentNamesAndComponentGroupNames.add((row['component_name'],row['component_group_name']));

                        row['calculated_concentration_units']='log2(FC)';
                        #descriptive statistics map
                        data_var = None;
                        data_cv = None;
                        data_lb = None;
                        data_ub = None;
                        row['test_stat']=fpkm['test_stat'];
                        row['test_description']='cuffdiff';
                        row['pvalue']=fpkm['p_value'];
                        row['pvalue_corrected']=fpkm['q_value'];
                        row['pvalue_corrected_description']='FDR';
                        row['mean']=fpkm['fold_change_log2'];
                        row['var']=None;
                        row['cv']=None;
                        row['n']=None;
                        row['ci_lb']=None;
                        row['ci_ub']=None;
                        row['ci_level']=None;
                        row['min']=None;
                        row['max']=None;
                        row['median']=None;
                        row['iq_1']=None;
                        row['iq_3']=None;                 
                        data_O.append(row);

            if add_self_vs_self_I:
                #make a sample for the unique components
                for cn in unique_componentNamesAndComponentGroupNames:
                    row = {};
                    row['analysis_id']=analysis_id_I;
                    row['experiment_id']=experiment_id_1;
                    row['time_point']=time_points[sample_name_abbreviation_cnt_1];
                    row['sample_name_abbreviation']=sample_name_abbreviation_1;
                    row['used_']=fpkm['used_']
                    row['comment_']=fpkm['comment_'];
                    row['component_name']=cn[0];
                    row['component_group_name']=cn[1];
                    row['calculated_concentration_units']='log2(FC)';
                    row['test_stat']=None;
                    row['test_description']='cuffdiff';
                    row['pvalue']=1.0;
                    row['pvalue_corrected']=1.0;
                    row['pvalue_corrected_description']='FDR';
                    row['mean']=0.0; # log2(1.0) = 0; no fold_change
                    row['var']=None;
                    row['cv']=None;
                    row['n']=None;
                    row['ci_lb']=None;
                    row['ci_ub']=None;
                    row['ci_level']=None;
                    row['min']=None;
                    row['max']=None;
                    row['median']=None;
                    row['iq_1']=None;
                    row['iq_3']=None;                 
                    data_O.append(row);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages',data_O);