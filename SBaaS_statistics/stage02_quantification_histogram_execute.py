#sbaas
from .stage02_quantification_histogram_io import stage02_quantification_histogram_io
from .stage02_quantification_histogram_dependencies import stage02_quantification_histogram_dependencies
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
from .stage02_quantification_dataPreProcessing_averages_query import stage02_quantification_dataPreProcessing_averages_query
#resources
from python_statistics.calculate_histogram import calculate_histogram

class stage02_quantification_histogram_execute(
            stage02_quantification_histogram_io,
            stage02_quantification_histogram_dependencies,
            ):
    def execute_binFeatures(self,analysis_id_I,features_I=[],feature_units_I=[],n_bins_I=[],
                            query_object_descStats_I = 'stage02_quantification_descriptiveStats_query'):
        '''bin features of continuous data from the normalized data
        INPUT:
        analysis_id_I = string,
        features_I = [] of string, e.g. ['mean','cv','var','median','calculated_concentration']
        feature_units_I = [] of string, e.g. ['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized']
        n_bins_I = int, the number of bins per feature (if bins is empty, bins will be calculated)
        
        query_object_descStats_I = query objects to select the data descriptive statistics data
            options: 'stage02_quantification_descriptiveStats_query'
                     'stage02_quantification_dataPreProcessing_averages_query'
        OUTPUT:
        '''
        data_O = [];
        calculatehistogram = calculate_histogram();
        
        # intantiate the query object:
        query_objects = {'stage02_quantification_dataPreProcessing_averages_query':stage02_quantification_dataPreProcessing_averages_query,
                        'stage02_quantification_descriptiveStats_query':stage02_quantification_descriptiveStats_query};
        if query_object_descStats_I in query_objects.keys():
            query_object_descStats = query_objects[query_object_descStats_I];
            query_instance_descStats = query_object_descStats(self.session,self.engine,self.settings);
            query_instance_descStats.initialize_supportedTables();

        quantification_dataPreProcessing_replicates_query=stage02_quantification_dataPreProcessing_replicates_query(self.session,self.engine,self.settings);
        quantification_dataPreProcessing_replicates_query.initialize_supportedTables();

        #bin each feature
        for features_cnt,features in enumerate(features_I):
            n_bins = 100;
            calc_bins_I = True;
            if n_bins_I and n_bins_I[features_cnt]:
                n_bins = n_bins_I[features_cnt];
                calc_bins_I = False;
            if features == 'calculated_concentration':
                for feature_units in feature_units_I:
                    #get all the data for the analysi
                    data_hist = [];
                    data_hist = quantification_dataPreProcessing_replicates_query.get_allCalculatedConcentrations_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,feature_units);
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            elif features == 'mean':
                for feature_units in feature_units_I:
                    #get all the data for the analysis
                    data_hist = [];
                    if hasattr(query_instance_descStats, 'get_allMeans_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                        data_hist = query_instance_descStats.get_allMeans_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,feature_units);
                    elif hasattr(query_instance_descStats, 'get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages'):
                        data_hist = query_instance_descStats.get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,feature_units);
                    else:
                        print('query instance does not have the required method.');
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            elif features == 'cv':
                for feature_units in feature_units_I:
                    #get all the data for the analysi
                    data_hist = [];
                    if hasattr(query_instance_descStats, 'get_allCVs_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                        data_hist = query_instance_descStats.get_allCVs_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,feature_units);
                    #elif hasattr(query_instance_descStats, 'get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages'):
                    #    data_hist = query_instance_descStats.get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,feature_units);
                    else:
                        print('query instance does not have the required method.');
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            elif features == 'var':
                for feature_units in feature_units_I:
                    #get all the data for the analysi
                    data_hist = [];
                    if hasattr(query_instance_descStats, 'get_allVariances_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                        data_hist = query_instance_descStats.get_allVariances_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,feature_units);
                    #elif hasattr(query_instance_descStats, 'get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages'):
                    #    data_hist = query_instance_descStats.get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,feature_units);
                    else:
                        print('query instance does not have the required method.');
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            elif features == 'median':
                for feature_units in feature_units_I:
                    #get all the data for the analysi
                    data_hist = [];
                    if hasattr(query_instance_descStats, 'get_allMedians_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats'):
                        data_hist = query_instance_descStats.get_allMedians_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,feature_units);
                    #elif hasattr(query_instance_descStats, 'get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages'):
                    #    data_hist = query_instance_descStats.get_allMeans_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,feature_units);
                    else:
                        print('query instance does not have the required method.');
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            else:
                print('feature not recongnized');
        #add the data to the database
        self.add_dataStage02QuantificationHistogram(data_O);