
from .stage02_quantification_opls_io import stage02_quantification_opls_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from matplotlib_utilities.matplot import matplot
# TODO: remove after making add methods
from .stage02_quantification_opls_postgresql_models import *

class stage02_quantification_opls_execute(stage02_quantification_opls_io,
                                         stage02_quantification_normalization_query,
                                         stage02_quantification_analysis_query):
    def execute_oplsda(self,analysis_id_I,
                      experiment_ids_I=[],
                      time_points_I=[],
                      concentration_units_I=[],
                      r_calc_I=None,
                    pls_model_I = 'PLS-DA',
                    response_I = None,
                    factor_I= "sample_name_abbreviation",
                    ncomp = 5,
                    Y_add = "NULL",
                    scale = "TRUE",
                    #validation = "LOO",
                    validation = "CV",
                    segments = 10,
                    method = "cppls",
                    stripped = "FALSE",
                    lower = 0.5,
                    upper = 0.5, 
                    trunc_pow = "FALSE", 
                    weights = "NULL",
                    p_method = "fdr",
                    nperm = 999):
        '''execute pls using R
        INPUT:
        analysis_id_I
        experiment_ids_I
        concentration_units_I
        r_calc_I
        PLS INPUT:

        '''

        print('execute_plsda...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        
        data_scores_O = [];
        data_loadings_O = [];
        data_validation_O = [];
        data_vip_O = [];
        data_coefficients_O = [];
        data_loadings_factors_O = [];
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            print('calculating pls for concentration_units ' + cu);
            data = [];
            # get data:
            data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            # call R
            data_scores,data_loadings = [],[];
            #TODO: add option parameters
            #data_scores,data_loadings = r_calc.calculate_plsda_mixomics(data);
            #data_scores,data_loadings = r_calc.calculate_oplsda_ropl(data);
            data_scores,data_loadings,data_perf,data_vip,data_coefficients,data_loadings_factors = r_calc.calculate_mvr(
                data,
                pls_model_I=pls_model_I,
                response_I=response_I,
                factor_I=factor_I,
                ncomp=ncomp,
                Y_add=Y_add,
                scale=scale,
                validation=validation,
                segments=segments,
                method=method,
                stripped=stripped,
                lower=lower,
                upper=upper,
                trunc_pow=trunc_pow,
                weights=weights,
                p_method=p_method,
                nperm=nperm);
            # add data to database
            for d in data_scores[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_scores_O.append(d);
            for d in data_loadings[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_loadings_O.append(d);
            for d in data_perf[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_validation_O.append(d);
            for d in data_vip[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_vip_O.append(d);
            for d in data_coefficients[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_coefficients_O.append(d);
            for d in data_loadings_factors[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_loadings_factors_O.append(d);
        # add data to the database
        self.add_dataStage02QuantificationOPLSScores(data_scores_O);
        self.add_dataStage02QuantificationOPLSLoadings(data_loadings_O);
        self.add_dataStage02QuantificationOPLSValidation(data_validation_O);
        self.add_dataStage02QuantificationOPLSVIP(data_vip_O);
        self.add_dataStage02QuantificationOPLSCoefficients(data_coefficients_O);
        self.add_dataStage02QuantificationOPLSLoadingsResponse(data_loadings_factors_O);
    def execute_oplsda(self,analysis_id_I,experiment_ids_I=[],time_points_I=[],concentration_units_I=[],r_calc_I=None):
        '''execute pls using R'''

        print('execute_plsda...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            print('calculating pls for concentration_units ' + cu);
            data = [];
            # get data:
            data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            # call R
            data_scores,data_loadings = [],[];
            #TODO: add option parameters
            data_scores,data_loadings = r_calc.calculate_plsda_mixomics(data);
            # add data to database
            for d in data_scores:
                row1 = data_stage02_quantification_opls_scores(analysis_id_I,
                        #d['experiment_id'],
                        d['sample_name_short'],
                        #d['time_point'],
                        d['score'],
                        d['axis'],
                        d['var_proportion'],
                        d['var_cumulative'],
                        cu,
                        True,None);
                self.session.add(row1);
            for d in data_loadings:
                row2 = data_stage02_quantification_opls_loadings(analysis_id_I,
                        #d['experiment_id'],
                        #d['time_point'],
                        d['component_group_name'],
                        d['component_name'],
                        d['loadings'],
                        d['axis'],
                        cu,
                        True,None);
                self.session.add(row2);
        self.session.commit();
    def execute_SUSplot(self,analysis_id_1_I,analysis_id_2_I):
        '''Generate the data for a SUS (shared and unique structures) plot

        INPUT:
        analysis_id_1_I = two-factor pls model (control vs. condition 1)
        analysis_id_2_I = two-factor pls model (control vs. condition 2)
        OUTPUT
        for each component:
            x = correlation of feature i from analysis_id_1
            y = correlation of feature j from analysis_id_2
        '''
        pass;