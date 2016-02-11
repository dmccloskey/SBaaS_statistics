from .stage02_quantification_anova_io import stage02_quantification_anova_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_pairWiseTest_query import stage02_quantification_pairWiseTest_query
# resources
from r_statistics.r_interface import r_interface

class stage02_quantification_anova_execute(stage02_quantification_anova_io,
                                         stage02_quantification_normalization_query,
                                         stage02_quantification_pairWiseTest_query):
    def execute_anova(self,analysis_id_I,concentration_units_I=[],component_names_I=[],r_calc_I=None):
        '''execute anova using R'''

        print('execute_anova...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        data_anova_O = [];
        data_pairwise_O = [];
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            print('calculating anova for concentration_units ' + cu);
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
                print('calculating anova for component_names ' + cn);
                # get data:
                data = [];
                data = self.get_RDataFrame_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized(analysis_id_I,cu,cn);
                # call R
                data_anova,data_pairwise = [],[];
                data_anova,data_pairwise = r_calc.calculate_anova(data);
                # add data to database
                for d in data_anova:
                    tmp = {'analysis_id':analysis_id_I,
                        'sample_name_abbreviation':d['sample_name_abbreviation'],
                        'component_group_name':component_group_names[cnt_cn],
                        'component_name':d['component_name'],
                        'test_stat':d['test_stat'],
                        'test_description':d['test_description'],
                        'pvalue':d['pvalue'],
                        'pvalue_corrected':d['pvalue_corrected'],
                        'pvalue_corrected_description':d['pvalue_corrected_description'],
                        'calculated_concentration_units':cu,
                        'used_':True,
                        'comment_':None};
                    data_anova_O.append(tmp);
                    #row1 = data_stage02_quantification_anova(
                    #        analysis_id_I,
                    #        d['sample_name_abbreviation'],
                    #        component_group_names[cnt_cn],
                    #        d['component_name'],
                    #        d['test_stat'],
                    #        d['test_description'],
                    #        d['pvalue'],
                    #        d['pvalue_corrected'],
                    #        d['pvalue_corrected_description'],
                    #        cu,
                    #        True,
                    #        None
                    #        );
                    #self.session.add(row1);
                for d in data_pairwise:
                    tmp = {'analysis_id':analysis_id_I,
                        'sample_name_abbreviation_1':d['sample_name_abbreviation_1'],
                        'sample_name_abbreviation_2':d['sample_name_abbreviation_2'],
                        'component_group_name':component_group_names[cnt_cn],
                        'component_name':d['component_name'],
                        'mean':d['mean'],
                        'test_stat':d['test_stat'],
                        'test_description':d['test_description'],
                        'pvalue':d['pvalue'],
                        'pvalue_corrected':d['pvalue_corrected'],
                        'pvalue_corrected_description':d['pvalue_corrected_description'],
                        'ci_lb':d['ci_lb'],
                        'ci_ub':d['ci_ub'],
                        'ci_level':d['ci_level'],
                        'fold_change':d['fold_change'],
                        'calculated_concentration_units':cu,
                        'used_':True,
                        'comment_':None};
                    data_pairwise_O.append(tmp);
                    #row2 = data_stage02_quantification_pairWiseTest(
                    #        analysis_id_I,
                    #        d['sample_name_abbreviation_1'],
                    #        d['sample_name_abbreviation_2'],
                    #        component_group_names[cnt_cn],
                    #        d['component_name'],
                    #        d['mean'],
                    #        d['test_stat'],
                    #        d['test_description'],
                    #        d['pvalue'],
                    #        d['pvalue_corrected'],
                    #        d['pvalue_corrected_description'],
                    #        d['ci_lb'],
                    #        d['ci_ub'],
                    #        d['ci_level'],
                    #        d['fold_change'],
                    #        cu,
                    #        True,
                    #        None
                    #        );
                    #self.session.add(row2);
        #self.session.commit();
        self.add_dataStage02QuantificationAnova(data_anova_O);
        self.add_dataStage02QuantificationPairWiseTest(data_pairwise_O);

    def execute_anova_v1(self,experiment_id_I):
        '''execute anova using R'''

        print('execute_anova...')
        r_calc = r_interface();

        # query metabolomics data from glogNormalization
        # get time points
        time_points = [];
        time_points = self.get_timePoint_experimentID_dataStage02GlogNormalized(experiment_id_I);
        for tp in time_points:
            print('calculating anova for time_point ' + tp);
            data_transformed = [];
            # get concentration units...
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_experimentIDAndTimePoint_dataStage02GlogNormalized(experiment_id_I,tp);
            for cu in concentration_units:
                print('calculating anova for concentration_units ' + cu);
                # get component_names:
                component_names, component_group_names = [],[];
                component_names, component_group_names = self.get_componentNames_experimentIDAndTimePointAndUnits_dataStage02GlogNormalized(experiment_id_I, tp, cu);
                for cnt_cn,cn in enumerate(component_names):
                    print('calculating anova for component_names ' + cn);
                    # get data:
                    data = [];
                    data = self.get_RDataFrame_experimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(experiment_id_I,tp,cu,cn);
                    # call R
                    data_anova,data_pairwise = [],[];
                    data_anova,data_pairwise = r_calc.calculate_anova(data);
                    # add data to database
                    for d in data_anova:
                        row1 = data_stage02_quantification_anova(experiment_id_I,experiment_id_I,
                                d['sample_name_abbreviation'],
                                tp,
                                component_group_names[cnt_cn],
                                d['component_name'],
                                d['test_stat'],
                                d['test_description'],
                                d['pvalue'],
                                d['pvalue_corrected'],
                                d['pvalue_corrected_description'],
                                cu,
                                True,None);
                        self.session.add(row1);
                    for d in data_pairwise:
                        row2 = data_stage02_quantification_pairWiseTest(experiment_id_I,
                                d['sample_name_abbreviation_1'],
                                d['sample_name_abbreviation_2'],
                                tp,tp,
                                component_group_names[cnt_cn],
                                d['component_name'],
                                d['mean'],
                                d['test_stat'],
                                d['test_description'],
                                d['pvalue'],
                                d['pvalue_corrected'],
                                d['pvalue_corrected_description'],
                                d['ci_lb'],
                                d['ci_ub'],
                                d['ci_level'],
                                d['fold_change'],
                                cu,
                                True,None);
                        self.session.add(row2);
        self.session.commit();