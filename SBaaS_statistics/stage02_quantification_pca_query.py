#lims
from SBaaS_LIMS.lims_experiment_postgresql_models import *
from SBaaS_LIMS.lims_sample_postgresql_models import *

from .stage02_quantification_analysis_postgresql_models import *
from .stage02_quantification_pca_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_pca_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_pca_loadings':data_stage02_quantification_pca_loadings,
        'data_stage02_quantification_pca_scores':data_stage02_quantification_pca_scores,
        'data_stage02_quantification_pca_validation':data_stage02_quantification_pca_validation,
                        };
        self.set_supportedTables(tables_supported);
    # data_stage02_quantification_pca_scores/loadings 
    def get_experimentID_analysisIDAndUnits_dataStage02QuantificationPCAScores(self,analysis_id_I,calculated_concentration_units_I):
        '''Querry experimentID that are used from the analysis ID and calculated concentration units'''
        try:
            experiment_ids = self.session.query(data_stage02_quantification_pca_scores.experiment_id).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.experiment_id).order_by(
                    data_stage02_quantification_pca_scores.experiment_id.asc()).all();
            experiment_ids_O = [];
            for tp in experiment_ids: experiment_ids_O.append(tp.experiment_id);
            return experiment_ids_O;
        except SQLAlchemyError as e:
            print(e);
    # Query time points from data_stage02_quantification_pca_scores
    def get_timePoint_experimentID_dataStage02QuantificationPCAScores(self,experiment_id_I):
        '''Querry time points that are used from the experiment'''
        #Tested
        try:
            time_points = self.session.query(data_stage02_quantification_pca_scores.time_point).filter(
                    data_stage02_quantification_pca_scores.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.time_point).order_by(
                    data_stage02_quantification_pca_scores.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_timePoint_analysisIDAndExperimentIDAndUnits_dataStage02QuantificationPCAScores(self,analysis_id_I,experiment_id_I,calculated_concentration_units_I):
        '''Querry time points that are used from the analysis ID and experiment ID and calculated concentration Units'''
        #Tested
        try:
            time_points = self.session.query(data_stage02_quantification_pca_scores.time_point).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_pca_scores.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.time_point).order_by(
                    data_stage02_quantification_pca_scores.time_point.asc()).all();
            time_points_O = [];
            for tp in time_points: time_points_O.append(tp.time_point);
            return time_points_O;
        except SQLAlchemyError as e:
            print(e);
    # Query concentration_units from data_stage01_quantification_pca_scores:    
    def get_concentrationUnits_experimentIDAndTimePoint_dataStage02QuantificationPCAScores(self, experiment_id_I,time_point_I):
        """get concentration_units from experiment ID and time point"""
        try:
            data = self.session.query(data_stage02_quantification_pca_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_pca_scores.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pca_scores.time_point.like(time_point_I),
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.calculated_concentration_units).order_by(
                    data_stage02_quantification_pca_scores.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    def get_concentrationUnits_analysisID_dataStage02QuantificationPCAScores(self, analysis_id_I):
        """get concentration_units from analysis ID"""
        try:
            data = self.session.query(data_stage02_quantification_pca_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.calculated_concentration_units).order_by(
                    data_stage02_quantification_pca_scores.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    # Query sample_name_short from data_stage01_quantification_pca_scores
    # Query data from data_stage01_quantification_pca_scores and data_stage01_quantification_pca_loadings
    def get_RExpressionData_experimentIDAndTimePointAndUnits_dataStage02QuantificationPCAScoresLoadings(self, experiment_id_I,time_point_I,concentration_units_I,exp_type_I=4):
        """get data from experiment ID"""
        try:
            data_scores = self.session.query(data_stage02_quantification_pca_scores.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_pca_scores.sample_name_short,
                    data_stage02_quantification_pca_scores.time_point,
                    data_stage02_quantification_pca_scores.score,
                    data_stage02_quantification_pca_scores.axis,
                    data_stage02_quantification_pca_scores.var_proportion,
                    data_stage02_quantification_pca_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_pca_scores.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pca_scores.time_point.like(time_point_I),
                    data_stage02_quantification_pca_scores.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pca_scores.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_pca_scores.sample_name_short,
                    data_stage02_quantification_pca_scores.time_point,
                    data_stage02_quantification_pca_scores.score,
                    data_stage02_quantification_pca_scores.axis,
                    data_stage02_quantification_pca_scores.var_proportion,
                    data_stage02_quantification_pca_scores.calculated_concentration_units).all();
            data_scores_O = []; #data_loadings_O = [];
            for d in data_scores: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['score'] = d.score;
                data_1['axis'] = d.axis;
                data_1['var_proportion'] = d.var_proportion;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_scores_O.append(data_1);
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pca_loadings.experiment_id,
                    data_stage02_quantification_pca_loadings.axis,
                    data_stage02_quantification_pca_loadings.component_group_name,
                    data_stage02_quantification_pca_loadings.component_name,
                    data_stage02_quantification_pca_loadings.loadings,
                    data_stage02_quantification_pca_loadings.calculated_concentration_units,
                    data_stage02_quantification_pca_loadings.time_point).filter(
                    data_stage02_quantification_pca_loadings.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pca_loadings.time_point.like(time_point_I),
                    data_stage02_quantification_pca_loadings.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pca_loadings.used_.is_(True)).group_by(data_stage02_quantification_pca_loadings.experiment_id,
                    data_stage02_quantification_pca_loadings.axis,
                    data_stage02_quantification_pca_loadings.component_group_name,
                    data_stage02_quantification_pca_loadings.component_name,
                    data_stage02_quantification_pca_loadings.loadings,
                    data_stage02_quantification_pca_loadings.calculated_concentration_units,
                    data_stage02_quantification_pca_loadings.time_point).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['time_point'] = d.time_point;
                data_1['axis'] = d.axis;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['loadings'] = d.loadings;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_loadings_O.append(data_1);
            return data_scores_O, data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisIDAndExperimentIDAndTimePointAndUnits_dataStage02QuantificationPCAScoresLoadings(self, analysis_id_I, experiment_id_I,time_point_I,concentration_units_I,exp_type_I=4):
        """get data from analysis ID and experiment ID and time point and calculated concentration units"""
        try:
            data_scores = self.session.query(data_stage02_quantification_pca_scores.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_pca_scores.sample_name_short,
                    data_stage02_quantification_pca_scores.time_point,
                    data_stage02_quantification_pca_scores.score,
                    data_stage02_quantification_pca_scores.axis,
                    data_stage02_quantification_pca_scores.var_proportion,
                    data_stage02_quantification_pca_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pca_scores.time_point.like(time_point_I),
                    data_stage02_quantification_pca_scores.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pca_scores.sample_name_short.like(sample_description.sample_name_short),
                    sample_description.sample_id.like(sample.sample_id),
                    sample.sample_name.like(experiment.sample_name),
                    experiment.id.like(experiment_id_I),
                    experiment.exp_type_id == exp_type_I,
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.experiment_id,
                    sample_description.sample_name_abbreviation,
                    sample_description.sample_replicate,
                    data_stage02_quantification_pca_scores.sample_name_short,
                    data_stage02_quantification_pca_scores.time_point,
                    data_stage02_quantification_pca_scores.score,
                    data_stage02_quantification_pca_scores.axis,
                    data_stage02_quantification_pca_scores.var_proportion,
                    data_stage02_quantification_pca_scores.calculated_concentration_units).all();
            data_scores_O = []; #data_loadings_O = [];
            for d in data_scores: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_replicate'] = d.sample_replicate;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['score'] = d.score;
                data_1['axis'] = d.axis;
                data_1['var_proportion'] = d.var_proportion;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_scores_O.append(data_1);
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pca_loadings.experiment_id,
                    data_stage02_quantification_pca_loadings.axis,
                    data_stage02_quantification_pca_loadings.component_group_name,
                    data_stage02_quantification_pca_loadings.component_name,
                    data_stage02_quantification_pca_loadings.loadings,
                    data_stage02_quantification_pca_loadings.calculated_concentration_units,
                    data_stage02_quantification_pca_loadings.time_point).filter(
                    data_stage02_quantification_pca_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_loadings.experiment_id.like(experiment_id_I),
                    data_stage02_quantification_pca_loadings.time_point.like(time_point_I),
                    data_stage02_quantification_pca_loadings.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pca_loadings.used_.is_(True)).group_by(data_stage02_quantification_pca_loadings.experiment_id,
                    data_stage02_quantification_pca_loadings.axis,
                    data_stage02_quantification_pca_loadings.component_group_name,
                    data_stage02_quantification_pca_loadings.component_name,
                    data_stage02_quantification_pca_loadings.loadings,
                    data_stage02_quantification_pca_loadings.calculated_concentration_units,
                    data_stage02_quantification_pca_loadings.time_point).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = {};
                data_1['experiment_id'] = d.experiment_id;
                data_1['time_point'] = d.time_point;
                data_1['axis'] = d.axis;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['loadings'] = d.loadings;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_loadings_O.append(data_1);
            return data_scores_O, data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisIDAndUnits_dataStage02QuantificationPCAScoresLoadings(self, analysis_id_I,concentration_units_I):
        """get data from analysis ID"""
        try:
            data_scores = self.session.query(data_stage02_quantification_pca_scores.analysis_id,
                    data_stage02_quantification_pca_scores.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_pca_scores.sample_name_short,
                    data_stage02_quantification_pca_scores.time_point,
                    data_stage02_quantification_pca_scores.score,
                    data_stage02_quantification_pca_scores.axis,
                    data_stage02_quantification_pca_scores.var_proportion,
                    data_stage02_quantification_pca_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_pca_scores.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_pca_scores.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.analysis_id,
                    data_stage02_quantification_pca_scores.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_pca_scores.sample_name_short,
                    data_stage02_quantification_pca_scores.time_point,
                    data_stage02_quantification_pca_scores.score,
                    data_stage02_quantification_pca_scores.axis,
                    data_stage02_quantification_pca_scores.var_proportion,
                    data_stage02_quantification_pca_scores.calculated_concentration_units).all();
            data_scores_O = []; #data_loadings_O = [];
            for d in data_scores: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_1['sample_name_short'] = d.sample_name_short;
                data_1['time_point'] = d.time_point;
                data_1['score'] = d.score;
                data_1['axis'] = d.axis;
                data_1['var_proportion'] = d.var_proportion;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_scores_O.append(data_1);
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pca_loadings.analysis_id,
                    data_stage02_quantification_pca_loadings.experiment_id,
                    data_stage02_quantification_pca_loadings.axis,
                    data_stage02_quantification_pca_loadings.component_group_name,
                    data_stage02_quantification_pca_loadings.component_name,
                    data_stage02_quantification_pca_loadings.loadings,
                    data_stage02_quantification_pca_loadings.calculated_concentration_units,
                    data_stage02_quantification_pca_loadings.time_point).filter(
                    data_stage02_quantification_pca_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_loadings.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pca_loadings.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_loadings.analysis_id,
                    data_stage02_quantification_pca_loadings.experiment_id,
                    data_stage02_quantification_pca_loadings.axis,
                    data_stage02_quantification_pca_loadings.component_group_name,
                    data_stage02_quantification_pca_loadings.component_name,
                    data_stage02_quantification_pca_loadings.loadings,
                    data_stage02_quantification_pca_loadings.calculated_concentration_units,
                    data_stage02_quantification_pca_loadings.time_point).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['experiment_id'] = d.experiment_id;
                data_1['time_point'] = d.time_point;
                data_1['axis'] = d.axis;
                data_1['component_group_name'] = d.component_group_name;
                data_1['component_name'] = d.component_name;
                data_1['loadings'] = d.loadings;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_loadings_O.append(data_1);
            return data_scores_O, data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisID_dataStage02QuantificationPCAScoresLoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            #data_scores = self.session.query(data_stage02_quantification_pca_scores.analysis_id,
            #        data_stage02_quantification_analysis.sample_name_abbreviation,
            #        data_stage02_quantification_pca_scores.sample_name_short,
            #        data_stage02_quantification_pca_scores.score,
            #        data_stage02_quantification_pca_scores.axis,
            #        data_stage02_quantification_pca_scores.var_proportion,
            #        data_stage02_quantification_pca_scores.var_cumulative,
            #        data_stage02_quantification_pca_scores.calculated_concentration_units).filter(
            #        data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
            #        data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
            #        data_stage02_quantification_pca_scores.axis<=axis_I,
            #        data_stage02_quantification_pca_scores.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
            #        data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
            #        data_stage02_quantification_pca_scores.analysis_id,
            #        data_stage02_quantification_analysis.sample_name_abbreviation,
            #        data_stage02_quantification_pca_scores.sample_name_short,
            #        data_stage02_quantification_pca_scores.score,
            #        data_stage02_quantification_pca_scores.axis,
            #        data_stage02_quantification_pca_scores.var_proportion,
            #        data_stage02_quantification_pca_scores.var_cumulative,
            #        data_stage02_quantification_pca_scores.calculated_concentration_units).all();
            data_scores = self.session.query(data_stage02_quantification_pca_scores).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.axis<=axis_I,
                    data_stage02_quantification_pca_scores.used_.is_(True)).order_by(
                    data_stage02_quantification_pca_scores.axis.asc(),
                    data_stage02_quantification_pca_scores.sample_name_short.asc(),
                    data_stage02_quantification_pca_scores.calculated_concentration_units.asc()).all();
            data_scores_O = []; #data_loadings_O = [];
            for d in data_scores: 
                data_scores_O.append(d.__repr__dict__());
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pca_loadings).filter(
                    data_stage02_quantification_pca_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_loadings.axis<=axis_I,
                    data_stage02_quantification_pca_loadings.used_.is_(True)).order_by(
                    data_stage02_quantification_pca_loadings.axis.asc(),
                    data_stage02_quantification_pca_loadings.component_name.asc(),
                    data_stage02_quantification_pca_loadings.calculated_concentration_units.asc()).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_loadings_O.append(d.__repr__dict__());
            return data_scores_O, data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationPCALoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pca_loadings).filter(
                    data_stage02_quantification_pca_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_loadings.axis<=axis_I,
                    data_stage02_quantification_pca_loadings.used_.is_(True)).all();
            data_loadings_O = [d.__repr__dict__() for d in data_loadings];
            return data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationPCAScores(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query scores
            data_scores = self.session.query(data_stage02_quantification_pca_scores).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.axis<=axis_I,
                    data_stage02_quantification_pca_scores.used_.is_(True)).all();
            data_scores_O = [d.__repr__dict__() for d in data_scores];
            return data_scores_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowAxisDict_analysisID_dataStage02QuantificationPCAScores(self, analysis_id_I,axis_I=3):
        """get rows from analysis ID"""
        try:
            # query scores
            #data_scores = self.session.query(data_stage02_quantification_pca_scores.analysis_id,
            #        data_stage02_quantification_analysis.sample_name_abbreviation,
            #        data_stage02_quantification_pca_scores.sample_name_short,
            #        data_stage02_quantification_pca_scores.score,
            #        data_stage02_quantification_pca_scores.axis,
            #        data_stage02_quantification_pca_scores.var_proportion,
            #        data_stage02_quantification_pca_scores.var_cumulative,
            #        data_stage02_quantification_pca_scores.calculated_concentration_units).filter(
            #        data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
            #        data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
            #        data_stage02_quantification_pca_scores.axis<=axis_I,
            #        data_stage02_quantification_pca_scores.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
            #        data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
            #        data_stage02_quantification_pca_scores.analysis_id,
            #        data_stage02_quantification_analysis.sample_name_abbreviation,
            #        data_stage02_quantification_pca_scores.sample_name_short,
            #        data_stage02_quantification_pca_scores.score,
            #        data_stage02_quantification_pca_scores.axis,
            #        data_stage02_quantification_pca_scores.var_proportion,
            #        data_stage02_quantification_pca_scores.var_cumulative,
            #        data_stage02_quantification_pca_scores.calculated_concentration_units).order_by(
            #        data_stage02_quantification_pca_scores.axis.asc(),
            #        data_stage02_quantification_pca_scores.sample_name_short.asc(),
            #        data_stage02_quantification_pca_scores.calculated_concentration_units.asc()).all();
            data_scores = self.session.query(data_stage02_quantification_pca_scores).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.axis<=axis_I,
                    data_stage02_quantification_pca_scores.used_.is_(True)).order_by(
                    data_stage02_quantification_pca_scores.axis.asc(),
                    data_stage02_quantification_pca_scores.sample_name_short.asc(),
                    data_stage02_quantification_pca_scores.calculated_concentration_units.asc()).all();
            data_scores_O = {};
            for d in data_scores: 
                if not d.axis in data_scores_O.keys():
                    data_scores_O[d.axis]=[];
                data_scores_O[d.axis].append(d.__repr__dict__());
            return data_scores_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowAxisDict_analysisID_dataStage02QuantificationPCALoadings(self, analysis_id_I,axis_I=3):
        """get rows from analysis ID"""
        try:
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pca_loadings).filter(
                    data_stage02_quantification_pca_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_loadings.axis<=axis_I,
                    data_stage02_quantification_pca_loadings.used_.is_(True)).order_by(
                    data_stage02_quantification_pca_loadings.axis.asc(),
                    data_stage02_quantification_pca_loadings.component_name.asc(),
                    data_stage02_quantification_pca_loadings.calculated_concentration_units.asc(),
                    ).all();
            data_loadings_O = {};
            for d in data_loadings: 
                if not d.axis in data_loadings_O.keys():
                    data_loadings_O[d.axis]=[];
                data_loadings_O[d.axis].append(d.__repr__dict__());
            return data_loadings_O;
        except SQLAlchemyError as e:
            print(e);

    def initialize_dataStage02_quantification_pca(self):
        try:
            data_stage02_quantification_pca_scores.__table__.create(self.engine,True);
            data_stage02_quantification_pca_loadings.__table__.create(self.engine,True);
            data_stage02_quantification_pca_validation.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification_pca(self):
        try:
            data_stage02_quantification_pca_scores.__table__.drop(self.engine,True);
            data_stage02_quantification_pca_loadings.__table__.drop(self.engine,True);
            data_stage02_quantification_pca_validation.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pca_scores(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pca_scores).filter(data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pca_scores).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pca_loadings(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pca_loadings).filter(data_stage02_quantification_pca_loadings.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pca_loadings).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pca_validation(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pca_validation).filter(data_stage02_quantification_pca_validation.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pca_validation).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);

    def add_dataStage02QuantificationPCAScores(self, data_I):
        '''add rows of data_stage02_quantification_pca_scores'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_pca_scores(d
                        #d['analysis_id'],
                        #d['sample_name_short'],
                        #d['sample_name_abbreviation'],
                        #d['score'],
                        #d['axis'],
                        #d['var_proportion'],
                        #d['var_cumulative'],
                        #d['pca_model'],
                        #d['pca_method'],
                        #d['pca_options'],
                        #d['calculated_concentration_units'],
                        #d['used_'],
                        #d['comment_']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationPCAScores(self,data_I):
        '''update rows of data_stage02_quantification_pca_scores'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_pca_scores).filter(
                            data_stage02_quantification_pca_scores.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'sample_name_short':d['sample_name_short'],
                            'sample_name_abbreviation':d['sample_name_abbreviation'],
                            'score':d['score'],
                            'axis':d['axis'],
                            'var_proportion':d['var_proportion'],
                            'var_cumulative':d['var_cumulative'],
                            'pca_model':d['pca_model'],
                            'pca_method':d['pca_method'],
                            'pca_options':d['pca_options'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_dataStage02QuantificationPCALoadings(self, data_I):
        '''add rows of data_stage02_quantification_pca_loadings'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_pca_loadings(d
                        #d['analysis_id'],
                        #d['component_group_name'],
                        #d['component_name'],
                        #d['loadings'],
                        #d['axis'],
                        #d['correlations'],
                        #d['pca_model'],
                        #d['pca_method'],
                        #d['pca_options'],
                        #d['calculated_concentration_units'],
                        #d['used_'],
                        #d['comment_']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationPCALoadings(self,data_I):
        '''update rows of data_stage02_quantification_pca_loadings'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_pca_loadings).filter(
                            data_stage02_quantification_pca_loadings.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'component_group_name':d['component_group_name'],
                            'component_name':d['component_name'],
                            'loadings':d['loadings'],
                            'axis':d['axis'],
                            'correlations':d['correlations'],
                            'pca_model':d['pca_model'],
                            'pca_method':d['pca_method'],
                            'pca_options':d['pca_options'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();         
    def add_dataStage02QuantificationPCAValidation(self, data_I):
        '''add rows of data_stage02_quantification_pca_validation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_pca_validation(d
                        #d['analysis_id'],
                        #d['pca_model'],
                        #d['pca_method'],
                        #d['pca_msep'],
                        #d['pca_rmsep'],
                        #d['pca_r2'],
                        #d['pca_q2'],
                        #d['pca_options'],
                        #d['crossValidation_ncomp'],
                        #d['crossValidation_method'],
                        #d['crossValidation_options'],
                        #d['permutation_nperm'],
                        #d['permutation_pvalue'],
                        #d['permutation_pvalue_corrected'],
                        #d['permutation_pvalue_corrected_description'],
                        #d['permutation_options'],
                        #d['calculated_concentration_units'],
                        #d['used_'],
                        #d['comment_']
                        );
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationPCAValidation(self,data_I):
        '''update rows of data_stage02_quantification_pca_validation'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_pca_validation).filter(
                            data_stage02_quantification_pca_validation.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'pca_model':d['pca_model'],
                            'pca_method':d['pca_method'],
                            'pca_scale':d['pca_scale'],
                            'pca_msep':d['pca_msep'],
                            'pca_rmsep':d['pca_rmsep'],
                            'pca_r2':d['pca_r2'],
                            'pca_q2':d['pca_q2'],
                            'pca_options':d['pca_options'],
                            'crossValidation_ncomp':d['crossValidation_ncomp'],
                            'crossValidation_method':d['crossValidation_method'],
                            'crossValidation_options':d['crossValidation_options'],
                            'permutation_nperm':d['permutation_nperm'],
                            'permutation_pvalue':d['permutation_pvalue'],
                            'permutation_pvalue_corrected':d['permutation_pvalue_corrected'],
                            'permutation_pvalue_corrected_description':d['permutation_pvalue_corrected_description'],
                            'permutation_options':d['permutation_options'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    # Query data from data_stage02_quantification_pca_validation
    def get_rows_analysisID_dataStage02QuantificationPCAValidation(self, analysis_id_I):
        """get rows by analysis ID from data_stage02_quantification_pca_validation"""
        try:
            data = self.session.query(data_stage02_quantification_pca_validation).filter(
                    data_stage02_quantification_pca_validation.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_validation.used_.is_(True)).all();
            data_O = []; 
            for d in data: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Query biplot data
    def get_biPlotData_analysisID_dataStage02QuantificationPCAScores(self, analysis_id_I):
        """get data from analysis ID"""
        try:
            data_scores = self.session.query(
                    data_stage02_quantification_pca_scores.analysis_id,
                    data_stage02_quantification_pca_scores.axis,
                    data_stage02_quantification_pca_scores.var_proportion,
                    data_stage02_quantification_pca_scores.var_cumulative,
                    data_stage02_quantification_pca_scores.pca_model,
                    data_stage02_quantification_pca_scores.pca_method,
                    data_stage02_quantification_pca_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_pca_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pca_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pca_scores.analysis_id,
                    data_stage02_quantification_pca_scores.axis,
                    data_stage02_quantification_pca_scores.var_proportion,
                    data_stage02_quantification_pca_scores.var_cumulative,
                    data_stage02_quantification_pca_scores.pca_model,
                    data_stage02_quantification_pca_scores.pca_method,
                    data_stage02_quantification_pca_scores.calculated_concentration_units).order_by(
                    data_stage02_quantification_pca_scores.axis.asc(),
                    data_stage02_quantification_pca_scores.pca_model.asc(),
                    data_stage02_quantification_pca_scores.pca_method.asc(),
                    data_stage02_quantification_pca_scores.calculated_concentration_units.asc(),
                    ).all();
            data_scores_O = []; #data_loadings_O = [];
            for d in data_scores: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['axis'] = d.axis;
                data_1['var_proportion'] = d.var_proportion;
                data_1['var_cumulative'] = d.var_cumulative;
                data_1['pca_model'] = d.pca_model;
                data_1['pca_method'] = d.pca_method;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_scores_O.append(data_1);
            return data_scores_O;
        except SQLAlchemyError as e:
            print(e);