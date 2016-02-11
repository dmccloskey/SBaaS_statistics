from SBaaS_base.sbaas_template_dependencies import sbaas_template_dependencies
from .stage02_quantification_svd_postgresql_models import *

class stage02_quantification_svd_dependencies(sbaas_template_dependencies):
    def get_supportedTables(self):
        '''return a {} of supported tables
        OUTPUT:
        tables_O = {} tablename:sqlalchemy object
        '''
        tables_O = {'data_stage02_quantification_svd_u':data_stage02_quantification_svd_u,
                        'data_stage02_quantification_svd_d':data_stage02_quantification_svd_d,
                        'data_stage02_quantification_svd_v':data_stage02_quantification_svd_v
                        };
        return tables_O;