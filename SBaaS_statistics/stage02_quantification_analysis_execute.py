
from .stage02_quantification_analysis_io import stage02_quantification_analysis_io

class stage02_quantification_analysis_execute(stage02_quantification_analysis_io):
    def execute_analysisConnection(self,
        connection_id = None,
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

        data_O = [];

        #query the connection information (in connection_order ASC)
        connections = [];
        
        #NOTE: each execution object is responsible for 1 connection
        execute_object = self.get_sbaasObject(connections[0]['execute_object'])
        for connection in connections:
            #execute_object = self.get_sbaasObject(connection['execute_object'])
            query_func = self.get_sbaasMethod(execute_object,connection['execute_method'])
            query_func(
                analysis_id_I=connection['analysis_id'],
                r_calc_I=r_calc_I,
                **analysis['execute_parameters']);

    def execute_analysisPipeline(self,
        pipeline_id = None,
        r_calc_I = None,
        ):
        '''Execute an analysis pipeline

        '''

        data_O = [];

        #query the pipeline information (in pipeline_order ASC)
        pipelines = [];
        
        for pipeline in pipelines:
            self.execute_analysisConnection(pipeline['connection_id'],r_calc_I=r_calc_I)

    def get_sbaasObject(self,object_I):
        '''Return an instanciated object
        '''
        object = None;

        #define the supported objects
        objects = {};

        #instanciate the module
        if object_I in objects.keys():
            object = objects[execute_object_I];
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
