
from .stage02_quantification_spls_io import stage02_quantification_spls_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict
import numpy as np

class stage02_quantification_spls_execute(stage02_quantification_spls_io):

    #TODO:
    #add in methods for plsda
    def execute_spls(self,analysis_id_I,
                pipeline_id_I=None,
                test_size_I = 0.,
                impfeat_methods_I=[
                    {'coefficients':'feature_importance','impfeat_options':None},
                    {'VIP':'feature_importance','impfeat_options':None}],
                    #loadings are saved implicitely
                response_class_methods_I=[{'response_class_method':'class_probability','response_class_options':None}],
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],
                r_calc_I=None
                ):
        '''execute spls using sciKit-learn
        INPUT:
        analysis_id
        pipeline_id_I
        impfeat_methods_I
        response_class_methods_I
        OPTIONAL INPUT:
        ...
            
        '''

        #print('execute_spls...')

        # instantiate helper classes
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calculateinterface = calculate_interface()
        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        dataPreProcessing_replicates_query.initialize_supportedTables();
        
        # instantiate data lists
        data_O=[]; #samples/features cov_matrix and precision_matrix
        data_impfeat_O=[]; #samples/features mahal_dist
        data_scores_O=[];
        data_loadings_O=[];
        data_loadingsResponse_O=[];

        # query metabolomics data from glogNormalization
        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu in calculated_concentration_units:
            #print('calculating spls for calculated_concentration_units ' + cu);
            data = [];
            # get data:
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
            models,methods,parameters = self.get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationSplsPipeline(pipeline_id_I);

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

            r_calc.clear_workspace();
            # add the data to the R workspace:
            dims = calculateinterface.data_train['data'].shape;
            r_calc.make_matrixFromList(
                calculateinterface.data_train['data'].ravel(),
                dims[0],
                dims[1],
                'x');
            response = calculateinterface.data_train['response'].ravel();
            r_calc.make_factorsFromList(response,'y');
            
            #iterate through the different models:
            for i,model in enumerate(models):
                #scale and/or center the data
                if model=='prep' and ('center' in parameters[i].keys() or 'scale' in parameters[i].keys()):
                    r_calc.pcaMethods_scale('x','x',parameters[i]['center'],parameters[i]['scale']);
                # call the spls method
                elif model == 'splsda':
                    r_calc.calculate_splsda(
                        spls_O='spls.o',
                        x='x',
                        y='y',
                        K=parameters[i]["K"],
                        eta=parameters[i]["eta"],
                        kappa=parameters[i]['kappa'],
                        classifier=parameters[i]['classifier'],
                        scale_x=parameters[i]['scale_x'],
                        );
                    #extract out the scores and loadings
                    scores,loadings=r_calc.extract_scoresAndLoadings_splsda(
                        spls_I='spls.o');
                elif model == 'sgpls': #TODO
                    r_calc.calculate_splsda(
                        spls_O='spls.o',
                        x='x',
                        y='y',

                        );
                    #extract out the scores and loadings
                    scores,loadings=r_calc.extract_scoresAndLoadings_sgpls(
                        spls_I='spls.o');
                elif model == 'splsda_mixOmics':
                    r_calc.calculate_splsda_mixOmics(
                        spls_O='spls.o',
                        x='x',
                        y='y',
                        ncomp=parameters[i]["ncomp"],
                        );
                    #extract out the scores and loadings
                    scores,loadings=r_calc.extract_scoresAndLoadings_splsda_mixOmics(
                        spls_I='spls.o');
            # score the model on the test data

            # reformat the scores and loadings
            data_O_listDict.clear_allData();
            # add in additional rows to the output data object
            data_O_listDict.add_column2DataFrame('sample_name_short',sample_names_short);
            data_O_listDict.add_column2DataFrame('response_name',response_label);
            data_O_listDict.add_column2DataFrame('test_size',test_size_I);
            data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
            data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
            data_O_listDict.add_column2DataFrame('used_',True);
            data_O_listDict.add_column2DataFrame('comment_',None);
            data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
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
                    if impfeat_value is None: continue;
                    impfeat_n,impfeat_std = calculateinterface.calculate_importantFeatures_std(impfeat_value);
                    impfeat_zscore,impfeat_pvalue = calculateinterface.calculate_ZScoreAndPValue(
                        impfeat_value,impfeat_n,impfeat_std);
                    response_name='all';
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList({'n':impfeat_n,'std':impfeat_std,'zscore':impfeat_zscore,'pvalue':impfeat_pvalue});
                elif row['impfeat_method'] in ['RFE','RFECV']:
                    dataFeatureSelection = calculateinterface.make_dataFeatureSelection(
                            row['impfeat_method'],row['impfeat_options']);
                    calculateinterface.fit_data2FeatureSelection();
                    impfeat_options_I = calculateinterface.data_model.get_params(); #update the parameters
                    impfeat_value,impfeat_score = calculateinterface.extract_dataFeatureSelection_ranking();
                    if impfeat_value is None: continue;
                    response_name='all';
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList({'score':impfeat_score});
                elif row['impfeat_method'] == 'coefficients':
                    impfeat_n,impfeat_value,impfeat_mean,impfeat_std = calculateinterface.extract_coefficientsSVM();
                    if impfeat_value is None: continue;
                    response_name='all';
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList({'n':impfeat_n,'std':impfeat_std,'mean':impfeat_mean});
                elif row['impfeat_method'] == 'VIP':
                    impfeat_n,impfeat_value,impfeat_mean,impfeat_std = calculateinterface.extract_coefficientsSVM();
                    if impfeat_value is None: continue;
                    response_name='all';
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList({'n':impfeat_n,'std':impfeat_std,'mean':impfeat_mean});
                data_O_listDict.convert_dictList2DataFrame();
                data_O_listDict.convert_dataFrame2ListDict();
                impfeat_statistics = data_O_listDict.get_listDict();
                data_O_listDict.clear_allData();
                # add in additional rows to the output data object
                data_O_listDict.add_column2DataFrame('component_name',calculateinterface.data['column_labels']['component_name'].ravel());
                data_O_listDict.add_column2DataFrame('component_group_name',calculateinterface.data['column_labels']['component_group_name'].ravel());
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('response_name',response_name);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
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
        #self.add_rows_table('data_stage02_quantification_spls_samples',data_O);
        self.add_rows_table('data_stage02_quantification_spls_impfeat',data_impfeat_O);
        self.add_rows_table('data_stage02_quantification_spls_scores',data_scores_O);
        self.add_rows_table('data_stage02_quantification_spls_loadings',data_loadings_O);
        self.add_rows_table('data_stage02_quantification_spls_loadingsResponse',data_loadingsResponse_O);

    def execute_splsHyperparameter(self,analysis_id_I,
                pipeline_id_I=None,
                param_dist_I={"kappa": 0.5,
                              "K": [1,2,3,4,5],
                              "eta": [0.1,.3,.5,.7,.9],
                              "classifier":'lda',
                            'scale_x':"FALSE",
                                },
                test_size_I = 0.,
                metric_method_I = 'error_rate',
                metric_options_I = None,
                crossval_method_I = 'v-fold',
                crossval_options_I = {'fold':5
                                      },
                hyperparameter_method_I = 'GridSearchCV',
                hyperparameter_options_I = {
                    'plot_it':"FALSE", 'n_core':2,
                    },
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],
                r_calc_I=None
                ):
        '''execute spls using sciKit-learn
        INPUT:
        analysis_id
        pipeline_id_I = 
        param_dist_I = {}, parameters to search over
        OPTIONAL INPUT:
        ...
            
        '''

        #print('execute_spls...')

        # instantiate helper classes
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        calculateinterface = calculate_interface()
        dataPreProcessing_replicates_query = stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        
        # instantiate data lists
        data_O=[];

        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu in calculated_concentration_units:
            #print('calculating spls for calculated_concentration_units ' + cu);
            data = [];
            # get data:
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
            models,methods,parameters = self.get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationSplsPipeline(pipeline_id_I);

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
            
            r_calc.clear_workspace();
            # add the data to the R workspace:
            dims = calculateinterface.data_train['data'].shape;
            r_calc.make_matrixFromList(
                calculateinterface.data_train['data'].ravel(),
                dims[0],
                dims[1],
                'x');
            response = calculateinterface.data_train['response'].ravel();
            levels = data_O_listDict.convert_list2Levels(response)
            r_calc.make_vectorFromList(levels,'y');
            r_calc.make_vectorFromList(param_dist_I['K'],'K');
            r_calc.make_vectorFromList(param_dist_I['eta'],'eta');

            #iterate through the different models:
            for i,model in enumerate(models):
                #scale and/or center the data
                if model=='prep' and ('center' in parameters[i].keys() or 'scale' in parameters[i].keys()):
                    r_calc.pcaMethods_scale('x','x',parameters[i]['center'],parameters[i]['scale']);

                # call the hyper parmeter CV method
                elif model == 'splsda':
                    r_calc.cv_splsda(
                        cvspls_O='cvspls.o',
                        x='x',
                        y='y',
                        fold = crossval_options_I['fold'],
                        K="K",
                        eta="eta",
                        kappa=param_dist_I['kappa'],
                        classifier=param_dist_I['classifier'],
                        scale_x=param_dist_I['scale_x'],
                        plot_it=hyperparameter_options_I['plot_it'],
                        n_core=hyperparameter_options_I['n_core']
                        );
                    grid_scores = r_calc.extract_cv_splsda(cvspls_I='cvspls.o');
                elif model == 'sgpls':
                    r_calc.cv_splsda(
                        cvspls_O='cvspls.o',
                        x='x',
                        y='y',
                        fold = 10,

                        );
                    grid_scores = r_calc.extract_cv_sgpls(cvspls_I='cvspls.o');

            # extract out the hyper parameter CV information
            pipeline_parameters = [];
            metric_scores = [];
            for i in range(grid_scores.shape[0]):
                for j in range(grid_scores.shape[1]):
                    tmp = {};
                    tmp['eta']=param_dist_I['eta'][i];
                    tmp['K']=param_dist_I['K'][j];
                    pipeline_parameters.append(tmp);
                    metric_scores.append(grid_scores[i,j]);

            data_O_listDict.set_dictList(
                {'metric_score':metric_scores,
                 'pipeline_parameters':pipeline_parameters});
            data_O_listDict.convert_dictList2DataFrame()

            #convert bounds to metric_statistics:
            hyperparameter_id = list(range(len(metric_scores)));
            hyperparameter_options = [hyperparameter_options_I for id in hyperparameter_id];
            crossval_options = [crossval_options_I for id in hyperparameter_id];

            # add in additional rows to the output data object
            data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
            data_O_listDict.add_column2DataFrame('test_size',test_size_I);
            data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
            data_O_listDict.add_column2DataFrame('used_',True);
            data_O_listDict.add_column2DataFrame('comment_',None);
            data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
            data_O_listDict.add_column2DataFrame('metric_statistics',None);
            data_O_listDict.add_column2DataFrame('metric_method',metric_method_I);
            data_O_listDict.add_column2DataFrame('metric_options',metric_options_I);
            data_O_listDict.add_column2DataFrame('crossval_method',crossval_method_I);
            data_O_listDict.add_column2DataFrame('crossval_options',crossval_options);
            data_O_listDict.add_column2DataFrame('hyperparameter_id',hyperparameter_id);
            data_O_listDict.add_column2DataFrame('hyperparameter_method',hyperparameter_method_I);
            data_O_listDict.add_column2DataFrame('hyperparameter_options',hyperparameter_options);

            # add data to the database
            data_O_listDict.convert_dataFrame2ListDict();
            data_O.extend(data_O_listDict.get_listDict());
            data_O_listDict.clear_allData();

            # reset calculate_interface
            calculateinterface.clear_data();
        # add data to the database
        self.add_rows_table('data_stage02_quantification_spls_hyperparameter',data_O);