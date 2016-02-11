#LIMS
from SBaaS_LIMS.lims_experiment_postgresql_models import *
from SBaaS_LIMS.lims_sample_postgresql_models import *
#SBaaS source data tables
from SBaaS_quantification.stage01_quantification_replicatesMI_postgresql_models import *
from SBaaS_quantification.stage01_quantification_physiologicalRatios_postgresql_models import *
#SBaaS
from .stage02_quantification_analysis_postgresql_models import *
from .stage02_quantification_normalization_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_normalization_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_quantification_normalization
        '''
        tables_supported = {'data_stage02_quantification_glogNormalized':data_stage02_quantification_glogNormalized,
                            'data_stage02_quantification_analysis':data_stage02_quantification_analysis,
                        };
        self.set_supportedTables(tables_supported);

    def get_RExpressionData_AnalysisIDAndExperimentIDAndTimePointAndUnitsAndSampleNameShort_dataStage01ReplicatesMI(self, analysis_id_I,experiment_id_I,time_point_I,concentration_units_I,sample_name_short_I):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage01_quantification_replicatesMI.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_analysis.analysis_id,
                    data_stage01_quantification_replicatesMI.sample_name_short,
                    data_stage01_quantification_replicatesMI.time_point,
                    data_stage01_quantification_replicatesMI.component_group_name,
                    data_stage01_quantification_replicatesMI.component_name,
                    data_stage01_quantification_replicatesMI.calculated_concentration,
                    data_stage01_quantification_replicatesMI.calculated_concentration_units).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_replicatesMI.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_analysis.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.time_point.like(time_point_I),
                    data_stage01_quantification_replicatesMI.calculated_concentration_units.like(concentration_units_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(sample_name_short_I),
                    data_stage02_quantification_analysis.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_analysis.analysis_id,
                    data_stage01_quantification_replicatesMI.sample_name_short,
                    data_stage01_quantification_replicatesMI.time_point,
                    data_stage01_quantification_replicatesMI.component_group_name,
                    data_stage01_quantification_replicatesMI.component_name,
                    data_stage01_quantification_replicatesMI.calculated_concentration,
                    data_stage01_quantification_replicatesMI.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage01ReplicatesMI(self, analysis_id_I,concentration_units_I,component_name_I,sample_name_abbreviation_I,exp_type_I=4):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage01_quantification_replicatesMI.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage01_quantification_replicatesMI.sample_name_short,
                    data_stage01_quantification_replicatesMI.time_point,
                    data_stage01_quantification_replicatesMI.component_group_name,
                    data_stage01_quantification_replicatesMI.component_name,
                    data_stage01_quantification_replicatesMI.calculated_concentration,
                    data_stage01_quantification_replicatesMI.calculated_concentration_units).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage01_quantification_replicatesMI.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage01_quantification_replicatesMI.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage01_quantification_replicatesMI.component_name.like(component_name_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage01_quantification_replicatesMI.calculated_concentration_units.like(concentration_units_I),
                    data_stage01_quantification_replicatesMI.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage01_quantification_replicatesMI.used_.is_(True)).group_by(
                    data_stage01_quantification_replicatesMI.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage01_quantification_replicatesMI.sample_name_short,
                    data_stage01_quantification_replicatesMI.time_point,
                    data_stage01_quantification_replicatesMI.component_group_name,
                    data_stage01_quantification_replicatesMI.component_name,
                    data_stage01_quantification_replicatesMI.calculated_concentration,
                    data_stage01_quantification_replicatesMI.calculated_concentration_units).all();
            data_O = [];
            concentrations_O = [];
            for d in data: 
                concentrations_O.append(d.calculated_concentration);
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O,concentrations_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_physiologicalRatios_replicates
    def get_RExpressionData_AnalysisIDAndExperimentIDAndSampleNameShortAndTimePoint_dataStage01PhysiologicalRatiosReplicates(self,analysis_id_I, experiment_id_I, sample_name_short_I, time_point_I):
        """Query calculated ratios"""
        try:
            data = self.session.query(data_stage01_quantification_physiologicalRatios_replicates).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_analysis.time_point.like(time_point_I),
                    data_stage02_quantification_analysis.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_physiologicalRatios_replicates.experiment_id.like(experiment_id_I),
                    data_stage01_quantification_physiologicalRatios_replicates.sample_name_short.like(sample_name_short_I),
                    data_stage01_quantification_physiologicalRatios_replicates.time_point.like(time_point_I),
                    data_stage01_quantification_physiologicalRatios_replicates.used_.is_(True)).all();
            rows_O = [];
            if data:
                for d in data:
                    rows_O.append({'experiment_id':d.experiment_id,
                        'sample_name_short':d.sample_name_short,
                        'time_point':d.time_point,
                        'physiologicalratio_id':d.physiologicalratio_id,
                        'physiologicalratio_name':d.physiologicalratio_name,
                        'physiologicalratio_value':d.physiologicalratio_value,
                        'physiologicalratio_description':d.physiologicalratio_description,
                        'used_':d.used_,
                        'comment_':d.comment_});
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    # data_stage02_quantification_glogNormalized
    # Query time points from data_stage02_quantification_glogNormalized
    def get_experimentID_analysisID_dataStage02GlogNormalized(self,analysis_id_I):
        '''Querry experimentIDs that are used from the experiment'''
        #Tested
        try:
            experiment_ids = self.session.query(data_stage02_quantification_glogNormalized.experiment_id).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id).order_by(
                    data_stage02_quantification_glogNormalized.experiment_id.asc()).all();
            experiment_ids_O = [];
            for tp in experiment_ids: experiment_ids_O.append(tp.experiment_id);
            return experiment_ids_O;
        except SQLAlchemyError as e:
            print(e);
    def get_experimentID_analysisIDAndUnits_dataStage02GlogNormalized(self,analysis_id_I,calculated_concentration_units_I):
        '''Querry experimentIDs that are used from the analysis ID and concentration units'''
        #Tested
        try:
            experiment_ids = self.session.query(data_stage02_quantification_glogNormalized.experiment_id).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id).order_by(
                    data_stage02_quantification_glogNormalized.experiment_id.asc()).all();
            experiment_ids_O = [];
            for tp in experiment_ids: experiment_ids_O.append(tp.experiment_id);
            return experiment_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # Query time points from data_stage02_quantification_glogNormalized
    def get_timePoint_experimentID_dataStage02GlogNormalized(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        #Tested
        try:
            time_points = self.session.query(data_stage02_quantification_glogNormalized.time_point).filter(
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.time_point).order_by(
                    data_stage02_quantification_glogNormalized.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_analysisIDAndExperimentID_dataStage02GlogNormalized(self,analysis_id_I,experiment_id_I):
        '''Querry time points that are used from the analysis id and experiment id'''
        #Tested
        try:
            time_points = self.session.query(data_stage02_quantification_glogNormalized.time_point).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.time_point).order_by(
                    data_stage02_quantification_glogNormalized.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_analysisIDAndExperimentIDAndUnits_dataStage02GlogNormalized(self,analysis_id_I,experiment_id_I,calculated_concentration_units_I):
        '''Querry time points that are used from the analysis id and experiment id and concentration units'''
        #Tested
        try:
            time_points = self.session.query(data_stage02_quantification_glogNormalized.time_point).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.time_point).order_by(
                    data_stage02_quantification_glogNormalized.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # Query concentration_units from data_stage01_quantification_glogNormalized:    
    def get_concentrationUnits_experimentIDAndTimePoint_dataStage02GlogNormalized(self, experiment_id_I,time_point_I):
        """get concentration_units from experiment ID and time point"""
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).order_by(
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_concentrationUnits_analysisIDAndExperimentIDAndTimePoint_dataStage02GlogNormalized(self,analysis_id_I, experiment_id_I,time_point_I):
        """get concentration_units from analysis ID and experiment ID and time point"""
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).order_by(
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_concentrationUnits_analysisID_dataStage02GlogNormalized(self, analysis_id_I):
        """get concentration_units from analysis id"""
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).order_by(
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    # Query component_names from data_stage01_quantification_glogNormalized:    
    def get_componentNames_experimentIDAndTimePointAndUnits_dataStage02GlogNormalized(self, experiment_id_I,time_point_I, concentration_units_I):
        """get component_names from experiment ID and time point and concentration_units"""
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.component_group_name).filter(
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.component_group_name).order_by(
                    data_stage02_quantification_glogNormalized.component_name.asc()).all();
            component_names_O = [];
            component_group_names_O = [];
            for d in data: 
                component_names_O.append(d.component_name);
                component_group_names_O.append(d.component_group_name);
            return component_names_O, component_group_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_analysisIDAndExperimentIDAndTimePointAndUnits_dataStage02GlogNormalized(self,analysis_id_I, experiment_id_I,time_point_I, concentration_units_I):
        """get component_names from analysis ID and experiment ID and time point and concentration_units"""
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.component_group_name).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.component_group_name).order_by(
                    data_stage02_quantification_glogNormalized.component_name.asc()).all();
            component_names_O = [];
            component_group_names_O = [];
            for d in data: 
                component_names_O.append(d.component_name);
                component_group_names_O.append(d.component_group_name);
            return component_names_O, component_group_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_analysisIDAndUnits_dataStage02GlogNormalized(self, analysis_id_I, concentration_units_I):
        """get component_names from analysis ID and concentration_units"""
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.component_group_name).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.component_group_name).order_by(
                    data_stage02_quantification_glogNormalized.component_name.asc()).all();
            component_names_O = [];
            component_group_names_O = [];
            for d in data: 
                component_names_O.append(d.component_name);
                component_group_names_O.append(d.component_group_name);
            return component_names_O, component_group_names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query sample_name_abbreviations from data_stage01_quantification_glogNormalized:    
    def get_sampleNameAbbreviations_experimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(self, experiment_id_I,time_point_I, concentration_units_I,component_name_I,exp_type_I=4):
        """get component_names from experiment ID and time point and concentration_units and component name"""
        try:
            data = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            component_names_O = [];
            for d in data: 
                component_names_O.append(d[0]);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(self,analysis_id_I, experiment_id_I,time_point_I, concentration_units_I,component_name_I):
        """get component_names from analysis ID and experiment ID and time point and concentration_units and component name"""
        try:
            data = self.session.query(data_stage02_quantification_analysis.sample_name_abbreviation).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_analysis.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation).order_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc()).all();
            component_names_O = [];
            for d in data: 
                component_names_O.append(d[0]);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized_v1(self, analysis_id_I,concentration_units_I,component_name_I,exp_type_I=4):
        """get component_names from analysis ID and concentration_units and component name"""
        try:
            data = self.session.query(sample_description.sample_name_abbreviation).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(data_stage02_quantification_glogNormalized.experiment_id),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short)).group_by(
                    sample_description.sample_name_abbreviation).order_by(
                    sample_description.sample_name_abbreviation.asc()).all();
            component_names_O = [];
            for d in data: 
                component_names_O.append(d[0]);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized(self, analysis_id_I,concentration_units_I,component_name_I):
        """get component_names from analysis ID and concentration_units and component name"""
        try:
            data = self.session.query(data_stage02_quantification_analysis.sample_name_abbreviation).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_glogNormalized.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation).order_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc()).all();
            component_names_O = [];
            for d in data: 
                component_names_O.append(d[0]);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisIDAndUnits_dataStage02GlogNormalized(self, analysis_id_I,concentration_units_I):
        """get component_names from analysis ID and concentration_units"""
        try:
            data = self.session.query(data_stage02_quantification_analysis.sample_name_abbreviation).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(data_stage02_quantification_glogNormalized.analysis_id),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_glogNormalized.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation).order_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc()).all();
            component_names_O = [];
            for d in data: 
                component_names_O.append(d[0]);
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    # Query the calculated_concentrations from data_stage01_quantification_glogNormalized
    def get_allCalculatedConcentrations_analysisIDAndUnits_dataStage02GlogNormalized(self, analysis_id_I,concentration_units_I):
        """get all calculated_calculated concentrations by analysis_id and calculated_concentration_units from analysis ID"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_glogNormalized.calculated_concentration).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_glogNormalized.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).order_by(
                    data_stage02_quantification_glogNormalized.calculated_concentration.asc()).all();
            data_O = [];
            for d in data: 
                data_O.append(d.calculated_concentration);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_glogNormalized
    def get_RExpressionData_experimentIDAndTimePointAndUnits_dataStage02GlogNormalized(self, experiment_id_I,time_point_I,concentration_units_I,exp_type_I=4):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisIDAndExperimentIDAndTimePointAndUnits_dataStage02GlogNormalized(self,analysis_id_I, experiment_id_I,time_point_I,concentration_units_I,exp_type_I=4):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized_v1(self, analysis_id_I,concentration_units_I,exp_type_I=4):
        """get data from analysis ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    sample_description.sample_name_short.like(data_stage02_quantification_glogNormalized.sample_name_short),
                    sample_description.time_point.like(data_stage02_quantification_glogNormalized.time_point),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(data_stage02_quantification_glogNormalized.experiment_id),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(self, analysis_id_I,concentration_units_I):
        """get data from analysis ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_glogNormalized.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisIDAndUnitsAndSampleNameAbbreviation_dataStage02GlogNormalized(self, analysis_id_I,concentration_units_I,sample_name_abbreviation_I):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_analysis.analysis_id.like(data_stage02_quantification_glogNormalized.analysis_id),
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_analysis.time_point.like(data_stage02_quantification_glogNormalized.time_point),
                    data_stage02_quantification_analysis.experiment_id.like(data_stage02_quantification_glogNormalized.experiment_id),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataFrame_experimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(self, experiment_id_I,time_point_I,concentration_units_I,component_name_I,exp_type_I=4):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataFrame_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized_v1(self,analysis_id_I, experiment_id_I,time_point_I,concentration_units_I,component_name_I,exp_type_I=4):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),					
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataFrame_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNames_dataStage02GlogNormalized(self,analysis_id_I, experiment_id_I,time_point_I,concentration_units_I,component_name_I):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),		
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),					
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),			
                    data_stage02_quantification_analysis.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_analysis.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataFrame_analysisIDAndUnitsAndComponentNames_dataStage02GlogNormalized(self,analysis_id_I,concentration_units_I,component_name_I):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),		
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),					
                    data_stage02_quantification_glogNormalized.experiment_id.like(data_stage02_quantification_analysis.experiment_id),	
                    data_stage02_quantification_glogNormalized.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataList_experimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(self, experiment_id_I,time_point_I,concentration_units_I,component_name_I,sample_name_abbreviation_I,exp_type_I=4):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            concentrations_O = [];
            for d in data: 
                concentrations_O.append(d.calculated_concentration);
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O,concentrations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataList_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized_v1(self,analysis_id_I, experiment_id_I,time_point_I,concentration_units_I,component_name_I,sample_name_abbreviation_I,exp_type_I=4):
        """get data from analysis ID and experiment ID and time point and concentration_units and component name and sample name abbreviation"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            concentrations_O = [];
            for d in data: 
                concentrations_O.append(d.calculated_concentration);
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O,concentrations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataList_analysisIDAndExperimentIDAndTimePointAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(self,analysis_id_I, experiment_id_I,time_point_I,concentration_units_I,component_name_I,sample_name_abbreviation_I,exp_type_I=4):
        """get data from analysis ID and experiment ID and time point and concentration_units and component name and sample name abbreviation"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units,
                    data_stage02_quantification_glogNormalized.used_,
                    data_stage02_quantification_glogNormalized.comment_).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_analysis.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_analysis.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units,
                    data_stage02_quantification_glogNormalized.used_,
                    data_stage02_quantification_glogNormalized.comment_).all();
            data_O = [];
            concentrations_O = [];
            for d in data: 
                concentrations_O.append(d.calculated_concentration);
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_1['used_'] = d.used_;
                data_1['comment_'] = d.comment_;
                data_O.append(data_1);
            return data_O,concentrations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized_v1(self, analysis_id_I,concentration_units_I,component_name_I,sample_name_abbreviation_I,exp_type_I=4):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    sample_description.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.time_point.like(data_stage02_quantification_glogNormalized.time_point),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(data_stage02_quantification_glogNormalized.experiment_id),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            concentrations_O = [];
            for d in data: 
                concentrations_O.append(d.calculated_concentration);
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O,concentrations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RDataList_analysisIDAndUnitsAndComponentNamesAndSampleNameAbbreviation_dataStage02GlogNormalized(self, analysis_id_I,concentration_units_I,component_name_I,sample_name_abbreviation_I):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_analysis.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_analysis.time_point.like(data_stage02_quantification_glogNormalized.time_point),
                    data_stage02_quantification_analysis.experiment_id.like(data_stage02_quantification_glogNormalized.experiment_id),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.analysis_id,
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            concentrations_O = [];
            for d in data: 
                concentrations_O.append(d.calculated_concentration);
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O,concentrations_O;
        except SQLAlchemyError as e:
            print(e);
    def get_data_experimentIDAndTimePointAndUnits_dataStage02GlogNormalized(self, experiment_id_I,time_point_I,concentration_units_I):
        """get data from experiment ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).filter(
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized.experiment_id,
                    data_stage02_quantification_glogNormalized.sample_name_short,
                    data_stage02_quantification_glogNormalized.time_point,
                    data_stage02_quantification_glogNormalized.component_group_name,
                    data_stage02_quantification_glogNormalized.component_name,
                    data_stage02_quantification_glogNormalized.calculated_concentration,
                    data_stage02_quantification_glogNormalized.calculated_concentration_units).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['calculated_concentration'] = d.calculated_concentration;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowsAndSampleNameAbbreviations_analysisID_dataStage02GlogNormalized(self,analysis_id_I,used__I=True):
        '''Query rows and sample_name_abbreviation by analysis_id from data_stage02_quantification_glogNormalized and data_stage02_quantification_analysis
        '''
        try:
            data = self.session.query(
                    data_stage02_quantification_glogNormalized,
                    data_stage02_quantification_analysis.sample_name_abbreviation).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_glogNormalized.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).group_by(
                    data_stage02_quantification_glogNormalized,
                    data_stage02_quantification_analysis.sample_name_abbreviation,).order_by(
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc(),
                    data_stage02_quantification_glogNormalized.component_name.asc()).all();
            data_O = [];
            for d in data: 
                data_1 = {};
                data_1 = d.data_stage02_quantification_glogNormalized.__repr__dict__();
                data_1.update({'sample_name_abbreviation':d.sample_name_abbreviation});
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02GlogNormalized(selfanalysis_id_I,used__I=True):
        """get rows by analysis ID"""
        #Tested
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.used_.is_(used__I)).all();
            data_O = [];
            for d in data: 
                data_O.append(d.__repr__dict__());
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Update data_stage02_quantification_glogNormalized
    def update_concentrations_dataStage02GlogNormalized_v1(self, experiment_id_I, time_point_I, dataListUpdated_I):
        # update the data_stage02_quantification_glogNormalized
        updates = [];
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage02_quantification_glogNormalized).filter(
                        data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                        data_stage02_quantification_glogNormalized.sample_name_short.like(d['sample_name_short']),
                        data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                        data_stage02_quantification_glogNormalized.component_name.like(d['component_name'])).update(		
                        {
                        'calculated_concentration':d['calculated_concentration']},
                        synchronize_session=False);
                if data_update == 0:
                    print('row not found.')
                    print(d)
                updates.append(data_update);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    def update_concentrations_dataStage02GlogNormalized(self, analysis_id_I, dataListUpdated_I):
        # update the data_stage02_quantification_glogNormalized
        updates = [];
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage02_quantification_glogNormalized).filter(
                        data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                        data_stage02_quantification_glogNormalized.experiment_id.like(d['experiment_id']),
                        data_stage02_quantification_glogNormalized.sample_name_short.like(d['sample_name_short']),
                        data_stage02_quantification_glogNormalized.time_point.like(d['time_point']),
                        data_stage02_quantification_glogNormalized.component_name.like(d['component_name']),
                        data_stage02_quantification_glogNormalized.calculated_concentration_units.like(d['calculated_concentration_units'])).update(		
                        {
                        'calculated_concentration':d['calculated_concentration']},
                        synchronize_session=False);
                if data_update == 0:
                    print('row not found.')
                    print(d)
                updates.append(data_update);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();
    def update_concentrationsAndUnits_dataStage02GlogNormalized(self, experiment_id_I, time_point_I, dataListUpdated_I):
        # update the data_stage02_quantification_glogNormalized
        updates = [];
        for d in dataListUpdated_I:
            try:
                data_update = self.session.query(data_stage02_quantification_glogNormalized).filter(
                        data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                        data_stage02_quantification_glogNormalized.sample_name_short.like(d['sample_name_short']),
                        data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                        data_stage02_quantification_glogNormalized.component_name.like(d['component_name'])).update(		
                        {
                        'calculated_concentration':d['calculated_concentration'],
                        'calculated_concentration_units':d['calculated_concentration_units']},
                        synchronize_session=False);
                if data_update == 0:
                    print('row not found.')
                    print(d)
                updates.append(data_update);
            except SQLAlchemyError as e:
                print(e);
        self.session.commit();

    def add_dataStage02QuantificationGlogNormalized(self, data_I):
        '''add rows of data_stage02_quantification_pca_scores'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_glogNormalized(d
                        #d['analysis_id'],
                        #d['experiment_id'],
                        #d['sample_name_short'],
                        #d['time_point'],
                        #d['component_group_name'],
                        #d['component_name'],
                        #d['calculated_concentration'],
                        #d['calculated_concentration_units'],
                        #d['used_'],
                        #d['comment_']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def initialize_dataStage02_quantification_glogNormalized(self):
        try:
            data_stage02_quantification_glogNormalized.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification_glogNormalized(self):
        try:
            data_stage02_quantification_glogNormalized.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_glogNormalized(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_glogNormalized).filter(data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def get_rows_unique_dataStage02GlogNormalized(self, analysis_id_I,
                        experiment_id_I,
                        sample_name_short_I,
                        time_point_I,
                        component_name_I,
                        calculated_concentration_units_I):
        """get rows by analysis ID and unique
        INPUT
        analysis_id_I,experiment_id_I,sample_name_short_I,time_point_I,component_name_I,calculated_concentration_units_I"""
        try:
            data = self.session.query(data_stage02_quantification_glogNormalized).filter(
                    data_stage02_quantification_glogNormalized.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_glogNormalized.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_glogNormalized.sample_name_short.like(sample_name_short_I),
                    data_stage02_quantification_glogNormalized.time_point.like(time_point_I),
                    data_stage02_quantification_glogNormalized.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_glogNormalized.component_name.like(component_name_I),
                    data_stage02_quantification_glogNormalized.used_.is_(True)).all();
            rows_O = [];
            for d in data: 
                rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);