from .stage02_quantification_anova_io import stage02_quantification_anova_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from listDict.listDict import listDict

class stage02_quantification_anova_execute(stage02_quantification_anova_io,):
    def execute_anova(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            experiment_ids_I = [],
            time_points_I = [],
            sample_name_abbreviations_I = [],
            sample_name_shorts_I = [],
            ci_level_I = 0.95,
            pvalue_corrected_description_I = "bonferroni",
            r_calc_I=None):
        '''execute anova using R'''

        print('execute_anova...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        dataPreProcessing_replicates_query.initialize_supportedTables();

        data_anova_O = [];
        data_pairwise_O = [];
        # query the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            # query the component_names/component_group_names:
            component_names = [];
            component_names = dataPreProcessing_replicates_query.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                cu,
                );
            if component_names_I:
                component_names = [cn for cn in component_names if cn['component_name'] in component_names_I];
            for cn in component_names:
                #print('calculating anova for component_names ' + cn);
                # get data:
                data = dataPreProcessing_replicates_query.get_RDataFrame_analysisIDAndCalculatedConcentrationUnitsAndComponentNames_dataStage02DataPreProcessingReplicates(
                    analysis_id_I,
                    cu,
                    cn['component_name'],
                    experiment_ids_I = experiment_ids_I,
                    time_points_I = time_points_I,
                    sample_name_abbreviations_I = sample_name_abbreviations_I,
                    sample_name_shorts_I = sample_name_shorts_I
                    );
                # call R
                r_calc.clear_workspace();
                calculated_concentrations = data.dataFrame['calculated_concentration'].get_values();
                sample_name_abbreviations = data.dataFrame['sample_name_abbreviation'].get_values();

                # calculate ANOVA
                r_calc.make_vectorFromList(calculated_concentrations,'concentrations');
                r_calc.make_vectorFromList(sample_name_abbreviations,'sna');
                r_calc.make_dataFrameFromLists(
                        labels_I=['concentrations','sna'],
                        dataFrame_O='dF');
                r_calc.calculate_aov(
                        function_I = 'concentrations ~ sna',
                        dataFrame_I = 'dF',
                        aov_O = 'aov.out');
                f_stat,pvalue = r_calc.extraction_aov(aov_I = 'aov.out');

                # add anova data to database
                data_anova = {};
                data_anova['sample_name_abbreviation'] = list(set(sample_name_abbreviations));
                data_anova['component_name'] = cn['component_name'];
                data_anova['test_stat'] = f_stat;
                data_anova['test_description'] = '1-way ANOVA; F value';
                data_anova['pvalue'] = pvalue;
                data_anova['pvalue_corrected'] = None;
                data_anova['pvalue_corrected_description'] = None;
                data_anova['analysis_id']=analysis_id_I;
                data_anova['component_group_name'] = cn['component_group_name'];
                data_anova['calculated_concentration_units'] = cu;
                data_anova['used_'] = True;
                data_anova['comment_'] = None;
                data_anova_O.append(data_anova);

                #PostHoc analysis
                r_calc.calculate_tukeyHSD(
                        aov_I='aov.out',
                        ci_level_I=ci_level_I,
                        tukeyhsd_O='tukeyhsd');
                diff,lb,ub,pvalue,labels=r_calc.extract_tukeyHSD(tukeyhsd_I='tukeyhsd');
                labels_1 = [x.split('-')[0] for x in labels];
                labels_2 = [x.split('-')[1] for x in labels];

                #Pvalue correction
                r_calc.make_vectorFromList(pvalue,'pvalues');
                pvalue_corrected = r_calc.calculate_pValueCorrected('pvalues','pvalues_O',method_I = pvalue_corrected_description_I);

                # add pairwise data to the database
                data_pairwise = {'mean':diff,'ci_lb':lb,'ci_ub':ub,'pvalue':pvalue,
                            'sample_name_abbreviation_1':labels_1,
                            'sample_name_abbreviation_2':labels_2,
                            };
                data_pairwise_listDict = listDict(dictList_I=data_pairwise);
                data_pairwise_listDict.convert_dictList2DataFrame();
                data_pairwise_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_pairwise_listDict.add_column2DataFrame('ci_level',ci_level_I);
                data_pairwise_listDict.add_column2DataFrame('test_description','TukeyHSD');
                data_pairwise_listDict.add_column2DataFrame('component_name',cn['component_name']);
                data_pairwise_listDict.add_column2DataFrame('component_group_name',cn['component_group_name']);
                data_pairwise_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_pairwise_listDict.add_column2DataFrame('used_',True);
                data_pairwise_listDict.add_column2DataFrame('comment_',None);
                # add in the corrected p-values
                data_pairwise_listDict.add_column2DataFrame('pvalue_corrected', pvalue_corrected);
                data_pairwise_listDict.add_column2DataFrame('pvalue_corrected_description', pvalue_corrected_description_I);
                data_pairwise_listDict.convert_dataFrame2ListDict();
                data_pairwise_O.extend(data_pairwise_listDict.get_listDict());

        #self.session.commit();
        self.add_rows_table('data_stage02_quantification_anova',data_anova_O);
        self.add_rows_table('data_stage02_quantification_anova_posthoc',data_pairwise_O);
    def execute_twoWayAnova(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            experiment_ids_I = [],
            time_points_I = [],
            sample_name_abbreviations_I = [],
            sample_name_shorts_I = [],
            ci_level_I = 0.95,
            pvalue_corrected_description_I = "bonferroni",
            r_calc_I=None):
        '''execute twoWayAnova using R'''

        print('execute_twoWayAnova...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        dataPreProcessing_replicates_query.initialize_supportedTables();

        data_anova_O = [];
        data_pairwise_O = [];
        # query the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            # query the component_names/component_group_names:
            component_names = [];
            component_names = dataPreProcessing_replicates_query.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                cu,
                );
            for cn in component_names:
                print('calculating twoWayAnova for component_names ' + cn);
                # get data:
                data = dataPreProcessing_replicates_query.get_RDataFrame_analysisIDAndCalculatedConcentrationUnitsAndComponentNames_dataStage02DataPreProcessingReplicates(
                    analysis_id_I,
                    cu,
                    cn['component_name'],
                    experiment_ids_I = experiment_ids_I,
                    time_points_I = time_points_I,
                    sample_name_abbreviations_I = sample_name_abbreviations_I,
                    sample_name_shorts_I = sample_name_shorts_I
                    );
                # call R
                r_calc.clear_workspace();
                calculated_concentrations = data.dataFrame['calculated_concentration'].get_values();
                sample_name_abbreviations = data.dataFrame['sample_name_abbreviation'].get_values();
                time_points = data.dataFrame['time_point'].get_values();

                # calculate ANOVA
                r_calc.make_vectorFromList(calculated_concentrations,'concentrations');
                r_calc.make_vectorFromList(sample_name_abbreviations,'sna');
                r_calc.make_vectorFromList(time_points,'tp');
                r_calc.make_dataFrameFromLists(
                        labels_I=['concentrations','sna','tp'],
                        dataFrame_O='dF');
                r_calc.calculate_aov(
                        function_I = 'concentrations ~ sna*tp',
                        dataFrame_I = 'dF',
                        aov_O = 'aov.out');
                f_stat,pvalue = r_calc.extraction_aov(aov_I = 'aov.out');

                # add anova data to database
                data_anova = {};
                data_anova['sample_name_abbreviation'] = list(set(sample_name_abbreviations));
                data_anova['time_point'] = list(set(time_points));
                data_anova['component_name'] = cn['component_name'];
                data_anova['test_stat'] = f_stat;
                data_anova['test_description'] = '1-way ANOVA; F value';
                data_anova['pvalue'] = pvalue;
                data_anova['pvalue_corrected'] = None;
                data_anova['pvalue_corrected_description'] = None;
                data_anova['analysis_id']=analysis_id_I;
                data_anova['component_group_name'] = cn['component_group_name'];
                data_anova['calculated_concentration_units'] = cu;
                data_anova['used_'] = True;
                data_anova['comment_'] = None;
                data_anova_O.append(data_anova);

                #PostHoc analysis
                r_calc.calculate_tukeyHSD(
                        aov_I='aov.out',
                        ci_level_I=ci_level_I,
                        tukeyhsd_O='tukeyhsd');
                diff,lb,ub,pvalue,labels=r_calc.extract_tukeyHSD(tukeyhsd_I='tukeyhsd');
                #TODO:
                #labels_1 = [x.split('-')[0] for x in labels];
                #labels_2 = [x.split('-')[1] for x in labels];

                #Pvalue correction
                r_calc.make_vectorFromList(pvalue,'pvalues');
                pvalue_corrected = r_calc.calculate_pValueCorrected('pvalues','pvalues_O',method_I = pvalue_corrected_description_I);

                # add pairwise data to the database
                data_pairwise = {'mean':diff,'ci_lb':lb,'ci_ub':ub,'pvalue':pvalue,
                            'sample_name_abbreviation_1':labels_1,
                            'sample_name_abbreviation_2':labels_2,
                            'time_point_1':labels_3,
                            'time_point_2':labels_4,
                            };
                data_pairwise_listDict = listDict(dictList_I=data_pairwise);
                data_pairwise_listDict.convert_dictList2DataFrame();
                data_pairwise_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_pairwise_listDict.add_column2DataFrame('ci_level',ci_level_I);
                data_pairwise_listDict.add_column2DataFrame('test_description','TukeyHSD');
                data_pairwise_listDict.add_column2DataFrame('component_name',cn['component_name']);
                data_pairwise_listDict.add_column2DataFrame('component_group_name',cn['component_group_name']);
                data_pairwise_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_pairwise_listDict.add_column2DataFrame('used_',True);
                data_pairwise_listDict.add_column2DataFrame('comment_',None);
                # add in the corrected p-values
                data_pairwise_listDict.add_column2DataFrame('pvalue_corrected', pvalue_corrected);
                data_pairwise_listDict.add_column2DataFrame('pvalue_corrected_description', pvalue_corrected_description_I);
                data_pairwise_listDict.convert_dataFrame2ListDict();
                data_pairwise_O.extend(data_pairwise_listDict.get_listDict());

        #self.session.commit();
        self.add_rows_table('data_stage02_quantification_anova',data_anova_O);
        self.add_rows_table('data_stage02_quantification_anova_posthoc',data_pairwise_O);

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
    def execute_anova_v2(self,analysis_id_I,concentration_units_I=[],component_names_I=[],r_calc_I=None):
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
                #print('calculating anova for component_names ' + cn);
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