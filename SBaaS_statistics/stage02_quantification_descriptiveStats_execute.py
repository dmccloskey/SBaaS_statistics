
from .stage02_quantification_descriptiveStats_io import stage02_quantification_descriptiveStats_io
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from matplotlib_utilities.matplot import matplot
from math import sqrt

class stage02_quantification_descriptiveStats_execute(stage02_quantification_descriptiveStats_io):
    def execute_descriptiveStats(self,analysis_id_I,experiment_ids_I=[],time_points_I=[],concentration_units_I=[],component_names_I=[],r_calc_I=None):
        '''execute descriptiveStats using R'''

        #print 'execute_descriptiveStats...'
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calc = calculate_interface();
        
        data_O = [];
        # get the experiment ids
        if experiment_ids_I:
            experiment_ids = experiment_ids_I;
        else:
            experiment_ids = [];
            experiment_ids = self.get_experimentID_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for experiment_id in experiment_ids:
            # get time points
            if time_points_I:
                time_points=time_points_I;
            else:
                time_points = [];
                time_points = self.get_timePoint_analysisIDAndExperimentID_dataStage02GlogNormalized(analysis_id_I,experiment_id);
            for tp in time_points:
                print('calculating descriptiveStats for time_point ' + tp);
                data_transformed = [];
                # get concentration units...
                if concentration_units_I:
                    concentration_units = concentration_units_I;
                else:
                    concentration_units = [];
                    concentration_units = self.get_concentrationUnits_analysisIDAndExperimentIDAndTimePoint_dataStage02GlogNormalized(analysis_id_I,experiment_id,tp);
                for cu in concentration_units:
                    print('calculating descriptiveStats for concentration_units ' + cu);
                    # get component_names:
                    component_names, component_group_names = [],[];
                    component_names, component_group_names = self.get_componentNames_analysisIDAndExperimentIDAndTimePointAndUnits_dataStage02GlogNormalized(analysis_id_I,experiment_id, tp, cu);
                    if component_names_I:
                        component_names_ind = [i for i,x in enumerate(component_names) if x in component_names_I];
                        component_names_cpy = copy.copy(component_names);
                        component_group_names = copy.copy(component_group_names);
                        component_names = [x for i,x in enumerate(component_names) if i in component_names_ind]
                        component_group_names = [x for i,x in enumerate(component_group_names) if i in component_names_ind]
                    for cnt_cn,cn in enumerate(component_names):
                        print('calculating descriptiveStats for component_names ' + cn);
                        data_plot_mean = [];
                        data_plot_var = [];
                        data_plot_ci = [];
                        data_plot_sna = [];
                        data_plot_component_names = [];
                        data_plot_calculated_concentration_units = [];
                        data_plot_data = [];
                        # get sample_name_abbreviations:
                        sample_name_abbreviations = [];
                        sample_name_abbreviations = self.get_sampleNameAbbreviations_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(analysis_id_I,experiment_id, tp, cu, cn)
                        for sna in sample_name_abbreviations:
                            print('calculating descriptiveStats for sample_name_abbreviations ' + sna);
                            # get data:
                            all_1,data_1 = [],[];
                            all_1,data_1 = self.get_RDataList_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,experiment_id,tp,cu,cn,sna);
                            if len(data_1)<2: continue
                            # call R
                            data_TTest = {};
                            data_TTest = r_calc.calculate_oneSampleTTest(data_1, alternative_I = "two.sided", mu_I = 0, paired_I="FALSE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                            if not data_TTest:
                                # calculate the mean, var, and confidence interval manually
                                data_ave_O, data_var_O, data_lb_O, data_ub_O = None,None,None,None;
                                data_ave_O, data_var_O, data_lb_O, data_ub_O = calc.calculate_ave_var(data_1,confidence_I = 0.95);
                                if data_ave_O:
                                    data_cv = sqrt(data_var_O)/data_ave_O*100;
                                else:
                                    data_cv = None;
                                data_TTest = {};
                                data_TTest['mean']=data_ave_O;
                                data_TTest['var']=data_var_O;
                                data_TTest['ci_lb']=data_lb_O;
                                data_TTest['ci_ub']=data_ub_O;
                                data_TTest['cv']=data_cv;
                                data_TTest['n']=len(data_1);
                                data_TTest['test_stat']=None;
                                data_TTest['test_description']=None;
                                data_TTest['pvalue']=None;
                                data_TTest['pvalue_corrected']=None;
                                data_TTest['pvalue_corrected_description']=None;
                                data_TTest['ci_level']=0.95;
                            # calculate the interquartile range
                            min_O, max_O, median_O, iq_1_O, iq_3_O=calc.calculate_interquartiles(data_1);
                            # record data for plotting
                            data_plot_mean.append(data_TTest['mean']);
                            data_plot_var.append(data_TTest['var']);
                            data_plot_ci.append([data_TTest['ci_lb'],data_TTest['ci_ub']]);
                            data_plot_data.append(data_1);
                            data_plot_sna.append(sna);
                            data_plot_component_names.append(cn);
                            data_plot_calculated_concentration_units.append(cu);
                            # add data to database
                            tmp = {'analysis_id':analysis_id_I,
                                    'experiment_id':experiment_id,
                                    'sample_name_abbreviation':sna,
                                    'time_point':tp,
                                    'component_group_name':component_group_names[cnt_cn],
                                    'component_name':cn,
                                    'mean':data_TTest['mean'],
                                    'var':data_TTest['var'],
                                    'cv':data_TTest['cv'],
                                    'n':data_TTest['n'],
                                    'test_stat':data_TTest['test_stat'],
                                    'test_description':data_TTest['test_description'],
                                    'pvalue':data_TTest['pvalue'],
                                    'pvalue_corrected':data_TTest['pvalue_corrected'],
                                    'pvalue_corrected_description':data_TTest['pvalue_corrected_description'],
                                    'ci_lb':data_TTest['ci_lb'],
                                    'ci_ub':data_TTest['ci_ub'],
                                    'ci_level':data_TTest['ci_level'],
                                    'min':min_O,
                                    'max':max_O,
                                    'median':median_O,
                                    'iq_1':iq_1_O,
                                    'iq_3':iq_3_O,
                                    'calculated_concentration_units':cu,
                                    'used_':True,
                                    'comment_':None};
                            data_O.append(tmp);
        #                    row2 = data_stage02_quantification_descriptiveStats(
        #                            analysis_id_I,
        #                            experiment_id,
        #                            sna,
        #                            tp,
        #                            component_group_names[cnt_cn],
        #                            cn,
        #                            data_TTest['mean'],
        #                            data_TTest['var'],
        #                            data_TTest['cv'],
        #                            data_TTest['n'],
        #                            data_TTest['test_stat'],
        #                            data_TTest['test_description'],
        #                            data_TTest['pvalue'],
        #                            data_TTest['pvalue_corrected'],
        #                            data_TTest['pvalue_corrected_description'],
        #                            data_TTest['ci_lb'],
        #                            data_TTest['ci_ub'],
        #                            data_TTest['ci_level'],
        #                            min_O,
        #                            max_O,
        #                            median_O,
        #                            iq_1_O,
        #                            iq_3_O,
        #                            cu,
        #                            True,
        #                            None
        #                            );
        #                    self.session.add(row2);
        #self.session.commit();
        self.add_dataStage02QuantificationDescriptiveStats(data_O);
    def execute_boxAndWhiskersPlot(self,analysis_id_I,concentration_units_I=[],component_names_I=[]):
        '''generate a boxAndWhiskers plot from descriptiveStats table'''
        
        r_calc = r_interface();
        calc = calculate_interface();
        mplot = matplot();
        # get concentration units...
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            print('calculating descriptiveStats for concentration_units ' + cu);
            # get component_names:
            component_names, component_group_names = [],[];
            component_names, component_group_names = self.get_componentNames_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I, cu);
            if component_names_I:
                component_names_ind = [i for i,x in enumerate(component_names) if x in component_names_I];
                component_names_cpy = copy.copy(component_names);
                component_group_names = copy.copy(component_group_names);
                component_names = [x for i,x in enumerate(component_names) if i in component_names_ind]
                component_group_names = [x for i,x in enumerate(component_group_names) if i in component_names_ind]
            for cnt_cn,cn in enumerate(component_names):
                print('calculating descriptiveStats for component_names ' + cn);
                data_plot_mean = [];
                data_plot_var = [];
                data_plot_ci = [];
                data_plot_sna = [];
                data_plot_component_names = [];
                data_plot_calculated_concentration_units = [];
                data_plot_data = [];
                # get sample_name_abbreviations:
                sample_name_abbreviations = [];
                sample_name_abbreviations = self.get_sampleNameAbbreviations_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized(analysis_id_I, cu, cn)
                for sna in sample_name_abbreviations:
                    print('calculating descriptiveStats for sample_name_abbreviations ' + sna);
                    # get data:
                    all_1,data_1 = [],[];
                    all_1,data_1 = self.get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,cn,sna);
                    # call R
                    data_TTest = {};
                    data_TTest = r_calc.calculate_oneSampleTTest(data_1, alternative_I = "two.sided", mu_I = 0, paired_I="FALSE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                    # record data for plotting
                    data_plot_mean.append(data_TTest['mean']);
                    data_plot_var.append(data_TTest['var']);
                    data_plot_ci.append([data_TTest['ci_lb'],data_TTest['ci_lb']]);
                    data_plot_data.append(data_1);
                    data_plot_sna.append(sna);
                    data_plot_component_names.append(cn);
                    data_plot_calculated_concentration_units.append(cu);
                # visualize the stats:
                #mplot.barPlot(data_plot_component_names[0],data_plot_sna,data_plot_sna[0],'samples',data_plot_mean,data_plot_var);
                mplot.boxAndWhiskersPlot(data_plot_component_names[0],data_plot_sna,data_plot_sna[0],'samples',data_plot_data,data_plot_mean,data_plot_ci);
    def execute_boxAndWhiskersPlot_v1(self,experiment_id_I,component_names_I=[]):
        '''generate a boxAndWhiskers plot from descriptiveStats table'''
        
        r_calc = r_interface();
        calc = calculate_interface();
        mplot = matplot();
        print('execute_boxAndWhiskersPlot...')
        # query metabolomics data from glogNormalization
        # get time points
        time_points = [];
        time_points = self.get_timePoint_experimentID_dataStage02GlogNormalized(experiment_id_I);
        for tp in time_points:
            print('calculating descriptiveStats for time_point ' + tp);
            data_transformed = [];
            # get concentration units...
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_experimentIDAndTimePoint_dataStage02GlogNormalized(experiment_id_I,tp);
            for cu in concentration_units:
                print('calculating descriptiveStats for concentration_units ' + cu);
                # get component_names:
                component_names, component_group_names = [],[];
                component_names, component_group_names = self.get_componentNames_experimentIDAndTimePointAndUnits_dataStage02GlogNormalized(experiment_id_I, tp, cu);
                if component_names_I:
                    component_names_ind = [i for i,x in enumerate(component_names) if x in component_names_I];
                    component_names_cpy = copy.copy(component_names);
                    component_group_names = copy.copy(component_group_names);
                    component_names = [x for i,x in enumerate(component_names) if i in component_names_ind]
                    component_group_names = [x for i,x in enumerate(component_group_names) if i in component_names_ind]
                for cnt_cn,cn in enumerate(component_names):
                    print('calculating descriptiveStats for component_names ' + cn);
                    data_plot_mean = [];
                    data_plot_var = [];
                    data_plot_ci = [];
                    data_plot_sna = [];
                    data_plot_component_names = [];
                    data_plot_calculated_concentration_units = [];
                    data_plot_data = [];
                    # get sample_name_abbreviations:
                    sample_name_abbreviations = [];
                    sample_name_abbreviations = self.get_sampleNameAbbreviations_experimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(experiment_id_I, tp, cu, cn)
                    for sna in sample_name_abbreviations:
                        print('calculating descriptiveStats for sample_name_abbreviations ' + sna);
                        # get data:
                        all_1,data_1 = [],[];
                        all_1,data_1 = self.get_RDataList_experimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(experiment_id_I,tp,cu,cn,sna);
                        # call R
                        data_TTest = {};
                        data_TTest = r_calc.calculate_oneSampleTTest(data_1, alternative_I = "two.sided", mu_I = 0, paired_I="FALSE", var_equal_I = "TRUE", ci_level_I = 0.95, padjusted_method_I = "bonferroni");
                        # record data for plotting
                        data_plot_mean.append(data_TTest['mean']);
                        data_plot_var.append(data_TTest['var']);
                        data_plot_ci.append([data_TTest['ci_lb'],data_TTest['ci_lb']]);
                        data_plot_data.append(data_1);
                        data_plot_sna.append(sna);
                        data_plot_component_names.append(cn);
                        data_plot_calculated_concentration_units.append(cu);
                    # visualize the stats:
                    #mplot.barPlot(data_plot_component_names[0],data_plot_sna,data_plot_sna[0],'samples',data_plot_mean,data_plot_var);
                    mplot.boxAndWhiskersPlot(data_plot_component_names[0],data_plot_sna,data_plot_sna[0],'samples',data_plot_data,data_plot_mean,data_plot_ci);