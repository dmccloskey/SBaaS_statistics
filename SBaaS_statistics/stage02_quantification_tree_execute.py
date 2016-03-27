
from .stage02_quantification_tree_io import stage02_quantification_tree_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict
import numpy as np

class stage02_quantification_tree_execute(stage02_quantification_tree_io):
    def execute_tree(self,analysis_id_I,
                pipeline_id_I=None,
                test_size_I = 0.,
                impfeat_methods_I=[{'impfeat_method':'feature_importance','impfeat_options':None}],
                response_class_methods_I=[{'response_class_method':'class_probability','response_class_options':None}],
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],
                ):
        '''execute tree using sciKit-learn
        INPUT:
        analysis_id
        model_I = string, 'DecisionTreeClassifier', 'RandomForestClassifier', 'ExtraTreesClassifier', or 'AdaBoostClassifier'
        method_I = string, 'scikit-learn'
        parameters_I = {}, default=None, which will use recommended settings
        impfeat_method_I = 'feature_importance',
        impfeat_options_I = {}, default=None,
        OPTIONAL INPUT:
        ...
            
        '''

        #print('execute_tree...')

        # instantiate helper classes
        calculateinterface = calculate_interface()
        #stage02quantificationnormalizationquery = stage02_quantification_normalization_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        #stage02quantificationnormalizationquery.initialize_supportedTables();
        #stage02quantificationanalysisquery = stage02_quantification_analysis_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        #stage02quantificationanalysisquery.initialize_supportedTables();
        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        
        # instantiate data lists
        data_O=[]; #samples/features cov_matrix and precision_matrix
        data_impfeat_O=[]; #samples/features mahal_dist
        data_response_class_O=[]; #samples/features score
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

            # get the model pipeline:
            models,methods,parameters = self.get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationTreePipeline();

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
                test_size_I=test_size_I,
                random_state_I=calculateinterface.random_state
                );
            # instantiate the output dicts
            data_O_listDict = listDict();

            # call the tree method
            calculateinterface.make_dataModel(model_I,parameters_I);
            parameters_I = calculateinterface.data_model.get_params(); #update the parameters
            # score the model on the test data

            # extract out the response information
            for row in response_class_methods_I:
                if row['response_class_method'] == 'class_probability':
                    response_value_tmp, response_label_tmp = calculateinterface.extract_classProbabilities(
                        response_method_I=row['response_class_method'],
                        response_options_I=row['response_class_options']); #dim [nsamples,nresponses]
                    # reshape the responses
                    dictList = {};
                    for i,response in enumerate(response_label_tmp):
                        dictList[response]=response_value_tmp[:,i]
                    data_O_listDict.set_dictList(dictList);
                    data_O_listDict.convert_dictList2DataFrame();
                    response_value, response_label = data_O_listDict.get_flattenedDataAndColumnLabels();
                    data_O_listDict.clear_allData();
                    # reshape the sample_names_short
                    dictList = {};
                    for i,response in enumerate(response_label_tmp):
                        dictList[response]=calculateinterface.data_train['row_labels']['sample_name_short'].get_values()
                    data_O_listDict.set_dictList(dictList);
                    data_O_listDict.convert_dictList2DataFrame();
                    sample_names_short, response_label = data_O_listDict.get_flattenedDataAndColumnLabels();
                    data_O_listDict.clear_allData();
                elif row['response_class_method'] == 'decision_function':
                    response_value, response_label = calculateinterface.extract_decisionFunction(
                        response_method_I=row['response_class_method'],
                        response_options_I=row['response_class_options']);
                    data_O_listDict.set_dictList(dictList);
                    data_O_listDict.convert_dictList2DataFrame();
                    data_O_listDict.convert_dataFrame2ListDict();
                    response_class_statistics = data_O_listDict.get_listDict();
                data_O_listDict.clear_allData();
                # add in additional rows to the output data object
                data_O_listDict.add_column2DataFrame('sample_name_short',sample_names_short);
                data_O_listDict.add_column2DataFrame('response_name',response_label);
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('model',model_I);
                data_O_listDict.add_column2DataFrame('method',method_I);
                data_O_listDict.add_column2DataFrame('parameters',parameters_I);
                data_O_listDict.add_column2DataFrame('response_class_value',response_value);
                data_O_listDict.add_column2DataFrame('response_class_method',row['response_class_method']);
                data_O_listDict.add_column2DataFrame('response_class_options',row['response_class_options']);
                data_O_listDict.add_column2DataFrame('response_class_statistics',None);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_response_class_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();

            # extract out feature information
            for row in impfeat_methods_I:
                if row['impfeat_method'] == 'feature_importance':
                    impfeat_value = calculateinterface.extract_importantFeatures();
                    impfeat_n,impfeat_std = calculateinterface.calculate_importantFeatures_std(impfeat_value);
                    impfeat_zscore,impfeat_pvalue = calculateinterface.calculate_ZScoreAndPValue(
                        impfeat_value,impfeat_n,impfeat_std);
                    response_name='all';
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList({'n':impfeat_n,'std':impfeat_std,'zscore':impfeat_zscore,'pvalue':impfeat_pvalue});
                elif row['impfeat_method'] in ['RFE','RFECV']:
                    dataFeatureSelection = calculateinterface.make_dataFeatureSelection(
                            model_I,parameters_I,
                            row['impfeat_method'],row['impfeat_options']);
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
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('response_name',response_name);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('model',model_I);
                data_O_listDict.add_column2DataFrame('method',method_I);
                data_O_listDict.add_column2DataFrame('parameters',parameters_I);
                data_O_listDict.add_column2DataFrame('impfeat_value',impfeat_value);
                data_O_listDict.add_column2DataFrame('impfeat_method',row['impfeat_method']);
                data_O_listDict.add_column2DataFrame('impfeat_options',row['impfeat_options']);
                data_O_listDict.add_column2DataFrame('impfeat_statistics',impfeat_statistics);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_impfeat_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();
            #data_features_O.append(impfeat_listDict.get_listDict());

            #extract out sample information

            # reset calculate_interface
            calculateinterface.clear_data();
        # add data to the database
        #self.add_rows_table('data_stage02_quantification_tree_samples',data_O);
        self.add_rows_table('data_stage02_quantification_tree_impfeat',data_impfeat_O);
        self.add_rows_table('data_stage02_quantification_tree_responseClassification',data_response_class_O);

    def execute_treeHyperparameter(self,analysis_id_I,
                model_I='RandomForestClassifier',
                method_I="scikit-learn",
                parameters_I={'scale':True,'center':True},
                param_dist_I={"max_depth": [3, None],
                              "max_features": [1, 10],
                              "min_samples_split": [1, 10],
                              "min_samples_leaf": [1, 10],
                              "bootstrap": [True, False],
                              "criterion": ["gini", "entropy"]},
                test_size_I = 0.,
                metric_method_I = 'accuracy',
                metric_options_I = None,
                crossval_method_I = 'KFold',
                crossval_options_I = {'n_folds':3, 'shuffle':False, 'random_state':None},
                hyperparameter_method_I = 'RandomizedSearchCV',
                hyperparameter_options_I = {'n_iter':10, 'fit_params':None, 'n_jobs':4, 'iid':True, 'refit':True, 'verbose':0,  'random_state':None, 'error_score':'raise'},
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],
                ):
        '''execute tree using sciKit-learn
        INPUT:
        analysis_id
        model_I = string, 'DecisionTreeClassifier', 'RandomForestClassifier', 'ExtraTreesClassifier', or 'AdaBoostClassifier'
        method_I = string, 'scikit-learn'
        parameters_I = {}, parameters to search over
        OPTIONAL INPUT:
        ...
            
        '''

        #print('execute_tree...')

        # instantiate helper classes
        calculateinterface = calculate_interface()
        #stage02quantificationnormalizationquery = stage02_quantification_normalization_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        #stage02quantificationnormalizationquery.initialize_supportedTables();
        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        
        # instantiate data lists
        data_O=[]; #samples/features cov_matrix and precision_matrix
        data_validation_O=[]; #samples/features mahal_dist

        # query metabolomics data from glogNormalization
        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            #calculated_concentration_units = stage02quantificationnormalizationquery.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
            calculated_concentration_units = dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu in calculated_concentration_units:
            #print('calculating tree for calculated_concentration_units ' + cu);
            data = [];
            # get data:
            #data = stage02quantificationnormalizationquery.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
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
                test_size_I=test_size_I,
                random_state_I=calculateinterface.random_state
                );
            # instantiate the output dicts
            data_O_listDict = listDict();

            # call the hyper parmaeter CV method
            calculateinterface.make_dataModelAndHyperparameterCV(
                    model_I=model_I,
                    param_dist_I=param_dist_I,
                    hyperparameter_method_I=hyperparameter_method_I,
                    hyperparameter_options_I=hyperparameter_options_I,
                    crossval_method_I=crossval_method_I,
                    crossval_options_I=crossval_options_I,
                    crossval_labels_I=calculateinterface.data_train['row_labels']['sample_name_short'].get_values(),
                    metric_method_I=metric_method_I,
                    metric_options_I=metric_options_I,
                    raise_I=False);
            # score the model on the test data

            # extract out the cross validation information
            
            # add in additional rows to the output data object
            data_O_listDict.add_column2DataFrame('sample_name_short',sample_names_short);
            data_O_listDict.add_column2DataFrame('response_name',response_label);
            data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
            data_O_listDict.add_column2DataFrame('test_size',test_size_I);
            data_O_listDict.add_column2DataFrame('used_',True);
            data_O_listDict.add_column2DataFrame('comment_',None);
            data_O_listDict.add_column2DataFrame('model',model_I);
            data_O_listDict.add_column2DataFrame('method',method_I);
            data_O_listDict.add_column2DataFrame('parameters',parameters_I);
            data_O_listDict.add_column2DataFrame('response_class_value',response_value);
            data_O_listDict.add_column2DataFrame('response_class_method',row['response_class_method']);
            data_O_listDict.add_column2DataFrame('response_class_options',row['response_class_options']);
            data_O_listDict.add_column2DataFrame('response_class_statistics',None);
            # add data to the database
            data_O_listDict.convert_dataFrame2ListDict();
            data_response_class_O.extend(data_O_listDict.get_listDict());
            data_O_listDict.clear_allData();

            # reset calculate_interface
            calculateinterface.clear_data();
        # add data to the database
        self.add_rows_table('data_stage02_quantification_tree_hyperparameter',data_O);