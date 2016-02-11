#sbaas
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query
#sbaas models
from .stage02_quantification_histogram_postgresql_models import *

class stage02_quantification_histogram_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_histogram':data_stage02_quantification_histogram,
                        };
        self.set_supportedTables(tables_supported);
    def drop_dataStage02_quantification_histogram(self):
        try:
            data_stage02_quantification_histogram.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage02_quantification_histogram(self):
        try:
            data_stage02_quantification_histogram.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);

    #data_stage02_quantification_histogram      
    def reset_dataStage02_quantification_histogram(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_histogram).filter(data_stage02_quantification_histogram.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);  
    def add_dataStage02QuantificationHistogram(self, data_I):
        '''add rows of data_stage02_quantification_histogram'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_histogram(d
                        #d['analysis_id'],
                        #d['feature_id'],
                        #d['feature_units'],
                        #d['bin'],
                        #d['bin_width'],
                        #d['frequency'],
                        #d['used_'],
                        #d['comment_'],
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationHistogram(self,data_I):
        '''update rows of data_stage02_quantification_lineage'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_histogram).filter(
                           data_stage02_quantification_histogram.id==d['id']).update(
                            {'analysis_id':d['analysis_id'],
                            'feature_id':d['feature_id'],
                            'feature_units':d['feature_units'],
                            'bin':d['bin'],
                            'bin_width':d['bin_width'],
                            'frequency':d['frequency'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    # query data from data_stage02_quantification_histogram
    def get_rows_analysisID_dataStage02QuantificationHistogram(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_histogram).filter(
                    data_stage02_quantification_histogram.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_histogram.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsAsFeaturesDict_analysisID_dataStage02QuantificationHistogram(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_histogram).filter(
                    data_stage02_quantification_histogram.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_histogram.used_.is_(True)).all();
            rows_O = {};
            if data: 
                for d in data:
                    if d.feature_id in rows_O.keys():
                        rows_O[d.feature_id].append(d.__repr__dict__());
                    else:
                        rows_O[d.feature_id] = [];
                        rows_O[d.feature_id].append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
