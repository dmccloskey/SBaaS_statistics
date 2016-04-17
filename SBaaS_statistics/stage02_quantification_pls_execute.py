
from .stage02_quantification_pls_io import stage02_quantification_pls_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict

class stage02_quantification_pls_execute(stage02_quantification_pls_io,
                                         #stage02_quantification_normalization_query,
                                         stage02_quantification_analysis_query):
    def execute_plsda(self,analysis_id_I,
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
        
        quantification_dataPreProcessing_replicates_query=stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        
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
            concentration_units = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            #concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            print('calculating pls for concentration_units ' + cu);
            data = [];
            # get data:
            data = quantification_dataPreProcessing_replicates_query.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            #data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            # will need to refactor in the future...
            if type(data)==type(listDict()):
                data.convert_dataFrame2ListDict()
                data = data.get_listDict();
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
        self.add_dataStage02QuantificationPLSScores(data_scores_O);
        self.add_dataStage02QuantificationPLSLoadings(data_loadings_O);
        self.add_dataStage02QuantificationPLSValidation(data_validation_O);
        self.add_dataStage02QuantificationPLSVIP(data_vip_O);
        self.add_dataStage02QuantificationPLSCoefficients(data_coefficients_O);
        self.add_dataStage02QuantificationPLSLoadingsResponse(data_loadings_factors_O);
    def execute_plsda_pairWise(self,analysis_id_I,
                    concentration_units_I=[],
                    sample_name_abbreviations_I=[],
                    sample_name_abbreviation_control_I=None,
                    redundancy_I=True,
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
            # get sample_name_abbreviations:
            sample_name_abbreviations = [];
            sample_name_abbreviations = self.get_sampleNameAbbreviations_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            # apply an order/filter on the sample_name_abbreviations
            if sample_name_abbreviations_I:
                sample_name_abbreviations = [sna for sna in sample_name_abbreviations_I];
            # specify a control to compare all samples to
            if sample_name_abbreviation_control_I:
                sample_name_abbreviations_1 = [sna for sna in [sample_name_abbreviation_control_I]];
                if len(sample_name_abbreviations_1)<1:
                    print(sample_name_abbreviation_control_I + ' not found.');
                    return;
                sample_name_abbreviations_2 = [sna for sna in sample_name_abbreviations if sna != sample_name_abbreviation_control_I];
            else:
                sample_name_abbreviations_1 = sample_name_abbreviations;
                sample_name_abbreviations_2 = sample_name_abbreviations;
            for sna_1_cnt,sna_1 in enumerate(sample_name_abbreviations_1):
                if redundancy_I: list_2 = sample_name_abbreviations_2;
                else: list_2 = sample_name_abbreviations_2[sna_1+1:];
                for cnt,sna_2 in enumerate(list_2):
                    if redundancy_I: sna_2_cnt = cnt;
                    else: sna_2_cnt = sna_1_cnt+cnt+1;
                    if sna_1 != sna_2:
                        print('calculating pairwiseTTest for sample_name_abbreviations ' + sna_1 + ' vs. ' + sna_2);
                        # get data:
                        data_1,data_2 = [],[];
                        data_1 = self.get_RExpressionData_analysisIDAndUnitsAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,sna_1);
                        data_2 = self.get_RExpressionData_analysisIDAndUnitsAndSampleNameAbbreviation_dataStage02GlogNormalized(analysis_id_I,cu,sna_2);
                        data_1.extend(data_2);
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
        self.add_dataStage02QuantificationPLSScores(data_scores_O);
        self.add_dataStage02QuantificationPLSLoadings(data_loadings_O);
        self.add_dataStage02QuantificationPLSValidation(data_validation_O);
        self.add_dataStage02QuantificationPLSVIP(data_vip_O);
        self.add_dataStage02QuantificationPLSCoefficients(data_coefficients_O);
        self.add_dataStage02QuantificationPLSLoadingsResponse(data_loadings_factors_O);
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
                row1 = data_stage02_quantification_pls_scores(analysis_id_I,
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
                row2 = data_stage02_quantification_pls_loadings(analysis_id_I,
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