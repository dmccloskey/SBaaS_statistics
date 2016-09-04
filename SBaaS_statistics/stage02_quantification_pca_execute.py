
from .stage02_quantification_pca_io import stage02_quantification_pca_io
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
# resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_interface import calculate_interface
from matplotlib_utilities.matplot import matplot
from listDict.listDict import listDict
import copy

class stage02_quantification_pca_execute(stage02_quantification_pca_io,
                                         stage02_quantification_analysis_query):
    def execute_pca(self,analysis_id_I,experiment_ids_I=[],time_points_I=[],concentration_units_I=[],r_calc_I=None,
                    pca_model_I="pca",pca_method_I="svd",
                    imputeMissingValues="TRUE",
                    cv="q2",
                    ncomps="7",
                    scale="uv",
                    center="TRUE",
                    segments="10",
                    nruncv="1",
                    crossValidation_type="krzanowski",
            query_object_descStats_I = 'stage02_quantification_dataPreProcessing_replicates_query',
            ):
        '''execute pca using R'''

        print('execute_pca...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query,
                        'stage02_quantification_dataPreProcessing_replicates_query':stage02_quantification_dataPreProcessing_replicates_query,
                        };
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        descStats_replicate_keys = ['median','iq_1','iq_3','min','max']
        data_scores_O = [];
        data_loadings_O = [];
        data_validation_O = [];
        # get the analysis information
        analysis_info = [];
        analysis_info = self.get_rows_analysisID_dataStage02QuantificationAnalysis(analysis_id_I);
        # query metabolomics data from glogNormalization
        # get concentration units
        if concentration_units_I:
            concentration_units = concentration_units_I;
        else:
            concentration_units = [];
            #concentration_units = quantification_dataPreProcessing_replicates_query.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            if hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(analysis_id_I);
            elif hasattr(query_instance_descStats, 'get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages'):
                calculated_concentration_units = query_instance_descStats.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
            else:
                print('query instance does not have the required method.');
        for cu in concentration_units:
            print('calculating pca for concentration_units ' + cu);
            data = [];
            # get data:
            # get data:
            #data = quantification_dataPreProcessing_replicates_query.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            if hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates'):
                data = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages'):
                data_tmp = [];
                data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
                if type(data_tmp)==type(listDict()):
                    data_tmp.convert_dataFrame2ListDict()
                    data_tmp = data_tmp.get_listDict();
                for d in data_tmp:
                    for i,k in enumerate(descStats_replicate_keys):
                        tmp = copy.copy(d);
                        tmp['calculated_concentration']=tmp[k];
                        tmp['sample_name_short']='%s_%s'%(tmp['sample_name_abbreviation'],i);
                        data.append(tmp);
            elif hasattr(query_instance_descStats, 'get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                data_tmp = [];
                data_tmp = query_instance_descStats.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,cu);
                if type(data_tmp)==type(listDict()):
                    data_tmp.convert_dataFrame2ListDict()
                    data_tmp = data_tmp.get_listDict();
                for d in data_tmp:
                    for i,k in enumerate(descStats_replicate_keys):
                        tmp = copy.copy(d);
                        tmp['calculated_concentration']=tmp[k];
                        tmp['sample_name_short']='%s_%s'%(tmp['sample_name_abbreviation'],i);
                        data.append(tmp);
            # will need to refactor in the future...
            if type(data)==type(listDict()):
                data.convert_dataFrame2ListDict()
                data = data.get_listDict();
            # call R
            data_scores,data_loadings,data_perf = [],[],[];
            if pca_method_I == "robustPca":
                data_scores,data_loadings,data_perf = r_calc.calculate_pca_princomp(data,
                    cor_I = "FALSE",
                    scores_I = "TRUE",
                    covmat_I="NULL",
                    na_action_I='na.omit',
                    robust_pca_I=True,
                    center_I = center,
                    scale_I=scale)
                #data_scores,data_loadings = r_calc.calculate_pca_prcomp(data, retx_I = "TRUE", center_I = "FALSE", na_action_I='na.omit',scale_I="TRUE");
            else:
                data_scores,data_loadings,data_perf = r_calc.calculate_pca_pcaMethods(data,
                    pca_model_I=pca_model_I,
                    pca_method_I=pca_method_I,
                    imputeMissingValues=imputeMissingValues,
                    cv=cv,
                    ncomps=ncomps,
                    scale=scale,
                    center=center,
                    segments=segments,
                    nruncv=nruncv,
                    crossValidation_type = crossValidation_type);
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
        # add data to the database
        self.add_dataStage02QuantificationPCAScores(data_scores_O);
        self.add_dataStage02QuantificationPCALoadings(data_loadings_O);
        self.add_dataStage02QuantificationPCAValidation(data_validation_O);
    def execute_pcaPlot(self,analysis_id_I,experiment_ids_I=[],time_points_I=[],concentration_units_I=[]):
        '''generate a pca plot'''

        print('execute_pcaPlot...')
        mplot = matplot();
        # query metabolomics data from pca_scores and pca_loadings
        # get concentration units...
        concentration_units = [];
        concentration_units = self.get_concentrationUnits_analysisID_dataStage02Scores(analysis_id_I);
        for cu in concentration_units:
            if cu=='height_ratio_glog_normalized' or cu=='height_ratio': continue; # skip for now...
            print('plotting pca for concentration_units ' + cu);
            # get data:
            data_scores,data_loadings = [],[];
            data_scores,data_loadings = self.get_RExpressionData_analysisIDAndUnits_dataStage02QuantificationPCAScoresLoadings(analysis_id_I,cu);
            # plot the data:
            PCs = [[1,2],[1,3],[2,3]];
            for PC in PCs:
                # scores
                title,xlabel,ylabel,x_data,y_data,text_labels,samples = self.matplot._extractPCAScores(data_scores,PC[0],PC[1]);
                mplot.volcanoPlot(title,xlabel,ylabel,x_data,y_data,text_labels);
                # loadings
                title,xlabel,ylabel,x_data,y_data,text_labels = self.matplot._extractPCALoadings(data_loadings,PC[0],PC[1]);
                mplot.volcanoPlot(title,xlabel,ylabel,x_data,y_data,text_labels);