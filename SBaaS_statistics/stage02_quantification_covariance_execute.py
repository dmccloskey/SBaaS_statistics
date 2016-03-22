
from .stage02_quantification_covariance_io import stage02_quantification_covariance_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface

class stage02_quantification_covariance_execute(stage02_quantification_covariance_io,
                                         ):
    def execute_covariance(self,analysis_id_I,concentration_units_I=[],
                    covariance_method_I="covariance"):
        '''execute covariance using R'''

        #print('execute_covariance...')
        calculateinterface = calculate_interface()
        stage02quantificationnormalizationquery = stage02_quantification_normalization_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        stage02quantificationnormalizationquery.initialize_supportedTables();
        stage02quantificationanalysisquery = stage02_quantification_analysis_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        stage02quantificationanalysisquery.initialize_supportedTables();
        data_U_O = [];
        data_d_O = [];
        data_V_O = [];
        # get the analysis information
        analysis_info = [];
        analysis_info = stage02quantificationanalysisquery.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        #analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            concentration_units = stage02quantificationnormalizationquery.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
            #concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            #print('calculating covariance for concentration_units ' + cu);
            data = [];
            # get data:
            data = stage02quantificationnormalizationquery.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            #data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            # call R
            data_U,data_d,data_V = [],[],[];
            data_U,data_d,data_V = r_calc.calculateinterface(data,
                    covariance_method_I=covariance_method_I,
                    );
            # add data to database
            for d in data_U[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_U_O.append(d);
            for d in data_d[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_d_O.append(d);
            for d in data_V[:]:
                d['analysis_id']=analysis_id_I;
                d['calculated_concentration_units']=cu;
                d['used_']=True;
                d['comment_']=None;
                data_V_O.append(d);
        # add data to the database
        self.add_rows_table('data_stage02_quantification_covariance_u',data_U_O);
        self.add_rows_table('data_stage02_quantification_covariance_d',data_d_O);
        self.add_rows_table('data_stage02_quantification_covariance_v',data_V_O);
        #self.add_dataStage02QuantificationSVD('data_stage02_quantification_covariance_u',data_U_O);
        #self.add_dataStage02QuantificationSVD('data_stage02_quantification_covariance_d',data_d_O);
        #self.add_dataStage02QuantificationSVD('data_stage02_quantification_covariance_v',data_V_O);