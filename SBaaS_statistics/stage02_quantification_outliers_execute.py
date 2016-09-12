# system
import copy
# SBaaS
from .stage02_quantification_outliers_io import stage02_quantification_outliers_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_outliers import calculate_outliers
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict

class stage02_quantification_outliers_execute(stage02_quantification_outliers_io):
    def execute_calculateOutliersDeviation(
        self,analysis_id_I,
        calculated_concentration_units_I=[],
        component_names_I=[],
        component_group_names_I=[],
        experiment_ids_I = [],
        time_points_I = [],
        sample_name_abbreviations_I = [],
        sample_name_shorts_I = [],
        where_clause_I = None,
        deviation_I=0.2,
        method_I='cv',
        query_object_I = 'stage02_quantification_dataPreProcessing_replicates_query',
        query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates',):
        '''calculate outliers based on their deviation
        INPUT:
        OUTPUT:
        '''

        print('execute_calculateOutliersDeviation...')
        
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calc = calculate_interface();
        calculateoutliers = calculate_outliers();
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
            data_1 = [d['calculated_concentration'] for d in data]
            if len(data_1)<2: continue
            # calculate outliers
            outliers = [];
            outliers = calculateoutliers.calculate_outliers_deviation(data,"calculated_concentration",deviation_I,method_I,data_labels_I = 'sample_name_short');
            # record data
            if outliers:
                data_O.extend(outliers);   
             # add to the database
        self.add_dataStage02QuantificationOutliersDeviation(data_O); 

    def execute_calculateOutliersOneClassSVM(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            experiment_ids_I = [],
            time_points_I = [],
            sample_name_abbreviations_I = [],
            sample_name_shorts_I = [],
            where_clause_I = None,
            query_object_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates',
            ):
        '''
        Check for outliers using a oneClassSVM
        INPUT:
        OUTPUT:
        '''
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
            #dim: [nfeatures,nsamples]
            data_listDict = listDict(listDict_I=data_analysis[row]);
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

