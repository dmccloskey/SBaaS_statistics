
from .stage02_quantification_analysis_io import stage02_quantification_analysis_io

class stage02_quantification_analysis_execute(stage02_quantification_analysis_io):
    def execute_analysisPipeline(self,
        pipeline_id = None,
        analysis_group_id_I = None,
        r_calc_I = None,
        ):
        '''Execute an analysis pipeline'''

        data_O = [];

        #query the analysis groups
        analysis_groups = []

        #query the pipeline information
        pipelines = [];
        
        for pipeline in pipelines:
            #1. query the data
            data_listDict = [];
            #2. group the data
            data_analysis = [];
            #3. loop through the data
            for data in data_analysis:
                #4. transform each unique group
                data_O_listDict = [];


                data_O.append(data_O_listDict)

        #store the data

