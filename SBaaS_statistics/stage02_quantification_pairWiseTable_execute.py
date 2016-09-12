
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
            redundancy_I=True,
            value_I = 'mean',
            query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
            query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats'):
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
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        data_pairwise_O = [];

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
        
        #reorganize into analysis groups:
        calculated_concentration_units = list(set([c['calculated_concentration_units'] for c in data_listDict]));
        calculated_concentration_units.sort();
        sample_name_abbreviations = list(set([c['sample_name_abbreviation'] for c in data_listDict]));
        sample_name_abbreviations.sort();
        data_analysis = {'_del_':{'_del_':[]}};
        for row in data_listDict:
            cu = row['calculated_concentration_units']
            sna = row['sample_name_abbreviation']
            if not cu in data_analysis.keys(): data_analysis[cu]={};
            if not sna in data_analysis[cu].keys(): data_analysis[cu][sna]=[];
            data_analysis[cu][sna].append(row);
        del data_analysis['_del_'];

        #apply the analysis to each unique group
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            print('calculating pairwiseCorrelation for concentration_units ' + cu);
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
                        data_1 = data_analysis[cu][sna_1];
                        data_2 = data_analysis[cu][sna_2];

                        if len(data_1)!=len(data_2):
                            print('the number of components in sn_1 and sn_2 are not equal.');

                        # recorde the data
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
        # add data to database
        self.add_rows_table('data_stage02_quantification_pairWiseTable',data_pairwise_O);

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