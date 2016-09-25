
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

        #reorganize into analysis groups:
        pipeline_orders = list(set([p['pipeline_order'] for p in pipelines]));
        pipeline_orders.sort();
        data_analysis = {'_del_':[]};
        for row in data_listDict:
            po = row['pipeline_order']
            if not po in data_analysis.keys(): data_analysis[po]=[];
            data_analysis[po].append(row);
        del data_analysis['_del_'];
        
        for pipeline_order in pipeline_orders:
            #1. query the data
            data_listDict = [];
            for analysis in analysis_ids:
                data_tmp = [];

            #2. group the data
            data_analysis = [];

            #3. transform each unique group
            for data in data_analysis:
                data_O_listDict = [];


                data_O.append(data_O_listDict)

        #store the data

