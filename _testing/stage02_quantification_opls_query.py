#SBaaS
from .stage02_quantification_analysis_postgresql_models import *
from .stage02_quantification_opls_postgresql_models import *

from SBaaS_base.sbaas_base import sbaas_base

class stage02_quantification_opls_query(sbaas_base):
    # data_stage02_quantification_opls/loadings 
    # Query concentration_units from data_stage01_quantification_pca_scores:    
    def get_concentrationUnits_analysisID_dataStage02QuantificationOPLSScores(self, analysis_id_I):
        """get concentration_units from analysis ID"""
        try:
            data = self.session.query(data_stage02_quantification_opls_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_opls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_opls_scores.calculated_concentration_units).order_by(
                    data_stage02_quantification_opls_scores.calculated_concentration_units.asc()).all();
            units_O = [];
            for d in data: 
                units_O.append(d[0]);
            return units_O;
        except SQLAlchemyError as e:
            print(e);
    # Query sample_name_short from data_stage01_quantification_pca_scores
    # Query biplot data
    def get_biPlotData_analysisID_dataStage02QuantificationOPLSScores(self, analysis_id_I):
        """get data from analysis ID"""
        try:
            data_scores = self.session.query(
                    data_stage02_quantification_opls_scores.analysis_id,
                    data_stage02_quantification_opls_scores.axis,
                    data_stage02_quantification_opls_scores.var_proportion,
                    data_stage02_quantification_opls_scores.var_cumulative,
                    data_stage02_quantification_opls_scores.pls_model,
                    data_stage02_quantification_opls_scores.pls_method,
                    data_stage02_quantification_opls_scores.calculated_concentration_units).filter(
                    data_stage02_quantification_opls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_scores.used_.is_(True)).group_by(
                    data_stage02_quantification_opls_scores.analysis_id,
                    data_stage02_quantification_opls_scores.axis,
                    data_stage02_quantification_opls_scores.var_proportion,
                    data_stage02_quantification_opls_scores.var_cumulative,
                    data_stage02_quantification_opls_scores.pls_model,
                    data_stage02_quantification_opls_scores.pls_method,
                    data_stage02_quantification_opls_scores.calculated_concentration_units).order_by(
                    data_stage02_quantification_opls_scores.axis.asc(),
                    data_stage02_quantification_opls_scores.pls_model.asc(),
                    data_stage02_quantification_opls_scores.pls_method.asc(),
                    data_stage02_quantification_opls_scores.calculated_concentration_units.asc(),
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
    def get_VIPs_analysisID_dataStage02QuantificationOPLSLoadings(self, analysis_id_I):
        """get VIPs by analysis ID from data_stage02_quantification_opls_loadings"""
        try:
            # query loadings
            data_loadings = self.session.query(
                data_stage02_quantification_opls_loadings.analysis_id,
                data_stage02_quantification_opls_loadings.component_name,
                data_stage02_quantification_opls_loadings.component_group_name,
                data_stage02_quantification_opls_loadings.calculated_concentration_units,
                data_stage02_quantification_opls_loadings.pls_method,
                data_stage02_quantification_opls_loadings.pls_model,
                data_stage02_quantification_opls_loadings.pls_vip).filter(
                data_stage02_quantification_opls_loadings.analysis_id.like(analysis_id_I),
                data_stage02_quantification_opls_loadings.used_.is_(True)).group_by(  
                data_stage02_quantification_opls_loadings.analysis_id,
                data_stage02_quantification_opls_loadings.component_name,
                data_stage02_quantification_opls_loadings.component_group_name,
                data_stage02_quantification_opls_loadings.calculated_concentration_units,
                data_stage02_quantification_opls_loadings.pls_method,
                data_stage02_quantification_opls_loadings.pls_model,
                data_stage02_quantification_opls_loadings.pls_vip).order_by(
                data_stage02_quantification_opls_loadings.pls_vip.asc(),
                data_stage02_quantification_opls_loadings.component_group_name.asc(),
                data_stage02_quantification_opls_loadings.calculated_concentration_units.asc(),
                data_stage02_quantification_opls_loadings.pls_method.asc(),
                data_stage02_quantification_opls_loadings.pls_model.asc()).all();
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
    def get_RExpressionData_analysisIDAndUnits_dataStage02QuantificationOPLSScoresLoadings(self, analysis_id_I,concentration_units_I):
        """get data from analysis ID"""
        try:
            data_scores = self.session.query(data_stage02_quantification_opls_scores,
                    data_stage02_quantification_analysis.sample_name_abbreviation,).filter(
                    data_stage02_quantification_opls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_scores.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_scores.experiment_id.like(data_stage02_quantification_analysis.experiment_id),
                    data_stage02_quantification_opls_scores.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_opls_scores.time_point.like(data_stage02_quantification_analysis.time_point),
                    data_stage02_quantification_opls_scores.used_.is_(True)).all();
            data_scores_O = []; #data_loadings_O = [];
            for d in data_scores: 
                data_1 = d.data_stage02_quantification_opls_scores.__repr__dict__();
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_scores_O.append(data_1);
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_opls_loadings).filter(
                    data_stage02_quantification_opls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_loadings.calculated_concentration_units.like(concentration_units_I),
                    data_stage02_quantification_opls_loadings.used_.is_(True)).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = d.__repr__dict__();
                data_loadings_O.append(data_1);
            return data_scores_O, data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_RExpressionData_analysisID_dataStage02QuantificationOPLSScoresLoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            data_scores = self.session.query(data_stage02_quantification_opls_scores,
                    data_stage02_quantification_analysis.sample_name_abbreviation,).filter(
                    data_stage02_quantification_opls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_scores.axis<=axis_I,
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_scores.sample_name_short.like(data_stage02_quantification_analysis.sample_name_short),
                    data_stage02_quantification_opls_scores.used_.is_(True)).all();
            data_scores_O = []; 
            for d in data_scores: 
                data_1 = {};
                data_1 = d.data_stage02_quantification_opls_scores.__repr__dict__();
                data_1['sample_name_abbreviation'] = d.sample_name_abbreviation;
                data_scores_O.append(data_1);
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_opls_loadings).filter(
                    data_stage02_quantification_opls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_loadings.axis<=axis_I,
                    data_stage02_quantification_opls_loadings.used_.is_(True)).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_loadings_O.append(data_1);
            return data_scores_O, data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisID_dataStage02QuantificationOPLSLoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_opls_loadings).filter(
                    data_stage02_quantification_opls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_loadings.axis<=axis_I,
                    data_stage02_quantification_opls_loadings.used_.is_(True)).all();
            data_loadings_O = [];
            for d in data_loadings: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_loadings_O.append(data_1);
            return data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowAxisDict_analysisID_dataStage02QuantificationOPLSScores(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query scores
            data_scores = self.session.query(data_stage02_quantification_opls_scores).filter(
                    data_stage02_quantification_opls_scores.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_scores.axis<=axis_I,
                    data_stage02_quantification_opls_scores.used_.is_(True)).all();
            data_scores_O = {};
            for d in data_scores: 
                if not d.axis in data_scores_O.keys():
                    data_scores_O[d.axis]=[];
                data_scores_O[d.axis].append(d.__repr__dict__());
            return data_scores_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rowAxisDict_analysisID_dataStage02QuantificationOPLSLoadings(self, analysis_id_I,axis_I=3):
        """get data from analysis ID"""
        try:
            # query loadings
            data_loadings = self.session.query(data_stage02_quantification_opls_loadings).filter(
                    data_stage02_quantification_opls_loadings.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_loadings.axis<=axis_I,
                    data_stage02_quantification_opls_loadings.used_.is_(True)).all();
            data_loadings_O = {};
            for d in data_loadings: 
                if not d.axis in data_loadings_O.keys():
                    data_loadings_O[d.axis]=[];
                data_loadings_O[d.axis].append(d.__repr__dict__());
            return data_loadings_O;
        except SQLAlchemyError as e:
            print(e);
    def initialize_dataStage02_quantification_pls(self):
        try:
            data_stage02_quantification_opls_scores.__table__.create(self.engine,True);
            data_stage02_quantification_opls_loadings.__table__.create(self.engine,True);
            data_stage02_quantification_opls_validation.__table__.create(self.engine,True);
            data_stage02_quantification_opls_vip.__table__.create(self.engine,True);
            data_stage02_quantification_opls_coefficients.__table__.create(self.engine,True);
            data_stage02_quantification_opls_loadingsResponse.__table__.create(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def drop_dataStage02_quantification_pls(self):
        try:
            data_stage02_quantification_opls_scores.__table__.drop(self.engine,True);
            data_stage02_quantification_opls_loadings.__table__.drop(self.engine,True);
            data_stage02_quantification_opls_validation.__table__.drop(self.engine,True);
            data_stage02_quantification_opls_vip.__table__.drop(self.engine,True);
            data_stage02_quantification_opls_coefficients.__table__.drop(self.engine,True);
            data_stage02_quantification_opls_loadingsResponse.__table__.drop(self.engine,True);
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_scores(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_opls_scores).filter(data_stage02_quantification_opls_scores.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_opls_scores).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_loadings(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_opls_loadings).filter(data_stage02_quantification_opls_loadings.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_opls_loadings).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_validation(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_opls_validation).filter(data_stage02_quantification_opls_validation.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_opls_validation).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_vip(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_opls_vip).filter(data_stage02_quantification_opls_vip.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_opls_vip).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_loadingsResponse(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_opls_loadingsResponse).filter(data_stage02_quantification_opls_loadingsResponse.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_opls_loadingsResponse).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);
    def reset_dataStage02_quantification_pls_coefficients(self,analysis_id_I = None):
        try:
            if analysis_id_I:
                reset = self.session.query(data_stage02_quantification_opls_coefficients).filter(data_stage02_quantification_opls_coefficients.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
            else:
                reset = self.session.query(data_stage02_quantification_opls_coefficients).delete(synchronize_session=False);
            self.session.commit();
        except SQLAlchemyError as e:
            print(e);

    def add_dataStage02QuantificationOPLSScores(self, data_I):
        '''add rows of data_stage02_quantification_opls_scores'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_opls_scores(
                        d['analysis_id'],
                        d['sample_name_short'],
                        d['response_name'],
                        d['score'],
                        d['score_response'],
                        d['axis'],
                        d['var_proportion'],
                        d['var_cumulative'],
                        d['pls_model'],
                        d['pls_method'],
                        d['pls_options'],
                        d['calculated_concentration_units'],
                        d['used_'],
                        d['comment_'],);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationOPLSScores(self,data_I):
        '''update rows of data_stage02_quantification_opls_scores'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_opls_scores).filter(
                            data_stage02_quantification_opls_scores.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'sample_name_short':d['sample_name_short'],
                            'response_name':d['response_name'],
                            'score':d['score'],
                            'score_response':d['score_response'],
                            'axis':d['axis'],
                            'var_proportion':d['var_proportion'],
                            'var_cumulative':d['var_cumulative'],
                            'pls_model':d['pls_model'],
                            'pls_method':d['pls_method'],
                            'pls_options':d['pls_options'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def add_dataStage02QuantificationOPLSLoadings(self, data_I):
        '''add rows of data_stage02_quantification_opls_loadings'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_opls_loadings(
                        d['analysis_id'],
                        d['component_group_name'],
                        d['component_name'],
                        d['loadings'],
                        d['axis'],
                        d['correlations'],
                        d['pls_model'],
                        d['pls_method'],
                        d['pls_options'],
                        d['calculated_concentration_units'],
                        d['used_'],
                        d['comment_'],);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationOPLSLoadings(self,data_I):
        '''update rows of data_stage02_quantification_opls_loadings'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_opls_loadings).filter(
                            data_stage02_quantification_opls_loadings.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'component_group_name':d['component_group_name'],
                            'component_name':d['component_name'],
                            'loadings':d['loadings'],
                            'axis':d['axis'],
                            'correlations':d['correlations'],
                            'pls_model':d['pls_model'],
                            'pls_method':d['pls_method'],
                            'pls_options':d['pls_options'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();         
    def add_dataStage02QuantificationOPLSValidation(self, data_I):
        '''add rows of data_stage02_quantification_opls_validation'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_opls_validation(
                        d['analysis_id'],
                        d['pls_model'],
                        d['pls_method'],
                        d['pls_msep'],
                        d['pls_rmsep'],
                        d['pls_r2'],
                        d['pls_r2x'],
                        d['pls_q2'],
                        d['pls_options'],
                        d['crossValidation_ncomp'],
                        d['crossValidation_method'],
                        d['crossValidation_options'],
                        d['permutation_nperm'],
                        d['permutation_pvalue'],
                        d['permutation_pvalue_corrected'],
                        d['permutation_pvalue_corrected_description'],
                        d['permutation_options'],
                        d['calculated_concentration_units'],
                        d['used_'],
                        d['comment_'],);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationOPLSValidation(self,data_I):
        '''update rows of data_stage02_quantification_opls_validation'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_opls_validation).filter(
                            data_stage02_quantification_opls_validation.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'pls_model':d['pls_model'],
                            'pls_method':d['pls_method'],
                            'pls_scale':d['pls_scale'],
                            'pls_msep':d['pls_msep'],
                            'pls_rmsep':d['pls_rmsep'],
                            'pls_r2':d['pls_r2'],
                            'pls_r2x':d['pls_r2x'],
                            'pls_q2':d['pls_q2'],
                            'pls_options':d['pls_options'],
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
    def add_dataStage02QuantificationOPLSVIP(self, data_I):
        '''add rows of data_stage02_quantification_opls_vip'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_opls_vip(
                        d['analysis_id'],
                        d['response_name'],
                        d['component_group_name'],
                        d['component_name'],
                        d['pls_vip'],
                        d['pls_model'],
                        d['pls_method'],
                        d['pls_options'],
                        d['calculated_concentration_units'],
                        d['used_'],
                        d['comment_'],);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationOPLSVIP(self,data_I):
        '''update rows of data_stage02_quantification_opls_vip'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_opls_vip).filter(
                            data_stage02_quantification_opls_vip.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'response_name':d['response_name'],
                            'component_group_name':d['component_group_name'],
                            'component_name':d['component_name'],
                            'pls_vip':d['pls_vip'],
                            'pls_model':d['pls_model'],
                            'pls_method':d['pls_method'],
                            'pls_options':d['pls_options'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit(); 
    def add_dataStage02QuantificationOPLSCoefficients(self, data_I):
        '''add rows of data_stage02_quantification_opls_coefficients'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_opls_coefficients(
                        d['analysis_id'],
                        d['response_name'],
                        d['component_group_name'],
                        d['component_name'],
                        d['pls_coefficients'],
                        d['pls_model'],
                        d['pls_method'],
                        d['pls_options'],
                        d['calculated_concentration_units'],
                        d['used_'],
                        d['comment_'],);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationOPLSCoefficients(self,data_I):
        '''update rows of data_stage02_quantification_opls_coefficients'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_opls_coefficients).filter(
                            data_stage02_quantification_opls_coefficients.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'response_name':d['response_name'],
                            'component_group_name':d['component_group_name'],
                            'component_name':d['component_name'],
                            'pls_coefficients':d['pls_coefficients'],
                            'pls_model':d['pls_model'],
                            'pls_method':d['pls_method'],
                            'pls_options':d['pls_options'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit(); 
    def add_dataStage02QuantificationOPLSLoadingsResponse(self, data_I):
        '''add rows of data_stage02_quantification_opls_loadings'''
        if data_I:
            for d in data_I:
                try:
                    data_add = data_stage02_quantification_opls_loadingsResponse(
                        d['analysis_id'],
                        d['response_name'],
                        d['loadings_response'],
                        d['axis'],
                        d['correlations_response'],
                        d['pls_model'],
                        d['pls_method'],
                        d['pls_options'],
                        d['calculated_concentration_units'],
                        d['used_'],
                        d['comment_'],);
                    self.session.add(data_add);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();
    def update_dataStage02QuantificationOPLSLoadingsResponse(self,data_I):
        '''update rows of data_stage02_quantification_opls_loadingsResponse'''
        if data_I:
            for d in data_I:
                try:
                    data_update = self.session.query(data_stage02_quantification_opls_loadingsResponse).filter(
                            data_stage02_quantification_opls_loadingsResponse.id.like(d['id'])).update(
                            {
                            'analysis_id':d['analysis_id'],
                            'response_name':d['response_name'],
                            'loadings_response':d['loadings_response'],
                            'axis':d['axis'],
                            'correlations_response':d['correlations_response'],
                            'pls_model':d['pls_model'],
                            'pls_method':d['pls_method'],
                            'pls_options':d['pls_options'],
                            'calculated_concentration_units':d['calculated_concentration_units'],
                            'used_':d['used_'],
                            'comment_':d['comment_'],},
                            synchronize_session=False);
                except SQLAlchemyError as e:
                    print(e);
            self.session.commit();

    # Query data from data_stage02_quantification_opls_validation
    def get_rows_analysisID_dataStage02QuantificationOPLSValidation(self, analysis_id_I):
        """get rows by analysis ID from data_stage02_quantification_opls_validation"""
        try:
            data = self.session.query(data_stage02_quantification_opls_validation).filter(
                    data_stage02_quantification_opls_validation.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_opls_validation.used_.is_(True)).all();
            data_O = []; 
            for d in data: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # Query data from data_stage02_quantification_opls_vip
    def get_rows_analysisID_dataStage02QuantificationOPLSVIP(self, analysis_id_I):
        """get rows by analysis ID from data_stage02_quantification_opls_vip"""
        try:
            data = self.session.query(data_stage02_quantification_opls_vip).filter(
                data_stage02_quantification_opls_vip.analysis_id.like(analysis_id_I),
                data_stage02_quantification_opls_vip.used_.is_(True)).order_by(
                data_stage02_quantification_opls_vip.pls_vip.asc(),
                data_stage02_quantification_opls_vip.response_name.asc(),
                data_stage02_quantification_opls_vip.component_name.asc(),
                data_stage02_quantification_opls_vip.calculated_concentration_units.asc(),
                data_stage02_quantification_opls_vip.pls_method.asc(),
                data_stage02_quantification_opls_vip.pls_model.asc()).all();
            data_O = []; 
            for d in data: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);

    # Query data from data_stage02_quantification_opls_coefficients
    def get_rows_analysisID_dataStage02QuantificationOPLSCoefficients(self, analysis_id_I):
        """get rows by analysis ID from data_stage02_quantification_opls_coefficients"""
        try:
            data = self.session.query(data_stage02_quantification_opls_coefficients).filter(
                data_stage02_quantification_opls_coefficients.analysis_id.like(analysis_id_I),
                data_stage02_quantification_opls_coefficients.used_.is_(True)).order_by(
                data_stage02_quantification_opls_coefficients.pls_coefficients.asc(),
                data_stage02_quantification_opls_coefficients.response_name.asc(),
                data_stage02_quantification_opls_coefficients.component_name.asc(),
                data_stage02_quantification_opls_coefficients.calculated_concentration_units.asc(),
                data_stage02_quantification_opls_coefficients.pls_method.asc(),
                data_stage02_quantification_opls_coefficients.pls_model.asc()).all();
            data_O = []; 
            for d in data: 
                data_1 = {};
                data_1 = d.__repr__dict__();
                data_O.append(data_1);
            return data_O;
        except SQLAlchemyError as e:
            print(e);