# System
import json
# SBaaS
from .stage02_quantification_pairWiseCorrelation_query import stage02_quantification_pairWiseCorrelation_query
from SBaaS_base.sbaas_template_io import sbaas_template_io

# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData
from ddt_python.ddt_container import ddt_container

class stage02_quantification_pairWiseCorrelation_io(stage02_quantification_pairWiseCorrelation_query,sbaas_template_io):

    def stage02_quantification_pairWiseCorrelation_correlation_js(self,):
        '''table of correlations'''
        pass;

    def stage02_quantification_pairWiseCorrelationReplicates_correlation_js(self,):
        '''table of correlations'''
        pass;
   