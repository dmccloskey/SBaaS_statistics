#LIMS
from SBaaS_LIMS.lims_experiment_postgresql_models import *
from SBaaS_LIMS.lims_sample_postgresql_models import *
#SBaaS
from .stage02_quantification_statistics_postgresql_models import *

from SBaaS_base.sbaas_base import sbaas_base

class stage02_quantification_statistics_query(sbaas_base):
    def get_RExpressionData_AnalysisIDAndExperimentIDAndTimePointAndUnitsAndSampleNameShort_dataStage01ReplicatesMI(self, analysis_id_I,experiment_id_I,time_point_I,concentration_units_I,sample_name_short_I):
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
                    data_stage01_quantification_replicatesMI.sample_name_short,
                    data_stage01_quantification_replicatesMI.time_point,
                    data_stage01_quantification_replicatesMI.component_group_name,
                    data_stage01_quantification_replicatesMI.component_name,
                    data_stage01_quantification_replicatesMI.calculated_concentration,
                    data_stage01_quantification_replicatesMI.calculated_concentration_units).all();
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