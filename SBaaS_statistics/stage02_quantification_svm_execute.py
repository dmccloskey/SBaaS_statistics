
from .stage02_quantification_svm_io import stage02_quantification_svm_io

class stage02_quantification_svm_execute(stage02_quantification_svm_io):
    def execute_svm(self,analysis_id_I,
                model_I='SVC',
                method_I="scikit-learn",
                parameters_I=None,
                impfeat_method_I='feature_importance',
                impfeat_options_I=None,
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],
                ):
        '''execute svm
        INPUT:
        analysis_id
        model_I = string, 'SVC', 'LinearSVC', 'NuSVC', or 'AdaBoostClassifier'
        method_I = string, 'scikit-learn'
        parameters_I = {}, default=None, which will use recommended settings
        impfeat_method_I = 'RFE','RFECV'
        impfeat_options_I = {}, default=None,
        OPTIONAL INPUT:
        ...
            
        '''

        # instanciate helper classes
        calculateinterface = calculate_interface()
        #stage02quantificationnormalizationquery = stage02_quantification_normalization_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        #stage02quantificationnormalizationquery.initialize_supportedTables();
        #stage02quantificationanalysisquery = stage02_quantification_analysis_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        #stage02quantificationanalysisquery.initialize_supportedTables();
        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        
        # instanciate data lists
        data_O=[]; #samples/features cov_matrix and precision_matrix
        data_features_O=[]; #samples/features mahal_dist
        data_scores_O=[]; #samples/features score
        
        # instantiate constants
        test_size = 0;

        ## get the analysis information
        #analysis_info = [];
        #analysis_info = stage02quantificationanalysisquery.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        #analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from glogNormalization
        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            #calculated_concentration_units = stage02quantificationnormalizationquery.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
            #calculated_concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
            calculated_concentration_units = dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu in calculated_concentration_units:
            #print('calculating tree for calculated_concentration_units ' + cu);
            data = [];
            # get data:
            #data = stage02quantificationnormalizationquery.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            #data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            data_listDict = dataPreProcessing_replicates_query.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                cu,
                experiment_ids_I=experiment_ids_I,
                sample_name_abbreviations_I=sample_name_abbreviations_I,
                sample_name_shorts_I=sample_name_shorts_I,
                component_names_I=component_names_I,
                component_group_names_I=component_group_names_I,
                time_points_I=time_points_I,);
            # make the data matrix
            #dim: [nsamples,nfeatures]
            value_label = 'calculated_concentration';
            row_labels = ['experiment_id','sample_name_abbreviation','sample_name_short','time_point'];
            column_labels = ['component_name','component_group_name'];
            factor_label = 'sample_name_abbreviation'
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
                data_y_I=calculateinterface.make_dataFactorFromRowLabels(factor_label), #sample_name_abbreviation
                data_z_I=calculateinterface.data['row_indexes'],
                test_size_I=test_size,
                random_state_I=calculateinterface.random_state
                );
            # instantiate the output dict
            data_O_listDict = listDict();
            # call the tree method
            calculateinterface.make_dataModel(model_I,parameters_I);
            parameters_I = calculateinterface.data_model.get_params(); #update the parameters
            # score the model on the test data

            # extract out feature information
            if impfeat_method_I == 'coefficients':
                impfeat_value = calculateinterface.extract_coefficients();
                impfeat_n,impfeat_std = calculateinterface.calculate_importantFeatures_std(impfeat_value);
                impfeat_zscore,impfeat_pvalue = calculateinterface.calculate_ZScoreAndPValue(
                    impfeat_value,impfeat_n,impfeat_std);
                response_name='all';
                #convert impfeat_statistics to the proper data structure
                data_O_listDict.set_dictList({'n':impfeat_n,'std':impfeat_std,'zscore':impfeat_zscore,'pvalue':impfeat_pvalue});
                data_O_listDict.convert_dictList2DataFrame();
                data_O_listDict.convert_dataFrame2ListDict();
                impfeat_statistics = data_O_listDict.get_listDict();
                data_O_listDict.clear_allData();
            elif impfeat_method_I in ['RFE','RFECV']:
                dataFeatureSelection = calculateinterface.make_dataFeatureSelection(
                        model_I,parameters_I,
                        impfeat_method_I,impfeat_options_I);
                impfeat_options_I = calculateinterface.data_model.get_params(); #update the parameters
                impfeat_value,impfeat_score = calculateinterface.extract_dataFeatureSelection_ranking();
                response_name='all';
                #convert impfeat_statistics to the proper data structure
                data_O_listDict.set_dictList({'score':impfeat_score});
                data_O_listDict.convert_dictList2DataFrame();
                data_O_listDict.convert_dataFrame2ListDict();
                impfeat_statistics = data_O_listDict.get_listDict();
                data_O_listDict.clear_allData();
            # add in additional rows to the output data object
            data_O_listDict.add_column2DataFrame('component_name',calculateinterface.data['column_labels']['component_name'].ravel());
            data_O_listDict.add_column2DataFrame('component_group_name',calculateinterface.data['column_labels']['component_group_name'].ravel());
            data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
            data_O_listDict.add_column2DataFrame('response_name',response_name);
            data_O_listDict.add_column2DataFrame('used_',True);
            data_O_listDict.add_column2DataFrame('comment_',None);
            data_O_listDict.add_column2DataFrame('model',model_I);
            data_O_listDict.add_column2DataFrame('method',method_I);
            data_O_listDict.add_column2DataFrame('parameters',parameters_I);
            data_O_listDict.add_column2DataFrame('impfeat_value',impfeat_value);
            data_O_listDict.add_column2DataFrame('impfeat_method',impfeat_method_I);
            data_O_listDict.add_column2DataFrame('impfeat_options',impfeat_options_I);
            data_O_listDict.add_column2DataFrame('impfeat_statistics',impfeat_statistics);
            # add data to the database
            data_O_listDict.convert_dataFrame2ListDict();
            self.add_rows_table('data_stage02_quantification_tree_impfeat',data_O_listDict.get_listDict());
            #data_features_O.append(impfeat_listDict.get_listDict());

            #extract out sample information

            # reset calculate_interface
            calculateinterface.clear_data();
        # add data to the database
        #self.add_rows_table('data_stage02_quantification_tree_samples',data_O);
        #self.add_rows_table('data_stage02_quantification_tree_features',data_features_O);
        #self.add_rows_table('data_stage02_quantification_tree_scores',data_scores_O);