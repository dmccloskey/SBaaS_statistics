#lims
from SBaaS_LIMS.lims_experiment_postgresql_models import *
from SBaaS_LIMS.lims_sample_postgresql_models import *

from .stage02_quantification_svm_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_svm_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_svm':data_stage02_quantification_svm
                        };
        self.set_supportedTables(tables_supported);
    def initialize_dataStage02_quantification(self):
        try:
            data_stage02_quantification_svm.__table__.create(engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification(self):
        try:
            data_stage02_quantification_svm.__table__.drop(engine,True);
        except SQLAlchemyError as e:
            print(e);