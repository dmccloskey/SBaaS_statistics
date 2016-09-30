
from .stage02_quantification_covariance_io import stage02_quantification_covariance_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict

class stage02_quantification_covariance_execute(stage02_quantification_covariance_io,
                                         ):
    def execute_covariance(self,analysis_id_I,
                data_matrix_shape_I='featuresBySamples',
                covariance_model_I="MinCovDet",
                covariance_method_I="scikit-learn_MinCovDet",
                covariance_options_I=None,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],
            where_clause_I = None,
            query_object_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates',
            includeAll_calculatedConcentrationUnits_I=False,
                ):
        '''execute covariance using sciKit-learn
        INPUT:
        analysis_id
        data_matrix_shape_I = string, "featuresBySamples" or "samplesByFeatures"
        covariance_model_I = string, 'EmpiricalCovariance' or 'MinCovDet'
        covariance_method_I = string, 'scikit-learn_EmpiricalCovariance' or 'scikit-learn_MinCovDet'
        covariance_options_I = {}, default=None, which will use recommended settings

        OPTIONAL INPUT:
        ...

        BEHAVIOR:
        the covariance is calculated on the axis 1 and the mahalanobis distance is calulated on axis 0
        data_matrix_shape_I == "featuresBySamples"
            covariance matrix = dim[nsamples,nsamples]
            precision matrix = dim[nsamples,nsamples]
            precision matrix = dim[nsamples,nsamples]
            mahalanobis distance matrix = dim[nfeatures,]
            
        '''

        print('execute_covariance...')

        # instanciate helper classes
        calculateinterface = calculate_interface()

        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance = query_object(self.session,self.engine,self.settings);
            query_instance.initialize_supportedTables();

        # instanciate data lists
        data_O=[]; #samples/features cov_matrix and precision_matrix
        data_mahalanobis_O=[]; #samples/features mahal_dist
        data_score_O=[]; #samples/features score
        
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
        calculated_concentration_units = list(set([c['calculated_concentration_units'] for c in data_listDict]));
        calculated_concentration_units.sort();
        data_analysis = {'_del_':[]};
        for row in data_listDict:
            if includeAll_calculatedConcentrationUnits_I:
                cu = ','.join(calculated_concentration_units);
            else:
                cu = row['calculated_concentration_units']
            if not cu in data_analysis.keys(): data_analysis[cu]=[];
            data_analysis[cu].append(row);
        del data_analysis['_del_'];
        for cu in calculated_concentration_units:
            print('calculating covariance for calculated_concentration_units ' + cu);

            data_listDict = listDict(listDict_I=data_analysis[cu])
            data_listDict.convert_listDict2DataFrame();
            # make the data matrix
            if data_matrix_shape_I == 'featuresBySamples':
                #dim: [nfeatures,nsamples]
                value_label = 'calculated_concentration';
                row_labels = ['component_name','component_group_name'];
                column_labels = ['experiment_id','sample_name_abbreviation','sample_name_short','time_point'];
                factor_label = 'component_name'
            elif data_matrix_shape_I == 'samplesByFeatures':
                #dim: [nsamples,nfeatures]
                value_label = 'calculated_concentration';
                row_labels = ['experiment_id','sample_name_abbreviation','sample_name_short','time_point'];
                column_labels = ['component_name','component_group_name'];
                factor_label = 'sample_name_short'
            else:
                print('data_matrix_shape_I not recongnized.');
            data_listDict.set_pivotTable(
                value_label_I=value_label,
                row_labels_I=row_labels,
                column_labels_I=column_labels
                );
            calculateinterface.set_listDict(data_listDict);
            calculateinterface.make_dataAndLabels(
                row_labels_I=row_labels,
                column_labels_I=column_labels
                );
            # make the train/test split
            calculateinterface.make_trainTestSplit(
                data_X_I=calculateinterface.data['data'],
                data_y_I=calculateinterface.data['row_labels'],
                test_size_I=0,
                random_state_I=calculateinterface.random_state
                );
            # call the covariance method
            if covariance_model_I == 'MinCovDet':
                calculateinterface.make_dataModel_MinCovDet();
            elif covariance_model_I == 'EmpiricalCovariance':
                calculateinterface.make_dataModel_EmpiricalCovariance();
            else:
                print('covariance_model_I not recognized.');
            cov_matrix, precision_matrix, mahal_dist, loglik, pval = calculateinterface.extract_covarianceInformation();
            # add data to the database
            if data_matrix_shape_I == 'featuresBySamples':
                for i in range(cov_matrix.shape[0]):
                    for j in range(cov_matrix.shape[1]):
                        tmp = {};
                        tmp['analysis_id']=analysis_id_I;
                        tmp['calculated_concentration_units']=cu;
                        tmp['used_']=True;
                        tmp['comment_']=None;
                        tmp['covariance_model'] = covariance_model_I;
                        tmp['covariance_method'] = covariance_method_I;
                        tmp['covariance_options'] = covariance_options_I;
                        tmp['sample_name_abbreviation_1']=calculateinterface.data['column_labels']['sample_name_abbreviation'][i]
                        tmp['sample_name_abbreviation_2']=calculateinterface.data['column_labels']['sample_name_abbreviation'][j]
                        tmp['sample_name_short_1']= calculateinterface.data['column_labels']['sample_name_short'][i]
                        tmp['sample_name_short_2']= calculateinterface.data['column_labels']['sample_name_short'][j]
                        tmp['covariance']=cov_matrix[i,j]
                        tmp['precision']=precision_matrix[i,j]
                        data_O.append(tmp);
                for i in range(mahal_dist.shape[0]):
                    tmp = {};
                    tmp['analysis_id']=analysis_id_I;
                    tmp['calculated_concentration_units']=cu;
                    tmp['used_']=True;
                    tmp['comment_']=None;
                    tmp['covariance_model'] = covariance_model_I;
                    tmp['covariance_method'] = covariance_method_I;
                    tmp['covariance_options'] = covariance_options_I;
                    tmp['component_name']=calculateinterface.data_train['response']['component_name'][i]
                    tmp['component_group_name']= calculateinterface.data_train['response']['component_group_name'][i]
                    tmp['mahalanobis']=mahal_dist[i] #check the correct dimension
                    data_mahalanobis_O.append(tmp);
                tmp = {};
                tmp['analysis_id']=analysis_id_I;
                tmp['calculated_concentration_units']=cu;
                tmp['used_']=True;
                tmp['comment_']=None;
                tmp['covariance_model'] = covariance_model_I;
                tmp['covariance_method'] = covariance_method_I;
                tmp['covariance_options'] = covariance_options_I;
                tmp['log_likelihood']= loglik
                tmp['pvalue']=pval
                data_score_O.append(tmp);
            elif data_matrix_shape_I == 'samplesByFeatures':
                for i in range(cov_matrix.shape[0]):
                    for j in range(cov_matrix.shape[1]):
                        tmp = {};
                        tmp['analysis_id']=analysis_id_I;
                        tmp['calculated_concentration_units']=cu;
                        tmp['used_']=True;
                        tmp['comment_']=None;
                        tmp['covariance_model'] = covariance_model_I;
                        tmp['covariance_method'] = covariance_method_I;
                        tmp['covariance_options'] = covariance_options_I;
                        tmp['component_name_1']=calculateinterface.data['column_labels']['component_name'][i]
                        tmp['component_name_2']=calculateinterface.data['column_labels']['component_name'][j]
                        tmp['component_group_name_1']= calculateinterface.data['column_labels']['component_group_name'][i]
                        tmp['component_group_name_2']= calculateinterface.data['column_labels']['component_group_name'][j]
                        tmp['covariance']=cov_matrix[i,j]
                        tmp['precision']=precision_matrix[i,j]
                        data_O.append(tmp);
                for i in range(mahal_dist.shape[0]):
                    tmp = {};
                    tmp['analysis_id']=analysis_id_I;
                    tmp['calculated_concentration_units']=cu;
                    tmp['used_']=True;
                    tmp['comment_']=None;
                    tmp['covariance_model'] = covariance_model_I;
                    tmp['covariance_method'] = covariance_method_I;
                    tmp['covariance_options'] = covariance_options_I;
                    tmp['sample_name_abbreviation']=calculateinterface.data_train['response']['sample_name_abbreviation'][i]
                    tmp['sample_name_short']= calculateinterface.data_train['response']['sample_name_short'][i]
                    tmp['mahalanobis']=mahal_dist[i] #check the correct dimension
                    data_mahalanobis_O.append(tmp);
                tmp = {};
                tmp['analysis_id']=analysis_id_I;
                tmp['calculated_concentration_units']=cu;
                tmp['used_']=True;
                tmp['comment_']=None;
                tmp['covariance_model'] = covariance_model_I;
                tmp['covariance_method'] = covariance_method_I;
                tmp['covariance_options'] = covariance_options_I;
                tmp['log_likelihood']= loglik
                tmp['pvalue']=pval
                data_score_O.append(tmp);
            # reset calculate_interface
            calculateinterface.clear_data();
        # add data to the database
        if data_matrix_shape_I == 'featuresBySamples':
            self.add_rows_table('data_stage02_quantification_covariance_samples',data_O);
            self.add_rows_table('data_stage02_quantification_covariance_features_mahalanobis',data_mahalanobis_O);
            self.add_rows_table('data_stage02_quantification_covariance_features_score',data_score_O);
        elif data_matrix_shape_I == 'samplesByFeatures':
            self.add_rows_table('data_stage02_quantification_covariance_features',data_O);
            self.add_rows_table('data_stage02_quantification_covariance_samples_mahalanobis',data_mahalanobis_O);
            self.add_rows_table('data_stage02_quantification_covariance_samples_score',data_score_O);