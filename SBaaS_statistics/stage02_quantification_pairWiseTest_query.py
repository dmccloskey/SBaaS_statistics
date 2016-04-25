#SBaaS
from .stage02_quantification_analysis_postgresql_models import *
from .stage02_quantification_pairWiseTest_postgresql_models import *
#Resources
from math import log

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_pairWiseTest_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_pairWiseTest':data_stage02_quantification_pairWiseTest,
                        };
        self.set_supportedTables(tables_supported);
    # data_stage02_quantification_pairWiseTest
    def get_experimentID_analysisID_dataStage02pairWiseTest(self,analysis_id_I):
        '''Querry experimentID that are used from the analysis id'''
        try:
            experiment_ids = self.session.query(data_stage02_quantification_pairWiseTest.time_point_1,
                    data_stage02_quantification_pairWiseTest.time_point_2).filter(
                    data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.experiment_id).order_by(
                    data_stage02_quantification_pairWiseTest.experiment_id.asc()).all();
            experiment_ids_O = [];
            for tp in experiment_ids: experiment_ids_O.append(tp.experiment_id);
            return experiment_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_experimentID_analysisIDAndUnits_dataStage02pairWiseTest(self,analysis_id_I,calculated_concentration_units_I):
        '''Querry experimentID that are used from the analysis id and calculated concentration units'''
        try:
            experiment_ids = self.session.query(data_stage02_quantification_pairWiseTest.time_point_1,
                    data_stage02_quantification_pairWiseTest.time_point_2).filter(
                    data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.experiment_id).order_by(
                    data_stage02_quantification_pairWiseTest.experiment_id.asc()).all();
            experiment_ids_O = [];
            for tp in experiment_ids: experiment_ids_O.append(tp.experiment_id);
            return experiment_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # Query time points from data_stage02_quantification_pairWiseTest
    def get_timePoint_experimentID_dataStage02pairWiseTest(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        #Tested
        try:
            time_points = self.session.query(data_stage02_quantification_pairWiseTest.time_point_1,
                    data_stage02_quantification_pairWiseTest.time_point_2).filter(
                    data_stage02_quantification_pairWiseTest.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.time_point_1,
                    data_stage02_quantification_pairWiseTest.time_point_2).order_by(
                    data_stage02_quantification_pairWiseTest.time_point_1.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point_1);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_analysisIDAndExperimentIDAndUnits_dataStage02pairWiseTest(self,analysis_id_I,experiment_id_I,calculated_concentration_units_I):
        '''Querry time points that are used from the experiment'''
        #Tested
        try:
            time_points = self.session.query(data_stage02_quantification_pairWiseTest.time_point_1,
                    data_stage02_quantification_pairWiseTest.time_point_2).filter(
                    data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_pairWiseTest.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.time_point_1,
                    data_stage02_quantification_pairWiseTest.time_point_2).order_by(
                    data_stage02_quantification_pairWiseTest.time_point_1.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point_1);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # Query concentration_units from data_stage01_quantification_pairWiseTest:    
    def get_concentrationUnits_experimentIDAndTimePoint_dataStage02pairWiseTest(self, experiment_id_I,time_point_I):
        """get concentration_units from experiment ID and time point"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTest.calculated_concentration_units).filter(
                    data_stage02_quantification_pairWiseTest.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pairWiseTest.time_point_1.like(time_point_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units).order_by(
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_concentrationUnits_analysisID_dataStage02pairWiseTest(self, analysis_id_I):
        """get concentration_units from analysis ID"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTest.calculated_concentration_units).filter(
                    data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units).order_by(
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    # Query sample_name_abbreviations from data_stage01_quantification_pairWiseTest:    
    def get_sampleNameAbbreviations_experimentIDAndTimePointAndUnits_dataStage02pairWiseTest(self, experiment_id_I,time_point_I, concentration_units_I):
        """get component_names from experiment ID and time point and concentration_units"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1).filter(
                    data_stage02_quantification_pairWiseTest.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pairWiseTest.time_point_1.like(time_point_I),
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1).order_by(
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1.asc()).all();
            component_names_O = [];
            for d in data: 
                component_names_O.append(d[0]);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndExperimentIDAndTimePointAndUnits_dataStage02pairWiseTest(self,analysis_id_I, experiment_id_I,time_point_I, concentration_units_I):
        """get component_names from analysis ID and experiment ID and time point and concentration_units"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1).filter(
                    data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTest.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pairWiseTest.time_point_1.like(time_point_I),
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1).order_by(
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1.asc()).all();
            component_names_O = [];
            for d in data: 
                component_names_O.append(d[0]);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndUnits_dataStage02pairWiseTest(self,analysis_id_I, concentration_units_I):
        """get component_names from analysis ID and concentration_units"""
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1).filter(
                    data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True)).group_by(
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1).order_by(
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1.asc()).all();
            component_names_O = [];
            for d in data: 
                component_names_O.append(d[0]);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_pairWiseTest
    def get_RDataList_experimentIDAndTimePointAndUnitsAndSampleNameAbbreviations_dataStage02pairWiseTest(self, experiment_id_I,time_point_I,
              concentration_units_I,sample_name_abbreviation_1_I,sample_name_abbreviation_2_I):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTest.experiment_id,
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1,
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2,
                    data_stage02_quantification_pairWiseTest.time_point_1,
                    data_stage02_quantification_pairWiseTest.time_point_2,
                    data_stage02_quantification_pairWiseTest.component_group_name,
                    data_stage02_quantification_pairWiseTest.component_name,
                    data_stage02_quantification_pairWiseTest.test_stat,
                    data_stage02_quantification_pairWiseTest.test_description,
                    data_stage02_quantification_pairWiseTest.pvalue,
                    data_stage02_quantification_pairWiseTest.pvalue_corrected,
                    data_stage02_quantification_pairWiseTest.pvalue_corrected_description,
                    data_stage02_quantification_pairWiseTest.mean,
                    data_stage02_quantification_pairWiseTest.ci_lb,
                    data_stage02_quantification_pairWiseTest.ci_ub,
                    data_stage02_quantification_pairWiseTest.ci_level,
                    data_stage02_quantification_pairWiseTest.fold_change,
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units).filter(
                    data_stage02_quantification_pairWiseTest.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pairWiseTest.time_point_1.like(time_point_I),
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1.like(sample_name_abbreviation_1_I),
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2.like(sample_name_abbreviation_2_I),
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True),
                    data_stage02_quantification_pairWiseTest.ci_level != None).group_by(
                    data_stage02_quantification_pairWiseTest.experiment_id,
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1,
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2,
                    data_stage02_quantification_pairWiseTest.time_point_1,
                    data_stage02_quantification_pairWiseTest.time_point_2,
                    data_stage02_quantification_pairWiseTest.component_group_name,
                    data_stage02_quantification_pairWiseTest.component_name,
                    data_stage02_quantification_pairWiseTest.test_stat,
                    data_stage02_quantification_pairWiseTest.test_description,
                    data_stage02_quantification_pairWiseTest.pvalue,
                    data_stage02_quantification_pairWiseTest.pvalue_corrected,
                    data_stage02_quantification_pairWiseTest.pvalue_corrected_description,
                    data_stage02_quantification_pairWiseTest.mean,
                    data_stage02_quantification_pairWiseTest.ci_lb,
                    data_stage02_quantification_pairWiseTest.ci_ub,
                    data_stage02_quantification_pairWiseTest.ci_level,
                    data_stage02_quantification_pairWiseTest.fold_change,
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units).order_by(
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2.asc(),
                    data_stage02_quantification_pairWiseTest.component_group_name.asc()).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation_1'] = d.sample_name_abbreviation_1;
                data_1['sample_name_abbreviation_2'] = d.sample_name_abbreviation_2;
                data_1['time_point_1'] = d.time_point_1;
                data_1['time_point_2'] = d.time_point_2;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['test_stat'] = d.test_stat;
                data_1['test_description'] = d.test_description;
                data_1['pvalue_negLog10'] = -log(d.pvalue,10);
                data_1['pvalue_corrected_negLog10'] = -log(d.pvalue_corrected,10);
                data_1['pvalue_corrected_description'] = d.pvalue_corrected_description;
                data_1['mean'] = d.mean;
                data_1['ci_lb'] = d.ci_lb;
                data_1['ci_ub'] = d.ci_ub;
                data_1['ci_level'] = d.ci_level;
                data_1['fold_change_log2'] = log(d.fold_change,2);
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataList_analysisIDAndUnitsAndSampleNameAbbreviations_dataStage02pairWiseTest(self, analysis_id_I,
              concentration_units_I,sample_name_abbreviation_1_I,sample_name_abbreviation_2_I):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTest.analysis_id,
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1,
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2,
                    data_stage02_quantification_pairWiseTest.component_group_name,
                    data_stage02_quantification_pairWiseTest.component_name,
                    data_stage02_quantification_pairWiseTest.test_stat,
                    data_stage02_quantification_pairWiseTest.test_description,
                    data_stage02_quantification_pairWiseTest.pvalue,
                    data_stage02_quantification_pairWiseTest.pvalue_corrected,
                    data_stage02_quantification_pairWiseTest.pvalue_corrected_description,
                    data_stage02_quantification_pairWiseTest.mean,
                    data_stage02_quantification_pairWiseTest.ci_lb,
                    data_stage02_quantification_pairWiseTest.ci_ub,
                    data_stage02_quantification_pairWiseTest.ci_level,
                    data_stage02_quantification_pairWiseTest.fold_change,
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units).filter(
                    data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1.like(sample_name_abbreviation_1_I),
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2.like(sample_name_abbreviation_2_I),
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True),
                    data_stage02_quantification_pairWiseTest.ci_level != None).group_by(
                    data_stage02_quantification_pairWiseTest.analysis_id,
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_1,
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2,
                    data_stage02_quantification_pairWiseTest.component_group_name,
                    data_stage02_quantification_pairWiseTest.component_name,
                    data_stage02_quantification_pairWiseTest.test_stat,
                    data_stage02_quantification_pairWiseTest.test_description,
                    data_stage02_quantification_pairWiseTest.pvalue,
                    data_stage02_quantification_pairWiseTest.pvalue_corrected,
                    data_stage02_quantification_pairWiseTest.pvalue_corrected_description,
                    data_stage02_quantification_pairWiseTest.mean,
                    data_stage02_quantification_pairWiseTest.ci_lb,
                    data_stage02_quantification_pairWiseTest.ci_ub,
                    data_stage02_quantification_pairWiseTest.ci_level,
                    data_stage02_quantification_pairWiseTest.fold_change,
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units).order_by(
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2.asc(),
                    data_stage02_quantification_pairWiseTest.component_group_name.asc()).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['sample_name_abbreviation_1'] = d.sample_name_abbreviation_1;
                data_1['sample_name_abbreviation_2'] = d.sample_name_abbreviation_2;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['test_stat'] = d.test_stat;
                data_1['test_description'] = d.test_description;
                data_1['pvalue_negLog10'] = -log(d.pvalue,10);
                data_1['pvalue_corrected_negLog10'] = -log(d.pvalue_corrected,10);
                data_1['pvalue_corrected_description'] = d.pvalue_corrected_description;
                data_1['mean'] = d.mean;
                data_1['ci_lb'] = d.ci_lb;
                data_1['ci_ub'] = d.ci_ub;
                data_1['ci_level'] = d.ci_level;
                data_1['fold_change_log2'] = log(d.fold_change,2);
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02pairWiseTest(self, analysis_id_I):
        """get data from analysis ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_pairWiseTest).filter(
                    data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pairWiseTest.used_.is_(True),
                    data_stage02_quantification_pairWiseTest.ci_lb != None,
                    data_stage02_quantification_pairWiseTest.ci_ub != None,
                    data_stage02_quantification_pairWiseTest.ci_level != None).order_by(
                    data_stage02_quantification_pairWiseTest.calculated_concentration_units.asc(),
                    data_stage02_quantification_pairWiseTest.sample_name_abbreviation_2.asc(),
                    data_stage02_quantification_pairWiseTest.component_group_name.asc()).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['sample_name_abbreviation_1'] = d.sample_name_abbreviation_1;
                data_1['sample_name_abbreviation_2'] = d.sample_name_abbreviation_2;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['test_stat'] = d.test_stat;
                data_1['test_description'] = d.test_description;
                data_1['pvalue_negLog10'] = -log(d.pvalue,10);
                data_1['pvalue_corrected_negLog10'] = -log(d.pvalue_corrected,10);
                data_1['pvalue_corrected_description'] = d.pvalue_corrected_description;
                data_1['mean'] = d.mean;
                data_1['ci_lb'] = d.ci_lb;
                data_1['ci_ub'] = d.ci_ub;
                data_1['ci_level'] = d.ci_level;
                data_1['fold_change_log2'] = log(d.fold_change,2);
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_1['used_'] = d.used_;
                data_1['comment_'] = d.comment_;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage02_quantification_pairWiseTest(self):
        try:
            data_stage02_quantification_pairWiseTest.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification_pairWiseTest(self):
        try:
            data_stage02_quantification_pairWiseTest.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pairWiseTest(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pairWiseTest).filter(data_stage02_quantification_pairWiseTest.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pairWiseTest).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def add_dataStage02QuantificationPairWiseTest(self, data_I):
        '''add rows of data_stage02_quantification_pairWiseTest'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_pairWiseTest(d);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();