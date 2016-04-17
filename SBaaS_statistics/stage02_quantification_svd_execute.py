
from .stage02_quantification_svd_io import stage02_quantification_svd_io
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict

class stage02_quantification_svd_execute(stage02_quantification_svd_io,
                                         ):
    def execute_svd(self,analysis_id_I,concentration_units_I=[],r_calc_I=None,
                    svd_method_I="svd"):
        '''execute svd using R'''

        #print('execute_svd...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();

        stage02quantificationnormalizationquery = stage02_quantification_normalization_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        stage02quantificationnormalizationquery.initialize_supportedTables();

        stage02quantificationanalysisquery = stage02_quantification_analysis_query(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
        stage02quantificationanalysisquery.initialize_supportedTables();

        quantification_dataPreProcessing_replicates_query=stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
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
            concentration_units = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            #concentration_units = stage02quantificationnormalizationquery.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
            #concentration_units = self.get_concentrationUnits_analysisID_dataStage02GlogNormalized(analysis_id_I);
        for cu in concentration_units:
            #print('calculating svd for concentration_units ' + cu);
            data = [];
            # get data:
            data = quantification_dataPreProcessing_replicates_query.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            #data = stage02quantificationnormalizationquery.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            #data = self.get_RExpressionData_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,cu);
            # will need to refactor in the future...
            if type(data)==type(listDict()):
                data.convert_dataFrame2ListDict()
                data = data.get_listDict();
            # call R
            data_U,data_d,data_V = [],[],[];
            data_U,data_d,data_V = r_calc.calculate_svd(data,
                    svd_method_I=svd_method_I,
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
        self.add_rows_table('data_stage02_quantification_svd_u',data_U_O);
        self.add_rows_table('data_stage02_quantification_svd_d',data_d_O);
        self.add_rows_table('data_stage02_quantification_svd_v',data_V_O);