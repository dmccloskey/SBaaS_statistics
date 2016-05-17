#SBaaS
from .stage02_quantification_analysis_postgresql_models import *
from .stage02_quantification_pls_postgresql_models import *

from SBaaS_base.sbaas_base_query_update import sbaas_base_query_update
from SBaaS_base.sbaas_base_query_drop import sbaas_base_query_drop
from SBaaS_base.sbaas_base_query_initialize import sbaas_base_query_initialize
from SBaaS_base.sbaas_base_query_insert import sbaas_base_query_insert
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_pls_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_pls_coefficients':data_stage02_quantification_pls_coefficients,
            'data_stage02_quantification_pls_loadings':data_stage02_quantification_pls_loadings,
            'data_stage02_quantification_pls_loadingsResponse':data_stage02_quantification_pls_loadingsResponse,
            'data_stage02_quantification_pls_scores':data_stage02_quantification_pls_scores,
            'data_stage02_quantification_pls_validation':data_stage02_quantification_pls_validation,
            'data_stage02_quantification_pls_vip':data_stage02_quantification_pls_vip,
                        };
        self.set_supportedTables(tables_supported);
    # data_stage02_quantification_pls/loadings 
    # Query concentration_units from data_stage01_quantification_pca_scores:    
    def get_concentrationUnits_analysisID_dataStage02QuantificationPLSScores(self, analysis_id_I):
        """get concentration_units from analysis ID"""
        try:
            data = self.session.query(data_stage02_quantification_pls_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_pls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pls_scores.calculated_concentration_units).order_by(
                    data_stage02_quantification_pls_scores.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    # Query sample_name_short from data_stage01_quantification_pca_scores
    # Query biplot data
    def get_biPlotData_analysisID_dataStage02QuantificationPLSScores(self, analysis_id_I):
        """get data from analysis ID"""
        try:
            data_scores = self.session.query(
                    data_stage02_quantification_pls_scores.analysis_id,
                    data_stage02_quantification_pls_scores.axis,
                    data_stage02_quantification_pls_scores.var_proportion,
                    data_stage02_quantification_pls_scores.var_cumulative,
                    data_stage02_quantification_pls_scores.pls_model,
                    data_stage02_quantification_pls_scores.pls_method,
                    data_stage02_quantification_pls_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_pls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_pls_scores.analysis_id,
                    data_stage02_quantification_pls_scores.axis,
                    data_stage02_quantification_pls_scores.var_proportion,
                    data_stage02_quantification_pls_scores.var_cumulative,
                    data_stage02_quantification_pls_scores.pls_model,
                    data_stage02_quantification_pls_scores.pls_method,
                    data_stage02_quantification_pls_scores.calculated_concentration_units).order_by(
                    data_stage02_quantification_pls_scores.axis.asc(),
                    data_stage02_quantification_pls_scores.pls_model.asc(),
                    data_stage02_quantification_pls_scores.pls_method.asc(),
                    data_stage02_quantification_pls_scores.calculated_concentration_units.asc(),
                    ).all();
            data_scores_O = []; #data_loadings_O = [];
            for d in data_scores: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['axis'] = d.axis;
                data_1['var_proportion'] = d.var_proportion;
                data_1['var_cumulative'] = d.var_cumulative;
                data_1['pls_model'] = d.pls_model;
                data_1['pls_method'] = d.pls_method;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_scores_O.append(data_1);
            return data_scores_O;
        except SQLAlchemyError as e:
            print(e);
    # Query VIP data
    def get_VIPs_analysisID_dataStage02QuantificationPLSLoadings(self, analysis_id_I):
        """get VIPs by analysis ID from data_stage02_quantification_pls_loadings"""
        try:
            # query loadings
            data_loadings = self.session.query(
                data_stage02_quantification_pls_loadings.analysis_id,
                data_stage02_quantification_pls_loadings.component_name,
                data_stage02_quantification_pls_loadings.component_group_name,
                data_stage02_quantification_pls_loadings.calculated_concentration_units,
                data_stage02_quantification_pls_loadings.pls_method,
                data_stage02_quantification_pls_loadings.pls_model,
                data_stage02_quantification_pls_loadings.pls_vip).filter(
                data_stage02_quantification_pls_loadings.analysis_id.like(analysis_id_I),
                data_stage02_quantification_pls_loadings.used_.is_(True)).group_by(  
                data_stage02_quantification_pls_loadings.analysis_id,
                data_stage02_quantification_pls_loadings.component_name,
                data_stage02_quantification_pls_loadings.component_group_name,
                data_stage02_quantification_pls_loadings.calculated_concentration_units,
                data_stage02_quantification_pls_loadings.pls_method,
                data_stage02_quantification_pls_loadings.pls_model,
                data_stage02_quantification_pls_loadings.pls_vip).order_by(
                data_stage02_quantification_pls_loadings.pls_vip.asc(),
                data_stage02_quantification_pls_loadings.component_group_name.asc(),
                data_stage02_quantification_pls_loadings.calculated_concentration_units.asc(),
                data_stage02_quantification_pls_loadings.pls_method.asc(),
                data_stage02_quantification_pls_loadings.pls_model.asc()).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = {};
                data_1['analysis_id'] = d.analysis_id;
                data_1['component_name'] = d.component_name;
                data_1['component_group_name'] = d.component_group_name;
                data_1['pls_model'] = d.pls_model;
                data_1['pls_method'] = d.pls_method;
                data_1['pls_vip'] = d.pls_vip;
                data_1['calculated_concentration_units'] = d.calculated_concentration_units;
                data_loadings_O.append(data_1);
            return data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    # Query data from data_stage01_quantification_pca_scores and data_stage01_quantification_pca_loadings
    def get_RExpressionData_analysisIDAndUnits_dataStage02QuantificationPLSScoresLoadings(self, analysis_id_I,concentration_units_I):
        """get data from analysis ID"""
        try:
            data_scores = self.session.query(data_stage02_quantification_pls_scores,
                    data_stage02_quantification_analysis.sample_name_abbreviation,).filter(
                    data_stage02_quantification_pls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_scores.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_scores.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_pls_scores.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_pls_scores.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_pls_scores.used_.is_(True)).all();
            data_scores_O = []; #data_loadings_O = [];
            for d in data_scores: 
                data_1 = d.data_stage02_quantification_pls_scores.__repr__dict__();
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_scores_O.append(data_1);
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pls_loadings).filter(
                    data_stage02_quantification_pls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_loadings.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_pls_loadings.used_.is_(True)).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = d.__repr__dict__();
                data_loadings_O.append(data_1);
            return data_scores_O, data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisID_dataStage02QuantificationPLSScoresLoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            data_scores = self.session.query(data_stage02_quantification_pls_scores,
                    data_stage02_quantification_analysis.sample_name_abbreviation,).filter(
                    data_stage02_quantification_pls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_scores.axis<=axis_I,
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_scores.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_pls_scores.used_.is_(True)).all();
            data_scores_O = []; 
            for d in data_scores: 
                data_1 = {};
                data_1 = d.data_stage02_quantification_pls_scores.__repr__dict__();
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_scores_O.append(data_1);
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pls_loadings).filter(
                    data_stage02_quantification_pls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_loadings.axis<=axis_I,
                    data_stage02_quantification_pls_loadings.used_.is_(True)).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_loadings_O.append(data_1);
            return data_scores_O, data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationPLSScores(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query scores
            data_scores = self.session.query(data_stage02_quantification_pls_scores).filter(
                    data_stage02_quantification_pls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_scores.axis<=axis_I,
                    data_stage02_quantification_pls_scores.used_.is_(True)).all();
            data_scores_O = [d.__repr__dict__() for d in data_scores];
            return data_scores_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationPLSLoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pls_loadings).filter(
                    data_stage02_quantification_pls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_loadings.axis<=axis_I,
                    data_stage02_quantification_pls_loadings.used_.is_(True)).all();
            data_loadings_O = [d.__repr__dict__() for d in data_loadings];
            return data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowAxisDict_analysisID_dataStage02QuantificationPLSScores(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query scores
            data_scores = self.session.query(data_stage02_quantification_pls_scores).filter(
                    data_stage02_quantification_pls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_scores.axis<=axis_I,
                    data_stage02_quantification_pls_scores.used_.is_(True)).all();
            data_scores_O = {};
            for d in data_scores: 
                if not d.axis in data_scores_O.keys():
                    data_scores_O[d.axis]=[];
                data_scores_O[d.axis].append(d.__repr__dict__());
            return data_scores_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowAxisDict_analysisID_dataStage02QuantificationPLSLoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_pls_loadings).filter(
                    data_stage02_quantification_pls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_loadings.axis<=axis_I,
                    data_stage02_quantification_pls_loadings.used_.is_(True)).all();
            data_loadings_O = {};
            for d in data_loadings: 
                if not d.axis in data_loadings_O.keys():
                    data_loadings_O[d.axis]=[];
                data_loadings_O[d.axis].append(d.__repr__dict__());
            return data_loadings_O;
        except SQLAlchemyError as e:
            print(e);

    def reset_dataStage02_quantification_pls_scores(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pls_scores).filter(data_stage02_quantification_pls_scores.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pls_scores).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_loadings(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pls_loadings).filter(data_stage02_quantification_pls_loadings.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pls_loadings).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_validation(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pls_validation).filter(data_stage02_quantification_pls_validation.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pls_validation).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_vip(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pls_vip).filter(data_stage02_quantification_pls_vip.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pls_vip).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_loadingsResponse(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pls_loadingsResponse).filter(data_stage02_quantification_pls_loadingsResponse.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pls_loadingsResponse).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_coefficients(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_pls_coefficients).filter(data_stage02_quantification_pls_coefficients.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_pls_coefficients).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);

    # Query data from data_stage02_quantification_pls_validation
    def get_rows_analysisID_dataStage02QuantificationPLSValidation(self, analysis_id_I):
        """get rows by analysis ID from data_stage02_quantification_pls_validation"""
        try:
            data = self.session.query(data_stage02_quantification_pls_validation).filter(
                    data_stage02_quantification_pls_validation.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_pls_validation.used_.is_(True)).all();
            data_O = []; 
            for d in data: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # Query data from data_stage02_quantification_pls_vip
    def get_rows_analysisID_dataStage02QuantificationPLSVIP(self, analysis_id_I):
        """get rows by analysis ID from data_stage02_quantification_pls_vip"""
        try:
            data = self.session.query(data_stage02_quantification_pls_vip).filter(
                data_stage02_quantification_pls_vip.analysis_id.like(analysis_id_I),
                data_stage02_quantification_pls_vip.used_.is_(True)).order_by(
                data_stage02_quantification_pls_vip.pls_vip.asc(),
                data_stage02_quantification_pls_vip.response_name.asc(),
                data_stage02_quantification_pls_vip.component_name.asc(),
                data_stage02_quantification_pls_vip.calculated_concentration_units.asc(),
                data_stage02_quantification_pls_vip.pls_method.asc(),
                data_stage02_quantification_pls_vip.pls_model.asc()).all();
            data_O = []; 
            for d in data: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # Query data from data_stage02_quantification_pls_coefficients
    def get_rows_analysisID_dataStage02QuantificationPLSCoefficients(self, analysis_id_I):
        """get rows by analysis ID from data_stage02_quantification_pls_coefficients"""
        try:
            data = self.session.query(data_stage02_quantification_pls_coefficients).filter(
                data_stage02_quantification_pls_coefficients.analysis_id.like(analysis_id_I),
                data_stage02_quantification_pls_coefficients.used_.is_(True)).order_by(
                data_stage02_quantification_pls_coefficients.pls_coefficients.asc(),
                data_stage02_quantification_pls_coefficients.response_name.asc(),
                data_stage02_quantification_pls_coefficients.component_name.asc(),
                data_stage02_quantification_pls_coefficients.calculated_concentration_units.asc(),
                data_stage02_quantification_pls_coefficients.pls_method.asc(),
                data_stage02_quantification_pls_coefficients.pls_model.asc()).all();
            data_O = []; 
            for d in data: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);