#SBaaS
from .stage02_quantification_analysis_io import stage02_quantification_analysis_io
#SBaaS execution methods
try:
    from .stage02_quantification_anova_execute import stage02_quantification_anova_execute
    from .stage02_quantification_cluster_execute import stage02_quantification_cluster_execute
    from .stage02_quantification_correlation_execute import stage02_quantification_correlation_execute
    from .stage02_quantification_count_execute import stage02_quantification_count_execute
    from .stage02_quantification_covariance_execute import stage02_quantification_covariance_execute
    from .stage02_quantification_dataPreProcessing_averages_execute import stage02_quantification_dataPreProcessing_averages_execute
    from .stage02_quantification_dataPreProcessing_pairWiseTest_execute import stage02_quantification_dataPreProcessing_pairWiseTest_execute
    from .stage02_quantification_dataPreProcessing_points_execute import stage02_quantification_dataPreProcessing_points_execute
    from .stage02_quantification_dataPreProcessing_replicates_execute import stage02_quantification_dataPreProcessing_replicates_execute
    from .stage02_quantification_descriptiveStats_execute import stage02_quantification_descriptiveStats_execute
    from .stage02_quantification_enrichment_execute import stage02_quantification_enrichment_execute
    from .stage02_quantification_heatmap_execute import stage02_quantification_heatmap_execute
    from .stage02_quantification_histogram_execute import stage02_quantification_histogram_execute
    from .stage02_quantification_outliers_execute import stage02_quantification_outliers_execute
    from .stage02_quantification_pairWiseCorrelation_execute import stage02_quantification_pairWiseCorrelation_execute
    from .stage02_quantification_pairWisePLS_execute import stage02_quantification_pairWisePLS_execute #will be refactored...
    from .stage02_quantification_pairWiseTable_execute import stage02_quantification_pairWiseTable_execute
    from .stage02_quantification_pairWiseTest_execute import stage02_quantification_pairWiseTest_execute
    from .stage02_quantification_spls_execute import stage02_quantification_spls_execute #works for pca and pls
    from .stage02_quantification_svd_execute import stage02_quantification_svd_execute
    from .stage02_quantification_svm_execute import stage02_quantification_svm_execute
    from .stage02_quantification_tree_execute import stage02_quantification_tree_execute
except ImportError as e:
    print(e);
#System
import json
import time as time
import datetime
from inspect import signature
from sys import getsizeof

