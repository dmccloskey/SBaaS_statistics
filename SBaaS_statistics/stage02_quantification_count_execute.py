#sbaas
from .stage02_quantification_count_io import stage02_quantification_count_io
from .stage02_quantification_count_dependencies import stage02_quantification_count_dependencies
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_correlation_query import stage02_quantification_correlation_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
#sbaas models
from .stage02_quantification_count_postgresql_models import *
#resources
from python_statistics.calculate_count import calculate_count

class stage02_quantification_count_execute(
            stage02_quantification_count_io,
            stage02_quantification_normalization_query,
            stage02_quantification_descriptiveStats_query,
            stage02_quantification_analysis_query,
            stage02_quantification_correlation_query,
            stage02_quantification_count_dependencies
            ):

    def execute_countElementsInFeatures_correlationProfile(self,
            analysis_id_I,
            features_I=['profile_match', 'component_match', 'profile_match_description'],
            feature_units_I=['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized'],
            distance_measures_I=['spearman','pearson'],
            correlation_coefficient_thresholds_I={'>':0.8,'<':-0.8,}):
        '''count unique features of discrete or categorical data from data_stage02_correlation_profile
        INPUT:
        analysis_id_I = string,
        features_I = [] of string, e.g. ['profile_match', 'component_match', 'profile_match_description']
        feature_units_I = [] of string, e.g. ['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized']'
        distance_measures_I = [] of string, ['spearman','pearson']
        pvalue_threshold_I = {} of string:float, e.g., {'>':0.8,'<':-0.8,}

        OUTPUT:
        '''
        supported_comparators = ['>','<']
        data_O = [];
        calculatecount = calculate_count();
        #count each element of eachfeature
        for features_cnt,features in enumerate(features_I):
            if features == 'profile_match':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allProfileMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationProfile(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            elif features == 'profile_match_description':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allProfileMatchDescription_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationProfile(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            elif features == 'component_match':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allComponentMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationProfile(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            else:
                print("feature not yet supported");
        #add the data to the database
        self.add_dataStage02QuantificationCountCorrelationProfile(data_O);

    def execute_countElementsInFeatures_correlationTrend(self,
            analysis_id_I,
            features_I=['trend_match', 'component_match', 'trend_match_description'],
            feature_units_I=['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized'],
            distance_measures_I=['spearman','pearson'],
            correlation_coefficient_thresholds_I={'>':0.8,'<':-0.8,}):
        '''count unique features of discrete or categorical data from data_stage02_correlation_trend
        INPUT:
        analysis_id_I = string,
        features_I = [] of string, e.g. ['trend_match', 'component_match', 'trend_match_description']
        feature_units_I = [] of string, e.g. ['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized']'
        distance_measures_I = [] of string, ['spearman','pearson']
        pvalue_threshold_I = {} of string:float, e.g., {'>':0.8,'<':-0.8,}

        OUTPUT:
        '''
        supported_comparators = ['>','<']
        data_O = [];
        calculatecount = calculate_count();
        #count each element of eachfeature
        for features_cnt,features in enumerate(features_I):
            if features == 'trend_match':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allTrendMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationTrend(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            elif features == 'trend_match_description':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allTrendMatchDescription_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationTrend(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            elif features == 'component_match':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allComponentMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationTrend(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            else:
                print("feature not yet supported");
        #add the data to the database
        self.add_dataStage02QuantificationCountCorrelationTrend(data_O);

    def execute_countElementsInFeatures_correlationPattern(self,
            analysis_id_I,
            features_I=['pattern_match', 'component_match', 'pattern_match_description'],
            feature_units_I=['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized'],
            distance_measures_I=['spearman','pearson'],
            correlation_coefficient_thresholds_I={'>':0.8,'<':-0.8,}):
        '''count unique features of discrete or categorical data from data_stage02_correlation_pattern
        INPUT:
        analysis_id_I = string,
        features_I = [] of string, e.g. ['pattern_match', 'component_match', 'pattern_match_description']
        feature_units_I = [] of string, e.g. ['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized']'
        distance_measures_I = [] of string, ['spearman','pearson']
        pvalue_threshold_I = {} of string:float, e.g., {'>':0.8,'<':-0.8,}

        OUTPUT:
        '''
        supported_comparators = ['>','<']
        data_O = [];
        calculatecount = calculate_count();
        #count each element of eachfeature
        for features_cnt,features in enumerate(features_I):
            if features == 'pattern_match':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allPatternMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            elif features == 'pattern_match_description':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allPatternMatchDescription_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            elif features == 'component_match':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allComponentMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            else:
                print("feature not yet supported");
        #add the data to the database
        self.add_dataStage02QuantificationCountCorrelationPattern(data_O);

    def execute_countElementsInFeatures_replicates(self,
            analysis_id_I,
            features_I=['calculated_concentrations','experiment_id','time_point','sample_name_short'],
            feature_units_I=['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized'],
            value_I=0.0,
            operator_I = '<'):
        '''count unique features of discrete or categorical data from data_stage02_correlation_pattern
        INPUT:
        analysis_id_I = string,
        features_I = [] of string, e.g. ['pattern_match', 'component_match', 'pattern_match_description']

        feature_units_I = [] of string, e.g. ['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized']'

        OUTPUT:

        TODO:...
        '''
        supported_comparators = ['>','<']
        data_O = [];
        calculatecount = calculate_count();
        #count each element of eachfeature
        for features_cnt,features in enumerate(features_I):
            if features == 'pattern_match':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allPatternMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            elif features == 'pattern_match_description':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allPatternMatchDescription_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            elif features == 'component_match':
                for feature_units in feature_units_I:
                    for distance in distance_measures_I:
                        for k,v in correlation_coefficient_thresholds_I.items():
                            if not k in supported_comparators:
                                print(k + " not yet supported");
                                continue;
                            #get all the data for the analysis
                            data_count = [];
                            data_count= self.get_allComponentMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(analysis_id_I,feature_units,distance,k,v);
                            #count the elements of each feature
                            if data_count:
                                elements_unqiue,elements_count ,elements_count_fraction = calculatecount.count_elements(data_count);
                                correlationCoefficient_threshold_string = self.make_correlationCoefficientThresholdStr(k,v);
                                data_O.extend(
                                    self.record_count_correlation(analysis_id_I,
                                        features,feature_units,
                                        distance,correlationCoefficient_threshold_string,
                                        elements_unqiue,elements_count,elements_count_fraction)) ;
            else:
                print("feature not yet supported");
        #add the data to the database
        self.add_dataStage02QuantificationCountCorrelationPattern(data_O);

    def execute_countElementsInFeatures_descriptiveStats(self,):
        ''' '''