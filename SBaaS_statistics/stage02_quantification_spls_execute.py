
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

    #TODO: add in methods pca
    #TODO: break into smaller functions to call resampling methods
    def execute_spls(self,analysis_id_I,
                pipeline_id_I=None,
                test_size_I = 0.,
                loadings_methods_I=[
                    {'metric_method':'loadings','metric_options':None},
                    {'metric_method':'correlations','metric_options':None}],
                impfeat_methods_I=[
                    {'impfeat_method':'coefficients','impfeat_options':None},
                    {'impfeat_method':'VIP','impfeat_options':None},],
                scores_methods_I=[
                    {'metric_method':'scores','metric_options':None},
                    {'metric_method':'scores_response','metric_options':None},
                    #{'metric_method':'explained_variance','metric_options':None},
                    ],
                loadings_response_methods_I=[
                    {'metric_method':'loadings_response','metric_options':None},
                    {'metric_method':'correlations_response','metric_options':None},
                    ],
                axis_metric_methods_I=[
                    {'metric_method':'var_proportion','metric_options':None},
                    {'metric_method':'var_cumulative','metric_options':None},
                    ],
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
                r_calc_I=None,
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
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance_descStats = query_object(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();
        
        # instantiate data lists
        data_O=[]; 
        data_axis_O=[];
        data_impfeat_O=[]; 
        data_scores_O=[];
        data_loadings_O=[];
        data_loadingsResponse_O=[];

        # get the model pipeline:
        models,methods,parameters = self.get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationSPLSPipeline(pipeline_id_I);
        
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
            cu = row['calculated_concentration_units']
            if not cu in data_analysis.keys(): data_analysis[cu]=[];
            data_analysis[cu].append(row);
        del data_analysis['_del_'];

        #apply the analysis to each group
        for cu in calculated_concentration_units:
            print('generating a heatmap for concentration_units ' + cu);
            # get the data
            data = data_analysis[cu];
            data_listDict = listDict(listDict_I=data);
            data_listDict.convert_listDict2DataFrame();

        ##depreicated
        ## get concentration units
        #if calculated_concentration_units_I:
        #    calculated_concentration_units = calculated_concentration_units_I;
        #else:
        #    calculated_concentration_units = [];
        #    if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates'):
        #        calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        #    elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
        #        calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        #    elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
        #        calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
        #    else:
        #        print('query instance does not have the required method.');
        #for cu in calculated_concentration_units:
        #    #print('calculating spls for calculated_concentration_units ' + cu);
        #    if hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates'):
        #        data_listDict = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
        #            analysis_id_I,
        #            cu,
        #            experiment_ids_I=experiment_ids_I,
        #            sample_name_abbreviations_I=sample_name_abbreviations_I,
        #            sample_name_shorts_I=sample_name_shorts_I,
        #            component_names_I=component_names_I,
        #            component_group_names_I=component_group_names_I,
        #            time_points_I=time_points_I,);
        #    elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
        #        data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
        #            analysis_id_I,
        #            cu,
        #            experiment_ids_I=experiment_ids_I,
        #            sample_name_abbreviations_I=sample_name_abbreviations_I,
        #            sample_name_shorts_I=sample_name_shorts_I,
        #            component_names_I=component_names_I,
        #            component_group_names_I=component_group_names_I,
        #            time_points_I=time_points_I,);
        #        data_listDict = self._extract_averagesData(data_tmp);
        #    elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
        #        data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
        #            analysis_id_I,
        #            cu,
        #            experiment_ids_I=experiment_ids_I,
        #            sample_name_abbreviations_I=sample_name_abbreviations_I,
        #            sample_name_shorts_I=sample_name_shorts_I,
        #            component_names_I=component_names_I,
        #            component_group_names_I=component_group_names_I,
        #            time_points_I=time_points_I,);
        #        data_listDict = self._extract_averagesData(data_tmp);
        #    else:
        #        print('query instance does not have the required method.');


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

            # define constants for convenience
            sample_name_shorts = calculateinterface.data_train['row_labels']['sample_name_short'].ravel()
            sample_name_shorts_n = len(sample_name_shorts)
            response = calculateinterface.data_train['response'].ravel();
            response_unique = data_listDict.get_uniqueValues_list(response);
            response_unique_n = len(response_unique);
            component_names = calculateinterface.data['column_labels']['component_name'].ravel();
            component_names_n = len(component_names);
            component_group_names = calculateinterface.data['column_labels']['component_group_name'].ravel();
            ncomp = None;

            #TODO: if 'R' in methods:

            r_calc.clear_workspace();
            # add the data to the R workspace:
            dims = calculateinterface.data_train['data'].shape;
            r_calc.make_matrixFromList(
                calculateinterface.data_train['data'].ravel(),
                dims[0],
                dims[1],
                'x.matrix');
            levels = data_O_listDict.convert_list2Levels(response)
            r_calc.make_vectorFromList(levels,'y.vector');
            r_calc.make_factorsFromList(response,'factors_f');
            r_calc.make_dummyMatrixFromFactors('factors_f','dummy');
            
            #iterate through the different models:
            #ASSUMPTION: the actual calculation model is assumed to be the last model in the pipeline
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
                elif model == 'splsda_mixOmics':
                    r_calc.calculate_splsda_mixOmics(
                        spls_O='result_O',
                        x='x.matrix',
                        y='y.vector',
                        ncomp=parameters[i]["ncomp"],
                        );
                elif model == 'oplsda':
                    # call the method
                    pass;
                elif model == 'plsda':
                    # check/correct ncomp/segments
                    ncomp = self._check_ncomp(response_unique,parameters[i]['ncomp'])
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
                    pass;
                elif model == 'robustPca': #CV not supported
                    # check/correct ncomp/segments
                    ncomp = parameters[i]['ncomp']
                    # call the hyper parmeter CV method
                    r_calc.princomp_pca(
                        'x.matrix',
                        'result_O',
                        robust_I=parameters[i]['robust'],
                        na_action_I=parameters[i]['na_action'],
                        cor_I=parameters[i]['cor'],
                        scores_I=parameters[i]['scores'],
                        covmat_I=parameters[i]['covmat'],
                        center_I=parameters[i]['center'],
                        scale_I=parameters[i]['scale']
                        )
                elif model == 'pca':
                    # check/correct ncomp/segments
                    ncomp = parameters[i]['ncomp'] #no need to correct the # of components
                    # call the hyper parmeter CV method
                    r_calc.pcaMethods_pca(
                        'x.matrix',
                        'result_O',
                        pca_method_I=parameters[i]['method'],
                        ncomps=ncomp,
                        imputeMissingValues=parameters[i]['imputeMissingValues'],
                        #prep arguments
                        center=parameters[i]['center'],
                        scale=parameters[i]['scale'],
                        #Q2 arguments
                        cv=parameters[i]['cv'],
                        segments=parameters[i]['segments'],
                        nruncv= parameters[i]['nruncv'], 
                        type = parameters[i]['type'], 
                        )
                else:
                    print('model not recognized.');
            # score the model on the test data
            
            # extract out loadings response information
            for row in loadings_response_methods_I:
                if row['metric_method'] == 'loadings_response':
                    loadings_y = r_calc.extract_mvr_Yloadings('result_O');
                    response_value = loadings_y.reshape(-1);
                    assert(len(response_value)==ncomp*response_unique_n);
                    axis = [c+1 for c in range(ncomp)]*response_unique_n;
                    response_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in response_unique]).reshape(-1);
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'metric_value':response_value,
                         'axis':axis});
                #TODO: this belongs in a seperate database table...
                #elif row['impfeat_response_method'] == 'correlations_response':
                #    cor_y = r_calc.calculate_mvr_correlationResponse(
                #        'result_O',
                #        'correlation_f',
                #        comps='1:'+str(ncomp), 
                #        );
                #    response_value = cor_y.reshape(-1);
                #    assert(len(response_value)==component_names_n*response_unique_n);
                #    response_name = [r for r in response_unique]*component_names_n;
                #    component_name = np.array([np.full(response_unique_n,r,dtype=np.dtype((str, 500))) for r in component_names]).reshape(-1);
                #    component_group_name = np.array([np.full(response_unique_n,r,dtype=np.dtype((str, 500))) for r in component_group_names]).reshape(-1);
                #    data_O_listDict.set_dictList(
                #        {'response_name':response_name,
                #         'metric_value':response_value,
                #         'component_name':component_name,
                #         'component_group_name':component_group_name});
                data_O_listDict.convert_dictList2DataFrame();
                # add in additional rows to the output data object
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                data_O_listDict.add_column2DataFrame('metric_method',row['metric_method']);
                data_O_listDict.add_column2DataFrame('metric_options',row['metric_options']);
                data_O_listDict.add_column2DataFrame('metric_statistics',None);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_loadingsResponse_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();

            # extract out scores information
            for row in scores_methods_I:
                if row['metric_method'] == 'scores' and model in ['pca','robustPca']:
                    scores_x = r_calc.extract_pcaMethods_scores('result_O');
                    response_value = scores_x.reshape(-1);
                    assert(len(response_value)==ncomp*sample_name_shorts_n);
                    axis = [c+1 for c in range(ncomp)]*sample_name_shorts_n;
                    response_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in response]).reshape(-1);
                    sample_name_short = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in sample_name_shorts]).reshape(-1);
                    #response_value = [];
                    #axis = []
                    #for r in range(scores_x.shape[0]):
                    #    for c in range(scores_x.shape[1]):
                    #        axis.append(c+1);
                    #        response_value.append(scores_x[r,c])
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'sample_name_short':sample_name_short,
                         'metric_value':response_value,
                         'axis':axis});
                elif row['metric_method'] == 'scores':
                    scores_x = r_calc.extract_mvr_scores('result_O');
                    response_value = scores_x.reshape(-1);
                    assert(len(response_value)==ncomp*sample_name_shorts_n);
                    axis = [c+1 for c in range(ncomp)]*sample_name_shorts_n;
                    response_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in response]).reshape(-1);
                    sample_name_short = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in sample_name_shorts]).reshape(-1);
                    #response_value = [];
                    #axis = []
                    #for r in range(scores_x.shape[0]):
                    #    for c in range(scores_x.shape[1]):
                    #        axis.append(c+1);
                    #        response_value.append(scores_x[r,c])
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'sample_name_short':sample_name_short,
                         'metric_value':response_value,
                         'axis':axis});
                elif row['metric_method'] == 'scores_response':
                    scores_y = r_calc.extract_mvr_Yscores('result_O');
                    response_value = scores_y.reshape(-1);
                    assert(len(response_value)==ncomp*sample_name_shorts_n);
                    axis = [c+1 for c in range(ncomp)]*sample_name_shorts_n;
                    response_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in response]).reshape(-1);
                    sample_name_short = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in sample_name_shorts]).reshape(-1);
                    #response_value = [];
                    #axis = []
                    #for r in range(scores_y.shape[0]):
                    #    for c in range(scores_y.shape[1]):
                    #        axis.append(c+1);
                    #        response_value.append(scores_y[r,c])
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'sample_name_short':sample_name_short,
                         'metric_value':response_value,
                         'axis':axis});
                data_O_listDict.convert_dictList2DataFrame();
                # add in additional rows to the output data object
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                data_O_listDict.add_column2DataFrame('metric_method',row['metric_method']);
                data_O_listDict.add_column2DataFrame('metric_options',row['metric_options']);
                data_O_listDict.add_column2DataFrame('metric_statistics',None);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_scores_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();

            # extract out axis information
            for row in axis_metric_methods_I:
                if row['metric_method']=='var_proportional' and model in ['pca','robustPca']:
                    var_proportion,var_cumulative = r_calc.calculate_pcaMethods_explainedVariance('result_O');
                    response_value = var_proportion.reshape(-1)
                    assert(len(response_value)==ncomp);
                    axis = [c+1 for c in range(ncomp)];
                    data_O_listDict.set_dictList(
                        {
                         'metric_value':response_value,
                         'axis':axis});
                elif row['metric_method']=='var_cumulative' and model in ['pca','robustPca']:
                    var_proportion,var_cumulative = r_calc.calculate_pcaMethods_explainedVariance('result_O');
                    response_value = var_cumulative.reshape(-1)
                    assert(len(response_value)==ncomp);
                    axis = [c+1 for c in range(ncomp)];
                    data_O_listDict.set_dictList(
                        {
                         'metric_value':response_value,
                         'axis':axis});
                elif row['metric_method']=='var_proportional':
                    var_proportion,var_cumulative = r_calc.calculate_mvr_explainedVariance('result_O');
                    var_proportion,var_cumulative = r_calc.calculate_pcaMethods_explainedVariance('result_O');
                    response_value = var_proportion.reshape(-1)
                    assert(len(response_value)==ncomp);
                    axis = [c+1 for c in range(ncomp)];
                    data_O_listDict.set_dictList(
                        {
                         'metric_value':response_value,
                         'axis':axis});
                elif row['metric_method']=='var_cumulative':
                    var_proportion,var_cumulative = r_calc.calculate_mvr_explainedVariance('result_O');
                    response_value = var_cumulative.reshape(-1)
                    assert(len(response_value)==ncomp);
                    axis = [c+1 for c in range(ncomp)];
                    data_O_listDict.set_dictList(
                        {
                         'metric_value':response_value,
                         'axis':axis});
                data_O_listDict.convert_dictList2DataFrame();
                # add in additional rows to the output data object
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                data_O_listDict.add_column2DataFrame('metric_method',row['metric_method']);
                data_O_listDict.add_column2DataFrame('metric_options',row['metric_options']);
                data_O_listDict.add_column2DataFrame('metric_statistics',None);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_axis_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();
                
            # extract out loadings information
            for row in loadings_methods_I:
                if row['metric_method'] == 'loadings' and model in ['pca','robustPca']:
                    loadings_x = r_calc.extract_pcaMethods_loadings('result_O');
                    impfeat_value = loadings_x.reshape(-1);
                    assert(len(impfeat_value)==ncomp*component_names_n);
                    axis = [c+1 for c in range(ncomp)]*component_names_n;
                    component_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_names]).reshape(-1);
                    component_group_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_group_names]).reshape(-1);
                    data_O_listDict.set_dictList(
                        {
                         'component_name':component_name,
                         'component_group_name':component_group_name,
                         'metric_value':impfeat_value,
                         'axis':axis});
                #elif row['metric_method'] == 'correlations' and model in ['pca','robustPca']:
                #    cor_x = r_calc.calculate_pcaMethods_correlation(
                #        'result_O',
                #        'correlation_m',
                #        comps='1:'+str(ncomp), 
                #        );
                #    impfeat_value = cor_x.reshape(-1);
                #    assert(len(impfeat_value)==ncomp*component_names_n);
                #    axis = [c+1 for c in range(ncomp)]*component_names_n;
                #    component_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_names]).reshape(-1);
                #    component_group_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_group_names]).reshape(-1);
                #    data_O_listDict.set_dictList(
                #        {
                #         'component_name':component_name,
                #         'component_group_name':component_group_name,
                #         'metric_value':impfeat_value,
                #         'axis':axis});
                elif row['metric_method'] == 'loadings':
                    loadings_x = r_calc.extract_mvr_loadings('result_O');
                    impfeat_value = loadings_x.reshape(-1);
                    assert(len(impfeat_value)==ncomp*component_names_n);
                    axis = [c+1 for c in range(ncomp)]*component_names_n;
                    component_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_names]).reshape(-1);
                    component_group_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_group_names]).reshape(-1);
                    #response_name=[];
                    #impfeat_value = [];
                    #axis = [];
                    #for r in range(loadings_x.shape[0]):
                    #    for c in range(loadings_x.shape[1]): #comp
                    #        axis.append(c+1);
                    #        impfeat_value.append(loadings_x[r,c])
                    #        response_name.append('all');
                    data_O_listDict.set_dictList(
                        {
                         'component_name':component_name,
                         'component_group_name':component_group_name,
                         'metric_value':impfeat_value,
                         'axis':axis});
                elif row['metric_method']=='correlations':
                    cor_x = r_calc.calculate_mvr_correlation(
                        'result_O',
                        'correlation_m',
                        comps='1:'+str(ncomp), 
                        );
                    impfeat_value = cor_x.reshape(-1);
                    assert(len(impfeat_value)==ncomp*component_names_n);
                    axis = [c+1 for c in range(ncomp)]*component_names_n;
                    component_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_names]).reshape(-1);
                    component_group_name = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_group_names]).reshape(-1);
                    #response_name=[];
                    #impfeat_value = [];
                    #axis = [];
                    #for r in range(cor_x.shape[0]):
                    #    for c in range(cor_x.shape[1]): #comp
                    #        axis.append(c+1);
                    #        response_value.append(cor_x[r,c])
                    #        response_name.append('all');
                    data_O_listDict.set_dictList(
                        {
                         'component_name':component_name,
                         'component_group_name':component_group_name,
                         'metric_value':impfeat_value,
                         'axis':axis});
                data_O_listDict.convert_dictList2DataFrame();
                # add in additional rows to the output data object
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                data_O_listDict.add_column2DataFrame('metric_method',row['metric_method']);
                data_O_listDict.add_column2DataFrame('metric_options',row['metric_options']);
                data_O_listDict.add_column2DataFrame('metric_statistics',None);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_loadings_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();

            # extract out feature information
            for row in impfeat_methods_I:
                if row['impfeat_method'] == 'coefficients':
                    coefficients,coefficients_comps_reduced,coefficients_reduced=r_calc.extract_mvr_coefficients('result_O');
                    if coefficients is None: continue;     
                    # flatten the coefficients
                    #impfeat_value1 = coefficients.reshape(-1);
                    #assert(len(impfeat_value1)==component_names_n*(response_unique_n)*ncomp);
                    #axis1 = [c+1 for c in range(ncomp)]*component_names_n;
                    #component_name1 = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in response_unique]).reshape(-1)*component_names_n;
                    #response_name1 = np.full(len(impfeat_value),r,dtype=np.dtype((str, 500)));
                    #component_name1 = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_names]).reshape(-1);
                    #component_group_name1 = np.array([np.full(ncomp,r,dtype=np.dtype((str, 500))) for r in component_group_names]).reshape(-1);
                    # flatten the coefficients_comps    
                    impfeat_value2 = coefficients.reshape(-1);
                    assert(len(impfeat_value2)==component_names_n*response_unique_n);
                    response_name2 = [r for r in response_unique]*component_names_n;
                    component_name2 = np.array([np.full(response_unique_n,r,dtype=np.dtype((str, 500))) for r in component_names]).reshape(-1);
                    component_group_name2 = np.array([np.full(response_unique_n,r,dtype=np.dtype((str, 500))) for r in component_group_names]).reshape(-1);
                    # flatten the coefficients_reduced     
                    impfeat_value3 = coefficients_reduced.reshape(-1);
                    assert(len(impfeat_value3)==component_names_n);
                    response_name3 = np.full(component_names_n,'all',dtype=np.dtype((str, 500)));
                    component_name3 = component_names;
                    component_group_name3 = component_group_names;
                    #response_name=[];
                    #impfeat_value = [];
                    #axis = [];
                    #for r in range(coefficients.shape[0]):
                    #    for c in range(coefficients.shape[1]):
                    #        for z in range(coefficients.shape[2]):
                    #            response_name.append(response_unique[c]);
                    #            impfeat_value.append(coefficients[r,c,z]);
                    #            axis.append(z);
                    #for r in range(coefficients_comps_reduced.shape[0]):
                    #    for c in range(coefficients_comps_reduced.shape[1]):
                    #        response_name.append(response_unique[c]);
                    #        impfeat_value.append(coefficients_comps_reduced[r,c]);
                    #        axis.append(-1);
                    #for r in range(coefficients_comps_reduced.shape[0]):
                    #    response_name.append('all');
                    #    impfeat_value.append(coefficients_reduced[r]);
                    #    axis.append(-1);
                    impfeat_value = np.concatenate((impfeat_value2,impfeat_value3), axis=0);
                    response_name = np.concatenate((response_name2,response_name3), axis=0);
                    component_name = np.concatenate((component_name2,component_name3), axis=0);
                    component_group_name = np.concatenate((component_group_name2,component_group_name3), axis=0);
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'component_name':component_name,
                         'component_group_name':component_group_name,
                         'impfeat_value':impfeat_value,
                         });
                elif row['impfeat_method'] == 'VIP':
                    vip,vip_reduced = r_calc.extract_mvr_vip('result_O');
                    if vip is None: continue;
                    #vip
                    impfeat_value1 = vip.reshape(-1);
                    assert(len(impfeat_value1)==component_names_n*response_unique_n);
                    response_name1 = np.array([np.full(component_names_n,r,dtype=np.dtype((str, 500))) for r in response_unique]).reshape(-1);
                    component_name1 = [r for r in component_names]*response_unique_n;
                    component_group_name1 = [r for r in component_group_names]*response_unique_n;
                    #vip reduced
                    impfeat_value2 = vip_reduced.reshape(-1);
                    assert(len(impfeat_value2)==component_names_n);
                    response_name2 = np.full(component_names_n,'all',dtype=np.dtype((str, 500)));
                    component_name2 = component_names;
                    component_group_name2 = component_group_names;
                    ##check
                    #response_name=[];
                    #impfeat_value = [];
                    #axis = [];
                    #for r in range(vip.shape[0]):
                    #    for c in range(vip.shape[1]):
                    #        impfeat_value.append(vip[r,c]);
                    #        response_name.append(response_unique[r])
                    #        axis.append(-1);
                    #for c in range(vip.shape[1]):
                    #    impfeat_value.append(vip_reduced[c]);
                    #    response_name.append('all');
                    #    axis.append(-1);
                    impfeat_value = np.concatenate((impfeat_value1,impfeat_value2), axis=0);
                    response_name = np.concatenate((response_name1,response_name2), axis=0);
                    component_name = np.concatenate((component_name1,component_name2), axis=0);
                    component_group_name = np.concatenate((component_group_name1,component_group_name2), axis=0);
                    #convert impfeat_statistics to the proper data structure
                    data_O_listDict.set_dictList(
                        {'response_name':response_name,
                         'component_name':component_name,
                         'component_group_name':component_group_name,
                         'impfeat_value':impfeat_value,
                         });
                data_O_listDict.convert_dictList2DataFrame();
                # add in additional rows to the output data object
                data_O_listDict.add_column2DataFrame('analysis_id',analysis_id_I);
                data_O_listDict.add_column2DataFrame('calculated_concentration_units',cu);
                data_O_listDict.add_column2DataFrame('test_size',test_size_I);
                data_O_listDict.add_column2DataFrame('used_',True);
                data_O_listDict.add_column2DataFrame('comment_',None);
                data_O_listDict.add_column2DataFrame('pipeline_id',pipeline_id_I);
                data_O_listDict.add_column2DataFrame('impfeat_method',row['impfeat_method']);
                data_O_listDict.add_column2DataFrame('impfeat_options',row['impfeat_options']);
                data_O_listDict.add_column2DataFrame('impfeat_statistics',None);
                # add data to the database
                data_O_listDict.convert_dataFrame2ListDict();
                data_impfeat_O.extend(data_O_listDict.get_listDict());
                data_O_listDict.clear_allData();

            #extract out sample information

            # reset calculate_interface
            calculateinterface.clear_data();
        # add data to the database
        self.add_rows_table('data_stage02_quantification_spls_impfeat',data_impfeat_O);
        self.add_rows_table('data_stage02_quantification_spls_scores',data_scores_O);
        self.add_rows_table('data_stage02_quantification_spls_loadings',data_loadings_O);
        self.add_rows_table('data_stage02_quantification_spls_loadingsResponse',data_loadingsResponse_O);
        self.add_rows_table('data_stage02_quantification_spls_axis',data_axis_O);

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
                where_clause_I = None,
                query_object_I = 'stage02_quantification_dataPreProcessing_replicates_query',
                query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates',
            
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
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance_descStats = query_object(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();
        
        # instantiate data lists
        data_O=[];

        # get the model pipeline:
        models,methods,parameters = self.get_modelsAndMethodsAndParameters_pipelineID_dataStage02QuantificationSPLSPipeline(pipeline_id_I);
        
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
            cu = row['calculated_concentration_units']
            if not cu in data_analysis.keys(): data_analysis[cu]=[];
            data_analysis[cu].append(row);
        del data_analysis['_del_'];

        #apply the analysis to each group
        for cu in calculated_concentration_units:
            print('generating a heatmap for concentration_units ' + cu);
            # get the data
            data = data_analysis[cu];
            data_listDict = listDict(listDict_I=data);
            data_listDict.convert_listDict2DataFrame();

        ## get concentration units
        #if calculated_concentration_units_I:
        #    calculated_concentration_units = calculated_concentration_units_I;
        #else:
        #    calculated_concentration_units = [];
        #    if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates'):
        #        calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        #    elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
        #        calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        #    elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
        #        calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
        #    else:
        #        print('query instance does not have the required method.');
        #for cu in calculated_concentration_units:
        #    #print('calculating spls for calculated_concentration_units ' + cu);
        #    if hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates'):
        #        data_listDict = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
        #            analysis_id_I,
        #            cu,
        #            experiment_ids_I=experiment_ids_I,
        #            sample_name_abbreviations_I=sample_name_abbreviations_I,
        #            sample_name_shorts_I=sample_name_shorts_I,
        #            component_names_I=component_names_I,
        #            component_group_names_I=component_group_names_I,
        #            time_points_I=time_points_I,);
        #    elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
        #        data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
        #            analysis_id_I,
        #            cu,
        #            experiment_ids_I=experiment_ids_I,
        #            sample_name_abbreviations_I=sample_name_abbreviations_I,
        #            sample_name_shorts_I=sample_name_shorts_I,
        #            component_names_I=component_names_I,
        #            component_group_names_I=component_group_names_I,
        #            time_points_I=time_points_I,);
        #        data_listDict = self._extract_averagesData(data_tmp);
        #    elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
        #        data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(
        #            analysis_id_I,
        #            cu,
        #            experiment_ids_I=experiment_ids_I,
        #            sample_name_abbreviations_I=sample_name_abbreviations_I,
        #            sample_name_shorts_I=sample_name_shorts_I,
        #            component_names_I=component_names_I,
        #            component_group_names_I=component_group_names_I,
        #            time_points_I=time_points_I,);
        #        data_listDict = self._extract_averagesData(data_tmp);
        #    else:
        #        print('query instance does not have the required method.');

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
                    ncomp = self._check_ncomp(data_listDict.get_uniqueValues_list(response),parameters[i]['ncomp']) #PLSDA only
                    segments = self._check_folds(response,crossval_options_I['segments'])
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
                elif model == 'robustPca': #CV not supported
                    # check/correct ncomp/segments
                    ncomp = parameters[i]['ncomp']
                    segments = self._check_folds(response,crossval_options_I['segments'])
                    # call the hyper parmeter CV method
                    r_calc.princomp_pca(
                        'x.matrix',
                        'cvresult_O',
                        robust_I=False,
                        na_action_I=parameters[i]['na_action'],
                        cor_I=parameters[i]['cor'],
                        scores_I=parameters[i]['scores'],
                        covmat_I=parameters[i]['covmat'],
                        center_I=parameters[i]['center'],
                        scale_I=parameters[i]['scale']
                        )
                    # extract the CV information
                    pipeline_parameters = [];
                    metric_scores = [];
                    metric_methods = [];
                elif model == 'pca':
                    # check/correct ncomp/segments
                    ncomp = parameters[i]['ncomp'] #no need to correct the # of components
                    segments = self._check_folds(response,crossval_options_I['segments'])
                    # call the hyper parmeter CV method
                    r_calc.pcaMethods_pca(
                        'x.matrix',
                        'cvresult_O',
                        pca_method_I=parameters[i]['method'],
                        ncomps=ncomp,
                        imputeMissingValues=parameters[i]['imputeMissingValues'],
                        #prep arguments
                        center=parameters[i]['center'],
                        scale=parameters[i]['scale'],
                        #Q2 arguments
                        cv=crossval_options_I['cv'], #change to parameters elsewhere
                        segments=segments,
                        nruncv= crossval_options_I['nruncv'], #change to parameters elsewhere
                        type = crossval_options_I['type'], #change to parameters elsewhere
                        )
                    # extract the CV information
                    r2_reduced=r_calc.extract_pcaMethods_R2cum('cvresult_O')
                    q2_reduced=r_calc.extract_pcaMethods_cvstat('cvresult_O');
                    rmsep_reduced = r_calc.pcaMethod_kEstimate(
                            'x.matrix',
                            'result_errors',
                            pca_method_I=parameters[i]['method'],
                            ncomps=ncomp,
                            em="nrmsep",
                            segments=segments,
                            nruncv=crossval_options_I['nruncv']);
                    msep_reduced = np.square(rmsep_reduced);
                    pipeline_parameters = [];
                    metric_scores = [];
                    metric_methods = [];
                    for i in range(len(r2_reduced)): 
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

    def _check_ncomp(self,
        response_unique_I,
        ncomp_I):
        '''check that the number of principal components is not greater than the number of unique responses
        INPUT:
        response_unique_I
        ncomp_I
        OUTPUT:
        ncomp_O
        '''
        ncomp_O = ncomp_I;
        if len(response_unique_I)<ncomp_O:
            ncomp_O = len(response_unique_I);
        return ncomp_O;

    def _check_folds(self,
        samples_I,
        nfolds_I):
        '''check that the number of folds for cross validation is not greater than the number of unique samples
        INPUT:
        samples_I
        nfolds_I
        OUTPUT:
        nfolds_O
        '''
        nfolds_O = nfolds_I;
        if len(samples_I)<nfolds_O:
            nfolds_O = len(samples_I);
            nfolds_O = int(0.75*len(samples_I));
        return nfolds_O;