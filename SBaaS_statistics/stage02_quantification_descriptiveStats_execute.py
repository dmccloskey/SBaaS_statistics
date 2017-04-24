
from .stage02_quantification_descriptiveStats_io import stage02_quantification_descriptiveStats_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from matplotlib_utilities.matplot import matplot
from math import sqrt
from listDict.listDict import listDict

class stage02_quantification_descriptiveStats_execute(stage02_quantification_descriptiveStats_io):
    def execute_descriptiveStats(self,analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            experiment_ids_I = [],
            time_points_I = [],
            sample_name_abbreviations_I = [],
            sample_name_shorts_I = [],
            where_clause_I = None,
            ci_level_I = 0.95,
            pvalue_corrected_description_I = "bonferroni",
            query_object_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates',
            r_calc_I=None):
        '''execute descriptiveStats using R'''

        #print 'execute_descriptiveStats...'
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calc = calculate_interface();
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance = query_object(self.session,self.engine,self.settings);
            query_instance.initialize_supportedTables();

        data_O = [];       
            
        #query the data:
        data_listDict = [];
        if hasattr(query_instance, query_func_I):
            query_func = getattr(query_instance, query_func_I);
            try:
                data_listDict = query_func(analysis_id_I,
                    calculated_concentration_units_I=calculated_concentration_units_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    sample_name_shorts_I=sample_name_shorts_I,
                    sample_name_abbreviations_I=sample_name_abbreviations_I,
                    time_points_I=time_points_I,
                    experiment_ids_I=experiment_ids_I,
                    where_clause_I=where_clause_I,
                    );
            except AssertionError as e:
                print(e);
        else:
            print('query instance does not have the required method.');
        
        #reorganize into analysis groups:
        unique_groups = list(set(
            [(c['analysis_id'],c['experiment_id'],
              c['time_point'],c['calculated_concentration_units'],
              c['component_name'],c['sample_name_abbreviation']) 
             for c in data_listDict]));
        unique_groups.sort();
        data_analysis = {'_del_':[]};
        for row in data_listDict:
            unique_group = (row['analysis_id'],row['experiment_id'],
              row['time_point'],row['calculated_concentration_units'],
              row['component_name'],row['sample_name_abbreviation'])
            if not unique_group in data_analysis.keys(): data_analysis[unique_group]=[];
            data_analysis[unique_group].append(row);
        del data_analysis['_del_'];

        #apply the anlaysis to each unique group
        for row in unique_groups:
            data = data_analysis[row];
            data_1 = [d['calculated_concentration'] for d in data if not d['calculated_concentration'] is None]
            if len(data_1)<2: continue
            # call R
            data_TTest = {};
            data_TTest = r_calc.calculate_oneSampleTTest(data_1, alternative_I = "two.sided", mu_I = 0,
                                                         paired_I="FALSE", var_equal_I = "TRUE",
                                                         ci_level_I = ci_level_I,
                                                         padjusted_method_I = pvalue_corrected_description_I);
            if not data_TTest:
                # calculate the mean, var, and confidence interval manually
                data_ave_O, data_var_O, data_lb_O, data_ub_O = None,None,None,None;
                data_ave_O, data_var_O, data_lb_O, data_ub_O = calc.calculate_ave_var(
                    data_1,
                    confidence_I = ci_level_I);
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
            # add data to database
            tmp = {'analysis_id':analysis_id_I,
                    'experiment_id':data_analysis[row][0]['experiment_id'],
                    'sample_name_abbreviation':data_analysis[row][0]['sample_name_abbreviation'],
                    'time_point':data_analysis[row][0]['time_point'],
                    'component_group_name':data_analysis[row][0]['component_group_name'],
                    'component_name':data_analysis[row][0]['component_name'],
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
                    'calculated_concentration_units':data_analysis[row][0]['calculated_concentration_units'],
                    'used_':True,
                    'comment_':None};
            data_O.append(tmp);
        self.add_rows_table('data_stage02_quantification_descriptiveStats',data_O);
    def execute_descriptiveStats_v1(self,analysis_id_I,experiment_ids_I=[],time_points_I=[],concentration_units_I=[],component_names_I=[],r_calc_I=None):
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
    def execute_descriptiveStats_v2(self,analysis_id_I,
            experiment_ids_I=[],
            time_points_I=[],
            calculated_concentration_units_I=[],
            sample_name_abbreviations_I=[],
            component_names_I=[],
            r_calc_I=None):
        '''execute descriptiveStats using R'''

        #print 'execute_descriptiveStats...'
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calc = calculate_interface();
        
        quantification_dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);

        data_O = [];
        # get the calculated_concentration_units/experiment_ids/sample_name_abbreviations/time_points/component_names that are unique
        unique_groups = [];
        unique_groups = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePointsAndComponentNames_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
            analysis_id_I,
            calculated_concentration_units_I=calculated_concentration_units_I,
            experiment_ids_I=experiment_ids_I,
            sample_name_abbreviations_I=sample_name_abbreviations_I,
            time_points_I=time_points_I,
            component_names_I=component_names_I,
            );
        # will need to refactor in the future...
        if type(unique_groups)==type(listDict()):
            unique_groups.convert_dataFrame2ListDict()
            unique_groups = unique_groups.get_listDict();
        for row in unique_groups:
            # get data:
            all_1,data_1 = [],[];
            all_1,data_1 = quantification_dataPreProcessing_replicates_query.get_RDataList_analysisIDAndExperimentIDAndTimePointAndCalculatedConcentrationUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02DataPreProcessingReplicates(
                analysis_id_I,
                row['experiment_id'],
                row['time_point'],
                row['calculated_concentration_units'],
                row['component_name'],
                row['sample_name_abbreviation'],
                );
            if len(data_1)<2: continue
            # will need to refactor in the future...
            if type(all_1)==type(listDict):
                all_1.convert_dataFrame2ListDict()
                all_1 = all_1.get_listDict();
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
            # add data to database
            tmp = {'analysis_id':analysis_id_I,
                    'experiment_id':row['experiment_id'],
                    'sample_name_abbreviation':row['sample_name_abbreviation'],
                    'time_point':row['time_point'],
                    'component_group_name':row['component_group_name'],
                    'component_name':row['component_name'],
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
                    'calculated_concentration_units':row['calculated_concentration_units'],
                    'used_':True,
                    'comment_':None};
            data_O.append(tmp);
        self.add_rows_table('data_stage02_quantification_descriptiveStats',data_O);
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