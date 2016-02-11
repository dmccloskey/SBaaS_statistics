#sbaas
from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query
#sbaas models
from .stage02_quantification_count_postgresql_models import *

class stage02_quantification_count_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_countCorrelationPattern':data_stage02_quantification_countCorrelationPattern,
            'data_stage02_quantification_countCorrelationProfile':data_stage02_quantification_countCorrelationProfile,
            'data_stage02_quantification_countCorrelationTrend':data_stage02_quantification_countCorrelationTrend,
                        };
        self.set_supportedTables(tables_supported);
    def drop_dataStage02_quantification_count(self):
        try:
            #data_stage02_quantification_count.__table__.drop(self.engine,True);
            data_stage02_quantification_countCorrelationProfile.__table__.drop(self.engine,True);
            data_stage02_quantification_countCorrelationTrend.__table__.drop(self.engine,True);
            data_stage02_quantification_countCorrelationPattern.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage02_quantification_count(self):
        try:
            #data_stage02_quantification_count.__table__.create(self.engine,True);
            data_stage02_quantification_countCorrelationProfile.__table__.create(self.engine,True);
            data_stage02_quantification_countCorrelationTrend.__table__.create(self.engine,True);
            data_stage02_quantification_countCorrelationPattern.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);

    #data_stage02_quantification_count (not currently used yet...)     
    def reset_dataStage02_quantification_count(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_count).filter(data_stage02_quantification_count.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);  
    def add_dataStage02QuantificationCount(self, data_I):
        '''add rows of data_stage02_quantification_count'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_count(d
                        #d['analysis_id'],
                        #    d['feature_id'],
                        #    d['feature_units'],
                        #    d['element_id'],
                        #    d['frequency'],
                        #    d['fraction'],
                        #    d['used_'],
                        #    d['comment_'],
                            );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationCount(self,data_I):
        '''update rows of data_stage02_quantification_lineage'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_count).filter(
                           data_stage02_quantification_count.id==d['id']).update(
                            {'analysis_id':d['analysis_id'],
                            'feature_id':d['feature_id'],
                            'feature_units':d['feature_units'],
                            'element_id':d['element_id'],
                            'frequency':d['frequency'],
                            'fraction':d['fraction'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    # query data from data_stage02_quantification_count
    def get_rows_analysisID_dataStage02QuantificationCount(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_count).filter(
                    data_stage02_quantification_count.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_count.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsAsFeaturesDict_analysisID_dataStage02QuantificationCount(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_count).filter(
                    data_stage02_quantification_count.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_count.used_.is_(True)).all();
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

    #data_stage02_quantification_countCorrelationProfile     
    def reset_dataStage02_quantification_countCorrelationProfile(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_countCorrelationProfile).filter(data_stage02_quantification_countCorrelationProfile.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);  
    def add_dataStage02QuantificationCountCorrelationProfile(self, data_I):
        '''add rows of data_stage02_quantification_countCorrelationProfile'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_countCorrelationProfile(d
                        #d['analysis_id'],
                        #    d['feature_id'],
                        #    d['feature_units'],
                        #    d['distance_measure'],
                        #    d['correlation_coefficient_threshold'],
                        #    d['element_id'],
                        #    d['frequency'],
                        #    d['fraction'],
                        #    d['used_'],
                        #    d['comment_'],
                            );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationCountCorrelationProfile(self,data_I):
        '''update rows of data_stage02_quantification_countCorrelationProfile'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_countCorrelationProfile).filter(
                           data_stage02_quantification_countCorrelationProfile.id==d['id']).update(
                            {'analysis_id':d['analysis_id'],
                            'feature_id':d['feature_id'],
                            'feature_units':d['feature_units'],
                            'distance_measure':d['distance_measure'],
                            'correlation_coefficient_threshold':d['correlation_coefficient_threshold'],
                            'element_id':d['element_id'],
                            'frequency':d['frequency'],
                            'fraction':d['fraction'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    # query data from data_stage02_quantification_countCorrelationProfile
    def get_rows_analysisID_dataStage02QuantificationCountCorrelationProfile(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_countCorrelationProfile).filter(
                    data_stage02_quantification_countCorrelationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_countCorrelationProfile.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsAsFeaturesDict_analysisID_dataStage02QuantificationCountCorrelationProfile(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_countCorrelationProfile).filter(
                    data_stage02_quantification_countCorrelationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_countCorrelationProfile.used_.is_(True)).all();
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

    #data_stage02_quantification_countCorrelationTrend     
    def reset_dataStage02_quantification_countCorrelationTrend(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_countCorrelationTrend).filter(data_stage02_quantification_countCorrelationTrend.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);  
    def add_dataStage02QuantificationCountCorrelationTrend(self, data_I):
        '''add rows of data_stage02_quantification_countCorrelationTrend'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_countCorrelationTrend(d
                        #d['analysis_id'],
                        #    d['feature_id'],
                        #    d['feature_units'],
                        #    d['distance_measure'],
                        #    d['correlation_coefficient_threshold'],
                        #    d['element_id'],
                        #    d['frequency'],
                        #    d['fraction'],
                        #    d['used_'],
                        #    d['comment_'],
                            );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationCountCorrelationTrend(self,data_I):
        '''update rows of data_stage02_quantification_countCorrelationTrend'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_countCorrelationTrend).filter(
                           data_stage02_quantification_countCorrelationTrend.id==d['id']).update(
                            {'analysis_id':d['analysis_id'],
                            'feature_id':d['feature_id'],
                            'feature_units':d['feature_units'],
                            'distance_measure':d['distance_measure'],
                            'correlation_coefficient_threshold':d['correlation_coefficient_threshold'],
                            'element_id':d['element_id'],
                            'frequency':d['frequency'],
                            'fraction':d['fraction'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    # query data from data_stage02_quantification_countCorrelationTrend
    def get_rows_analysisID_dataStage02QuantificationCountCorrelationTrend(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_countCorrelationTrend).filter(
                    data_stage02_quantification_countCorrelationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_countCorrelationTrend.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsAsFeaturesDict_analysisID_dataStage02QuantificationCountCorrelationTrend(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_countCorrelationTrend).filter(
                    data_stage02_quantification_countCorrelationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_countCorrelationTrend.used_.is_(True)).all();
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
            
    #data_stage02_quantification_countCorrelationPattern     
    def reset_dataStage02_quantification_countCorrelationPattern(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_countCorrelationPattern).filter(data_stage02_quantification_countCorrelationPattern.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);  
    def add_dataStage02QuantificationCountCorrelationPattern(self, data_I):
        '''add rows of data_stage02_quantification_countCorrelationPattern'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_countCorrelationPattern(d
                        #d['analysis_id'],
                        #    d['feature_id'],
                        #    d['feature_units'],
                        #    d['distance_measure'],
                        #    d['correlation_coefficient_threshold'],
                        #    d['element_id'],
                        #    d['frequency'],
                        #    d['fraction'],
                        #    d['used_'],
                        #    d['comment_'],
                            );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationCountCorrelationPattern(self,data_I):
        '''update rows of data_stage02_quantification_countCorrelationPattern'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_countCorrelationPattern).filter(
                           data_stage02_quantification_countCorrelationPattern.id==d['id']).update(
                            {'analysis_id':d['analysis_id'],
                            'feature_id':d['feature_id'],
                            'feature_units':d['feature_units'],
                            'distance_measure':d['distance_measure'],
                            'correlation_coefficient_threshold':d['correlation_coefficient_threshold'],
                            'element_id':d['element_id'],
                            'frequency':d['frequency'],
                            'fraction':d['fraction'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    # query data from data_stage02_quantification_countCorrelationPattern
    def get_rows_analysisID_dataStage02QuantificationCountCorrelationPattern(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_countCorrelationPattern).filter(
                    data_stage02_quantification_countCorrelationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_countCorrelationPattern.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsAsFeaturesDict_analysisID_dataStage02QuantificationCountCorrelationPattern(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_countCorrelationPattern).filter(
                    data_stage02_quantification_countCorrelationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_countCorrelationPattern.used_.is_(True)).all();
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