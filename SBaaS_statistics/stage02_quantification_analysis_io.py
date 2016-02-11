from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from SBaaS_base.sbaas_template_io import sbaas_template_io
# Resources
from io_utilities.base_importData import base_importData
from io_utilities.base_exportData import base_exportData

class stage02_quantification_analysis_io(stage02_quantification_analysis_query,
                                    sbaas_template_io #abstract io methods
                                    ):
    def import_dataStage02QuantificationAnalysis_add(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.add_dataStage02QuantificationAnalysis(data.data);
        data.clear_data();

    def import_dataStage02QuantificationAnalysis_update(self, filename):
        '''table adds'''
        data = base_importData();
        data.read_csv(filename);
        data.format_data();
        self.update_dataStage02QuantificationAnalysis(data.data);
        data.clear_data();