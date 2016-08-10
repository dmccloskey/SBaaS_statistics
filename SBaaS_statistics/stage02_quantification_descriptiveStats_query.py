from .stage02_quantification_descriptiveStats_postgresql_models import *
from .stage02_quantification_analysis_postgresql_models import *

#SBaaS_base
from SBaaS_base.sbaas_base_query_select import sbaas_base_query_select
from SBaaS_base.sbaas_base_query_delete import sbaas_base_query_delete
#SBaaS_template
from SBaaS_base.sbaas_template_query import sbaas_template_query

#Resources
from math import sqrt
from listDict.listDict import listDict

class stage02_quantification_descriptiveStats_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for 
        '''
        tables_supported = {'data_stage02_quantification_descriptiveStats':data_stage02_quantification_descriptiveStats,
                        };
        self.set_supportedTables(tables_supported);

    # data_stage02_quantification_descriptiveStats
    # query sample_names from data_stage02_quantification_descriptiveStats
    def get_sampleNameAbbreviationsAndTimePoints_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I):
        '''Querry sample_name_abbreviations that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.sample_name_abbreviation,
                    data_stage02_quantification_descriptiveStats.time_point).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation,
                    data_stage02_quantification_descriptiveStats.time_point).order_by(
                    data_stage02_quantification_descriptiveStats.time_point.asc(),
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc()).all();
            sample_name_abbreviations_O = [];
            time_points_O = [];
            if data: 
                for d in data:
                    sample_name_abbreviations_O.append(d.sample_name_abbreviation);
                    time_points_O.append(d.time_point);
            return sample_name_abbreviations_O,time_points_O;
        except SQLAlchemyError as e:
            print(e);
    def get_sampleNameAbbreviations_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I):
        '''Querry sample_name_abbreviations that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.sample_name_abbreviation).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation).order_by(
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.sample_name_abbreviation);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query calculated_concentration_units from data_stage02_quantification_descriptiveStats
    def get_calculatedConcentrationUnits_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I):
        '''Querry calculated_concentration_units that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.calculated_concentration_units).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units).order_by(
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.calculated_concentration_units);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query component_names from data_stage02_quantification_descriptiveStats
    def get_componentNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,analysis_id_I,calculated_concentration_units_I):
        '''Querry component_names that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.component_name).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.component_name).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_name);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_analysisIDAndCalculatedConcentrationUnitsAndCVThreshold_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I,
            cv_threshold_I,
            used__I=True):
        '''Query rows by analysis_id and calculated_concentration_units that are used
           and that are greater that cv_threshold_I
           INPUT:
           analysis_id_I = string
           calculated_concentration_units_I = string
           cv_threshold_I = float, rows > cv_threshold_I will be selected
           used__I = boolean
           OUTPUT:
           component_names_O'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.component_name).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.cv>cv_threshold_I,
                    data_stage02_quantification_descriptiveStats.used_.is_(used__I)).group_by(
                    data_stage02_quantification_descriptiveStats.component_name).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            component_names_O = [d.component_name for d in data];
            return component_names_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNamesAndComponentGroupNames_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,analysis_id_I,calculated_concentration_units_I):
        '''Querry component_names that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.component_name,
                                      data_stage02_quantification_descriptiveStats.component_group_name).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.component_name,
                    data_stage02_quantification_descriptiveStats.component_group_name).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            component_name_O = [];
            component_group_name_O = [];
            if data: 
                for d in data:
                    component_name_O.append(d.component_name);
                    component_group_name_O.append(d.component_group_name);
            return component_name_O,component_group_name_O;
        except SQLAlchemyError as e:
            print(e);
    def get_componentNames_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I):
        '''Querry component_names that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.component_name).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                    data_stage02_quantification_descriptiveStats.component_name).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.component_name);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    # query data from data_stage02_quantification_descriptiveStats
    def get_data_analysisIDAndSampleNameAbbreviationAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
                                analysis_id_I,
                                sample_name_abbreviation_I,
                                component_name_I,
                                calculated_concentration_units_I):
        '''Querry data by sample_name_abbreviation, component_name, and calculated_concentration_units that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_descriptiveStats.component_name.like(component_name_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).all();
            mean,stdev,ci_lb,ci_ub,calculated_concentration_units = None,None,None,None,None;
            if len(data)>1:
                print('More than 1 row found');
            if data: 
                for d in data:
                    mean=d.mean;
                    if d.var and not d.var is None: stdev=sqrt(d.var);
                    else: stdev=0.0;
                    ci_lb=d.ci_lb;
                    ci_ub=d.ci_ub;
                    calculated_concentration_units=d.calculated_concentration_units;
            return mean,stdev,ci_lb,ci_ub,calculated_concentration_units;
        except SQLAlchemyError as e:
            print(e);
    def get_data_analysisIDAndSampleNameAbbreviationAndTimePointAndComponentNameAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
                                analysis_id_I,
                                sample_name_abbreviation_I,
                                time_point_I,
                                component_name_I,
                                calculated_concentration_units_I):
        '''Querry data by sample_name_abbreviation, component_name, and calculated_concentration_units that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_descriptiveStats.time_point.like(time_point_I),
                    data_stage02_quantification_descriptiveStats.component_name.like(component_name_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).all();
            mean,stdev,ci_lb,ci_ub,calculated_concentration_units = None,None,None,None,None;
            if len(data)>1:
                print('More than 1 row found');
            if data: 
                for d in data:
                    mean=d.mean;
                    if d.var and not d.var is None: stdev=sqrt(d.var);
                    else: stdev=0.0;
                    ci_lb=d.ci_lb;
                    ci_ub=d.ci_ub;
                    calculated_concentration_units=d.calculated_concentration_units;
            return mean,stdev,ci_lb,ci_ub,calculated_concentration_units;
        except SQLAlchemyError as e:
            print(e);
    # query rows from data_stage02_quantification_descriptiveStats
    def get_rows_analysisID_dataStage02QuantificationDescriptiveStats(self,analysis_id_I,used__I=True):
        '''Querry rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(used__I)).order_by(
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc(),
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append({'analysis_id':d.analysis_id,
                    'experiment_id':d.experiment_id,
                    'sample_name_abbreviation':d.sample_name_abbreviation,
                    'time_point':d.time_point,
                    'component_group_name':d.component_group_name,
                    'component_name':d.component_name,
                    'test_stat':d.test_stat,
                    'test_description':d.test_description,
                    'pvalue':d.pvalue,
                    'pvalue_corrected':d.pvalue_corrected,
                    'pvalue_corrected_description':d.pvalue_corrected_description,
                    'mean':d.mean,
                    'var':d.var,
                    'cv':d.cv,
                    'n':d.n,
                    'ci_lb':d.ci_lb,
                    'ci_ub':d.ci_ub,
                    'ci_level':d.ci_level,
                    'min':d.min,
                    'max':d.max,
                    'median':d.median,
                    'iq_1':d.iq_1,
                    'iq_3':d.iq_3,
                    'calculated_concentration_units':d.calculated_concentration_units,
                    'used_':d.used_,
                    'comment_':d.comment_
                    });
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
        #    analysis_id_I,
        #    calculated_concentration_units_I):
        #'''Querry rows by analysis_id and calculated_concentration_units that are used'''
        #try:
        #    data = self.session.query(data_stage02_quantification_descriptiveStats).filter(
        #            data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
        #            data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
        #            data_stage02_quantification_descriptiveStats.used_.is_(True)).all();
        #    rows_O = [d.__repr__dict() for d in data];
        #    return rows_O;
        #except SQLAlchemyError as e:
        #    print(e);
                analysis_id_I,
                calculated_concentration_units_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_data_stage02_quantification_descriptiveStats
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_descriptiveStats'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'calculated_concentration_units',
            'value':calculated_concentration_units_I,
            'operator':'LIKE',
            'connector':'AND'
                        },
            {"table_name":tables[0],
            'column_name':'used_',
            'value':'true',
            'operator':'IS',
            'connector':'AND'
                },
	    ];
        query['order_by'] = [
            {"table_name":tables[0],
            'column_name':'experiment_id',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_group_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'time_point',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'sample_name_abbreviation',
            'order':'ASC',
            },
        ];

        #additional blocks
        for k,v in query_I.items():
            if not k in query.keys():
                query[k] = [];
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndCVThreshold_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I,
            cv_threshold_I,
            used__I=True):
        '''Query rows by analysis_id and calculated_concentration_units that are used
           and that are greater that cv_threshold_I
           INPUT:
           analysis_id_I = string
           calculated_concentration_units_I = string
           cv_threshold_I = float, rows > cv_threshold_I will be selected
           used__I = boolean
           OUTPUT:
           rows_O = listDict with columns for sample_name_short from analysis_id
           '''
        try:
            data = self.session.query(
                    data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.cv>cv_threshold_I,
                    data_stage02_quantification_descriptiveStats.used_.is_(used__I)).all();
            rows_O = [d.__repr__dict__() for d in data];
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndSampleNameAbbreviation_dataStage02QuantificationDescriptiveStats(self, analysis_id_I,calculated_concentration_units_I,sample_name_abbreviation_I):
        """get rows by analysis_id, calculated_concentration_units, and sample_name_abbreviation from data_stage02_quantification_descriptiveStats"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_descriptiveStats).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.sample_name_abbreviation.like(sample_name_abbreviation_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.component_name.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_dataStage02QuantificationDescriptiveStats(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_id_I,
                sample_name_abbreviation_I,
                time_point_I,
            ):
        """query unique rows from data_stage02_quantification_descriptiveStats"""
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats
                ).filter(
                data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_descriptiveStats.experiment_id.like(experiment_id_I),
                data_stage02_quantification_descriptiveStats.time_point.like(time_point_I),
                data_stage02_quantification_descriptiveStats.sample_name_abbreviation.like(sample_name_abbreviation_I),
                data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc(),
                data_stage02_quantification_descriptiveStats.component_name.asc(),
                ).all();
            data_O=[d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndComponentName_dataStage02QuantificationDescriptiveStats(self, analysis_id_I,calculated_concentration_units_I,component_name_I):
        """get rows by analysis_id, calculated_concentration_units, and component_name from data_stage02_quantification_descriptiveStats_averages"""
        #Tested
        try:
            data = self.session.query(
                    data_stage02_quantification_descriptiveStats_averages).filter(
                    data_stage02_quantification_descriptiveStats_averages.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats_averages.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats_averages.component_name.like(component_name_I),
                    data_stage02_quantification_descriptiveStats_averages.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats_averages.sample_name_abbreviation.asc()).all();
            data_O = [d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    def get_rows_analysisIDAndCalculatedConcentrationUnitsAndExperimentIDsAndSampleNameAbbreviationsAndTimePointsAndComponentName_dataStage02QuantificationDescriptiveStats(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_id_I,
                sample_name_abbreviation_I,
                time_point_I,
                component_name_I,
            ):
        """query unique rows from data_stage02_quantification_descriptiveStats"""
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats
                ).filter(
                data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_descriptiveStats.experiment_id.like(experiment_id_I),
                data_stage02_quantification_descriptiveStats.time_point.like(time_point_I),
                data_stage02_quantification_descriptiveStats.sample_name_abbreviation.like(sample_name_abbreviation_I),
                data_stage02_quantification_descriptiveStats.component_name.like(component_name_I),
                data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc(),
                data_stage02_quantification_descriptiveStats.component_name.asc(),
                ).all();
            data_O=[d.__repr__dict__() for d in data];
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Query unique groups from 
    def get_analysisIDAndExperimentIDsAndSampleNameAbbreviationsAndTimePoints_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
                analysis_id_I,
                calculated_concentration_units_I,
                experiment_ids_I=[],
                sample_name_abbreviations_I=[],
                time_points_I=[],
            ):
        """query unique rows from data_preProcessing_analysis and data_stage02_quantification_descriptiveStats"""
        try:
            data = self.session.query(
                data_stage02_quantification_descriptiveStats.analysis_id,
                data_stage02_quantification_descriptiveStats.calculated_concentration_units,
                data_stage02_quantification_descriptiveStats.experiment_id,
                data_stage02_quantification_descriptiveStats.sample_name_abbreviation,
                data_stage02_quantification_descriptiveStats.time_point,
                ).filter(
                data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                data_stage02_quantification_descriptiveStats.used_.is_(True)).group_by(
                data_stage02_quantification_descriptiveStats.analysis_id,
                data_stage02_quantification_descriptiveStats.calculated_concentration_units,
                data_stage02_quantification_descriptiveStats.experiment_id,
                data_stage02_quantification_descriptiveStats.sample_name_abbreviation,
                data_stage02_quantification_descriptiveStats.time_point).order_by(
                data_stage02_quantification_descriptiveStats.analysis_id.asc(),
                data_stage02_quantification_descriptiveStats.calculated_concentration_units.asc(),
                data_stage02_quantification_descriptiveStats.experiment_id.asc(),
                data_stage02_quantification_descriptiveStats.sample_name_abbreviation.asc(),
                data_stage02_quantification_descriptiveStats.time_point.asc()).all();
            data_O=[];
            if data:
                data_O = listDict(record_I=data);
                data_O.convert_record2DataFrame();
                data_O.filterIn_byDictList({'experiment_id':experiment_ids_I,
                                            'sample_name_abbreviation':sample_name_abbreviations_I,
                                           'time_point':time_points_I,
                                           });
                data_O.convert_dataFrame2ListDict();
            return data_O;
        except SQLAlchemyError as e:
            print(e);
    # Query specific columns of data_stage02_quantification_descriptiveStats
    def get_allMeans_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all mean values by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.mean).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.mean).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.mean);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allCVs_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all CVs by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.cv).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.cv).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.cv);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allMedians_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all medians by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.median).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.median).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.median);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    def get_allVariances_analysisIDAndCalculatedConcentrationUnits_dataStage02QuantificationDescriptiveStats(self,
            analysis_id_I,
            calculated_concentration_units_I):
        '''Query all variances by analysis_id and calculated_concentration_units that are used'''
        try:
            data = self.session.query(data_stage02_quantification_descriptiveStats.var).filter(
                    data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(calculated_concentration_units_I),
                    data_stage02_quantification_descriptiveStats.used_.is_(True)).order_by(
                    data_stage02_quantification_descriptiveStats.var).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.var);
            return rows_O;
        except SQLAlchemyError as e:
            print(e);

    def reset_dataStage02_quantification_descriptiveStats(self,analysis_id_I = None, calculated_concentration_units_I = []):
        try:
            if analysis_id_I and calculated_concentration_units_I:
                for ccu in calculated_concentration_units_I:
                    reset = self.session.query(data_stage02_quantification_descriptiveStats).filter(
                        data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I),
                        data_stage02_quantification_descriptiveStats.calculated_concentration_units.like(ccu),
                        ).delete(synchronize_session=False);
                self.session.commit();
            elif analysis_id_I:
                reset = self.session.query(data_stage02_quantification_descriptiveStats).filter(data_stage02_quantification_descriptiveStats.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
                self.session.commit();
        except SQLAlchemyError as e:
            print(e);
   