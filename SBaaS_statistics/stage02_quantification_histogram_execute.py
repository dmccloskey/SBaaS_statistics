#sbaas
from .stage02_quantification_histogram_io import stage02_quantification_histogram_io
from .stage02_quantification_histogram_dependencies import stage02_quantification_histogram_dependencies
from .stage02_quantification_normalization_query import stage02_quantification_normalization_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from .stage02_quantification_dataPreProcessing_replicates_query import stage02_quantification_dataPreProcessing_replicates_query
#sbaas models
from .stage02_quantification_histogram_postgresql_models import *
#resources
from python_statistics.calculate_histogram import calculate_histogram

class stage02_quantification_histogram_execute(
            stage02_quantification_histogram_io,
            stage02_quantification_normalization_query,
            stage02_quantification_descriptiveStats_query,
            stage02_quantification_analysis_query,
            stage02_quantification_histogram_dependencies,
            stage02_quantification_dataPreProcessing_replicates_query
            ):
    def execute_binFeatures(self,analysis_id_I,features_I=[],feature_units_I=[],n_bins_I=[]):
        '''bin features of continuous data from the normalized data
        INPUT:
        analysis_id_I = string,
        features_I = [] of string, e.g. ['mean','cv','var','median','calculated_concentration']
        feature_units_I = [] of string, e.g. ['umol*gDW-1_glog_normalized','umol*gDW-1','height','height_glog_normalized','ratio','ratio_glog_normalized']
        n_bins_I = int, the number of bins per feature (if bins is empty, bins will be calculated)

        OUTPUT:
        '''
        data_O = [];
        calculatehistogram = calculate_histogram();
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
                    data_hist = self.get_allCalculatedConcentrations_analysisIDAndUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,feature_units);
                    #data_hist = self.get_allCalculatedConcentrations_analysisIDAndUnits_dataStage02GlogNormalized(analysis_id_I,feature_units);
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            elif features == 'mean':
                for feature_units in feature_units_I:
                    #get all the data for the analysi
                    data_hist = [];
                    data_hist = self.get_allMeans_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,feature_units);
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            elif features == 'cv':
                for feature_units in feature_units_I:
                    #get all the data for the analysi
                    data_hist = [];
                    data_hist = self.get_allCVs_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,feature_units);
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            elif features == 'var':
                for feature_units in feature_units_I:
                    #get all the data for the analysi
                    data_hist = [];
                    data_hist = self.get_allVariances_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,feature_units);
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            elif features == 'median':
                for feature_units in feature_units_I:
                    #get all the data for the analysi
                    data_hist = [];
                    data_hist = self.get_allMedians_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(analysis_id_I,feature_units);
                    #make the bins for the histogram
                    if data_hist:
                        x_O,dx_O,y_O = calculatehistogram.histogram(data_I=data_hist,n_bins_I=n_bins,calc_bins_I=calc_bins_I);
                        tmp = self.record_histogram(analysis_id_I,features,feature_units,x_O,dx_O,y_O);
                        data_O.extend(tmp);
            else:
                print('feature not recongnized');
        #add the data to the database
        self.add_dataStage02QuantificationHistogram(data_O);