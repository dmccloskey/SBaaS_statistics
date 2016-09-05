
from .stage02_quantification_spls_io import stage02_quantification_spls_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict
import numpy as np

class stage02_quantification_spls_execute(stage02_quantification_spls_io):

    #TODO:
    #add in methods for pls,plsda,pca
    def execute_spls(self,analysis_id_I,
                pipeline_id_I=None,
                test_size_I = 0.,
                impfeat_methods_I=[
                    {'impfeat_method':'coefficients','impfeat_options':None},
                    {'impfeat_method':'VIP','impfeat_options':None},
                    {'impfeat_method':'loadings','impfeat_options':None},
                    {'impfeat_method':'correlations','impfeat_options':None}],
                response_class_methods_I=[
                    {'response_class_method':'scores','response_class_options':None},
                    {'response_class_method':'scores_response','response_class_options':None},
                    {'response_class_method':'explained_variance','response_class_options':None},
                    #{'response_class_method':'var_proportion','response_class_options':None},
                    #{'response_class_method':'var_cumulative','response_class_options':None},
                    ],
                impfeat_response_methods_I=[
                    {'impfeat_response_method':'correlations_response','impfeat_response_options':None},
                    {'impfeat_response_method':'loadings_response','impfeat_response_options':None},
                    ],
                calculated_concentration_units_I=[],
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                sample_name_shorts_I=[],
                component_names_I=[],
                component_group_names_I=[],
                time_points_I=[],
                r_calc_I=None,
                query_object_descStats_I = 'stage02_quantification_dataPreProcessing_replicates_query',
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
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query,
                        'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();
        
        # instantiate data lists
        data_O=[]; 
        data_impfeat_O=[]; 
        data_scores_O=[];
        data_loadings_O=[];
        data_loadingsResponse_O=[];

        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu in calculated_concentration_units:
            #print('calculating spls for calculated_concentration_units ' + cu);
            if hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates'):
                data_listDict = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                    analysis_id_I,
                    cu,
                    experiment_ids_I=experiment_ids_I,
                    sample_name_abbreviations_I=sample_name_abbreviations_I,
                    sample_name_shorts_I=sample_name_shorts_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    time_points_I=time_points_I,);
            elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,
                    cu,
                    experiment_ids_I=experiment_ids_I,
                    sample_name_abbreviations_I=sample_name_abbreviations_I,
                    sample_name_shorts_I=sample_name_shorts_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    time_points_I=time_points_I,);
                data_listDict = self._extract_averagesData(data_tmp);
            elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                    analysis_id_I,
                    cu,
                    experiment_ids_I=experiment_ids_I,
                    sample_name_abbreviations_I=sample_name_abbreviations_I,
                    sample_name_shorts_I=sample_name_shorts_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    time_points_I=time_points_I,);
                data_listDict = self._extract_averagesData(data_tmp);
            else:
                print('query instance does not have the required method.');

            # get the model pipeline:
            models,methods,parameters = self.get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationSPLSPipeline(pipeline_id_I);

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
                'x.matrix');
            response = calculateinterface.data_train['response'].ravel();
            levels = data_O_listDict.convert_list2Levels(response)
            r_calc.make_vectorFromList(levels,'y.vector');
            r_calc.make_factorsFromList(response,'factors_f');
            r_calc.make_dummyMatrixFromFactors('factors_f','dummy');
            factors_unique = data_listDict.get_uniqueValues_list(response);
            
            #iterate through the different models:
            for i,model in enumerate(models):
                #scale and/or center the data
                if model=='prep' and ('center' in parameters[i].keys() or 'scale' in parameters[i].keys()):
                    r_calc.pcaMethods_scale('x.matrix','x.matrix',parameters[i]['center'],parameters[i]['scale']);
                # call the spls method
                elif model == 'splsda':
                    r_calc.calculate_splsda(
                        spls_O='result_O',
                        x='x.matrix',
                        y='y.vector',
                        K=parameters[i]["K"],
                        eta=parameters[i]["eta"],
                        kappa=parameters[i]['kappa'],
                        classifier=parameters[i]['classifier'],
                        scale_x=parameters[i]['scale_x'],
                        );
                    ##extract out the scores and loadings
                    #scores,loadings=r_calc.extract_scoresAndLoadings_splsda(
                    #    spls_I='result_O');
                elif model == 'sgpls': #TODO
                    r_calc.calculate_splsda(
                        spls_O='result_O',
                        x='x.matrix',
                        y='y.vector',

                        );
                    ##extract out the scores and loadings
                    #scores,loadings=r_calc.extract_scoresAndLoadings_sgpls(
                    #    spls_I='result_O');
                elif model == 'splsda_mixOmics':
                    r_calc.calculate_splsda_mixOmics(
                        spls_O='result_O',
                        x='x.matrix',
                        y='y.vector',
                        ncomp=parameters[i]["ncomp"],
                        );
                    ##extract out the scores and loadings
                    #scores,loadings=r_calc.extract_scoresAndLoadings_splsda_mixOmics(
                    #    spls_I='result_O');
                elif model == 'oplsda':
                    # call the method
                    # extract the scores and loadings
                    scores,loadings=[],[]
                elif model == 'plsda':
                    # check/correct ncomp/segments
                    ncomp = parameters[i]['ncomp'];
                    if len(factors_unique)<ncomp:
                        ncomp = len(factors_unique);
                    # add in additional dataframe to the R workspace required for mvr
                    r_calc.make_dataFrameFromLists(
                        labels_I=['x.matrix','dummy'],
                        dataFrame_O = 'dataframe',
                        )
                    # call the method
                    r_calc.call_mvr(
                        'result_O',
                        fit = 'dummy ~ x.matrix',     
                        data = 'dataframe',  
                        ncomp=ncomp,
                        scale=parameters[i]['scale'],
                        validation=parameters[i]['validation'], #change to parameters when not performing CV
                        segments=parameters[i]['segments'],
                        method=parameters[i]['method'],
                        lower=parameters[i]['lower'],
                        upper=parameters[i]['upper'], 
                        weights=parameters[i]['weights'],
                        );
                elif model == 'plsda-mixomics':
                    # call the method
                    # extract the scores and loadings
                    scores,loadings=[],[]
            # score the model on the test data
            
            # extract out response impFeature information
            for row in impfeat_response_methods_I:
                if row['impfeat_response_method'] == 'loadings_response':
                    loadings_y = rcalc.extract_mvr_Yloadings('extract_mvr_Yloadings');
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'response_class_value':response_value,
                         'axis':axis});
                elif row['impfeat_response_method'] == 'correlations_response':
                    cor_y = r_calc.calculate_mvr_correlationResponse(
                        'result_O',
                        'correlation_f',
                        comps='1:'+str(loadings_y.shape[1]), #not safe!
                        );
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'response_class_value':response_value,
                         'axis':axis});
                data_O_listDict.convert_dictList2DataFrame();
                data_O_listDict.convert_dataFrame2ListDict();
                # add in additional rows to the output data object
                #TODO: ensure length of factors_unique is consistent!
                data_O_listDict.add_column2DataFrame('response_name',factors_unique);
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                data_O_listDict.add_column2DataFrame('impfeat_response_method',row['response_class_method']);
                data_O_listDict.add_column2DataFrame('impfeat_response_options',row['response_class_options']);
                data_O_listDict.add_column2DataFrame('impfeat_response_statistics',None);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_response_class_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();

            # extract out response information
            for row in response_class_methods_I:
                sns = calculateinterface.data['row_labels']['sample_name_short'].ravel()
                rn = calculateinterface.data['row_labels'][factor_label].ravel()
                if row['response_class_method'] == 'scores':
                    scores_x = rcalc._extract_mvr_scores('result_O');
                    response_value = [];
                    axis = []
                    for r in range(scores_x.shape[0]):
                        for c in range(scores_x.shape[1]):
                            axis.append(c+1);
                            response_value.append(scores_x[r,c])
                    data_O_listDict.set_dictList(
                        {
                         'response_class_value':response_value,
                         'axis':axis});
                elif row['response_class_method'] == 'scores_response':
                    scores_y = rcalc.extract_mvr_Yscores('result_O');
                    response_value = [];
                    axis = []
                    for r in range(scores_y.shape[0]):
                        for c in range(scores_y.shape[1]):
                            axis.append(c+1);
                            response_value.append(scores_y[r,c])
                    data_O_listDict.set_dictList(
                        {
                         'response_class_value':response_value,
                         'axis':axis});
                elif row['response_class_method'] in ['var_proportional','var_cumulative','explained_variance']:
                    var_proportion,var_cumulative = rcalc.calculate_mvr_explainedVariance('result_O');
                    response_value = [];
                    response_value += [var for var in len(sns)*var_proportion];
                    response_value += [var for var in len(sns)*var_cumulative];
                    axis = [c+1 for c in range(2*len(sns)*len(var_proportion))];
                    data_O_listDict.set_dictList(
                        {
                         'response_class_value':response_value,
                         'axis':axis});
                data_O_listDict.convert_dictList2DataFrame();
                data_O_listDict.convert_dataFrame2ListDict();
                # add in additional rows to the output data object
                #TODO: ensure length of sample_name_short is consistent!
                sns_multiple = len(response_value)/len(sns);
                data_O_listDict.add_column2DataFrame('sample_name_short',sns*sns_multiple);
                data_O_listDict.add_column2DataFrame('response_name',rn*sns_multiple);
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                #data_O_listDict.add_column2DataFrame('response_class_value',response_value);
                data_O_listDict.add_column2DataFrame('response_class_method',row['response_class_method']);
                data_O_listDict.add_column2DataFrame('response_class_options',row['response_class_options']);
                data_O_listDict.add_column2DataFrame('response_class_statistics',None);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_response_class_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();

            # extract out feature information
            for row in impfeat_methods_I:
                if row['impfeat_method'] == 'loadings':
                    loadings_x = r_calc.extract_mvr_loadings('result_O');
                    response_name=[];
                    impfeat_value = [];
                    axis = [];
                    for r in range(loadings_x.shape[0]):
                        for c in range(loadings_x.shape[1]): #comp
                            axis.append(c+1);
                            response_value.append(loadings_x[r,c])
                            response_name.append('all');
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'impfeat_value':impfeat_value,
                         'axis':axis});
                elif row['impfeat_method'] in 'correlations':
                    cor_x = r_calc.calculate_mvr_correlation(
                        'result_O',
                        'correlation_m',
                        comps='1:'+str(loadings_x.shape[1]), #not safe!
                        );
                    response_name=[];
                    impfeat_value = [];
                    axis = [];
                    for r in range(cor_x.shape[0]):
                        for c in range(cor_x.shape[1]): #comp
                            axis.append(c+1);
                            response_value.append(cor_x[r,c])
                            response_name.append('all');
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'impfeat_value':impfeat_value,
                         'axis':axis});
                elif row['impfeat_method'] == 'coefficients':
                    coefficients,coefficients_comps_reduced,coefficients_reduced=r_calc.extract_mvr_coefficients('result_O');
                    if coefficients is None: continue;
                    response_name=[];
                    impfeat_value = [];
                    axis = [];
                    #TODO: check factors-unique/coefficients shape consistency
                    for r in range(coefficients.shape[0]):
                        for c in range(coefficients.shape[1]):
                            for z in range(coefficients.shape[2]):
                                response_name.append(factors_unique[c]);
                                impfeat_value.append(coefficients[r,c,z]);
                                axis.append(z);
                    for r in range(coefficients_comps_reduced.shape[0]):
                        for c in range(coefficients_comps_reduced.shape[1]):
                            response_name.append(factors_unique[c]);
                            impfeat_value.append(coefficients_comps_reduced[r,c]);
                            axis.append(-1);
                    for r in range(coefficients_comps_reduced.shape[0]):
                        response_name.append('all');
                        impfeat_value.append(coefficients_reduced[r]);
                        axis.append(-1);
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'impfeat_value':impfeat_value,
                         'axis':axis});
                elif row['impfeat_method'] == 'VIP':
                    vip,vip_reduced = r_calc.extract_mvr_vip('result_O');
                    if vip is None: continue;
                    response_name=[];
                    impfeat_value = [];
                    axis = [];
                    for r in range(vip.shape[0]):
                        for c in range(vip.shape[1]):
                            impfeat_value.append(vip[r,c]);
                            response_name.append(factors_unique[r])
                            axis.append(-1);
                    for c in range(vip.shape[1]):
                        impfeat_value.append(vip_reduced[c]);
                        response_name.append('all');
                        axis.append(-1);
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'impfeat_value':impfeat_value,
                         'axis':axis});
                data_O_listDict.convert_dictList2DataFrame();
                data_O_listDict.convert_dataFrame2ListDict();
                # add in additional rows to the output data object
                cn = calculateinterface.data['column_labels']['component_name'].ravel();
                cn_multiple = len(impfeat_value)/len(cn);
                cgn = calculateinterface.data['column_labels']['component_group_name'].ravel();
                data_O_listDict.add_column2DataFrame('component_name',cn*cn_multiple);
                data_O_listDict.add_column2DataFrame('component_group_name',cng*cn_multiple);
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                #data_O_listDict.add_column2DataFrame('response_name',response_name);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                #data_O_listDict.add_column2DataFrame('impfeat_value',impfeat_value);
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
        self.add_rows_table('data_stage02_quantification_spls_responseClassification',data_scores_O);
        self.add_rows_table('data_stage02_quantification_spls_impfeat',data_loadings_O);
        self.add_rows_table('data_stage02_quantification_spls_impfeatResponse',data_loadingsResponse_O);

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
                r_calc_I=None,
                query_object_descStats_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            
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
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query,
                        'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();
        
        # instantiate data lists
        data_O=[];

        # get concentration units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu in calculated_concentration_units:
            #print('calculating spls for calculated_concentration_units ' + cu);
            if hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates'):
                data_listDict = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                    analysis_id_I,
                    cu,
                    experiment_ids_I=experiment_ids_I,
                    sample_name_abbreviations_I=sample_name_abbreviations_I,
                    sample_name_shorts_I=sample_name_shorts_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    time_points_I=time_points_I,);
            elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,
                    cu,
                    experiment_ids_I=experiment_ids_I,
                    sample_name_abbreviations_I=sample_name_abbreviations_I,
                    sample_name_shorts_I=sample_name_shorts_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    time_points_I=time_points_I,);
                data_listDict = self._extract_averagesData(data_tmp);
            elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
                    analysis_id_I,
                    cu,
                    experiment_ids_I=experiment_ids_I,
                    sample_name_abbreviations_I=sample_name_abbreviations_I,
                    sample_name_shorts_I=sample_name_shorts_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
                    time_points_I=time_points_I,);
                data_listDict = self._extract_averagesData(data_tmp);
            else:
                print('query instance does not have the required method.');

            # get the model pipeline:
            models,methods,parameters = self.get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationSPLSPipeline(pipeline_id_I);

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
                'x.matrix');
            response = calculateinterface.data_train['response'].ravel();
            levels = data_O_listDict.convert_list2Levels(response)
            r_calc.make_vectorFromList(levels,'y.vector');
            r_calc.make_factorsFromList(response,'factors_f');
            r_calc.make_dummyMatrixFromFactors('factors_f','dummy');

            #iterate through the different models:
            for i,model in enumerate(models):
                #scale and/or center the data
                if model=='prep' and ('center' in parameters[i].keys() or 'scale' in parameters[i].keys()):
                    r_calc.pcaMethods_scale('x.matrix','x.matrix',parameters[i]['center'],parameters[i]['scale']);

                #TODO: split into internal functions
                # call the hyper parmeter CV method and extract the CV information
                elif model == 'splsda':
                    r_calc.make_vectorFromList(param_dist_I['K'],'K');
                    r_calc.make_vectorFromList(param_dist_I['eta'],'eta');
                    # call the hyper parmeter CV method
                    r_calc.cv_splsda(
                        cvspls_O='cvresult_O',
                        x='x.matrix',
                        y='y.vector',
                        fold = crossval_options_I['fold'],
                        K="K",
                        eta="eta",
                        kappa=param_dist_I['kappa'],
                        classifier=param_dist_I['classifier'],
                        scale_x=param_dist_I['scale_x'],
                        plot_it=hyperparameter_options_I['plot_it'],
                        n_core=hyperparameter_options_I['n_core']
                        );
                    # extract the CV information
                    grid_scores = r_calc.extract_cv_splsda(cvspls_I='cvresult_O');
                    pipeline_parameters = [];
                    metric_scores = [];
                    for i in range(grid_scores.shape[0]):
                        for j in range(grid_scores.shape[1]):
                            tmp = {};
                            tmp['eta']=param_dist_I['eta'][i];
                            tmp['K']=param_dist_I['K'][j];
                            pipeline_parameters.append(tmp);
                            metric_scores.append(grid_scores[i,j]);
                elif model == 'sgpls':
                    r_calc.make_vectorFromList(param_dist_I['K'],'K');
                    r_calc.make_vectorFromList(param_dist_I['eta'],'eta');
                    # call the hyper parmeter CV method
                    r_calc.cv_splsda(
                        cvspls_O='cvresult_O',
                        x='x.matrix',
                        y='y.vector',
                        fold = 10,

                        );
                    # extract the CV information
                    grid_scores = r_calc.extract_cv_sgpls(cvspls_I='cvresult_O');
                elif model == 'oplsda':
                    # call the hyper parmeter CV method
                    # extract the CV information
                    pipeline_parameters = [];
                    metric_scores = [];
                elif model == 'plsda':
                    # check/correct ncomp/segments
                    factors_unique = data_listDict.get_uniqueValues_list(response);
                    ncomp = parameters[i]['ncomp'];
                    segments = crossval_options_I['segments'];
                    if len(factors_unique)<ncomp:
                        ncomp = len(factors_unique);
                    if len(response)<segments:
                        segments = int(0.75*len(response));
                    # add in additional dataframe to the R workspace required for mvr
                    r_calc.make_dataFrameFromLists(
                        labels_I=['x.matrix','dummy'],
                        dataFrame_O = 'dataframe',
                        )
                    # call the hyper parmeter CV method
                    r_calc.call_mvr(
                        'cvresult_O',
                        fit = 'dummy ~ x.matrix',     
                        data = 'dataframe',  
                        ncomp=ncomp,
                        scale=parameters[i]['scale'],
                        validation=crossval_options_I['validation'], #change to parameters when not performing CV
                        segments=segments,
                        method=parameters[i]['method'],
                        lower=parameters[i]['lower'],
                        upper=parameters[i]['upper'], 
                        weights=parameters[i]['weights'],
                        );
                    # extract the CV information
                    msep_reduced,rmsep_reduced,r2_reduced,q2_reduced,r2x_reduced=r_calc.extract_mvr_performance(
                        'cvresult_O',
                        validation=crossval_options_I['validation'],)
                    pipeline_parameters = [];
                    metric_scores = [];
                    metric_methods = [];
                    for i in range(len(msep_reduced)): #model
                        tmp = {};
                        tmp['ncomp'] = i;
                        pipeline_parameters.append(tmp);
                        metric_scores.append(msep_reduced[i]);
                        metric_methods.append('msep');
                        pipeline_parameters.append(tmp);
                        metric_scores.append(rmsep_reduced[i]);
                        metric_methods.append('rmsep');
                        pipeline_parameters.append(tmp);
                        metric_scores.append(r2_reduced[i]);
                        metric_methods.append('r2');
                        pipeline_parameters.append(tmp);
                        metric_scores.append(q2_reduced[i]);
                        metric_methods.append('q2');
                        pipeline_parameters.append(tmp);
                        metric_scores.append(r2x_reduced[i]);
                        metric_methods.append('r2x');
                elif model == 'plsda-mixomics':
                    # call the hyper parmeter CV method
                    # extract the CV information
                    pipeline_parameters = [];
                    metric_scores = [];
                    metric_methods = [];
                    
            #convert bounds to metric_statistics:
            hyperparameter_id = list(range(len(metric_scores)));
            hyperparameter_options = [hyperparameter_options_I for id in hyperparameter_id];
            crossval_options = [crossval_options_I for id in hyperparameter_id];
            
            # extract out the hyper parameter CV information
            # and add rows/columns to the output object
            # NOTE: in R, multiple metrics can be calculated during a single CV
            if type(metric_method_I)==type(''):
                data_O_listDict.set_dictList(
                    {'metric_score':metric_scores,
                     'pipeline_parameters':pipeline_parameters});
                data_O_listDict.convert_dictList2DataFrame()

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
            elif type(metric_method_I)==type([]):
                data_O_listDict.set_dictList(
                    {'metric_score':metric_scores,
                        'metric_method':metric_methods,
                        'pipeline_parameters':pipeline_parameters});
                data_O_listDict.convert_dictList2DataFrame()

                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                data_O_listDict.add_column2DataFrame('metric_statistics',None);
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

    def _extract_averagesData(self,
            data_I,
            descStats_replicate_keys = ['median','iq_1','iq_3','min','max']):
        '''Parse data_stage02_quantification_preProcessing averages or
        data_stage02_quantification_descriptiveStats into replicates
        INPUT:
        data = query data
        descStats_replicate_keys = [] of strings, designating the column values to use as replicate points
        OUTPUT:
        listDict_O
        '''
        data = [];
        if type(data_I)==type(listDict()):
            data_I.convert_dataFrame2ListDict();
        for d in data_I.listDict:
            for i,k in enumerate(descStats_replicate_keys):
                tmp = copy.copy(d);
                tmp['calculated_concentration']=tmp[k];
                tmp['sample_name_short']='%s_%s'%(tmp['sample_name_abbreviation'],i);
                data.append(tmp);
        data_listDict = listDict(listDict_I=data);
        data_listDict.convert_listDict2DataFrame();
        return data_listDict;