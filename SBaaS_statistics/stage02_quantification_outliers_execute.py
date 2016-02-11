# system
import copy
# SBaaS
from .stage02_quantification_outliers_io import stage02_quantification_outliers_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_outliers import calculate_outliers
# remove after making add methods
from .stage02_quantification_outliers_postgresql_models import *

class stage02_quantification_outliers_execute(stage02_quantification_outliers_io,
                                              stage02_quantification_normalization_query):
    def execute_calculateOutliersDeviation(self,analysis_id_I,experiment_ids_I=[],time_points_I=[],concentration_units_I=[],component_names_I=[],
                                           deviation_I=0.2,method_I='cv'):
        '''calculate outliers based on their deviation
        INPUT:
        OUTPUT:
        '''

        print('execute_getDataStage01ReplicatesMI...')
        
        calculateoutliers = calculate_outliers();
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
                        # get sample_name_abbreviations:
                        sample_name_abbreviations = [];
                        sample_name_abbreviations = self.get_sampleNameAbbreviations_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(analysis_id_I,experiment_id, tp, cu, cn)
                        for sna in sample_name_abbreviations:
                            print('calculating descriptiveStats for sample_name_abbreviations ' + sna);
                            # get data:
                            all_1,data_1 = [],[];
                            all_1,data_1 = self.get_RDataList_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,experiment_id,tp,cu,cn,sna);
                            if len(data_1)<2: continue
                            # calculate outliers
                            outliers = [];
                            outliers = calculateoutliers.calculate_outliers(all_1,"calculated_concentration",deviation_I,method_I,data_labels_I = 'sample_name_short');
                            # record data
                            if outliers:
                                data_O.extend(outliers);   
             # add to the database
            self.add_dataStage02QuantificationOutliersDeviation(data_O); 
    def execute_calculateOutliersPCA(self,analysis_id_I,concentration_units_I=[],r_calc_I=None):
        '''calculate outliers based on a PCA analysis
        INPUT:
        OUTPUT:
        '''

        print('execute_calculateOutliersPCA...')

        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        
        data_scores_O = [];
        data_loadings_O = [];
        data_validation_O = [];
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            print('calculating pca for concentration_units ' + cu);
            data = [];
            # get data:
            data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            # call R
            data_scores,data_loadings,data_perf = [],[],[];
            data_scores,data_loadings,data_perf = r_calc.detect_outliers_svd(data);