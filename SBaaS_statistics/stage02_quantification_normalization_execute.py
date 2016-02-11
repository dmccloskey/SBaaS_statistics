from .stage02_quantification_normalization_io import stage02_quantification_normalization_io
from SBaaS_quantification.stage01_quantification_replicates_query import stage01_quantification_replicates_query
from SBaaS_quantification.stage01_quantification_replicatesMI_query import stage01_quantification_replicatesMI_query
# resources
from r_statistics.r_interface import r_interface
from matplotlib_utilities.matplot import matplot
# remove after making add methods
from .stage02_quantification_normalization_postgresql_models import *

class stage02_quantification_normalization_execute(stage02_quantification_normalization_io,
                                                   stage01_quantification_replicates_query,
                                                   stage01_quantification_replicatesMI_query):
    def execute_glogNormalization(self,analysis_id_I,concentration_units_I=[],plot_values_I = False,r_calc_I=None):
        '''glog normalize concentration values using R'''

        print('execute_glogNormalization...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        mplot = matplot();
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiment
        data_O = [];
        data_transformed = [];
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            for row in analysis_info:
                concentration_units_tmp = []
                concentration_units_tmp = self.get_concentrationUnits_experimentID_dataStage01ReplicatesMI(row['experiment_id']);
                concentration_units.extend(concentration_units_tmp)
            concentration_units = list(set(concentration_units));
        for cu in concentration_units:
            print('calculating glogNormalization for concentration_units ' + cu);
            data = [];
            # get all of the samples in the simulation
            for row in analysis_info:
                data_tmp = [];
                data_tmp = self.get_RExpressionData_AnalysisIDAndExperimentIDAndTimePointAndUnitsAndSampleNameShort_dataStage01ReplicatesMI(analysis_id_I,row['experiment_id'], row['time_point'], cu, row['sample_name_short']);
                data.extend(data_tmp)
            # call R
            concentrations = None;
            concentrations_glog = None;
            data_glog, concentrations, concentrations_glog = r_calc.calculate_glogNormalization(data)
            # record data
            data_transformed.extend(data_glog);
            #for i,d in enumerate(data_glog):
            #    #data_glog[i]['calculated_concentration_units']=cu+'_glog_normalized'
            #    d['analysis_id']=analysis_id_I;
            #    d['calculated_concentration_units'] = cu + '_glog_normalized';
            #    d['used_'] = True;
            #    d['comment_'] = None;
            #    data_transformed.append(d);
            # plot original values:
            if plot_values_I:
                mplot.densityPlot(concentrations);
                mplot.densityPlot(concentrations_glog);
            ## upload data
            #for d in data:
            #    d['analysis_id']=analysis_id_I;
            #    d['calculated_concentration_units'] = d['calculated_concentration_units'] + '_glog_normalized';
            #    d['used_'] = True;
            #    d['comment_'] = None;
            #    data_O.append(d);
            #    #row = data_stage02_quantification_glogNormalized(d);
            #    #row = None;
            #    #row = data_stage02_quantification_glogNormalized(analysis_id_I,d['experiment_id'], d['sample_name_short'],
            #    #                                            d['time_point'],d['component_group_name'],
            #    #                                            d['component_name'],d['calculated_concentration'],
            #    #                                            d['calculated_concentration_units'] + '_glog_normalized',
            #    #                                            True,None);
            #    #self.session.add(row);
            #data_transformed.extend(data_glog);
        # commit data to the session every timepoint
        self.add_dataStage02QuantificationGlogNormalized(data_transformed);
        #self.add_dataStage02QuantificationGlogNormalized(data_O);
        #self.session.commit();
        #self.update_concentrations_dataStage02GlogNormalized(analysis_id_I, data_transformed);
    def execute_glogNormalization_update(self,analysis_id_I):
        '''glog normalize concentration values using R'''

        print('execute_glogNormalization...')
        r_calc = r_interface();
        
        
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiment
        data_transformed = [];
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            print('calculating glogNormalization for concentration_units ' + cu);
            data = [];
            # get all of the samples in the analysis
            data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I, cu);
            # call R
            data_transformed = [];
            concentrations = None;
            concentrations_glog = None;
            data_glog, concentrations, concentrations_glog = r_calc.calculate_glogNormalization(data)
            ## plot original values:
            self.matplot.densityPlot(concentrations);
            self.matplot.densityPlot(concentrations_glog);
            # upload data
            data_transformed.extend(data_glog);
        # commit data to the session every timepoint
        self.session.commit();
        self.update_concentrations_dataStage02GlogNormalized(analysis_id_I, data_transformed)
    def execute_getDataStage01ReplicatesMI(self,analysis_id_I,concentration_units_I=[]):
        '''glog normalize concentration values using R'''

        print('execute_getDataStage01ReplicatesMI...')
        
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiment
        data_O = [];
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            for row in analysis_info:
                concentration_units_tmp = [];
                concentration_units_tmp = self.get_concentrationUnits_experimentID_dataStage01ReplicatesMI(row['experiment_id']);
                concentration_units.extend(concentration_units_tmp);
            concentration_units = list(set(concentration_units));
        for cu in concentration_units:
            print('calculating glogNormalization for concentration_units ' + cu);
            data = [];
            # get all of the samples in the simulation
            for row in analysis_info:
                data_tmp = [];
                data_tmp = self.get_RExpressionData_AnalysisIDAndExperimentIDAndTimePointAndUnitsAndSampleNameShort_dataStage01ReplicatesMI(analysis_id_I,row['experiment_id'], row['time_point'], cu, row['sample_name_short']);
                data.extend(data_tmp)
            # upload data
            for d in data:
                d['analysis_id']=analysis_id_I;
                d['used_']=True;
                d['comment_'] = None;
                data_O.append(d);
        #        row = None;
        #        row = data_stage02_quantification_glogNormalized(analysis_id_I,d['experiment_id'], d['sample_name_short'],
        #                                                    d['time_point'],d['component_group_name'],
        #                                                    d['component_name'],d['calculated_concentration'],
        #                                                    d['calculated_concentration_units'],
        #                                                    True,None);
        #        self.session.add(row);
        #self.session.commit();
        self.add_dataStage02QuantificationGlogNormalized(data_O);
    def execute_getDataStage01PhysiologicalRatios(self,analysis_id_I):
        '''glog normalize concentration values using R'''

        print('execute_getDataStage01ReplicatesMI...')
        
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiment
        data = [];
        data_O = [];
        # get all of the samples in the simulation
        for row in analysis_info:
            data_tmp = [];
            data_tmp = self.get_RExpressionData_AnalysisIDAndExperimentIDAndSampleNameShortAndTimePoint_dataStage01PhysiologicalRatiosReplicates(analysis_id_I,row['experiment_id'], row['sample_name_short'], row['time_point']);
            data.extend(data_tmp)
        # upload data
        for d in data:
            d['analysis_id']=analysis_id_I;
            d['component_group_name']=d['physiologicalratio_id']
            d['component_name']=d['physiologicalratio_name']
            d['calculated_concentration']=d['physiologicalratio_value']
            d['calculated_concentration_units']='ratio';
            d['used_']=True;
            d['comment_'] = d['physiologicalratio_description']
            data_O.append(d);
        #    row = None;
        #    row = data_stage02_quantification_glogNormalized(analysis_id_I,d['experiment_id'], d['sample_name_short'],
        #                                                d['time_point'],d['physiologicalratio_id'],
        #                                                d['physiologicalratio_name'],d['physiologicalratio_value'],
        #                                                'ratio',
        #                                                True,d['physiologicalratio_description']);
        #    self.session.add(row);
        #self.session.commit();
        self.add_dataStage02QuantificationGlogNormalized(data_O);
    def execute_componentNameSpecificNormalization(self,experiment_id_I,sample_name_abbreviations_I=[],cn_normalize_I='glu-L.glu_L_1.Light'):
        '''normalize concentration values to a specific component'''

        print('execute_componentGroupNameSpecificNormalization...')
        
        # query metabolomics data from the experiment
        # get sample name abbreviations
        if sample_name_abbreviations_I:
            sample_name_abbreviations = sample_name_abbreviations_I;
        else:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentID_dataStage01ReplicatesMI(experiment_id_I);
        for sna in sample_name_abbreviations:
            # get time points
            time_points = [];
            time_points = self.get_timePoint_experimentIDAndSampleNameAbbreviation_dataStage01ReplicatesMI(experiment_id_I,sna);
            for tp in time_points:
                print('calculating componentGroupNameSpecificNormalization for time_point ' + tp);
                # get sample_name_shorts
                sample_name_shorts = [];
                sample_name_shorts = self.get_sampleNameShort_experimentIDAndSampleNameAbbreviationAndTimePoint_dataStage01ReplicatesMI(experiment_id_I,sna,tp);
                for sns in sample_name_shorts:
                    data_transformed = [];
                    # get data for componentGroupName to be normalized to
                    cn_conc,cn_conc_units = None, None;
                    cn_conc,cn_conc_units = self.get_concentrationAndUnits_experimentIDAndTimePointAndSampleNameShortAndComponentName_dataStage01ReplicatesMI(experiment_id_I,tp,sns,cn_normalize_I);
                    # get concentration units...
                    concentration_units = [];
                    concentration_units = self.get_concentrationUnits_experimentIDAndTimePointAndSampleNameShort_dataStage01ReplicatesMI(experiment_id_I,tp,sns)
                    for cu in concentration_units:
                        normalize_units = cu + '*' + cn_conc_units + '_' + cn_normalize_I + '-1';
                        print('calculating componentGroupNameSpecificNormalization for concentration_units ' + cu);
                        data = [];
                        data = self.get_data_experimentIDAndTimePointAndSampleNameShortAndUnits_dataStage01ReplicatesMI(experiment_id_I, tp, sns, cu);
                        # normalize the data
                        concentrations = [];
                        concentrations_norm = [];
                        for i,d in enumerate(data):
                            concentrations.append(d['calculated_concentration']);
                            concentrations_norm.append(d['calculated_concentration']/cn_conc*100);
                            data[i].update({'calculated_concentration_normalized':d['calculated_concentration']/cn_conc*100});
                            data[i].update({'calculated_concentration_units_normalized':normalize_units});
                        ## plot original values:
                        #self.matplot.densityPlot(concentrations);
                        #self.matplot.densityPlot(concentrations_norm);
                        # upload data
                        for d in data:
                            row = data_stage02_quantification_glogNormalized(experiment_id_I, d['sample_name_short'],
                                                                        d['time_point'],d['component_group_name'],
                                                                        d['component_name'],d['calculated_concentration_normalized'],
                                                                        d['calculated_concentration_units_normalized'],
                                                                        True,None);
                            self.session.add(row);
                        data_transformed.extend(data);
            # commit data to the session every sample_name_abbreviation
            self.session.commit();
    def execute_sampleNameSpecificNormalization(self,sample_names_I = []):
        '''Normalize all components to the mean value of the same component in a specific sample or pool of samples
        INPUT:
        sample_names_I = [] of strings,
            if more than one sample, the average of all samples will be used
        '''
        pass;

    '''
    TODO:
    row-wise scaling (all metabolites for a specific sample)
    sum
    mean
    mode
    
    column-wise scaling (all samples for a specific metabolite)
    auto-scaling
    pareto-scaling
    range-scaling
    log[x]-scaling
    '''
    def execute_glogNormalization_v2(self,analysis_id_I,concentration_units_I=[],plot_values_I = False,r_calc_I=None):
        '''glog normalize concentration values using R'''

        print('execute_glogNormalization...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        mplot = matplot();
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from the experiment
        data_O = [];
        data_transformed = [];
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            for row in analysis_info:
                concentration_units_tmp = []
                concentration_units_tmp = self.get_concentrationUnits_experimentID_dataStage01ReplicatesMI(row['experiment_id']);
                concentration_units.extend(concentration_units_tmp)
            concentration_units = list(set(concentration_units));
        for cu in concentration_units:
            print('calculating glogNormalization for concentration_units ' + cu);
            data = [];
            # get all of the samples in the simulation
            for row in analysis_info:
                data_tmp = [];
                data_tmp = self.get_RExpressionData_AnalysisIDAndExperimentIDAndTimePointAndUnitsAndSampleNameShort_dataStage01ReplicatesMI(analysis_id_I,row['experiment_id'], row['time_point'], cu, row['sample_name_short']);
                data.extend(data_tmp)
            # call R
            concentrations = None;
            concentrations_glog = None;
            data_glog, concentrations, concentrations_glog = r_calc.calculate_glogNormalization(data)
            # record data
            for i,d in enumerate(data_glog):
                data_glog[i]['calculated_concentration_units']=cu+'_glog_normalized'
            # plot original values:
            if plot_values_I:
                mplot.densityPlot(concentrations);
                mplot.densityPlot(concentrations_glog);
            # upload data
            for d in data:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units'] = d['calculated_concentration_units'] + '_glog_normalized';
                d['used_'] = True;
                d['comment_'] = None;
                data_O.append(d);
                #row = None;
                #row = data_stage02_quantification_glogNormalized(d);
                #row = data_stage02_quantification_glogNormalized(analysis_id_I,d['experiment_id'], d['sample_name_short'],
                #                                            d['time_point'],d['component_group_name'],
                #                                            d['component_name'],d['calculated_concentration'],
                #                                            d['calculated_concentration_units'] + '_glog_normalized',
                #                                            True,None);
                #self.session.add(row);
            data_transformed.extend(data_glog);
        # commit data to the session every timepoint
        self.add_dataStage02QuantificationGlogNormalized(data_O);
        self.update_concentrations_dataStage02GlogNormalized(analysis_id_I, data_transformed);

