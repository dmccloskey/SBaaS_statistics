
from .stage02_quantification_pairWiseTable_io import stage02_quantification_pairWiseTable_io
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query

class stage02_quantification_pairWiseTable_execute(stage02_quantification_pairWiseTable_io):
    def execute_pairwiseTableAverages(self,analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
            query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats',
            redundancy_I=True,
            value_I = 'mean',):
        '''
        execute pairwiseTable
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'

        '''

        print('execute_pairwiseTable...')

        #query the data:
        self.execute_pairwiseTableAverages_queryData(
            analysis_id_I,
            calculated_concentration_units_I=calculated_concentration_units_I,
            component_names_I=component_names_I,
            component_group_names_I=component_group_names_I,
            sample_name_abbreviations_I=sample_name_abbreviations_I,
            time_points_I=time_points_I,
            experiment_ids_I=experiment_ids_I,
            test_descriptions_I=test_descriptions_I,
            pvalue_corrected_descriptions_I=pvalue_corrected_descriptions_I,
            where_clause_I=where_clause_I,
            query_object_descStats_I = query_object_descStats_I,
            query_func_descStats_I = query_func_descStats_I,
            );
        
        #transform the data
        self.execute_pairwiseTableAverages_transformData(
            analysis_id_I,
            redundancy_I=redundancy_I,
            value_I = value_I,
            );

        # add data to database
        self.execute_pairwiseTableAverages_storeData(
            data_O=data_pairwise_O,
            table_O = 'data_stage02_quantification_pairWiseTable',
            )

    def execute_pairwiseTableAverages_queryData(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
            query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats',
            ):
        ''' '''
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        #query the data:
        data_listDict = [];
        if hasattr(query_instance_descStats, query_func_descStats_I):
            query_func_descStats = getattr(query_instance_descStats, query_func_descStats_I);
            data_listDict = query_func_descStats(analysis_id_I,
                calculated_concentration_units_I=calculated_concentration_units_I,
                component_names_I=component_names_I,
                component_group_names_I=component_group_names_I,
                sample_name_abbreviations_I=sample_name_abbreviations_I,
                time_points_I=time_points_I,
                experiment_ids_I=experiment_ids_I,
                test_descriptions_I=test_descriptions_I,
                pvalue_corrected_descriptions_I=pvalue_corrected_descriptions_I,
                where_clause_I=where_clause_I,
                );
        else:
            print('query instance does not have the required method.');

        self.add_data(data_listDict);
    def execute_pairwiseTableAverages_transformDataCrossUnits(self,
            analysis_id_I,
            redundancy_I=True,
            value_I = 'mean',
            includeAll_calculatedConcentrationUnits_I=True):
        '''
        INPUT:
        analysis_id_I
        data_I = listDict
        ...
        OUTPUT:
        data_pairwise_O = listDict
        '''
        data_I=self.get_data();

        #reorganize into analysis groups:
        sample_name_abbreviations = list(set([c['sample_name_abbreviation'] for c in data_I]));
        sample_name_abbreviations.sort();
        data_analysis = {'_del_':[]};
        for row in data_listDict:
            sna = row['sample_name_abbreviation']
            if not sna in data_analysis.keys(): data_analysis[sna]=[];
            data_analysis[sna].append(row);

        del data_analysis['_del_'];

        data_pairwise_O = [];

        #apply the analysis to each unique group
        
        for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                    
            data_O=[];
            #pass 1: calculate the pairwise correlations
            if redundancy_I: list_2 = sample_name_abbreviations;
            else: list_2 = sample_name_abbreviations[sna_1_cnt+1:];
            for cnt,sna_2 in enumerate(list_2):
                if redundancy_I: sna_2_cnt = cnt;
                else: sna_2_cnt = sna_1_cnt+cnt+1;
                if sna_1 != sna_2:
                        
                    data_1,data_2 = [],[];
                    data_1 = data_analysis[sna_1];
                    data_2 = data_analysis[sna_2];
                    
                    #check the data
                    assert(len(data_1)==len(data_2));
                    cn_1 = list(set(d['component_name'] for d in data_1))
                    cn_1.sort();
                    cn_2 = list(set(d['component_name'] for d in data_2))
                    cn_2.sort();
                    assert(cn_1==cn_2);
                    #ensure the data is sorted
                    data_1 = sorted(data_1,key=lambda x: x['component_name'])
                    data_2 = sorted(data_2,key=lambda x: x['component_name'])

                    # record the data
                    for d_1_cnt,d_1 in enumerate(data_1):
                        assert(d_1['component_name']==data_2[d_1_cnt]['component_name']);
                        tmp = {'analysis_id':analysis_id_I,
                            'component_group_name':d_1['component_group_name'],
                            'component_name':d_1['component_name'],
                            'value_name':value_I,
                            'sample_name_abbreviation_1':sna_1,
                            'sample_name_abbreviation_2':sna_2,
                            'value_1':d_1[value_I],
                            'value_2':data_2[d_1_cnt][value_I],
                            'calculated_concentration_units_1':d_1['calculated_concentration_units'],
                            'calculated_concentration_units_2':data_2[d_1_cnt]['calculated_concentration_units'],
                            'used_':True,
                            'comment_':None};
                        data_pairwise_O.append(tmp)
        self.set_data(data_pairwise_O);
    def execute_pairwiseTableAverages_transformData(self,
            analysis_id_I,
            redundancy_I=True,
            value_I = 'mean',):
        '''
        INPUT:
        analysis_id_I
        data_I = listDict
        ...
        OUTPUT:
        data_pairwise_O = listDict
        '''
        data_I=self.get_data();

        #reorganize into analysis groups:
        calculated_concentration_units = list(set([c['calculated_concentration_units'] for c in data_I]));
        calculated_concentration_units.sort();
        sample_name_abbreviations = {k:[] for k in calculated_concentration_units};
        data_analysis = {'_del_':{'_del_':[]}};
        for row in data_listDict:
            cu = row['calculated_concentration_units']
            sna = row['sample_name_abbreviation']
            if not cu in data_analysis.keys(): data_analysis[cu]={};
            if not sna in data_analysis[cu].keys(): data_analysis[cu][sna]=[];
            if not sna in sample_name_abbreviations[cu]: sample_name_abbreviations[cu].append(sna);
            data_analysis[cu][sna].append(row);

        del data_analysis['_del_'];

        data_pairwise_O = [];

        #apply the analysis to each unique group
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseTable for concentration_units ' + cu);
            for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations):
                    
                data_O=[];
                #pass 1: calculate the pairwise correlations
                if redundancy_I: list_2 = sample_name_abbreviations[cu];
                else: list_2 = sample_name_abbreviations[cu][sna_1_cnt+1:];
                for cnt,sna_2 in enumerate(list_2):
                    if redundancy_I: sna_2_cnt = cnt;
                    else: sna_2_cnt = sna_1_cnt+cnt+1;
                    if sna_1 != sna_2:
                        
                        data_1,data_2 = [],[];
                        data_1 = data_analysis[cu][sna_1];
                        data_2 = data_analysis[cu][sna_2];

                        if len(data_1)!=len(data_2):
                            print('the number of components in sn_1 and sn_2 are not equal.');

                        # record the data
                        for d_1_cnt,d_1 in enumerate(data_1):
                            assert(d_1['component_name']==data_2[d_1_cnt]['component_name']);
                            tmp = {'analysis_id':analysis_id_I,
                                'component_group_name':d_1['component_group_name'],
                                'component_name':d_1['component_name'],
                                'value_name':value_I,
                                'sample_name_abbreviation_1':sna_1,
                                'sample_name_abbreviation_2':sna_2,
                                'value_1':d_1[value_I],
                                'value_2':data_2[d_1_cnt][value_I],
                                'calculated_concentration_units':cu,
                                'used_':True,
                                'comment_':None};
                            data_pairwise_O.append(tmp)
        
        self.set_data(data_pairwise_O);
    def execute_pairwiseTableAverages_storeData(self,
        table_O = 'data_stage02_quantification_pairWiseTable',
        query_object_O='self',
        query_func_O='add_rows_table',
        verbose_I = False,
        raise_I = False,
        safeInsert_I=False,):
        ''' '''

        data_O=self.get_data();
        #save the data
        if query_func_O == 'add_rows_table':
            self.add_rows_table(table_O,data_O,
                verbose_I = verbose_I,
                raise_I = raise_I,
                safeInsert_I=safeInsert_I,);
    def execute_pairwiseTableAverages_resetData(self,
            tables_I = [],
            analysis_id_I = None,
            warn_I=True,
            query_object_I='self',
            query_func_I='reset_dataStage02_quantification_pairWiseTable'):
        ''' '''
        ## intantiate the query object:
        #query_objects = {'self':self,
        #                };
        #if query_object_O in query_objects.keys():
        #    query_object = query_objects[query_object_O];
        #    query_instance = query_object_descStats(self.session,self.engine,self.settings);
        #    query_instance.initialize_supportedTables();
            
        #if hasattr(query_instance, query_func_O):
        #    query_func = getattr(query_instance, query_func_O);
        #    data_listDict = query_func(table_O,data_O
        #        );
        #else:
        #    print('query instance does not have the required method.');
        
        #reset the data
        if query_func_I == 'reset_dataStage02_quantification_pairWiseTable':
            self.reset_dataStage02_quantification_pairWiseTable(
                tables_I = tables_I,
                analysis_id_I = analysis_id_I,
                warn_I=warn_I,
                );

    def execute_pairwiseTableReplicates(self,analysis_id_I,
            time_points_I=[],
            experiment_ids_I=[],
            component_group_names_I=[],
            component_names_I=[],
            sample_name_abbreviations_I=[],
            sample_name_shorts_I=[],
            calculated_concentration_units_I=[],
            where_clause_I = None,
            redundancy_I=True,
            query_object_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates',):
        '''execute pairwiseTable
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        '''

        print('execute_pairwiseTableReplicates...')
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance = query_object(self.session,self.engine,self.settings);
            query_instance.initialize_supportedTables();

        data_pairwise_O = [];

        #query the data:
        data_listDict = [];
        if hasattr(query_instance, query_func_I):
            query_func = getattr(query_instance, query_func_I);
            try:
                data_listDict = query_func(analysis_id_I,
                    calculated_concentration_units_I=calculated_concentration_units_I,
                    component_names_I=component_names_I,
                    component_group_names_I=component_group_names_I,
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
        sample_name_shorts = list(set([c['sample_name_short'] for c in data_listDict]));
        sample_name_shorts.sort();
        data_analysis = {'_del_':{'_del_':[]}};
        for row in data_listDict:
            cu = row['calculated_concentration_units']
            sns = row['sample_name_short']
            if not cu in data_analysis.keys(): data_analysis[cu]={};
            if not sns in data_analysis[cu].keys(): data_analysis[cu][sns]=[];
            data_analysis[cu][sns].append(row);
        del data_analysis['_del_'];

        # apply the analysis to each unique group
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseTable for concentration_units ' + cu);
            for sn_1_cnt,sn_1 in enumerate(sample_name_shorts):
                if redundancy_I: list_2 = sample_name_shorts;
                else: list_2 = sample_name_shorts[sn_1_cnt+1:];
                for cnt,sn_2 in enumerate(list_2):
                    if redundancy_I: sn_2_cnt = cnt;
                    else: sn_2_cnt = sn_1_cnt+cnt+1;
                    if sn_1 != sn_2:
                        data_1,data_2 = [],[];
                        data_1 = data_analysis[cu][sn_1];
                        data_2 = data_analysis[cu][sn_2]; 

                        if len(data_1)!=len(data_2):
                            print('the number of components in sn_1 and sn_2 are not equal.');

                        # recorde the data
                        for d_1_cnt,d_1 in enumerate(data_1):
                            assert(d_1['component_name']==data_2[d_1_cnt]['component_name']);
                            tmp = {'analysis_id':analysis_id_I,
                                'sample_name_abbreviation_1':d_1['sample_name_abbreviation'],
                                'sample_name_abbreviation_2':data_2[d_1_cnt]['sample_name_abbreviation'],
                                'sample_name_short_1':sn_1,
                                'sample_name_short_2':sn_2,
                                'component_group_name':d_1['component_group_name'],
                                'component_name':d_1['component_name'],
                                'calculated_concentration_1':d_1['calculated_concentration'],
                                'calculated_concentration_2':data_2[d_1_cnt]['calculated_concentration'],
                                'calculated_concentration_units':d_1['calculated_concentration_units'],
                                'used_':True,
                                'comment_':None};
                            data_pairwise_O.append(tmp);
        # add data to database
        self.add_rows_table('data_stage02_quantification_pairWiseTable_replicates',data_pairwise_O);
    
    def execute_pairwiseTableFeaturesAverages(self,analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            test_descriptions_I=[],
            pvalue_corrected_descriptions_I=[],
            where_clause_I=None,
            query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats',
            redundancy_I=True,
            value_I = 'mean',
            includeAll_calculatedConcentrationUnits_I=False,
            ):
        '''execute pairwiseTable
        INPUT:
        analysis_id_I = string
        concentration_units_I = [] of strings
        component_names_I = [] of strings
        redundancy_I = boolean, default=True
        distance_measure_I = 'spearman' or 'pearson'
        value_I = string, e.g., value from descriptiveStats to use 'mean','median','pvalue',etc.
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        '''

        print('execute_pairwiseTable...')

        #query the data:
        data_listDict = self.execute_pairwiseTableFeaturesAverages_queryData(self,analysis_id_I,
            calculated_concentration_units_I=calculated_concentration_units_I,
            component_names_I=component_names_I,
            component_group_names_I=component_group_names_I,
            sample_name_abbreviations_I=sample_name_abbreviations_I,
            time_points_I=time_points_I,
            experiment_ids_I=experiment_ids_I,
            test_descriptions_I=test_descriptions_I,
            pvalue_corrected_descriptions_I=pvalue_corrected_descriptions_I,
            where_clause_I=where_clause_I,
            query_object_descStats_I = query_object_descStats_I,
            query_func_descStats_I = query_func_descStats_I)
            
        # transform the data
        if includeAll_calculatedConcentrationUnits_I:
            data_pairwise_O = self.execute_pairwiseTableFeaturesAverages_transformDataCrossUnits(
                analysis_id_I,
                data_I=data_listDict,
                redundancy_I = redundancy_I,
                value_I = value_I,
                );
        else:
            data_pairwise_O = self.execute_pairwiseTableFeaturesAverages_transformData(
                analysis_id_I,
                data_I=data_listDict,
                redundancy_I = redundancy_I,
                value_I = value_I,
                );
        
        #save/update the data
        self.execute_pairwiseTableFeaturesAverages_saveData(
            data_O = data_pairwise_O,
            table_O = 'data_stage02_quantification_pairwiseTableFeatures'
            );

    def execute_pairwiseTableFeaturesAverages_transformDataCrossUnits(self,
            analysis_id_I,
            redundancy_I=True,
            value_I = 'mean',
            includeAll_calculatedConcentrationUnits_I=True
            ):
        ''' '''

        data_I = self.get_data();

        #reorganize into analysis groups:
        component_names = list(set([c['component_name'] for c in data_I]));
        component_names.sort();
        data_analysis = {'_del_':{'_del_':[]}};
        for row in data_I:
            cn = row['component_name']
            if not cn in data_analysis.keys(): data_analysis[cn]=[];
            data_analysis[cn].append(row);            
        del data_analysis['_del_'];

        # instantiate the output list
        data_pairwise_O = [];

        #apply the analysis to each unique dimension
        for cn_1_cnt,cn_1 in enumerate(component_names):                    
            data_O=[];
            #pass 1: calculate the pairwise correlations
            if redundancy_I: list_2 = component_names;
            else: list_2 = component_names[cn_1_cnt+1:];
            for cnt,cn_2 in enumerate(list_2):
                if redundancy_I: cn_2_cnt = cnt;
                else: cn_2_cnt = cn_1_cnt+cnt+1;
                    
                data_1,data_2 = [],[];
                data_1 = data_analysis[cn_1];
                data_2 = data_analysis[cn_2];

                #check the data
                assert(len(data_1)==len(data_2));
                sns_1 = list(set(d['sample_name_abbreviation'] for d in data_1))
                sns_1.sort();
                sns_2 = list(set(d['sample_name_abbreviation'] for d in data_2))
                sns_2.sort();
                assert(sns_1==sns_2);
                data_1_sorted = sorted(data_1,key=lambda x: x['sample_name_abbreviation'])
                data_2_sorted = sorted(data_2,key=lambda x: x['sample_name_abbreviation'])

                # record the data
                for d_1_cnt,d_1 in enumerate(data_1_sorted):
                    assert(d_1['sample_name_abbreviation']==data_2_sorted[d_1_cnt]['sample_name_abbreviation']);
                    tmp = {'analysis_id':analysis_id_I,
                    'value_name':value_I,
                    'sample_name_abbreviation':d_1['sample_name_abbreviation'],
                        'value_1':d_1[value_I],
                        'value_2':data_2_sorted[d_1_cnt][value_I],
                    'component_name_1':cn_1,
                    'component_name_2':cn_2,
                    'component_group_name_1':d_1['component_group_name'],
                    'component_group_name_2':data_2_sorted[d_1_cnt]['component_group_name'],
                    'calculated_concentration_units_1':d_1['calculated_concentration_units'],
                    'calculated_concentration_units_2':data_2_sorted[d_1_cnt]['calculated_concentration_units'],
                    'used_':True,
                    'comment_':None};
                    data_pairwise_O.append(tmp)

        self.set_data(data_pairwise_O);
    def execute_pairwiseTableFeaturesAverages_transformData(self,
            analysis_id_I,
            redundancy_I=True,
            value_I = 'mean',
            ):
        ''' '''

        data_I = self.get_data();

        #reorganize into analysis groups:
        calculated_concentration_units = list(set([c['calculated_concentration_units'] for c in data_I]));
        calculated_concentration_units.sort();
        #component_names = list(set([c['component_name'] for c in data_I]));
        #component_names.sort();
        component_names = {k:[] for k in calculated_concentration_units};
        data_analysis = {'_del_':{'_del_':[]}};
        for row in data_I:
            cu = row['calculated_concentration_units']
            cn = row['component_name']
            if not cu in data_analysis.keys(): data_analysis[cu]={};
            if not cn in data_analysis[cu].keys(): data_analysis[cu][cn]=[];
            if not cn in component_names[cu]: component_names[cu].append(cn);
            data_analysis[cu][cn].append(row);            
        del data_analysis['_del_'];

        # instantiate the output list
        data_pairwise_O = [];

        #apply the analysis to each unique dimension
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseTable for concentration_units ' + cu);
            for cn_1_cnt,cn_1 in enumerate(component_names[cu]):                    
                data_O=[];
                #pass 1: calculate the pairwise correlations
                if redundancy_I: list_2 = component_names[cu];
                else: list_2 = component_names[cu][cn_1_cnt+1:];
                for cnt,cn_2 in enumerate(list_2):
                    if redundancy_I: cn_2_cnt = cnt;
                    else: cn_2_cnt = cn_1_cnt+cnt+1;
                    
                    data_1,data_2 = [],[];
                    data_1 = data_analysis[cu][cn_1];
                    data_2 = data_analysis[cu][cn_2]; 

                    if len(data_1)!=len(data_2):
                        print('the number of components in sn_1 and sn_2 are not equal.');
                        
                    # record the data
                    for d_1_cnt,d_1 in enumerate(data_1):
                        assert(d_1['sample_name_abbreviation']==data_2[d_1_cnt]['sample_name_abbreviation']);
                        tmp = {'analysis_id':analysis_id_I,
                        'value_name':value_I,
                        'sample_name_abbreviation':d_1['sample_name_abbreviation'],
                            'value_1':d_1[value_I],
                            'value_2':data_2[d_1_cnt][value_I],
                        'component_name_1':cn_1,
                        'component_name_2':cn_2,
                        'component_group_name_1':d_1['component_group_name'],
                        'component_group_name_2':data_2[d_1_cnt]['component_group_name'],
                        'calculated_concentration_units_1':d_1['calculated_concentration_units'],
                        'calculated_concentration_units_2':data_2[d_1_cnt]['calculated_concentration_units'],
                        'used_':True,
                        'comment_':None};
                        data_pairwise_O.append(tmp)

        self.set_data(data_pairwise_O);
    ##redundant
    #def execute_pairwiseTableFeaturesAverages_queryData(self,
    #        analysis_id_I,
    #        calculated_concentration_units_I=[],
    #        component_names_I=[],
    #        component_group_names_I=[],
    #        sample_name_abbreviations_I=[],
    #        time_points_I=[],
    #        experiment_ids_I=[],
    #        test_descriptions_I=[],
    #        pvalue_corrected_descriptions_I=[],
    #        where_clause_I=None,
    #        query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
    #        query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats',):
    #    ''' '''
    #    # intantiate the query object:
    #    query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
    #                    'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query,};
    #    if query_object_descStats_I in query_objects.keys():
    #        query_object_descStats = query_objects[query_object_descStats_I];
    #        query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
    #        query_instance_descStats.initialize_supportedTables();

    #    #query the data:
    #    data_listDict = [];
    #    if hasattr(query_instance_descStats, query_func_descStats_I):
    #        query_func_descStats = getattr(query_instance_descStats, query_func_descStats_I);
    #        data_listDict = query_func_descStats(analysis_id_I,
    #            calculated_concentration_units_I=calculated_concentration_units_I,
    #            component_names_I=component_names_I,
    #            component_group_names_I=component_group_names_I,
    #            sample_name_abbreviations_I=sample_name_abbreviations_I,
    #            time_points_I=time_points_I,
    #            experiment_ids_I=experiment_ids_I,
    #            test_descriptions_I=test_descriptions_I,
    #            pvalue_corrected_descriptions_I=pvalue_corrected_descriptions_I,
    #            where_clause_I=where_clause_I,
    #            );
    #    else:
    #        print('query instance does not have the required method.');
    #    self.add_data(data_listDict);
    #def execute_pairwiseTableFeaturesAverages_resetData(self,
    #        tables_I = [],
    #        analysis_id_I = None,
    #        warn_I=True,
    #        query_object_I='self',
    #        query_func_I='reset_dataStage02_quantification_pairWiseTable'):
    #    ''' '''
    #    ## intantiate the query object:
    #    #query_objects = {'self':self,
    #    #                };
    #    #if query_object_O in query_objects.keys():
    #    #    query_object = query_objects[query_object_O];
    #    #    query_instance = query_object_descStats(self.session,self.engine,self.settings);
    #    #    query_instance.initialize_supportedTables();
            
    #    #if hasattr(query_instance, query_func_O):
    #    #    query_func = getattr(query_instance, query_func_O);
    #    #    data_listDict = query_func(table_O,data_O
    #    #        );
    #    #else:
    #    #    print('query instance does not have the required method.');
        
    #    #reset the data
    #    if query_func_O == 'reset_dataStage02_quantification_pairWiseTable':
    #        self.reset_dataStage02_quantification_pairWiseTable(
    #            tables_I = tables_I,
    #            analysis_id_I = analysis_id_I,
    #            warn_I=warn_I,
    #            );
    #def execute_pairwiseTableFeaturesAverages_storeData(self,
    #        table_O='data_stage02_quantification_pairwiseTableFeatures',
    #        query_object_O='self',
    #        query_func_O='add_rows_table'):
    #    ''' '''
    #    ## intantiate the query object:
    #    #query_objects = {'self':self,
    #    #                };
    #    #if query_object_O in query_objects.keys():
    #    #    query_object = query_objects[query_object_O];
    #    #    query_instance = query_object_descStats(self.session,self.engine,self.settings);
    #    #    query_instance.initialize_supportedTables();
            
    #    #if hasattr(query_instance, query_func_O):
    #    #    query_func = getattr(query_instance, query_func_O);
    #    #    data_listDict = query_func(table_O,data_O
    #    #        );
    #    #else:
    #    #    print('query instance does not have the required method.');

    #    #save the data
    #    if query_func_O == 'add_rows_table':
    #        self.add_rows_table(table_O,data_O);