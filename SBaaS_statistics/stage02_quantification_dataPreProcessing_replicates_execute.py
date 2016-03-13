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
                mv = nvalues - ntablerows;
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
    def execute_deleteMissingValues(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                value_I = 0.0,
                operator_I='=',
                ):
        '''Delete missing values
        INPUT:
        value_I = float
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
            self.delete_rows_analysisIDAndCalculatedConcentrationUnitsAndCalculatedConcentrationValueAndOperator_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I = analysis_id_I,
                calculated_concentration_units_I = cu,
                value_I = value_I,
                operator_I = operator_I
                );

    #normalization methods
    def execute_normalization_analysis(self,
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
                };
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
    def execute_imputeMissingValues_replicatesPerCondition(self,
            analysis_id_I,
            imputation_method_I = 'ameliaII',
            imputation_options_I = {'n_imputations':1000,
                                'geometric_imputation':True},
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

        print('execute_calculateMissingValues_condition...')
        data_O = [];
        data_imputations = [];
        # get the calculated_concentration_units/experiment_ids/sample_name_abbreviations/time_points that are unique
        unique_groups = [];
        unique_groups = self.get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndSampleNameShortsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
            analysis_id_I,
            calculated_concentration_units_I=calculated_concentration_units_I,
            experiment_ids_I=experiment_ids_I,
            sample_name_abbreviations_I=sample_name_abbreviations_I,
            time_points_I=time_points_I,
            );
        for row in unique_groups:
            data_mv = [];
            data_mv = self.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                row['calculated_concentration_units'],
                row['experiment_id'],
                row['sample_name_abbreviation'],
                row['time_point'],
                );
            # compute missing values
            if imputation_method_I == 'ameliaII':
                data_update = [];
                data_update = r_calc.calculate_missingValues(
                    data_mv,
                    imputation_options_I['n_imputations'],
                    imputation_options_I['geometric_imputation']
                    );
                if data_update:
                    data_new_unique = list(set([(y['experiment_id'],y['sample_name_short'],y['time_point'],y['component_name']) for y in data_update])-set([(x['experiment_id'],x['sample_name_short'],x['time_point'],x['component_name']) for x in data_mv]));
                    data_new = [x for x in data_update if (x['experiment_id'],x['sample_name_short'],x['time_point'],x['component_name']) in data_new_unique];
                    data_O.extend(data_new);
            elif imputation_method_I == 'mean_row_condition':
                pass;
            elif imputation_method_I == 'mean_condition':
                pass;
            else:
                print('imputation_method_I not recognized.');
        #add the data to the DB
        if data_O:
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);
            # record data imputation method
            tmp = {
                "analysis_id":analysis_id_I,
                "imputation_method":imputation_method_I,
                "imputation_options":imputation_options_I,
                "normalization_method":None,
                "normalization_options":None,
                'calculated_concentration_units':row['calculated_concentration_units'],
                "used_":True,
                'comment_I':None
                }
            data_imputations.append(tmp);
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates_im',data_imputations);
    def execute_imputeMissingValues(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            experiment_ids_I=[],
            sample_name_shorts_I=[],
            time_points_I=[],
            imputation_method_I = 'lloq',
            imputation_options_I = {'table_name':''},
            ):
        '''Impute missing values for components that are missing in a replicate
        INPUT:
        OUTPUT:
        '''
        data_O = [];
        data_imputations = [];
        # get the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu in calculated_concentration_units:
            print('calculating normalization for concentration_units ' + cu);
            #get all component_names and component_group_names for the analysis
            all_components = [];
            all_components = self.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,cu);
            all_components_dict =  {row['component_name']:row['component_group_name'] for row in all_components};
            #get the components for each column (i.e., replicate)
            unique_groups = [];
            ##split1:
            #unique_groups = self.getGroup_analysisIDAndExperimentIDAndSampleNameShortAndTimePoint_analysisIDAndCalculatedConcentrationUnits_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
            #    analysis_id_I,cu);
            #split2
            unique_groups = self.get_analysisIDAndExperimentIDsAndSampleNameShortsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,cu,
                experiment_ids_I,
                sample_name_shorts_I,
                time_points_I);
            #fill values for each missing component
            for row in unique_groups:
                #get all components for the row
                unique_components = [];
                unique_components = self.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDAndSampleNameShortAndTimePoint_dataStage02QuantificationDataPreProcessingReplicates(
                    analysis_id_I,cu,row['experiment_id'],row['sample_name_short'],row['time_point']);
                unique_components_dict =  {row['component_name']:row['component_group_name'] for row in unique_components};
                missing_components = list(set(all_components_dict.keys()) - set(unique_components_dict.keys()))
                if missing_components:
                    for mcn in missing_components:
                        if imputation_method_I == 'value':
                            row['analysis_id'] = analysis_id_I;
                            row['experiment_id'] = row['experiment_id'];
                            row['sample_name_short'] = row['sample_name_short'];
                            row['time_point'] = row['time_point'];
                            row['calculated_concentration'] = imputation_options_I['value'];
                            row['calculated_concentration_units'] = cu;
                            row['component_name'] = mcn;
                            row['component_group_names'] = all_components_dict[mcn];
                            row['imputation_method'] = imputation_method_I;
                            row['used_'] = True;
                            row['comment_'] = None;
                        elif imputation_method_I == 'lloq':
                            pass;
                        elif imputation_method_I == 'mean_row':
                            pass;
                        elif imputation_method_I == 'mean_column':
                            pass;
                        elif imputation_method_I == 'mean_data':
                            pass;
                        elif imputation_method_I == 'median_row':
                            pass;
                        elif imputation_method_I == 'median_column':
                            pass;
                        elif imputation_method_I == 'median_data':
                            pass;
                        elif imputation_method_I == '1/2*min_row':
                            pass;
                        elif imputation_method_I == '1/2*min_column':
                            pass;
                        elif imputation_method_I == '1/2*min_data':
                            pass;
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