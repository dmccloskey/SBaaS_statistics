from .stage02_quantification_dataPreProcessing_replicates_io import stage02_quantification_dataPreProcessing_replicates_io
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
#resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_statisticsDescriptive import calculate_statisticsDescriptive

class stage02_quantification_dataPreProcessing_replicates_execute(stage02_quantification_dataPreProcessing_replicates_io,
                                           stage02_quantification_analysis_query):
    def execute_countMissingValues(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                value_I = None,
                operator_I='NA',
                ):
        '''Count the number of missing values
        INPUT:
        value_I = float, default: None (check for missing values)
        operator_I = string, (e.g., "=") to compare to the value
        OUTPUT:
        '''
        data_O = [];
        # query the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            # query the number of rows
            ntablerows = None;
            ntablerows = self.getCount_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                query_I={'where':[
                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                    'column_name':'analysis_id',
                    'value':analysis_id_I,
                    'operator':'LIKE',
                    'connector':'AND'
                    },
                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                    'column_name':'calculated_concentration_units',
                    'value':cu,
                    'operator':'LIKE',
                    'connector':'AND'
                    },
                ]}
                );
            if value_I is None:
                # query the number of unique component_name
                nrows = None;
                nrows = self.getCount_componentNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
                # query the number of unique sample_name_short/experiment_id/time_point
                ncols = None;
                ncols = self.getCount_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
                nvalues = nrows*ncols;
                mv = ntablerows - nvalues;
            else:
                mv = None;
                mv = self.getCount_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                    analysis_id_I,
                    query_I={'where':[
                        {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                        'column_name':'analysis_id',
                        'value':analysis_id_I,
                        'operator':'LIKE',
                        'connector':'AND'
                        },
                        {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                        'column_name':'calculated_concentration_units',
                        'value':cu,
                        'operator':'LIKE',
                        'connector':'AND'
                        },
                        {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                        'column_name':'calculated_concentration',
                        'value':value_I,
                        'operator':operator_I,
                        'connector':'AND'
                        },
                    ]}
                    );
            # calculate the number of missing values
            mvfraction = mv/ntablerows;
            tmp = {
                "analysis_id":analysis_id_I,
                "missing_values":mv,
                "missing_fraction":mvfraction,
                "calculated_concentration_units":cu,
                "mv_value":value_I,
                "mv_operator":operator_I,
                "used_":True,
                'comment_I':None}
            data_O.append(tmp);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates_mv',data_O);
    def execute_countMissingValues_v1(self,
                analysis_id_I,
                imputation_methods_I=[],
                normalization_methods_I=[],
                calculated_concentration_units_I=[],
                zeroAsMissingValue_I = True,
                ):
        '''Count the number of missing values
        INPUT:
        zeroAsMissingValue_I = Boolean, default: True, treat zero as a missing value 
        OUTPUT:
        '''
        data_O = [];
        # query the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            # query the number of rows
            ntablerows = None;
            ntablerows = self.getCount_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                query_I={'where':[
                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                    'column_name':'analysis_id',
                    'value':analysis_id_I,
                    'operator':'LIKE',
                    'connector':'AND'
                    },
                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                    'column_name':'calculated_concentration_units',
                    'value':cu,
                    'operator':'LIKE',
                    'connector':'AND'
                    },
                ]}
                );
            # query the number of unique component_name
            nrows = None;
            nrows = self.getCount_componentNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            # query the number of unique sample_name_short/experiment_id/time_point
            ncols = None;
            ncols = self.getCount_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I,cu);
            # calculate the number of missing values
            mv = ntablerows - (nrows*ncols);
            mvfraction = mv/ntablerows;
            tmp = {
                "analysis_id":analysis_id_I,
                "missing_values":mv,
                "missing_fraction":mvfraction,
                "calculated_concentration_units":cu,
                "used_":True,
                'comment_I':None}
            data_O.append(tmp);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates_mv',data_O);

    #normalization methods
    def execute_normalization_dataSet(self,
            analysis_id_I,
            imputation_methods_I=[],
            normalization_methods_I=[],
            calculated_concentration_units_I=[],
            normalization_method_I='gLog',
            normalization_options_I={'mult':"TRUE",'lowessnorm':"FALSE"},
            r_calc_I=None
            ):
        '''normalization of the full data set'''

        print('execute_glogNormalization...')
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();
        python_calc = calculate_statisticsDescriptive();
        data_O = [];
        data_normalized = [];
        data_normalizations = [];
        # get the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu in calculated_concentration_units:
            print('calculating normalization for concentration_units ' + cu);
            # get the data set
            data = [];
            data = self.get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                cu,
                query_I={},
                output_O='listDict',
                dictColumn_I=None);
            # normalize the data set
            if normalization_method_I == 'gLog':
                concentrations = None;
                concentrations_glog = None;
                data_glog, concentrations, concentrations_glog = r_calc.calculate_glogNormalization(
                    data,
                    normalization_options_I['mult'],
                    normalization_options_I['lowessnorm']);
                data_normalized.extend(data_glog);
            elif normalization_method_I in ["log2","log10","ln","abs","exp","exp2","^10","^2","sqrt"]:
                for d in data:
                    normalized_value = python_calc.scale_values(d['calculated_concentration'],normalization_method_I);
                    normalized_units = ('%s_%s_%s' %(d['calculated_concentration_units'],normalization_method_I,'normalized'));
                    d['calculated_concentration'] = normalized_value;
                    d['calculated_concentration_units'] = normalized_units;
                    d['imputation_method'] = None;
                data_normalized.extend(data);
            else:
                print('normalization_method_I not recognized');
                continue;
            # record data normalization method
            tmp = {
                "analysis_id":analysis_id_I,
                "imputation_method":None,
                "imputation_options":None,
                "normalization_method":normalization_method_I,
                "normalization_options":normalization_options_I,
                'calculated_concentration_units':cu,
                "used_":True,
                'comment_I':None
                }
            data_normalizations.append(tmp);
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_normalized);
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates_im',data_normalizations);
        
    def execute_normalization_rowWise(self,
            analysis_id_I,
            imputation_method_I=[],
            calculated_concentration_units_I=[],
            normalization_method_I='gLog',
            normalization_options_I=None,
            r_calc_I=None
            ):
        '''row-wise normalization of the data
        (all metabolites for a specific sample)
        sum
        mean
        mode
        component
        component_pool
        sample_specific
        '''
        pass;
    def execute_normalization_columnWise(self,
            analysis_id_I,
            imputation_method_I='',
            calculated_concentration_units_I=[],
            normalization_method_I='gLog',
            normalization_options_I=None,
            r_calc_I=None
            ):
        '''row-wise normalization of the data
        (all samples for a specific metabolite)
        auto-scaling
        pareto-scaling
        range-scaling
        log[x]-scaling
        '''
        pass;

    #missing value methods
    def execute_calculateMissingValues_ameliaII(self,
            analysis_id_I,
            imputation_method_I = 'ameliaII',
            imputation_options_I = {'n_imputations':1000},
            calculated_concentration_units_I=[],
            experiment_ids_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            r_calc_I=None):
        '''calculate estimates for missing replicates values using AmeliaII from R
        INPUT:
        experiment_id_I
        sample_name_abbreviations_I'''
        
        if r_calc_I: r_calc = r_calc_I;
        else: r_calc = r_interface();

        print('execute_calculateMissingValues_ameliaII...')
        data_O = [];
        data_imputations = [];
        # get the calculated_concentration_units/experiment_ids/sample_name_abbreviations/time_points that are unique
        unique_groups = [];
        unique_groups = get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
            analysis_id_I,
            calculated_concentration_units_I=calculated_concentration_units_I,
            experiment_ids_I=experiment_ids_I,
            sample_name_abbreviations_I=sample_name_abbreviations_I,
            time_points_I=time_points_I,
            );
        #unique_groups_1 = [];
        ##is there a more "pythonic" way of doing this?
        ##or alternatively, should this just be added into the query?
        #for row in unique_groups: 
        #    add_row = True
        #    if calculated_concentration_units_I and not row['calculated_concentration_units'] in calculated_concentration_units_I:
        #        add_row = False;
        #    elif experiment_ids_I and not row['experiment_id'] in experiment_ids_I:
        #        add_row = False;
        #    elif sample_name_abbreviations_I and not row['sample_name_abbreviation'] in sample_name_abbreviations_I:
        #        add_row = False;
        #    elif time_points_I and not row['time_point'] in time_points_I:
        #        add_row = False;
        #    if add_row:
        #        unique_groups_1.append(row);
        for row in unique_groups:
            data = [];
            data = get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                row['calculated_concentration_units'],
                row['experiment_id'],
                row['sample_name_abbreviation'],
                row['time_point'],
                );
            # compute missing values
            dataListUpdated = [];
            sns_NA = [];
            cn_NA = [];
            cc_NA = [];
            sns_NA, cn_NA, cc_NA = r_calc.calculate_missingValues(
                data,
                imputation_options_I['n_imputations']
                );
            for n in range(len(sns_NA)):
                component_group_name = None;
                # update data_stage01_quantification_replicatesMI
                row = data_stage01_quantification_replicatesMI(experiment_id_I,sns_NA[n],tp,component_group_name,cn_NA[n],"AmeliaII",None,cc_NA[n],calculated_concentration_units,True,None);
            # record data imputation method
            tmp = {
                "analysis_id":analysis_id_I,
                "imputation_method":imputation_method_I,
                "imputation_options":imputation_options_I,
                "normalization_method":None,
                "normalization_options":None,
                'calculated_concentration_units':cu,
                "used_":True,
                'comment_I':None
                }
            data_imputations.append(tmp);
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates_im',data_imputations);
    def execute_calculateMissingComponents_lloq(self,analysis_id):
        ''' '''
        pass;
    def execute_replaceMissingValues_dataSet(self,
            analysis_id_I,
            imputation_methods_I=[],
            normalization_methods_I=[],
            calculated_concentration_units_I=[],
            normalization_method_I='gLog',
            normalization_options_I={'mult':"TRUE",'lowessnorm':"FALSE"},
            ):
        '''replace missing values with the mean, median, 1/2*min of the data, or a user specified value'''
        pass;