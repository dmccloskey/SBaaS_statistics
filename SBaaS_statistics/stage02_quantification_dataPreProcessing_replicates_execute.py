from .stage02_quantification_dataPreProcessing_replicates_io import stage02_quantification_dataPreProcessing_replicates_io
from .stage02_quantification_analysis_query import stage02_quantification_analysis_query
from .stage02_quantification_descriptiveStats_query import stage02_quantification_descriptiveStats_query
#required for missing components LLOQ
from SBaaS_quantification.stage01_quantification_QCs_query import stage01_quantification_QCs_query
from SBaaS_LIMS.lims_biologicalMaterial_query import lims_biologicalMaterial_query
from SBaaS_LIMS.lims_experiment_query import lims_experiment_query
#resources
from r_statistics.r_interface import r_interface
from python_statistics.calculate_statisticsDescriptive import calculate_statisticsDescriptive
from python_statistics.calculate_interface import calculate_interface
from listDict.listDict import listDict
import copy

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
            ntablerows = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                column_name_I = 'analysis_id',
                aggregate_function_I='count',
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
                mv = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                    analysis_id_I,
                    column_name_I = 'analysis_id',
                    aggregate_function_I='count',
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
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            self.delete_rows_analysisIDAndCalculatedConcentrationUnitsAndCalculatedConcentrationValueAndOperator_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I = analysis_id_I,
                calculated_concentration_units_I = cu,
                value_I = value_I,
                operator_I = operator_I,
                warn_I=warn_I,
                );
    def execute_deleteOutliers(self,
                analysis_id_I,
                calculated_concentration_units_cv_I=['umol*gDW-1'],
                calculated_concentration_units_delete_I=['umol*gDW-1_glog_normalized'],
                cv_threshold_I=80,
                warn_I=False,
                ):
        '''Delete outlier metabolites/sample_name_abbreviation pairs
        INPUT:
        cv_threshold_I = float
        OUTPUT:
        '''
        quantification_descriptiveStats_query=stage02_quantification_descriptiveStats_query(self.session,self.engine,self.settings);
        quantification_analysis_query=stage02_quantification_analysis_query(self.session,self.engine,self.settings);

        # pass 1: query all experiment_id/sample_name_short/time_point/component_name that do not meet the threshold for specific calculated_concentration_units
        delete_rows = [];
        # query the calculated_concentration_units
        if calculated_concentration_units_cv_I:
            calculated_concentration_units = calculated_concentration_units_cv_I;
        else:
            calculated_concentration_units = [];
            calculated_concentration_units = self.get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDataPreProcessingReplicates(analysis_id_I);
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            #query rows with a cv>cv_threshold_I in the analysis
            desc_rows = [];
            desc_rows = quantification_descriptiveStats_query.get_rows_analysisIDAndCalculatedConcentrationUnitsAndCVThreshold_dataStage02QuantificationDescriptiveStats(
                analysis_id_I,
                calculated_concentration_units_I = cu,
                cv_threshold_I = cv_threshold_I,
                used__I=True);
            for desc_row in desc_rows:
                #query sample_name_shorts for each row
                experiment_id,sample_name_short,time_point = [],[],[];
                experiment_id,sample_name_short,time_point = quantification_analysis_query.get_experimentIDAndSampleNameShortAndTimePoint_analysisIDAndSampleNameAbbreviation_dataStage02QuantificationAnalysis(
                                                    analysis_id_I,
                                                    desc_row['sample_name_abbreviation']);
                for sns in sample_name_short:
                    row = copy.copy(desc_row);
                    row['sample_name_short'] = sns;
                    delete_rows.append(row)

        # pass 2: delete all experiment_id/sample_name_short/time_point/component_name that do not meet the threshold for specific calculated_concentration_units
        # query the calculated_concentration_units
        if calculated_concentration_units_delete_I:
            calculated_concentration_units = calculated_concentration_units_delete_I;
        for cu_cnt,cu in enumerate(calculated_concentration_units):
            for delete_row in delete_rows:
                #remove experiment_id/sample_name_short/time_point/component_name from the analysis
                self.delete_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDAndTimePointAndSampleNameShortAndComponentName_dataStage02QuantificationDataPreProcessingReplicates(
                    analysis_id_I = analysis_id_I,
                    calculated_concentration_units_I = cu,
                    experiment_id_I = delete_row['experiment_id'],
                    time_point_I = delete_row['time_point'],
                    sample_name_short_I = delete_row['sample_name_short'],
                    component_name_I = delete_row['component_name'],
                    warn_I=warn_I,
                    );

    #normalization methods
    def execute_normalization(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            normalization_method_I='glog',
            normalization_options_I={'mult':"TRUE",'lowessnorm':"FALSE"},
            r_calc_I=None
            ):
        '''normalization of the full data set
        INPUT:
        OUTPUT:
        '''

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
            #data = self.get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
            #    analysis_id_I,
            #    cu,
            #    query_I={},
            #    output_O='listDict',
            #    dictColumn_I=None);
            data = self.get_RExpressionData_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                cu
                );
            # will need to refactor in the future...
            if type(data)==type(listDict()):
                data.convert_dataFrame2ListDict()
                data = data.get_listDict();
            # normalize the data set
            if normalization_method_I == 'glog':
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
        median
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
        http://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-7-142
        Class I: can be applied with Class II and Class III
        centering xij-xihat

        Class II:
        auto-scaling (xij-xihat)/si
        pareto-scaling (xij-xihat)/sqrt(si)
        range-scaling (xij-xihat)/(ximax-ximin)
        vast-scaling (xij-xihat)/si * xihat/si
        level-scaling xij-xihat/xi

        Class III:
        log transformation
        power transformation 
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
        unique_groups = self.get_calculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
            analysis_id_I,
            calculated_concentration_units_I=calculated_concentration_units_I,
            experiment_ids_I=experiment_ids_I,
            sample_name_abbreviations_I=sample_name_abbreviations_I,
            time_points_I=time_points_I,
            );
        # will need to refactor in the future...
        if type(unique_groups)==type(listDict()):
            unique_groups.convert_dataFrame2ListDict()
            unique_groups = unique_groups.get_listDict();
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
            # avoid duplicate analysis_id/calculated_concentration_units
            if not tmp in data_imputations:
                data_imputations.append(tmp);
        #add the data to the DB
        if data_O:
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates_im',data_imputations);
        else:
            print('no missing values found.');
    def execute_imputeMissingValues_replicatesPerExperiment(self,
            analysis_id_I,
            imputation_method_I = 'ameliaII',
            imputation_options_I = {'n_imputations':1000,
                                'geometric_imputation':True},
            calculated_concentration_units_I=[],
            experiment_ids_I=[],
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
        # get the calculated_concentration_units/experiment_ids that are unique
        unique_groups = [];
        unique_groups = self.get_calculatedConcentrationUnitsAndExperimentIDs_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
            analysis_id_I,
            calculated_concentration_units_I=calculated_concentration_units_I,
            experiment_ids_I=experiment_ids_I,
            );
        # will need to refactor in the future...
        if type(unique_groups)==type(listDict()):
            unique_groups.convert_dataFrame2ListDict()
            unique_groups = unique_groups.get_listDict();
        for row in unique_groups:
            data_mv = [];
            data_mv = self.get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDs_dataStage02QuantificationDataPreProcessingReplicates(
                analysis_id_I,
                row['calculated_concentration_units'],
                row['experiment_id'],
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
            elif imputation_method_I == 'mean_row_experiment':
                pass;
            elif imputation_method_I == 'mean_experiment':
                pass;
            else:
                print('imputation_method_I not recognized.');
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
            # avoid duplicate analysis_id/calculated_concentration_units
            if not tmp in data_imputations:
                data_imputations.append(tmp);
        #add the data to the DB
        if data_O:
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates_im',data_imputations);
        else:
            print('no missing values found.');
    def execute_imputeMissingValues(self,
            analysis_id_I,
            calculated_concentration_units_I=[],
            experiment_ids_I=[],
            sample_name_shorts_I=[],
            time_points_I=[],
            imputation_method_I = 'lloq',
            imputation_options_I = {},
            ):
        '''Impute missing values for components that are missing in a replicate
        NOTES:
        row variabels are component_names
        column variabels
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
            missing_components_found = False;
            for unique_group in unique_groups:
                #get all components for the row
                unique_components = [];
                unique_components = self.getGroup_componentNameAndComponentGroupName_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDAndSampleNameShortAndTimePoint_dataStage02QuantificationDataPreProcessingReplicates(
                    analysis_id_I,cu,unique_group['experiment_id'],unique_group['sample_name_short'],unique_group['time_point']);
                unique_components_dict =  {row['component_name']:row['component_group_name'] for row in unique_components};
                missing_components = list(set(all_components_dict.keys()) - set(unique_components_dict.keys()))
                if missing_components:
                    missing_components_found = True;
                    for mcn in missing_components:
                        row_tmp = {};
                        if imputation_method_I == 'value':
                            row_tmp['calculated_concentration'] = imputation_options_I['value'];
                        elif imputation_method_I == 'lloq':
                            value_new,units = self._impute_missingComponents_replicates(
                                        sample_name_short_I=unique_group['sample_name_short'],
                                        component_name_I=mcn,
                                        experiment_id_I=unique_group['experiment_id'],
                                        biological_material_I=imputation_options_I['biological_material'],
                                        conversion_name_I=imputation_options_I['conversion_name']
                                        );
                            if 'scale' in imputation_options_I.keys(): value_new = imputation_options_I['scale']*value_new;
                            row_tmp['calculated_concentration'] = value_new;
                        elif imputation_method_I == 'mean_feature':
                            value_new = None;
                            value_new = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                                analysis_id_I,
                                column_name_I = 'calculated_concentration',
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
                            row_tmp['calculated_concentration'] = value_new;
                        elif imputation_method_I == 'mean_sample':
                            value_new = None;
                            value_new = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                                analysis_id_I,
                                column_name_I = 'calculated_concentration',
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
                            row_tmp['calculated_concentration'] = value_new;
                        elif imputation_method_I == 'mean_data':
                            value_new = None;
                            value_new = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                                analysis_id_I,
                                column_name_I = 'calculated_concentration',
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
                            row_tmp['calculated_concentration'] = value_new;
                        elif imputation_method_I == 'median_sample':
                            pass;
                        elif imputation_method_I == 'median_feature':
                            pass;
                        elif imputation_method_I == 'median_data':
                            pass;
                        elif imputation_method_I == 'min_sample':
                            pass;
                        elif imputation_method_I == 'min_feature':
                            pass;
                        elif imputation_method_I == 'min_data':
                            value_new = None;
                            value_new = self.getAggregateFunction_rows_analysisID_dataStage02QuantificationDataPreProcessingReplicates(
                                analysis_id_I,
                                column_name_I = 'calculated_concentration',
                                aggregate_function_I='min',
                                aggregate_label_I='min_1',
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
                            if 'scale' in imputation_options_I.keys(): value_new = imputation_options_I['scale']*value_new;
                            row_tmp['calculated_concentration'] = value_new;
                        # fill in the rest of the columns
                        row_tmp['analysis_id'] = analysis_id_I;
                        row_tmp['experiment_id'] = unique_group['experiment_id'];
                        row_tmp['sample_name_short'] = unique_group['sample_name_short'];
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
                    "used_":True,
                    'comment_':None
                    }
                data_imputations.append(tmp);
        # add the data to the DB
        if data_O:
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates',data_O);
            self.add_rows_table('data_stage02_quantification_dataPreProcessing_replicates_im',data_imputations);
        else:
            print('no missing values found.');
    def _impute_missingComponents_replicates(self,
                    sample_name_short_I,
                    component_name_I,
                    experiment_id_I,
                    biological_material_I=None,
                    conversion_name_I=None
                    ):
        '''Calculate missing components using the LLOQ of the analytical assay
        INPUT:
        experiment_id_I = string
        biological_material_I = string,
        conversion_name_I = string
        '''
        stage01quantificationQCsquery = stage01_quantification_QCs_query(self.session,self.engine,self.settings);
        limsbiologicalMaterialquery = lims_biologicalMaterial_query(self.session,self.engine,self.settings);
        limsexperimentquery = lims_experiment_query(self.session,self.engine,self.settings);
        calc = calculate_interface();
        # get the lloq
        lloq = None;
        conc_units = None;
        lloq, conc_units = stage01quantificationQCsquery.get_lloq_ExperimentIDAndComponentName_dataStage01LLOQAndULOQ(experiment_id_I,component_name_I);
        if not lloq:
            print('lloq not found'); 
            return None, None;
        # normalize the lloq
        if (biological_material_I and conversion_name_I):
            # get physiological parameters
            cvs = None;
            cvs_units = None;
            od600 = None;
            dil = None;
            dil_units = None;
            conversion = None;
            conversion_units = None;
            cvs, cvs_units, od600, dil,dil_units = limsexperimentquery.get_CVSAndCVSUnitsAndODAndDilAndDilUnits_sampleNameShort(experiment_id_I,sample_name_short_I);
            conversion, conversion_units = limsbiologicalMaterialquery.get_conversionAndConversionUnits_biologicalMaterialAndConversionName(biological_material_I,conversion_name_I);
            if not(cvs and cvs_units and od600 and dil and dil_units):
                print('cvs, cvs_units, or od600 are missing from physiological parameters');
                print('or dil and dil_units are missing from sample descripton');
                exit(-1);
            elif not(conversion and conversion_units):
                print('biological_material or conversion name is incorrect');
                exit(-1);  
            else:
                #calculate the cell volume
                cell_volume, cell_volume_units = calc.calculate_biomass_CVSAndCVSUnitsAndODAndConversionAndConversionUnits(cvs,cvs_units,od600,conversion,conversion_units);
                # calculate the normalized concentration
                norm_conc, norm_conc_units = calc.calculate_conc_concAndConcUnitsAndDilAndDilUnitsAndConversionAndConversionUnits(lloq,conc_units,dil,dil_units,cell_volume, cell_volume_units);
                #if norm_conc:
                return norm_conc,norm_conc_units;
        else:
            return lloq,conc_units;