class stage02_quantification_analysis_execute(stage02_quantification_analysis_io):
    def execute_analysisConnection(self,
        connection_id_I = None,
        r_calc_I = None,
        ):
        '''Execute an analysis connection
        
        DESCRIPTION:
        connections should conform to the following format:
        1. query the data
        2. query the data
        3. query the data
        ...
        N. transform the data
        N+1. store the data

        '''
        import psutil #default timer starts on module import

        data_O = [];
        diagnostics_O = [];

        #query the connection information (in connection_order ASC)
        connections = [];
        connections = self._get_rows_connectionID_dataStage02QuantificationAnalysisConnection(
            connection_id_I = connection_id_I);
        
        #NOTE: each execution object is responsible for 1 connection
        execute_object = self.get_sbaasObject(connections[0]['execute_object'])
        for connection_cnt,connection in enumerate(connections):
            connection_diagnostics = {};
            execution_startTime = time.time();

            #get the function
            #execute_object = self.get_sbaasObject(connection['execute_object'])
            query_func = self.get_sbaasMethod(execute_object,connection['execute_method'])

            #get and format the parameters
            method_signature = signature(query_func);
            method_parameters = [mp for mp in method_signature.parameters];
            addIn_parameters = {'analysis_id_I':connection['analysis_id'],
                                'r_calc_I':r_calc_I,
                                };
            parameters = self.parse_executeParameters(
                connection['execute_parameters'],
                addIn_parameters_I=addIn_parameters,
                method_parameters_I=method_parameters
                )
            try:
                query_func(**parameters);
            except TypeError as e:
                print(e);
            except Exception as e:
                print(e);

            #log diagnostics
            connection_diagnostics['analysis_id'] = connection['analysis_id'];
            connection_diagnostics['connection_id'] = connection_id_I;
            connection_diagnostics['connection_step'] = connection_cnt;
            connection_diagnostics['execution_startTime'] = datetime.datetime.now();
            connection_diagnostics['execution_time_units'] = 'seconds';
            connection_diagnostics['execution_time'] = time.time() - execution_startTime;
            connection_diagnostics['cpu_times'] = dict(psutil.cpu_times()._asdict())
            connection_diagnostics['cpu_times'].update({'cpu_percent_'+str(cnt):v for cnt,v in enumerate(psutil.cpu_percent(percpu=True))})
            connection_diagnostics['memory_virtual'] = dict(psutil.virtual_memory()._asdict());
            connection_diagnostics['memory_swap'] = dict(psutil.swap_memory()._asdict())
            connection_diagnostics['memory_process'] = self.get_memory();
            connection_diagnostics['memory_objects'] = getsizeof(execute_object)+getsizeof(query_func);
            connection_diagnostics['memory_data'] = getsizeof(execute_object.get_data())
            connection_diagnostics['memory_units'] = 'bytes';
            connection_diagnostics['disk_io'] = dict(psutil.disk_io_counters()._asdict())
            connection_diagnostics['network_io'] = dict(psutil.net_io_counters()._asdict())
            connection_diagnostics['message_log'] = None;
            connection_diagnostics['used_'] = True;
            connection_diagnostics['comment_'] = None;
            diagnostics_O.append(connection_diagnostics);
        return diagnostics_O;

    def execute_analysisPipeline(self,
        pipeline_id_I = None,
        r_calc_I = None,
        ):
        '''Execute an analysis pipeline

        '''
        diagnostics_O = [];
        #query the pipeline information (in pipeline_order ASC)
        pipelines = [];
        pipelines = self._get_rows_pipelineID_dataStage02QuantificationAnalysisPipeline(
            pipeline_id_I = pipeline_id_I
            );         
        for pipeline in pipelines:
            diagnostics = self.execute_analysisConnection(
                pipeline['connection_id'],
                r_calc_I=r_calc_I,
                );
            diagnostics_O.extend(diagnostics);
            
        for d in diagnostics_O: d['pipeline_id']=pipeline_id_I;
        #reset previous diagnostics before adding in more data
        self.reset_dataStage02_quantification_analysis_diagnostics(
            tables_I = ['data_stage02_quantification_analysis_diagnostics'],
            pipeline_id_I = pipeline_id_I,
            warn_I=False);
        #store the diagnostics
        self.add_rows_table("data_stage02_quantification_analysis_diagnostics",diagnostics_O)

    def get_sbaasObject(self,object_I):
        '''Return an instanciated object
        '''
        object = None;

        #define the supported objects
        objects = {"stage02_quantification_anova_execute":stage02_quantification_anova_execute,
            "stage02_quantification_cluster_execute":stage02_quantification_cluster_execute,
            "stage02_quantification_correlation_execute":stage02_quantification_correlation_execute,
            "stage02_quantification_count_execute":stage02_quantification_count_execute,
            "stage02_quantification_covariance_execute":stage02_quantification_covariance_execute,
            "stage02_quantification_dataPreProcessing_averages_execute":stage02_quantification_dataPreProcessing_averages_execute,
            "stage02_quantification_dataPreProcessing_pairWiseTest_execute":stage02_quantification_dataPreProcessing_pairWiseTest_execute,
            "stage02_quantification_dataPreProcessing_points_execute":stage02_quantification_dataPreProcessing_points_execute,
            "stage02_quantification_dataPreProcessing_replicates_execute":stage02_quantification_dataPreProcessing_replicates_execute,
            "stage02_quantification_descriptiveStats_execute":stage02_quantification_descriptiveStats_execute,
            "stage02_quantification_enrichment_execute":stage02_quantification_enrichment_execute,
            "stage02_quantification_heatmap_execute":stage02_quantification_heatmap_execute,
            "stage02_quantification_histogram_execute":stage02_quantification_histogram_execute,
            "stage02_quantification_outliers_execute":stage02_quantification_outliers_execute,
            "stage02_quantification_pairWiseCorrelation_execute":stage02_quantification_pairWiseCorrelation_execute,
            "stage02_quantification_pairWisePLS_execute":stage02_quantification_pairWisePLS_execute, #will be refactored...,
            "stage02_quantification_pairWiseTable_execute":stage02_quantification_pairWiseTable_execute,
            "stage02_quantification_pairWiseTest_execute":stage02_quantification_pairWiseTest_execute,
            "stage02_quantification_spls_execute":stage02_quantification_spls_execute, #works for pca and pls,
            "stage02_quantification_svd_execute":stage02_quantification_svd_execute,
            "stage02_quantification_svm_execute":stage02_quantification_svm_execute,
            "stage02_quantification_tree_execute":stage02_quantification_tree_execute,
            };

        #instanciate the module
        if object_I in objects.keys():
            object = objects[object_I];
            object = object(self.session,self.engine);
            object.initialize_supportedTables();
        else:
            print('Object not supported');

        return object;

    def get_sbaasMethod(self,object_I,method_I):
        '''Return an object's method
        '''
        
        method_O = None;
        if hasattr(object_I, method_I):
            method_O = getattr(object_I, method_I);
        else:
            print('Object does not support the requested method');

        return method_O;

    def parse_executeParameters(self,parameters_I,addIn_parameters_I=[],method_parameters_I=[]):
        '''Parse the execution method parameters
        INPUT:
        parameters_I = dict of method parameters
        OPTION INPUT:
        addIn_parameters_I = dict of parameters to add
        method_parameters_I = list of parameters of the target method to trim
        OUTPUT
        parameters_O = dict of method parameters
        '''
        parameters_O = {};

        #parse the parameters
        if type(parameters_I)==type({}):
            parameters_O = parameters_I; #TODO: refactor...
        elif type(parameters_I)==type(''):
            try:
                parameters_O = eval(parameters_I); #TODO: refactor...
            except SyntaxError as e:
                print(e)
            except Exception as e:
                print(e)
        else:
            print('execute_parameters type not recognized.');

        #add in additional parameters
        for k,v in addIn_parameters_I.items():
            parameters_O[k]=v;
        #if 'analysis_id_I' not in parameters_O.keys():
        #    parameters_O['analysis_id_I']=analysis_id_I;
        #elif parameters_O['analysis_id_I']!=analysis_id_I:
        #    print('parameters analysis_id_I and connection analysis_id are not equal.');
        #    print('connection analysis_id will be used.');
        #    parameters_O['analysis_id_I']=analysis_id_I;

        #trim the arguments to best match the method parameters: 
        if method_parameters_I:
            parameters_O = {k:parameters_O[k] for k in method_parameters_I if k in parameters_O.keys()};
        return parameters_O;


