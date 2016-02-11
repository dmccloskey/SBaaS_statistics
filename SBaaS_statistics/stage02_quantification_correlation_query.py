#lims
from SBaaS_LIMS.lims_experiment_postgresql_models import *
from SBaaS_LIMS.lims_sample_postgresql_models import *

from .stage02_quantification_correlation_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_correlation_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_correlationPattern':data_stage02_quantification_correlationPattern,
    'data_stage02_quantification_correlationProfile':data_stage02_quantification_correlationProfile,
    'data_stage02_quantification_correlationTrend':data_stage02_quantification_correlationTrend,
                        };
        self.set_supportedTables(tables_supported);
    # stage02_quantification_correlation
    def initialize_dataStage02_quantification_correlation(self):
        try:
            data_stage02_quantification_correlationProfile.__table__.create(self.engine,True);
            data_stage02_quantification_correlationTrend.__table__.create(self.engine,True);
            data_stage02_quantification_correlationPattern.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification_correlation(self):
        try:
            data_stage02_quantification_correlationProfile.__table__.drop(self.engine,True);
            data_stage02_quantification_correlationTrend.__table__.drop(self.engine,True);
            data_stage02_quantification_correlationPattern.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage02_quantification_correlationProfile
    def get_rows_analysisID_dataStage02QuantificationCorrelationProfile(self,analysis_id_I):
        '''Querry rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_correlationProfile).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02QuantificationCorrelationProfile(self, data_I):
        '''add rows of stage02_quantification_correlation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_correlationProfile(d
                        #d['analysis_id'],
                        #d['sample_name_abbreviations'],
                        #d['profile_match'],
                        #d['profile_match_description'],
                        #d['component_match'],
                        #d['component_match_units'],
                        #d['distance_measure'],
                        #d['correlation_coefficient'],
                        #d['component_group_name'],
                        #d['component_name'],
                        #d['component_profile'],
                        #d['pvalue'],
                        #d['pvalue_corrected'],
                        #d['pvalue_corrected_description'],
                        #d['calculated_concentration_units'],
                        #d['used_'],
                        #d['comment_'],
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationCorrelationProfile(self,data_I):
        '''update rows of stage02_quantification_correlation'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_correlationProfile).filter(
                            stage02_quantification_correlation.id==d['id']).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'sample_name_abbreviations':d['sample_name_abbreviations'],
                            'profile_match':d['profile_match'],
                            'profile_match_description':d['profile_match_description'],
                            'component_match':d['component_match'],
                            'component_match_units':d['component_match_units'],
                            'distance_measure':d['distance_measure'],
                            'correlation_coefficient':d['correlation_coefficient'],
                            'component_group_name':d['component_group_name'],
                            'component_name':d['component_name'],
                            'component_profile':d['component_profile'],
                            'pvalue':d['pvalue'],
                            'pvalue_corrected':d['pvalue_corrected'],
                            'pvalue_corrected_description':d['pvalue_corrected_description'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def reset_dataStage02_quantification_correlationProfile(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_correlationProfile).filter(data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def get_profiles_analysisID_dataStage02QuantificationCorrelationProfile(self,analysis_id_I):
        '''Querry rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_correlationProfile.profile_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.used_.is_(True)).group_by(
                    data_stage02_quantification_correlationProfile.profile_match).order_by(
                    data_stage02_quantification_correlationProfile.profile_match.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.profile_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allComponentProfiles_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndPValue_dataStage02QuantificationCorrelationProfile(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,pvalue_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationProfile.component_profile).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.pvalue>pvalue_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationProfile.component_profile).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationProfile.component_profile).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.pvalue<pvalue_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationProfile.component_profile).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationProfile.component_profile).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.pvalue>=pvalue_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationProfile.component_profile).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationProfile.component_profile).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.pvalue<=pvalue_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationProfile.component_profile).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_profile);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allProfileMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationProfile(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationProfile.profile_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.profile_match != None).order_by(
                    data_stage02_quantification_correlationProfile.profile_match).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationProfile.profile_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.profile_match != None).order_by(
                    data_stage02_quantification_correlationProfile.profile_match).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationProfile.profile_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.profile_match != None).order_by(
                    data_stage02_quantification_correlationProfile.profile_match).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationProfile.profile_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.profile_match != None).order_by(
                    data_stage02_quantification_correlationProfile.profile_match).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.profile_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allProfileMatchDescription_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationProfile(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationProfile.profile_match_description).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.profile_match_description != None).order_by(
                    data_stage02_quantification_correlationProfile.profile_match_description).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationProfile.profile_match_description).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.profile_match_description != None).order_by(
                    data_stage02_quantification_correlationProfile.profile_match_description).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationProfile.profile_match_description).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.profile_match_description != None).order_by(
                    data_stage02_quantification_correlationProfile.profile_match_description).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationProfile.profile_match_description).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.profile_match_description != None).order_by(
                    data_stage02_quantification_correlationProfile.profile_match_description).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.profile_match_description);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allComponentMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationProfile(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationProfile.component_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.component_match != None).order_by(
                    data_stage02_quantification_correlationProfile.component_match).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationProfile.component_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.component_match != None).order_by(
                    data_stage02_quantification_correlationProfile.component_match).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationProfile.component_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.component_match != None).order_by(
                    data_stage02_quantification_correlationProfile.component_match).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationProfile.component_match).filter(
                    data_stage02_quantification_correlationProfile.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationProfile.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationProfile.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationProfile.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationProfile.used_.is_(True),
                    data_stage02_quantification_correlationProfile.component_match != None).order_by(
                    data_stage02_quantification_correlationProfile.component_match).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    # query rows from data_stage02_quantification_correlationTrend      
    def get_rows_analysisID_dataStage02QuantificationCorrelationTrend(self,analysis_id_I):
        '''Querry rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_correlationTrend).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02QuantificationCorrelationTrend(self, data_I):
        '''add rows of stage02_quantification_correlation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_correlationTrend(d
                        #d['analysis_id'],
                        #d['sample_name_abbreviations'],
                        #d['trend_match'],
                        #d['trend_match_description'],
                        #d['component_match'],
                        #d['component_match_units'],
                        #d['distance_measure'],
                        #d['correlation_coefficient'],
                        #d['component_group_name'],
                        #d['component_name'],
                        #d['component_trend'],
                        #d['pvalue'],
                        #d['pvalue_corrected'],
                        #d['pvalue_corrected_description'],
                        #d['calculated_concentration_units'],
                        #d['used_'],
                        #d['comment_'],
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationCorrelationTrend(self,data_I):
        '''update rows of stage02_quantification_correlation'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_correlationTrend).filter(
                            stage02_quantification_correlation.id==d['id']).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'sample_name_abbreviations':d['sample_name_abbreviations'],
                            'trend_match':d['trend_match'],
                            'trend_match_description':d['trend_match_description'],
                            'component_match':d['component_match'],
                            'component_match_units':d['component_match_units'],
                            'distance_measure':d['distance_measure'],
                            'correlation_coefficient':d['correlation_coefficient'],
                            'component_group_name':d['component_group_name'],
                            'component_name':d['component_name'],
                            'component_trend':d['component_trend'],
                            'pvalue':d['pvalue'],
                            'pvalue_corrected':d['pvalue_corrected'],
                            'pvalue_corrected_description':d['pvalue_corrected_description'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit(); 
    def reset_dataStage02_quantification_correlationTrend(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_correlationTrend).filter(data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def get_trends_analysisID_dataStage02QuantificationCorrelationTrend(self,analysis_id_I):
        '''Querry rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_correlationTrend.trend_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.used_.is_(True)).group_by(
                    data_stage02_quantification_correlationTrend.trend_match).order_by(
                    data_stage02_quantification_correlationTrend.trend_match.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.trend_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allComponentTrends_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndPValue_dataStage02QuantificationCorrelationTrend(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,pvalue_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationTrend.component_trend).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.pvalue>pvalue_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationTrend.component_trend).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationTrend.component_trend).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.pvalue<pvalue_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationTrend.component_trend).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationTrend.component_trend).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.pvalue>=pvalue_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationTrend.component_trend).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationTrend.component_trend).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.pvalue<=pvalue_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationTrend.component_trend).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_trend);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allTrendMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationTrend(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationTrend.trend_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.trend_match != None).order_by(
                    data_stage02_quantification_correlationTrend.trend_match).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationTrend.trend_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.trend_match != None).order_by(
                    data_stage02_quantification_correlationTrend.trend_match).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationTrend.trend_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.trend_match != None).order_by(
                    data_stage02_quantification_correlationTrend.trend_match).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationTrend.trend_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.trend_match != None).order_by(
                    data_stage02_quantification_correlationTrend.trend_match).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.trend_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allTrendMatchDescription_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationTrend(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationTrend.trend_match_description).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.trend_match_description != None).order_by(
                    data_stage02_quantification_correlationTrend.trend_match_description).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationTrend.trend_match_description).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.trend_match_description != None).order_by(
                    data_stage02_quantification_correlationTrend.trend_match_description).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationTrend.trend_match_description).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.trend_match_description != None).order_by(
                    data_stage02_quantification_correlationTrend.trend_match_description).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationTrend.trend_match_description).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.trend_match_description != None).order_by(
                    data_stage02_quantification_correlationTrend.trend_match_description).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.trend_match_description);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allComponentMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationTrend(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationTrend.component_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.component_match != None).order_by(
                    data_stage02_quantification_correlationTrend.component_match).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationTrend.component_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.component_match != None).order_by(
                    data_stage02_quantification_correlationTrend.component_match).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationTrend.component_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.component_match != None).order_by(
                    data_stage02_quantification_correlationTrend.component_match).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationTrend.component_match).filter(
                    data_stage02_quantification_correlationTrend.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationTrend.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationTrend.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationTrend.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationTrend.used_.is_(True),
                    data_stage02_quantification_correlationTrend.component_match != None).order_by(
                    data_stage02_quantification_correlationTrend.component_match).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    # query rows from data_stage02_quantification_correlationPattern      
    def get_rows_analysisID_dataStage02QuantificationCorrelationPattern(self,analysis_id_I):
        '''Querry rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_correlationPattern).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allComponentPatterns_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndPValue_dataStage02QuantificationCorrelationPattern(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,pvalue_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationPattern.component_pattern).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.pvalue>pvalue_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationPattern.component_pattern).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationPattern.component_pattern).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.pvalue<pvalue_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationPattern.component_pattern).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationPattern.component_pattern).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.pvalue>=pvalue_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationPattern.component_pattern).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationPattern.component_pattern).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.pvalue<=pvalue_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True)).order_by(
                    data_stage02_quantification_correlationPattern.component_pattern).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_pattern);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allPatternMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.pattern_match != None).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.pattern_match != None).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.pattern_match != None).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.pattern_match != None).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.pattern_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allPatternMatchDescription_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match_description).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.pattern_match_description != None).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match_description).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match_description).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.pattern_match_description != None).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match_description).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match_description).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.pattern_match_description != None).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match_description).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match_description).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.pattern_match_description != None).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match_description).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.pattern_match_description);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allComponentMatch_analysisIDAndDistanceMeasureAndCalculatedConcentrationUnitsAndComparatorAndCorrelationCoefficient_dataStage02QuantificationCorrelationPattern(self,analysis_id_I,
        calculated_concentration_units_I,distance_measure_I,comparator_I,correlation_coefficient_I):
        '''Query rows that are used from the analysis'''
        try:
            if comparator_I == '>':
                data = self.session.query(data_stage02_quantification_correlationPattern.component_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient>correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.component_match != None).order_by(
                    data_stage02_quantification_correlationPattern.component_match).all();
            elif comparator_I == '<':
                data = self.session.query(data_stage02_quantification_correlationPattern.component_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient<correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.component_match != None).order_by(
                    data_stage02_quantification_correlationPattern.component_match).all();
            elif comparator_I == '>=':
                data = self.session.query(data_stage02_quantification_correlationPattern.component_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient>=correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.component_match != None).order_by(
                    data_stage02_quantification_correlationPattern.component_match).all();
            elif comparator_I == '<=':
                data = self.session.query(data_stage02_quantification_correlationPattern.component_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.distance_measure.like(distance_measure_I),
                    data_stage02_quantification_correlationPattern.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_correlationPattern.correlation_coefficient<=correlation_coefficient_I,
                    data_stage02_quantification_correlationPattern.used_.is_(True),
                    data_stage02_quantification_correlationPattern.component_match != None).order_by(
                    data_stage02_quantification_correlationPattern.component_match).all();
            else:
                print(comparator_I + " not yet supported");
                return None;
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02QuantificationCorrelationPattern(self, data_I):
        '''add rows of stage02_quantification_correlation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_correlationPattern(d
                        #d['analysis_id'],
                        #d['sample_name_abbreviations'],
                        #d['pattern_match'],
                        #d['pattern_match_description'],
                        #d['component_match'],
                        #d['component_match_units'],
                        #d['distance_measure'],
                        #d['correlation_coefficient'],
                        #d['component_group_name'],
                        #d['component_name'],
                        #d['component_pattern'],
                        #d['pvalue'],
                        #d['pvalue_corrected'],
                        #d['pvalue_corrected_description'],
                        #d['calculated_concentration_units'],
                        #d['used_'],
                        #d['comment_'],
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationCorrelationPattern(self,data_I):
        '''update rows of stage02_quantification_correlation'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_correlationPattern).filter(
                            stage02_quantification_correlation.id==d['id']).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'sample_name_abbreviations':d['sample_name_abbreviations'],
                            'pattern_match':d['pattern_match'],
                            'pattern_match_description':d['pattern_match_description'],
                            'component_match':d['component_match'],
                            'component_match_units':d['component_match_units'],
                            'distance_measure':d['distance_measure'],
                            'correlation_coefficient':d['correlation_coefficient'],
                            'component_group_name':d['component_group_name'],
                            'component_name':d['component_name'],
                            'component_pattern':d['component_pattern'],
                            'pvalue':d['pvalue'],
                            'pvalue_corrected':d['pvalue_corrected'],
                            'pvalue_corrected_description':d['pvalue_corrected_description'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit(); 
    def reset_dataStage02_quantification_correlationPattern(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_correlationPattern).filter(data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def get_patterns_analysisID_dataStage02QuantificationCorrelationPattern(self,analysis_id_I):
        '''Querry rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_correlationPattern.pattern_match).filter(
                    data_stage02_quantification_correlationPattern.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_correlationPattern.used_.is_(True)).group_by(
                    data_stage02_quantification_correlationPattern.pattern_match).order_by(
                    data_stage02_quantification_correlationPattern.pattern_match.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.pattern_match);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
   

