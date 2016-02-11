#lims
from SBaaS_LIMS.lims_experiment_postgresql_models import *
from SBaaS_LIMS.lims_sample_postgresql_models import *

from .stage02_quantification_anova_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_anova_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_anova':data_stage02_quantification_anova,
                        };
        self.set_supportedTables(tables_supported);
    def initialize_dataStage02_quantification_anova(self):
        try:
            data_stage02_quantification_anova.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification_anova(self):
        try:
            data_stage02_quantification_anova.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_anova(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_anova).filter(data_stage02_quantification_anova.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_anova).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationAnova(self, analysis_id_I):
        """get data from analysis ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_anova).filter(
                    data_stage02_quantification_anova.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_anova.used_.is_(True)).order_by(
                    data_stage02_quantification_anova.calculated_concentration_units.asc(),
                    data_stage02_quantification_anova.component_group_name.asc()).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02QuantificationAnova(self, data_I):
        '''add rows of data_stage02_quantification_anova'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_anova(d);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
