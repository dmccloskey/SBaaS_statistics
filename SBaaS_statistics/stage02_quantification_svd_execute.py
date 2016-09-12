
from .stage02_quantification_svd_io import stage02_quantification_svd_io
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict

class stage02_quantification_svd_execute(stage02_quantification_svd_io,
                                         ):
    def execute_svd(self,
                    analysis_id_I,
            calculated_concentration_units_I=[],
            component_names_I=[],
            component_group_names_I=[],
            sample_name_shorts_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            experiment_ids_I=[],
            where_clause_I=None,
            query_object_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            query_func_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDataPreProcessingReplicates',
                    r_calc_I=None,
                    svd_method_I="svd"):
        '''execute svd using R'''

        print('execute_svd...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();

        data_U_O = [];
        data_d_O = [];
        data_V_O = [];     
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_I in query_objects.keys():
            query_object = query_objects[query_object_I];
            query_instance = query_object(self.session,self.engine,self.settings);
            query_instance.initialize_supportedTables();

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
        data_analysis = {'_del_':{'_del_':[]}};
        for row in data_listDict:
            cu = row['calculated_concentration_units']
            if not cu in data_analysis.keys(): data_analysis[cu]=[];
            data_analysis[cu].append(row);
        del data_analysis['_del_'];
        
        #apply the analysis to each group
        for cu in calculated_concentration_units:
            #print('calculating svd for concentration_units ' + cu);
            data = data_analysis[cu];

            data_U,data_d,data_V = [],[],[];
            data_U,data_d,data_V = r_calc.calculate_svd(data,
                    svd_method_I=svd_method_I,
                    ); #TODO: refactor to call methods directly...
            # add data to database
            for d in data_U[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_U_O.append(d);
            for d in data_d[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_d_O.append(d);
            for d in data_V[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_V_O.append(d);
        # add data to the database
        self.add_rows_table('data_stage02_quantification_svd_u',data_U_O);
        self.add_rows_table('data_stage02_quantification_svd_d',data_d_O);
        self.add_rows_table('data_stage02_quantification_svd_v',data_V_O);