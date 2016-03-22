# system
import copy
# SBaaS
from .stage02_quantification_outliers_io import stage02_quantification_outliers_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_outliers import calculate_outliers
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict

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
                            outliers = calculateoutliers.calculate_outliers_deviation(all_1,"calculated_concentration",deviation_I,method_I,data_labels_I = 'sample_name_short');
                            # record data
                            if outliers:
                                data_O.extend(outliers);   
             # add to the database
            self.add_dataStage02QuantificationOutliersDeviation(data_O); 

    def execute_calculateOutliersOneClassSVM(self,analysis_id_I,
            calculated_concentration_units_I=[],
            experiment_ids_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            ):
        '''
        Check for outliers using a oneClassSVM
        INPUT:
        OUTPUT:
        '''
        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        calculateoutliers = calculate_interface();
        data_O = [];
        # get the calculated_concentration_units/experiment_ids/sample_name_abbreviations/time_points that are unique
        unique_groups = [];
        unique_groups = dataPreProcessing_replicates_query.get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndSampleNameShortsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
            analysis_id_I,
            calculated_concentration_units_I=calculated_concentration_units_I,
            experiment_ids_I=experiment_ids_I,
            sample_name_abbreviations_I=sample_name_abbreviations_I,
            time_points_I=time_points_I,
            );
        for row in unique_groups:
            data_outliers = [];
            data_outliers = dataPreProcessing_replicates_query.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                row['calculated_concentration_units'],
                row['experiment_id'],
                row['sample_name_abbreviation'],
                row['time_point'],
                );
            #dim: [nfeatures,nsamples]
            data_listDict = listDict(data_outliers);
            data_listDict.set_listDict_dataFrame();
            data_listDict.set_listDict_pivotTable(
                value_label_I='calculated_concentration',
                row_labels_I=['component_name','component_group_name'],
                column_labels_I=['experiment_id','sample_name_short','time_point']
                );
            calculateoutliers.set_listDict(data_listDict);
            calculateoutliers.make_dataAndLabels(
                row_labels_I=['component_name','component_group_name'],
                column_labels_I=['experiment_id','sample_name_short','time_point']
                );
            calculateoutliers.make_trainTestSplit(
                data_X_I=calculateoutliers.data['data'],
                data_y_I=calculateoutliers.data['row_labels']['component_name'].T,
                test_size_I=1,
                random_state_I=calculateoutliers.random_state
                );
            ##dim: [nsamples,nfeatures]
            #data_listDict = listDict(data_outliers);
            #data_listDict.set_listDict_dataFrame();
            #data_listDict.set_listDict_pivotTable(
            #    value_label_I='calculated_concentration',
            #    row_labels_I=['experiment_id','sample_name_short','time_point'],
            #    column_labels_I=['component_name','component_group_name']
            #    );
            #calculateoutliers.set_listDict(data_listDict);
            #calculateoutliers.make_dataAndLabels(
            #    row_labels_I=['experiment_id','sample_name_short','time_point'],
            #    column_labels_I=['component_name','component_group_name']
            #    );
            #calculateoutliers.make_trainTestSplit(
            #    data_X_I=calculateoutliers.data['data'],
            #    data_y_I=calculateoutliers.data['row_labels']['sample_name_short'].T,
            #    test_size_I=0,
            #    random_state_I=calculateoutliers.random_state
            #    );
            outliers_indexes = calculateoutliers.calculate_outliers_OneClassSVM(outlier_fraction_I=0.05);

            calculateoutliers.clear_data();

