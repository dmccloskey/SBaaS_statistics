# System
import json
# SBaaS
from .stage02_quantification_outliers_query import stage02_quantification_outliers_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class stage02_quantification_outliers_io(stage02_quantification_outliers_query,
                                                   stage02_quantification_analysis_query,
                                                   stage02_quantification_descriptiveStats_query,
                                                   sbaas_template_io):
    def export_dataStage02QuantificationOutliersDeviation_js(self,analysis_id_I,data_dir_I='tmp'):
        '''Export data for a box and whiskers plot
        '''

        #get the data for the analysis
        data_O = [];
        data_O = self.get_rows_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
        # dump chart parameters to a js files
        data1_keys = ['analysis_id','experiment_id','sample_name_abbreviation','component_name','time_point','calculated_concentration_units','component_group_name'
                    ];
        data1_nestkeys = ['component_group_name'];
        data1_keymap = {'xdata':'component_group_name',
                        'ydatamean':'mean',
                        'ydatalb':'ci_lb',
                        'ydataub':'ci_ub',
                        'ydatamin':'min',
                        'ydatamax':'max',
                        'ydataiq1':'iq_1',
                        'ydataiq3':'iq_3',
                        'ydatamedian':'median',
                        'serieslabel':'sample_name_abbreviation',
                        'featureslabel':'component_group_name'};
   