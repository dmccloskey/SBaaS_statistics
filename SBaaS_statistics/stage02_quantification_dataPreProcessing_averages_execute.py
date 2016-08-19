from .stage02_quantification_dataPreProcessing_averages_io import stage02_quantification_dataPreProcessing_averages_io
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
#resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_statisticsDescriptive import calculate_statisticsDescriptive
from listDict.listDict import listDict
import copy

class stage02_quantification_dataPreProcessing_averages_execute(stage02_quantification_dataPreProcessing_averages_io,
                                           stage02_quantification_analysis_query):

    #TODO: support for detecting and filling in null values
    def execute_countMissingValues(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                feature_I = 'mean',
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
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            # query the number of rows
            ntablerows = None;
            ntablerows = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingAverages(
                analysis_id_I,
                column_name_I = 'analysis_id',
                aggregate_function_I='count',
                query_I={'where':[
                    {"table_name":'data_stage02_quantification_dataPreProcessing_averages',
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
                nrows = self.getCount_componentNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
                # query the number of unique sample_name_short/experiment_id/time_point
                ncols = None;
                ncols = self.getCount_experimentIDAndSampleNameAbbreviationAndTimePoint_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I,cu);
                nvalues = nrows*ncols;
                mv = nvalues - ntablerows;
            else:
                mv = None;
                mv = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,
                    column_name_I = 'analysis_id',
                    aggregate_function_I='count',
                    query_I={'where':[
                        {"table_name":'data_stage02_quantification_dataPreProcessing_averages',
                        'column_name':'analysis_id',
                        'value':analysis_id_I,
                        'operator':'LIKE',
                        'connector':'AND'
                        },
                        {"table_name":'data_stage02_quantification_dataPreProcessing_averages',
                        'column_name':'calculated_concentration_units',
                        'value':cu,
                        'operator':'LIKE',
                        'connector':'AND'
                        },
                        {"table_name":'data_stage02_quantification_dataPreProcessing_averages',
                        'column_name':feature_I,
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
                "mv_feature":feature_I,
                'comment_I':None}
            data_O.append(tmp);
        # add data to the DB
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages_mv',data_O);
    def execute_deleteMissingValues(self,
                analysis_id_I,
                calculated_concentration_units_I=[],
                feature_I = 'mean',
                value_I = 0.0,
                operator_I='=',
                set_used_false_I = False,
                warn_I=False,
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
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            if set_used_false_I:
                continue;
                #TODO: update_rows_analysisIDAndCalculatedConcentrationUnitsAndCalculatedConcentrationValueAndOperator_dataStage02QuantificationDataPreProcessingAverages
                #set used_ = False;
            else:
                self.delete_rows_analysisIDAndCalculatedConcentrationUnitsAndFeatureValueAndOperator_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I = analysis_id_I,
                    calculated_concentration_units_I = cu,
                    feature_I = feature_I,
                    value_I = value_I,
                    operator_I = operator_I,
                    warn_I=warn_I,
                    );

    #normalization methods
    def execute_normalization(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            feature_I = 'mean',
            normalization_method_I='gLog',
            normalization_options_I={'mult':"TRUE",'lowessnorm':"FALSE"},
            r_calc_I=None
            ):
        '''normalization of the full data set
        INPUT:
        OUTPUT:
        '''

        print('execute_normalization...')
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
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
        for cu in calculated_concentration_units:
            print('calculating normalization for concentration_units ' + cu);
            # get the data set
            data = [];
            #data = self.get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
            #    analysis_id_I,
            #    cu,
            #    query_I={},
            #    output_O='listDict',
            #    dictColumn_I=None);
            data = self.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                analysis_id_I,
                cu
                );
            # will need to refactor in the future...
            if type(data)==type(listDict()):
                data.convert_dataFrame2ListDict()
                data = data.get_listDict();
            # normalize the data set
            if normalization_method_I == 'gLog':
                concentrations = None;
                concentrations_glog = None;
                #TODO: refactor...
                data_glog, concentrations, concentrations_glog = r_calc.calculate_glogNormalization(
                    data,
                    normalization_options_I['mult'],
                    normalization_options_I['lowessnorm']);
                data_normalized.extend(data_glog);
            elif normalization_method_I in ["log2","log10","ln","abs","exp","exp2","^10","^2","sqrt"]:
                for d in data:
                    normalized_value = python_calc.scale_values(d[feature_I],normalization_method_I);
                    d[feature_I] = normalized_value;
                    if type(feature_I)==type(''):
                        normalized_value = python_calc.scale_values(d[feature_I],normalization_method_I);
                        d[feature_I] = normalized_value;
                    elif type(feature_I)==type([]):
                        for feature in feature_I:
                            normalized_value = python_calc.scale_values(d[feature],normalization_method_I);
                            d[feature] = normalized_value;
                    normalized_units = ('%s_%s_%s' %(d['calculated_concentration_units'],normalization_method_I,'normalized'));
                    d['calculated_concentration_units'] = normalized_units;
                    d['imputation_method'] = None;
                data_normalized.extend(data);
            #TODO: add support for LB,UB,IQ1,IQ3,Min,Max
            elif normalization_method_I in ["FC-median",\
                "FC-mean","FC-mode","log2(FC-median)","log2(FC-mean)","log2(FC-mode)"]:
                #query the sample data to perform the fold-change
                dpave_list = self.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDataPreProcessingAverages(
                        analysis_id_I,
                        cu,
                        normalization_options_I['experiment_id_FC'],
                        normalization_options_I['sample_name_abbreviation_FC'],
                        normalization_options_I['time_point_FC'],
                        )
                dpave_dict = {row['component_name']:row for row in dpave_list};
                for d in data:
                    #query the mean/meadian from descriptive stats
                    desc_stats = [];
                    desc_stats = dpave_dict[d['component_name']];
                    ##check
                    #if d['component_name'] == '6pgc.6pgc_1.Light':
                    #    print('check');
                    if normalization_method_I in ["FC-median","log2(FC-median)"]:
                        data_1 = desc_stats['median'];
                    elif normalization_method_I in ["FC-mean","log2(FC-mean)"]:
                        data_1 = desc_stats['mean'];
                    elif normalization_method_I in ["FC-mode","log2(FC-mode)"]:
                        data_1 = desc_stats['mode'];
                    if type(feature_I)==type(''):
                        normalized_value = python_calc.calculate_foldChange(
                            data_1,
                            d[feature_I],
                            type_I = normalization_options_I['type'], # e.g., 'relative'
                            scale_values_I = normalization_options_I['scale_values'], # e.g. None
                            scale_fold_change_I = normalization_options_I['scale_fold_change'], #e.g. "log2"
                            );
                        if 'min_value' in normalization_options_I.keys():
                            if normalized_value < normalization_options_I['min_value']:
                                normalized_value = normalization_options_I['min_value']
                        if 'max_value' in normalization_options_I.keys():
                            if normalized_value > normalization_options_I['max_value']:
                                normalized_value = normalization_options_I['max_value']
                        d[feature_I] = normalized_value;
                    elif type(feature_I)==type([]):
                        for feature in feature_I:
                            normalized_value = python_calc.calculate_foldChange(
                                data_1,
                                d[feature],
                                type_I = normalization_options_I['type'], # e.g., 'relative'
                                scale_values_I = normalization_options_I['scale_values'], # e.g. None
                                scale_fold_change_I = normalization_options_I['scale_fold_change'], #e.g. "log2"
                                );
                            if 'min_value' in normalization_options_I.keys():
                                if normalized_value < normalization_options_I['min_value']:
                                    normalized_value = normalization_options_I['min_value']
                            if 'max_value' in normalization_options_I.keys():
                                if normalized_value > normalization_options_I['max_value']:
                                    normalized_value = normalization_options_I['max_value']
                            d[feature] = normalized_value;
                    normalized_units = ('%s_%s_%s' %(d['calculated_concentration_units'],normalization_method_I,'normalized'));
                    d['calculated_concentration_units'] = normalized_units;
                    d['imputation_method'] = None;
                    d['used_'] = True;
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
                'mv_feature':feature_I,
                "used_":True,
                'comment_I':None
                };
            data_normalizations.append(tmp);
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages',data_normalized);
        self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages_im',data_normalizations);
        
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
    def execute_imputeMissingValues(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            experiment_ids_I=[],
            sample_name_abbreviations_I=[],
            time_points_I=[],
            feature_I = 'mean',
            imputation_method_I = 'lloq',
            imputation_options_I = {'table_name':''},
            ):
        '''Impute missing values for components that are missing in a replicate
        INPUT:
        OUTPUT:
        '''
        data_O = [];
        data_imputations = [];
        print('execute_imputation...')
        # get the calculated_concentration_units
        if calculated_concentration_units_I:
            calculated_concentration_units = calculated_concentration_units_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingAverages(analysis_id_I);
        for cu in calculated_concentration_units:
            print('calculating imputation for concentration_units ' + cu);
            #get all component_names and component_group_names for the analysis
            all_components = [];
            all_components = self.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                analysis_id_I,cu);
            all_components_dict =  {row['component_name']:row['component_group_name'] for row in all_components};
            #get the components for each column (i.e., replicate)
            unique_groups = [];
            unique_groups = self.get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingAverages(
                analysis_id_I,cu,
                experiment_ids_I,
                sample_name_abbreviations_I,
                time_points_I);
            #fill values for each missing component
            missing_components_found = False;
            for unique_group in unique_groups.get_listDict():
                #get all components for the row
                unique_components = [];
                unique_components = self.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDAndSampleNameAbbreviationAndTimePoint_dataStage02QuantificationDataPreProcessingAverages(
                    analysis_id_I,cu,unique_group['experiment_id'],unique_group['sample_name_abbreviation'],unique_group['time_point']);
                unique_components_dict =  {row['component_name']:row['component_group_name'] for row in unique_components};
                missing_components = list(set(all_components_dict.keys()) - set(unique_components_dict.keys()))
                if missing_components:
                    missing_components_found = True;
                    for mcn in missing_components:
                        row_tmp = {};
                        if imputation_method_I == 'value':
                            row_tmp[feature_I] = imputation_options_I['value'];
                        elif imputation_method_I == 'lloq':
                            pass;
                        elif imputation_method_I == 'mean_feature':
                            value_new = None;
                            value_new = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingAverages(
                                analysis_id_I,
                                column_name_I = feature_I,
                                aggregate_function_I='avg',
                                aggregate_label_I='avg_1',
                                query_I={
                                    'where':[
                                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                                    'column_name':'calculated_concentration_units',
                                    'value':cu,
                                    'operator':'LIKE',
                                    'connector':'AND'
                                    },
                                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                                    'column_name':'component_name',
                                    'value':mcn,
                                    'operator':'LIKE',
                                    'connector':'AND'
                                    },
                                    ],
                                }
                                );
                            if 'scale' in imputation_options_I.keys(): value_new = imputation_options_I['scale']*value_new;
                            row_tmp[feature_I] = value_new;
                        elif imputation_method_I == 'mean_sample':
                            value_new = None;
                            value_new = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingAverages(
                                analysis_id_I,
                                column_name_I = feature_I,
                                aggregate_function_I='avg',
                                aggregate_label_I='avg_1',
                                query_I={
                                    'where':[
                                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                                    'column_name':'calculated_concentration_units',
                                    'value':cu,
                                    'operator':'LIKE',
                                    'connector':'AND'
                                    },
                                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                                    'column_name':'experiment_id',
                                    'value':unique_group['experiment_id'],
                                    'operator':'LIKE',
                                    'connector':'AND'
                                    },
                                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                                    'column_name':'sample_name_short',
                                    'value':unique_group['sample_name_short'],
                                    'operator':'LIKE',
                                    'connector':'AND'
                                    },
                                    ],
                                }
                                );
                            if 'scale' in imputation_options_I.keys(): value_new = imputation_options_I['scale']*value_new;
                            row_tmp[feature_I] = value_new;
                        elif imputation_method_I == 'mean_data':
                            value_new = None;
                            value_new = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingAverages(
                                analysis_id_I,
                                column_name_I = feature_I,
                                aggregate_function_I='avg',
                                aggregate_label_I='avg_1',
                                query_I={'where':[
                                    {"table_name":'data_stage02_quantification_dataPreProcessing_replicates',
                                    'column_name':'calculated_concentration_units',
                                    'value':cu,
                                    'operator':'LIKE',
                                    'connector':'AND'
                                    },
                                ]}
                                );
                            if 'scale' in imputation_options_I.keys(): value_new = imputation_options_I['scale']*value_new;
                            row_tmp[feature_I] = value_new;
                        elif imputation_method_I == 'median_row':
                            pass;
                        elif imputation_method_I == 'median_column':
                            pass;
                        elif imputation_method_I == 'median_data':
                            pass;
                        elif imputation_method_I == 'min_row':
                            pass;
                        elif imputation_method_I == 'min_column':
                            pass;
                        elif imputation_method_I == 'min_data':
                            value_new = None;
                            value_new = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingAverages(
                                analysis_id_I,
                                column_name_I = feature_I,
                                aggregate_function_I='min',
                                aggregate_label_I='min_1',
                                query_I={'where':[
                                    {"table_name":'data_stage02_quantification_dataPreProcessing_averages',
                                    'column_name':'analysis_id',
                                    'value':analysis_id_I,
                                    'operator':'LIKE',
                                    'connector':'AND'
                                    },
                                    {"table_name":'data_stage02_quantification_dataPreProcessing_averages',
                                    'column_name':'calculated_concentration_units',
                                    'value':cu,
                                    'operator':'LIKE',
                                    'connector':'AND'
                                    },
                                ]}
                                );
                            if 'scale' in imputation_options_I.keys(): value_new = imputation_options_I['scale']*value_new;
                            row_tmp[feature_I] = value_new;
                        # fill in the rest of the columns
                        row_tmp['analysis_id'] = analysis_id_I;
                        row_tmp['experiment_id'] = unique_group['experiment_id'];
                        row_tmp['sample_name_abbreviation'] = unique_group['sample_name_abbreviation'];
                        row_tmp['time_point'] = unique_group['time_point'];
                        row_tmp['calculated_concentration_units'] = cu;
                        row_tmp['component_name'] = mcn;
                        row_tmp['component_group_name'] = all_components_dict[mcn];
                        row_tmp['imputation_method'] = imputation_method_I;
                        row_tmp['used_'] = True;
                        row_tmp['comment_'] = None;
                        data_O.append(row_tmp);
            # record data imputation method
            if missing_components_found:
                tmp = {
                    "analysis_id":analysis_id_I,
                    "imputation_method":imputation_method_I,
                    "imputation_options":imputation_options_I,
                    "normalization_method":None,
                    "normalization_options":None,
                    'calculated_concentration_units':cu,
                    'mv_feature':feature_I,
                    "used_":True,
                    'comment_':None
                    }
                data_imputations.append(tmp);
        # add the data to the DB
        if data_O:
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages',data_O);
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_averages_im',data_imputations);
        else:
            print('no missing values found.');