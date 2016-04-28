#SBaaS
from .stage02_quantification_correlation_io import stage02_quantification_correlation_io
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
#Resources
from python_statistics.calculate_correlation import calculate_correlation

class stage02_quantification_correlation_execute(stage02_quantification_correlation_io,
                                                 stage02_quantification_descriptiveStats_query,
                                                 stage02_quantification_analysis_query):
    def execute_profileMatcher(self,analysis_id_I,
                        sample_name_abbreviations_I=[],
                        time_points_I=[],
                        profile_match_I=None,
                        profile_match_description_I=None,
                        component_match_I=None,
                        component_match_units_I=None,
                        distance_measure_I='pearson',
                        criteria_I='difference',
                        concentration_units_I=[]):
        '''Correlate a profile or component to other components
        INPUT:
        analysis_id = string
        sample_name_abbreviations_I = list of sample_name_abbreviations in order (default is ascending)
        time_points_I = list of time-points in order (default is ascending)
        Use case #1: single sample name abbreviation, multiple time-points (specify only the time_points_I)
                 #2: multiple sample name abbreviations, single time-point (specify only the sample_name_abbreviations_I)
                 #3: multiple sample name abbreviations, multiple time-points (specify both the sample_name_abbreviations_I and time_points_I)

        profile_match_I = string e.g. '0-4-3-2-1'
        profile_match_description_I = string e.g. "increase"
        or
        component_match_I = component_name
        component_match_units_I = calculated_concentration_units
        
        distance_measure_I = 'spearman' or 'pearson'
        criteria_I = "difference" use the mean difference to determine if two data points are different
                     "stdev" use the +/- stdev to determine if two data points are different
                     "lb/ub" use the lb/ub to determine if two data points are different
                     Default = difference
        concentration_units_I = [] of calculated_concentration_units
        '''
        data_O = [];
        calculatecorrelation = calculate_correlation();
        #get the sample_name_abbreviations in the analysis
        sample_name_abbreviations_tmp,time_points_tmp = [],[];
        sample_name_abbreviations_tmp,time_points_tmp = self.get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        if sample_name_abbreviations_I and time_points_I:
            sample_name_abbreviations,time_points = [],[];
            for sna_cnt,sna in enumerate(sample_name_abbreviations_I):
                if sna in sample_name_abbreviations_tmp:
                    sna_time_points = [x for i,x in time_points_tmp if sample_name_abbreviation_tmp[i]==sna];
                    if time_points_I[sna_cnt] in sna_time_points:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_I[sna_cnt]);
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif sample_name_abbreviations_I:
            sample_name_abbreviations,time_points = [],[];
            for i,sna in enumerate(sample_name_abbreviations_I):
                for j,sna_tmp in enumerate(sample_name_abbreviations_tmp):
                    if sna == sna_tmp:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_tmp[j]);
                        break;
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif time_points_I:
            sample_name_abbreviations,time_points= [],[];
            for i,tp in enumerate(time_points_I):
                for j,tp_tmp in enumerate(time_points_tmp):
                    if tp == tp_tmp:
                        sample_name_abbreviations.append(sample_name_abbreviations_tmp[j]);
                        time_points.append(tp);
                        break;
            if len(time_points)!=len(time_points_I):
                print('specified and queried time_points lengths do not match');
                return;
        else:
            sample_name_abbreviations=sample_name_abbreviations_tmp;
            time_points=time_points_tmp;
        #get the units in the analysis
        if concentration_units_I:
            calculated_concentration_units = concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        #parse the profile or get the component_match
        if profile_match_I:
            plist_compare = calculatecorrelation.convert_profileStr2List(profile_match_I)
        elif component_match_I:
            #get the component_match data
            data_means,data_stdevs,data_lbs,data_ubs,data_units = [],[],[],[],[];
            for sna in sample_name_abbreviations:
                # get each individual data point
                data_mean,data_stdev,data_lb,data_ub,data_unit = None,None,None,None,None;
                data_mean,data_stdev,data_lb,data_ub,data_unit = self.get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                    analysis_id_I,sna,component_match_I,component_match_units_I);
            #generate the profile
            plist_compare = calculatecorrelation.convert_data2profile(
                    data_I=data_means,
                    data_stdev_I=data_stdevs,
                    data_lb_I=data_lbs,
                    data_ub_I=data_ubs,
                    criteria_I=criteria_I);
        else:
            print('Need to specify either a profile or a component to match');
            return;
        for cu in calculated_concentration_units:
            #get the component_names in the analysis
            component_names,component_group_names = [],[];
            component_names,component_group_names = self.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
            for cn_cnt,cn in enumerate(component_names):
                #if cn=='phe-L.phe-L_1.Light':
                #    print("check");
                #get the component data
                data_means,data_stdevs,data_lbs,data_ubs,data_units = [],[],[],[],[];
                for sna_cnt,sna in enumerate(sample_name_abbreviations):
                    # get each individual data point
                    data_mean,data_stdev,data_lb,data_ub,data_unit = None,None,None,None,None;
                    data_mean,data_stdev,data_lb,data_ub,data_unit = self.get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                        analysis_id_I,sna,time_points[sna_cnt],cn,cu);
                    data_means.append(data_mean);
                    data_stdevs.append(data_stdev);
                    data_lbs.append(data_lb);
                    data_ubs.append(data_ub);
                    data_units.append(data_unit);
                #generate the profile
                plist = calculatecorrelation.convert_data2profile(
                    data_I=data_means,
                    data_stdev_I=data_stdevs,
                    data_lb_I=data_lbs,
                    data_ub_I=data_ubs,
                    criteria_I=criteria_I);
                pstr = calculatecorrelation.convert_profileList2Str(plist);
                #calculate the correlation coefficient
                if distance_measure_I=='pearson':
                    rho,pval = calculatecorrelation.calculate_correlation_pearsonr(plist_compare,plist);
                elif distance_measure_I=='spearman':
                    rho,pval = calculatecorrelation.calculate_correlation_spearmanr(plist_compare,plist);
                else:
                    print("distance measure not recognized");
                    return;
                #record the data
                data_tmp = {
                    'analysis_id':analysis_id_I,
                    'sample_name_abbreviations':sample_name_abbreviations,
                    'component_group_name':component_group_names[cn_cnt],
                    'component_name':cn,
                    'component_profile':pstr,
                    'profile_match':profile_match_I,
                    'profile_match_description':profile_match_description_I,
                    'component_match':component_match_I,
                    'component_match_units':component_match_units_I,
                    'distance_measure':distance_measure_I,
                    'correlation_coefficient':rho,
                    'pvalue':pval,
                    'pvalue_corrected':None,
                    'pvalue_corrected_description':None,
                    'calculated_concentration_units':cu,
                    'used_':True,
                    'comment_':None
                    };
                data_O.append(data_tmp);
        #add the data to the database
        self.add_dataStage02QuantificationCorrelationProfile(data_O);

    def execute_trendMatcher(self,analysis_id_I,
                        sample_name_abbreviations_I=[],
                        time_points_I=[],
                        trend_match_I=None,
                        trend_match_description_I=None,
                        component_match_I=None,
                        component_match_units_I=None,
                        distance_measure_I='pearson',
                        criteria_I='difference',
                        concentration_units_I=[]):
        '''Correlate a trend or component to other components
        INPUT:
        analysis_id = string
        sample_name_abbreviations_I = list of sample_name_abbreviations in order (default is ascending)
        time_points_I = list of time-points in order (default is ascending)
        Use case #1: single sample name abbreviation, multiple time-points (specify only the time_points_I)
                 #2: multiple sample name abbreviations, single time-point (specify only the sample_name_abbreviations_I)
                 #3: multiple sample name abbreviations, multiple time-points (specify both the sample_name_abbreviations_I and time_points_I)

        trend_match_I = string e.g. '0-1-2-3'
        trend_match_description_I = string e.g. "increase"
        or
        component_match_I = component_name
        component_match_units_I = calculated_concentration_units
        
        distance_measure_I = 'spearman' or 'pearson'
        criteria_I = "difference" use the mean difference to determine if two data points are different
                     "stdev" use the +/- stdev to determine if two data points are different
                     "lb/ub" use the lb/ub to determine if two data points are different
                     Default = difference
        '''
        data_O = [];
        calculatecorrelation = calculate_correlation();
        #get the sample_name_abbreviations in the analysis
        sample_name_abbreviations_tmp,time_points_tmp = [],[];
        sample_name_abbreviations_tmp,time_points_tmp = self.get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        if sample_name_abbreviations_I and time_points_I:
            sample_name_abbreviations,time_points = [],[];
            for sna_cnt,sna in enumerate(sample_name_abbreviations_I):
                if sna in sample_name_abbreviations_tmp:
                    sna_time_points = [x for i,x in time_points_tmp if sample_name_abbreviation_tmp[i]==sna];
                    if time_points_I[sna_cnt] in sna_time_points:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_I[sna_cnt]);
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif sample_name_abbreviations_I:
            sample_name_abbreviations,time_points = [],[];
            for i,sna in enumerate(sample_name_abbreviations_I):
                for j,sna_tmp in enumerate(sample_name_abbreviations_tmp):
                    if sna == sna_tmp:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_tmp[j]);
                        break;
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif time_points_I:
            sample_name_abbreviations,time_points= [],[];
            for i,tp in enumerate(time_points_I):
                for j,tp_tmp in enumerate(time_points_tmp):
                    if tp == tp_tmp:
                        sample_name_abbreviations.append(sample_name_abbreviations_tmp[j]);
                        time_points.append(tp);
                        break;
            if len(time_points)!=len(time_points_I):
                print('specified and queried time_points lengths do not match');
                return;
        else:
            sample_name_abbreviations=sample_name_abbreviations_tmp;
            time_points=time_points_tmp;
        #get the units in the analysis
        if concentration_units_I:
            calculated_concentration_units = concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        #parse the trend or get the component_match
        if trend_match_I:
            plist_compare = calculatecorrelation.convert_profileStr2List(trend_match_I)
        elif component_match_I:
            #get the component_match data
            data_means,data_stdevs,data_lbs,data_ubs,data_units = [],[],[],[],[];
            for sna in sample_name_abbreviations:
                # get each individual data point
                data_mean,data_stdev,data_lb,data_ub,data_unit = None,None,None,None,None;
                data_mean,data_stdev,data_lb,data_ub,data_unit = self.get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                    analysis_id_I,sna,component_match_I,component_match_units_I);
            #generate the trend
            plist_compare = calculatecorrelation.convert_data2trend(
                    data_I=data_means,
                    data_stdev_I=data_stdevs,
                    data_lb_I=data_lbs,
                    data_ub_I=data_ubs,
                    criteria_I=criteria_I);
        else:
            print('Need to specify either a trend or a component to match');
            return;
        for cu in calculated_concentration_units:
            #get the component_names in the analysis
            component_names,component_group_names = [],[];
            component_names,component_group_names = self.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
            for cn_cnt,cn in enumerate(component_names):
                #if cn=='g6p.g6p_1.Light':
                #    print("check");
                #get the component data
                data_means,data_stdevs,data_lbs,data_ubs,data_units = [],[],[],[],[];
                for sna_cnt,sna in enumerate(sample_name_abbreviations):
                    # get each individual data point
                    data_mean,data_stdev,data_lb,data_ub,data_unit = None,None,None,None,None;
                    data_mean,data_stdev,data_lb,data_ub,data_unit = self.get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                        analysis_id_I,sna,time_points[sna_cnt],cn,cu);
                    data_means.append(data_mean);
                    data_stdevs.append(data_stdev);
                    data_lbs.append(data_lb);
                    data_ubs.append(data_ub);
                    data_units.append(data_unit);
                #generate the trend
                plist = calculatecorrelation.convert_data2trend(
                    data_I=data_means,
                    data_stdev_I=data_stdevs,
                    data_lb_I=data_lbs,
                    data_ub_I=data_ubs,
                    criteria_I=criteria_I);
                pstr = calculatecorrelation.convert_profileList2Str(plist);
                #calculate the correlation coefficient
                if distance_measure_I=='pearson':
                    rho,pval = calculatecorrelation.calculate_correlation_pearsonr(plist_compare,plist);
                elif distance_measure_I=='spearman':
                    rho,pval = calculatecorrelation.calculate_correlation_spearmanr(plist_compare,plist);
                else:
                    print("distance measure not recognized");
                    return;
                #record the data
                data_tmp = {
                    'analysis_id':analysis_id_I,
                    'sample_name_abbreviations':sample_name_abbreviations,
                    'component_group_name':component_group_names[cn_cnt],
                    'component_name':cn,
                    'component_trend':pstr,
                    'trend_match':trend_match_I,
                    'trend_match_description':trend_match_description_I,
                    'component_match':component_match_I,
                    'component_match_units':component_match_units_I,
                    'distance_measure':distance_measure_I,
                    'correlation_coefficient':rho,
                    'pvalue':pval,
                    'pvalue_corrected':None,
                    'pvalue_corrected_description':None,
                    'calculated_concentration_units':cu,
                    'used_':True,
                    'comment_':None
                    };
                data_O.append(data_tmp);
        #add the data to the database
        self.add_dataStage02QuantificationCorrelationTrend(data_O);
    def execute_profileFinder(self,analysis_id_I,
                        sample_name_abbreviations_I=[],
                        time_points_I=[],
                        criteria_I='difference',
                        concentration_units_I=[]):
        '''Find profiles in the data
        INPUT:
        analysis_id = string
        sample_name_abbreviations_I = list of sample_name_abbreviations in order (default is ascending)
        time_points_I = list of time-points in order (default is ascending)
        Use case #1: single sample name abbreviation, multiple time-points (specify only the time_points_I)
                 #2: multiple sample name abbreviations, single time-point (specify only the sample_name_abbreviations_I)
                 #3: multiple sample name abbreviations, multiple time-points (specify both the sample_name_abbreviations_I and time_points_I)
        '''

        data_O = [];

        calculatecorrelation = calculate_correlation();
        #get the sample_name_abbreviations in the analysis
        sample_name_abbreviations_tmp,time_points_tmp = [],[];
        sample_name_abbreviations_tmp,time_points_tmp = self.get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        if sample_name_abbreviations_I and time_points_I:
            sample_name_abbreviations,time_points = [],[];
            for sna_cnt,sna in enumerate(sample_name_abbreviations_I):
                if sna in sample_name_abbreviations_tmp:
                    sna_time_points = [x for i,x in time_points_tmp if sample_name_abbreviation_tmp[i]==sna];
                    if time_points_I[sna_cnt] in sna_time_points:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_I[sna_cnt]);
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif sample_name_abbreviations_I:
            sample_name_abbreviations,time_points = [],[];
            for i,sna in enumerate(sample_name_abbreviations_I):
                for j,sna_tmp in enumerate(sample_name_abbreviations_tmp):
                    if sna == sna_tmp:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_tmp[j]);
                        break;
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif time_points_I:
            sample_name_abbreviations,time_points= [],[];
            for i,tp in enumerate(time_points_I):
                for j,tp_tmp in enumerate(time_points_tmp):
                    if tp == tp_tmp:
                        sample_name_abbreviations.append(sample_name_abbreviations_tmp[j]);
                        time_points.append(tp);
                        break;
            if len(time_points)!=len(time_points_I):
                print('specified and queried time_points lengths do not match');
                return;
        else:
            sample_name_abbreviations=sample_name_abbreviations_tmp;
            time_points=time_points_tmp;
        #get the units in the analysis
        if concentration_units_I:
            calculated_concentration_units = concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        for cu in calculated_concentration_units:
            #get the component_names in the analysis
            component_names,component_group_names = [],[];
            component_names,component_group_names = self.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
            for cn_cnt,cn in enumerate(component_names):
                if cn=='g6p.g6p_1.Light':
                    print("check");
                #get the component data
                data_means,data_stdevs,data_lbs,data_ubs,data_units = [],[],[],[],[];
                for sna_cnt,sna in enumerate(sample_name_abbreviations):
                    # get each individual data point
                    data_mean,data_stdev,data_lb,data_ub,data_unit = None,None,None,None,None;
                    data_mean,data_stdev,data_lb,data_ub,data_unit = self.get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                        analysis_id_I,sna,time_points[sna_cnt],cn,cu);
                    data_means.append(data_mean);
                    data_stdevs.append(data_stdev);
                    data_lbs.append(data_lb);
                    data_ubs.append(data_ub);
                    data_units.append(data_unit);
                #generate the profile
                plist = calculatecorrelation.convert_data2profile(
                    data_I=data_means,
                    data_stdev_I=data_stdevs,
                    data_lb_I=data_lbs,
                    data_ub_I=data_ubs,
                    criteria_I=criteria_I);
                #record the data
                pstr = calculatecorrelation.convert_profileList2Str(plist);
                data_O.append(pstr);
        #get the unique profiles
        profiles_unique_O = list(set(data_O));
        profiles_unique_O.sort();
        return profiles_unique_O;
    def execute_trendFinder(self,analysis_id_I,
                        sample_name_abbreviations_I=[],
                        time_points_I=[],
                        criteria_I='difference',
                        concentration_units_I=[]):
        '''Find trends in the data
        INPUT:
        analysis_id = string
        sample_name_abbreviations_I = list of sample_name_abbreviations in order (default is ascending)
        time_points_I = list of time-points in order (default is ascending)
        Use case #1: single sample name abbreviation, multiple time-points (specify only the time_points_I)
                 #2: multiple sample name abbreviations, single time-point (specify only the sample_name_abbreviations_I)
                 #3: multiple sample name abbreviations, multiple time-points (specify both the sample_name_abbreviations_I and time_points_I)
        '''

        data_O = [];

        calculatecorrelation = calculate_correlation();
        #get the sample_name_abbreviations in the analysis
        sample_name_abbreviations_tmp,time_points_tmp = [],[];
        sample_name_abbreviations_tmp,time_points_tmp = self.get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        if sample_name_abbreviations_I and time_points_I:
            sample_name_abbreviations,time_points = [],[];
            for sna_cnt,sna in enumerate(sample_name_abbreviations_I):
                if sna in sample_name_abbreviations_tmp:
                    sna_time_points = [x for i,x in time_points_tmp if sample_name_abbreviation_tmp[i]==sna];
                    if time_points_I[sna_cnt] in sna_time_points:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_I[sna_cnt]);
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif sample_name_abbreviations_I:
            sample_name_abbreviations,time_points = [],[];
            for i,sna in enumerate(sample_name_abbreviations_I):
                for j,sna_tmp in enumerate(sample_name_abbreviations_tmp):
                    if sna == sna_tmp:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_tmp[j]);
                        break;
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif time_points_I:
            sample_name_abbreviations,time_points= [],[];
            for i,tp in enumerate(time_points_I):
                for j,tp_tmp in enumerate(time_points_tmp):
                    if tp == tp_tmp:
                        sample_name_abbreviations.append(sample_name_abbreviations_tmp[j]);
                        time_points.append(tp);
                        break;
            if len(time_points)!=len(time_points_I):
                print('specified and queried time_points lengths do not match');
                return;
        else:
            sample_name_abbreviations=sample_name_abbreviations_tmp;
            time_points=time_points_tmp;
        #get the units in the analysis
        if concentration_units_I:
            calculated_concentration_units = concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        for cu in calculated_concentration_units:
            #get the component_names in the analysis
            component_names,component_group_names = [],[];
            component_names,component_group_names = self.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
            for cn_cnt,cn in enumerate(component_names):
                #if cn=='g6p.g6p_1.Light':
                #    print("check");
                #get the component data
                data_means,data_stdevs,data_lbs,data_ubs,data_units = [],[],[],[],[];
                for sna_cnt,sna in enumerate(sample_name_abbreviations):
                    # get each individual data point
                    data_mean,data_stdev,data_lb,data_ub,data_unit = None,None,None,None,None;
                    data_mean,data_stdev,data_lb,data_ub,data_unit = self.get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                        analysis_id_I,sna,time_points[sna_cnt],cn,cu);
                    data_means.append(data_mean);
                    data_stdevs.append(data_stdev);
                    data_lbs.append(data_lb);
                    data_ubs.append(data_ub);
                    data_units.append(data_unit);
                #generate the trend
                plist = calculatecorrelation.convert_data2trend(
                    data_I=data_means,
                    data_stdev_I=data_stdevs,
                    data_lb_I=data_lbs,
                    data_ub_I=data_ubs,
                    criteria_I=criteria_I);
                #record the data
                pstr = calculatecorrelation.convert_profileList2Str(plist);
                data_O.append(pstr);
        #get the unique trends
        trends_unique_O = list(set(data_O));
        trends_unique_O.sort();
        return trends_unique_O;
    

    def execute_patternMatcher(self,analysis_id_I,
                        sample_name_abbreviations_I=[],
                        time_points_I=[],
                        pattern_match_I=None,
                        pattern_match_description_I=None,
                        component_match_I=None,
                        component_match_units_I=None,
                        distance_measure_I='pearson',
                        concentration_units_I=[],
                        query_object_I = 'stage02_quantification_descriptiveStats_query'):
        '''Correlate a pattern or component to other components
        INPUT:
        analysis_id = string
        sample_name_abbreviations_I = list of sample_name_abbreviations in order (default is ascending)
        time_points_I = list of time-points in order (default is ascending)
        Use case #1: single sample name abbreviation, multiple time-points (specify only the time_points_I)
                 #2: multiple sample name abbreviations, single time-point (specify only the sample_name_abbreviations_I)
                 #3: multiple sample name abbreviations, multiple time-points (specify both the sample_name_abbreviations_I and time_points_I)

        pattern_match_I = string e.g. '0-1-2-3'
        pattern_match_description_I = string e.g. "increase"
        or
        component_match_I = component_name
        component_match_units_I = calculated_concentration_units
        
        distance_measure_I = 'spearman' or 'pearson'
        query_object_I = query object to select the data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        '''
        data_O = [];
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance = query_object(self.session,self.engine,self.settings);
            query_instance.initialize_supportedTables();

        calculatecorrelation = calculate_correlation();
        #get the sample_name_abbreviations in the analysis
        sample_name_abbreviations_tmp,time_points_tmp = [],[];
        if hasattr(query_instance, 'get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDescriptiveStats'):
            sample_name_abbreviations_tmp,time_points_tmp = query_instance.get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        elif hasattr(query_instance, 'get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
            sample_name_abbreviations_tmp,time_points_tmp = query_instance.get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
        else:
            print('query instance does not have the required method.');
        if sample_name_abbreviations_I and time_points_I:
            sample_name_abbreviations,time_points = [],[];
            for sna_cnt,sna in enumerate(sample_name_abbreviations_I):
                if sna in sample_name_abbreviations_tmp:
                    sna_time_points = [x for i,x in time_points_tmp if sample_name_abbreviation_tmp[i]==sna];
                    if time_points_I[sna_cnt] in sna_time_points:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_I[sna_cnt]);
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif sample_name_abbreviations_I:
            sample_name_abbreviations,time_points = [],[];
            for i,sna in enumerate(sample_name_abbreviations_I):
                for j,sna_tmp in enumerate(sample_name_abbreviations_tmp):
                    if sna == sna_tmp:
                        sample_name_abbreviations.append(sna);
                        time_points.append(time_points_tmp[j]);
                        break;
            if len(sample_name_abbreviations)!=len(sample_name_abbreviations_I):
                print('specified and queried sample_name_abbreviation lengths do not match');
                return;
        elif time_points_I:
            sample_name_abbreviations,time_points= [],[];
            for i,tp in enumerate(time_points_I):
                for j,tp_tmp in enumerate(time_points_tmp):
                    if tp == tp_tmp:
                        sample_name_abbreviations.append(sample_name_abbreviations_tmp[j]);
                        time_points.append(tp);
                        break;
            if len(time_points)!=len(time_points_I):
                print('specified and queried time_points lengths do not match');
                return;
        else:
            sample_name_abbreviations=sample_name_abbreviations_tmp;
            time_points=time_points_tmp;
        #get the units in the analysis
        if concentration_units_I:
            calculated_concentration_units = concentration_units_I;
        else:
            calculated_concentration_units = [];
            if hasattr(query_instance, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        #parse the pattern or get the component_match
        if pattern_match_I:
            plist_compare = calculatecorrelation.convert_profileStr2List(pattern_match_I)
        elif component_match_I:
            #get the component_match data
            data_means,data_stdevs,data_lbs,data_ubs,data_units = [],[],[],[],[];
            for sna in sample_name_abbreviations:
                # get each individual data point
                data_mean,data_stdev,data_lb,data_ub,data_unit = None,None,None,None,None;
                if hasattr(query_instance, 'get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                    data_mean,data_stdev,data_lb,data_ub,data_unit = query_instance.get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                        analysis_id_I,sna,component_match_I,component_match_units_I);
                elif hasattr(query_instance, 'get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                    data_mean,data_stdev,data_lb,data_ub,data_unit = query_instance.get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                        analysis_id_I,sna,component_match_I,component_match_units_I);
                else:
                    print('query instance does not have the required method.');
            #generate the pattern
            plist_compare = data_means;
        else:
            print('Need to specify either a pattern or a component to match');
            return;
        for cu in calculated_concentration_units:
            #get the component_names in the analysis
            component_names,component_group_names = [],[];
            if hasattr(query_instance, 'get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                component_names,component_group_names = query_instance.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
            elif hasattr(query_instance, 'get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                component_names,component_group_names = query_instance.get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
            #TODO: update descriptiveStats to include this method?
            #elif hasattr(query_instance, 'getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
            #    component_names,component_group_names = query_instance.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
            else:
                print('query instance does not have the required method.');
            for cn_cnt,cn in enumerate(component_names):
                #if cn=='g6p.g6p_1.Light':
                #    print("check");
                #get the component data
                data_means,data_stdevs,data_lbs,data_ubs,data_units = [],[],[],[],[];
                for sna_cnt,sna in enumerate(sample_name_abbreviations):
                    # get each individual data point
                    data_mean,data_stdev,data_lb,data_ub,data_unit = None,None,None,None,None;
                    if hasattr(query_instance, 'get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                        data_mean,data_stdev,data_lb,data_ub,data_unit = query_instance.get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                            analysis_id_I,sna,time_points[sna_cnt],cn,cu);
                    elif hasattr(query_instance, 'get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                        data_mean,data_stdev,data_lb,data_ub,data_unit = query_instance.get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                            analysis_id_I,sna,time_points[sna_cnt],cn,cu);
                    else:
                        print('query instance does not have the required method.');
                    data_means.append(data_mean);
                    data_stdevs.append(data_stdev);
                    data_lbs.append(data_lb);
                    data_ubs.append(data_ub);
                    data_units.append(data_unit);
                #generate the pattern
                plist = data_means;
                pstr = calculatecorrelation.convert_profileList2Str(plist);
                #calculate the correlation coefficient
                if distance_measure_I=='pearson':
                    rho,pval = calculatecorrelation.calculate_correlation_pearsonr(plist_compare,plist);
                elif distance_measure_I=='spearman':
                    rho,pval = calculatecorrelation.calculate_correlation_spearmanr(plist_compare,plist);
                else:
                    print("distance measure not recognized");
                    return;
                #record the data
                data_tmp = {
                    'analysis_id':analysis_id_I,
                    'sample_name_abbreviations':sample_name_abbreviations,
                    'component_group_name':component_group_names[cn_cnt],
                    'component_name':cn,
                    'component_pattern':pstr,
                    'pattern_match':pattern_match_I,
                    'pattern_match_description':pattern_match_description_I,
                    'component_match':component_match_I,
                    'component_match_units':component_match_units_I,
                    'distance_measure':distance_measure_I,
                    'correlation_coefficient':rho,
                    'pvalue':pval,
                    'pvalue_corrected':None,
                    'pvalue_corrected_description':None,
                    'calculated_concentration_units':cu,
                    'used_':True,
                    'comment_':None
                    };
                data_O.append(data_tmp);
        #add the data to the database
        self.add_rows_table('data_stage02_quantification_correlationPattern',data_O);