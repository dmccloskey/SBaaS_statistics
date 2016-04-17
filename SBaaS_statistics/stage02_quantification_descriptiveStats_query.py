from .stage02_quantification_descriptiveStats_postgresql_models import *
from .stage02_quantification_analysis_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

from math import sqrt

class stage02_quantification_descriptiveStats_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_descriptiveStats':data_stage02_quantification_descriptiveStats,
                        };
        self.set_supportedTables(tables_supported);

    # data_stage02_quantification_descriptiveStats
    # query sample_names from data_stage02_quantification_descriptiveStats
    def get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I):
        '''Querry sample_name_abbreviations that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.sample_name_abbreviation,
                    data_stage02_quantification_descriptiveStats.time_point).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation,
                    data_stage02_quantification_descriptiveStats.time_point).order_by(
                    data_stage02_quantification_descriptiveStats.time_point.asc(),
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            time_points_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
                    time_points_O.append(d.time_point);
            return sample_name_abbreviations_O,time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I):
        '''Querry sample_name_abbreviations that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.sample_name_abbreviation).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation).order_by(
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.sample_name_abbreviation);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query calculated_concentration_units from data_stage02_quantification_descriptiveStats
    def get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I):
        '''Querry calculated_concentration_units that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.calculated_concentration_units).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units).order_by(
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.calculated_concentration_units);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query component_names from data_stage02_quantification_descriptiveStats
    def get_componentNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,analysis_id_I,calculated_concentration_units_I):
        '''Querry component_names that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.component_name).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.component_name).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_name);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_analysisIDAndCalculatedConcentrationUnitsAndCVThreshold_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I,
            cv_threshold_I,
            used__I=True):
        '''Query rows by analysis_id and calculated_concentration_units that are used
           and that are greater that cv_threshold_I
           INPUT:
           analysis_id_I = string
           calculated_concentration_units_I = string
           cv_threshold_I = float, rows > cv_threshold_I will be selected
           used__I = boolean
           OUTPUT:
           component_names_O'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.component_name).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.cv>cv_threshold_I,
                    data_stage02_quantification_descriptiveStats.used_.is_(used__I)).group_by(
                    data_stage02_quantification_descriptiveStats.component_name).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            component_names_O = [d.component_name for d in data];
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,analysis_id_I,calculated_concentration_units_I):
        '''Querry component_names that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.component_name,
                                      data_stage02_quantification_descriptiveStats.component_group_name).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.component_name,
                    data_stage02_quantification_descriptiveStats.component_group_name).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            component_name_O = [];
            component_group_name_O = [];
            if data: 
                for d in data:
                    component_name_O.append(d.component_name);
                    component_group_name_O.append(d.component_group_name);
            return component_name_O,component_group_name_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I):
        '''Querry component_names that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.component_name).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.component_name).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_name);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage02_quantification_descriptiveStats
    def get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
                                analysis_id_I,
                                sample_name_abbreviation_I,
                                component_name_I,
                                calculated_concentration_units_I):
        '''Querry data by sample_name_abbreviation, component_name, and calculated_concentration_units that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_descriptiveStats.component_name.like(component_name_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).all();
            mean,stdev,ci_lb,ci_ub,calculated_concentration_units = None,None,None,None,None;
            if len(data)>1:
                print('More than 1 row found');
            if data: 
                for d in data:
                    mean=d.mean;
                    stdev=sqrt(d.var);
                    ci_lb=d.ci_lb;
                    ci_ub=d.ci_ub;
                    calculated_concentration_units=d.calculated_concentration_units;
            return mean,stdev,ci_lb,ci_ub,calculated_concentration_units;
        except SQLAlchemyError as e:
            print(e);
    def get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
                                analysis_id_I,
                                sample_name_abbreviation_I,
                                time_point_I,
                                component_name_I,
                                calculated_concentration_units_I):
        '''Querry data by sample_name_abbreviation, component_name, and calculated_concentration_units that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_descriptiveStats.time_point.like(time_point_I),
                    data_stage02_quantification_descriptiveStats.component_name.like(component_name_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).all();
            mean,stdev,ci_lb,ci_ub,calculated_concentration_units = None,None,None,None,None;
            if len(data)>1:
                print('More than 1 row found');
            if data: 
                for d in data:
                    mean=d.mean;
                    stdev=sqrt(d.var);
                    ci_lb=d.ci_lb;
                    ci_ub=d.ci_ub;
                    calculated_concentration_units=d.calculated_concentration_units;
            return mean,stdev,ci_lb,ci_ub,calculated_concentration_units;
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage02_quantification_descriptiveStats
    def get_rows_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I,used__I=True):
        '''Querry rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(used__I)).order_by(
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc(),
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append({'analysis_id':d.analysis_id,
                    'experiment_id':d.experiment_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    'time_point':d.time_point,
                    'component_group_name':d.component_group_name,
                    'component_name':d.component_name,
                    'test_stat':d.test_stat,
                    'test_description':d.test_description,
                    'pvalue':d.pvalue,
                    'pvalue_corrected':d.pvalue_corrected,
                    'pvalue_corrected_description':d.pvalue_corrected_description,
                    'mean':d.mean,
                    'var':d.var,
                    'cv':d.cv,
                    'n':d.n,
                    'ci_lb':d.ci_lb,
                    'ci_ub':d.ci_ub,
                    'ci_level':d.ci_level,
                    'min':d.min,
                    'max':d.max,
                    'median':d.median,
                    'iq_1':d.iq_1,
                    'iq_3':d.iq_3,
                    'calculated_concentration_units':d.calculated_concentration_units,
                    'used_':d.used_,
                    'comment_':d.comment_
                    });
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Querry rows by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append({'analysis_id':d.analysis_id,
                    'experiment_id':d.experiment_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    'time_point':d.time_point,
                    'component_group_name':d.component_group_name,
                    'component_name':d.component_name,
                    'test_stat':d.test_stat,
                    'test_description':d.test_description,
                    'pvalue':d.pvalue,
                    'pvalue_corrected':d.pvalue_corrected,
                    'pvalue_corrected_description':d.pvalue_corrected_description,
                    'mean':d.mean,
                    'var':d.var,
                    'cv':d.cv,
                    'n':d.n,
                    'ci_lb':d.ci_lb,
                    'ci_ub':d.ci_ub,
                    'ci_level':d.ci_level,
                    'min':d.min,
                    'max':d.max,
                    'median':d.median,
                    'iq_1':d.iq_1,
                    'iq_3':d.iq_3,
                    'calculated_concentration_units':d.calculated_concentration_units,
                    'used_':d.used_,
                    'comment_':d.comment_
                    });
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndCVThreshold_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I,
            cv_threshold_I,
            used__I=True):
        '''Query rows by analysis_id and calculated_concentration_units that are used
           and that are greater that cv_threshold_I
           INPUT:
           analysis_id_I = string
           calculated_concentration_units_I = string
           cv_threshold_I = float, rows > cv_threshold_I will be selected
           used__I = boolean
           OUTPUT:
           rows_O = listDict with columns for sample_name_short from analysis_id
           '''
        try:
            data = self.session.query(
                    data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.cv>cv_threshold_I,
                    data_stage02_quantification_descriptiveStats.used_.is_(used__I)).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # Query specific columns of data_stage02_quantification_descriptiveStats
    def get_allMeans_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all mean values by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.mean).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.mean).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.mean);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allCVs_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all CVs by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.cv).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.cv).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.cv);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allMedians_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all medians by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.median).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.median).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.median);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allVariances_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all variances by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.var).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.var).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.var);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    def initialize_dataStage02_quantification_descriptiveStats(self):
        try:
            data_stage02_quantification_descriptiveStats.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification_descriptiveStats(self):
        try:
            data_stage02_quantification_descriptiveStats.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_descriptiveStats(self,analysis_id_I = None, calculated_concentration_units_I = []):
        try:
            if analysis_id_I and calculated_concentration_units_I:
                for ccu in calculated_concentration_units_I:
                    reset = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                        data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                        data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(ccu),
                        ).delete(synchronize_session=False);
                self.session.commit();
            elif analysis_id_I:
                reset = self.session.query(data_stage02_quantification_descriptiveStats).filter(data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);

    def add_dataStage02QuantificationDescriptiveStats(self, data_I):
        '''add rows of data_stage02_quantification_descriptiveStats'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_descriptiveStats(d
                        #d['analysis_id'],
                        #d['experiment_id'],
                        #d['sample_name_abbreviation'],
                        #d['time_point'],
                        ##d['time_point_units'],
                        #d['component_group_name'],
                        #d['component_name'],
                        #d['mean'],
                        #d['var'],
                        #d['cv'],
                        #d['n'],
                        #d['test_stat'],
                        #d['test_description'],
                        #d['pvalue'],
                        #d['pvalue_corrected'],
                        #d['pvalue_corrected_description'],
                        #d['ci_lb'],
                        #d['ci_ub'],
                        #d['ci_level'],
                        #d['min'],
                        #d['max'],
                        #d['median'],
                        #d['iq_1'],
                        #d['iq_3'],
                        #d['calculated_concentration_units'],
                        #d['used_'],
                        #d['comment_']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationDescriptiveStats(self,data_I):
        '''update rows of data_stage02_quantification_descriptiveStats'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                            data_stage02_quantification_descriptiveStats.id==d['id']).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'experiment_id':d['experiment_id'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'time_point':d['time_point'],
                            #'time_point_units':d['time_point_units'],
                            'component_group_name':d['component_group_name'],
                            'component_name':d['component_name'],
                            'mean':d['mean'],
                            'var':d['var'],
                            'cv':d['cv'],
                            'n':d['n'],
                            'test_stat':d['test_stat'],
                            'test_description':d['test_description'],
                            'pvalue':d['pvalue'],
                            'pvalue_corrected':d['pvalue_corrected'],
                            'pvalue_corrected_description':d['pvalue_corrected_description'],
                            'ci_lb':d['ci_lb'],
                            'ci_ub':d['ci_ub'],
                            'ci_level':d['ci_level'],
                            'min':d['min'],
                            'max':d['max'],
                            'median':d['median'],
                            'iq_1':d['iq_1'],
                            'iq_3':d['iq_3'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
   