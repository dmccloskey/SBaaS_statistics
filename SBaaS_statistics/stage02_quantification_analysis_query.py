#lims
from SBaaS_LIMS.lims_experiment_postgresql_models import *
from SBaaS_LIMS.lims_sample_postgresql_models import *

from .stage02_quantification_analysis_postgresql_models import *

from SBaaS_base.sbaas_template_query import sbaas_template_query

class stage02_quantification_analysis_query(sbaas_template_query):
    def initialize_supportedTables(self):
        '''Set the supported tables dict for stage02_quantification_analysis
        '''
        tables_supported = {'data_stage02_quantification_analysis':data_stage02_quantification_analysis,
                        };
        self.set_supportedTables(tables_supported);
    # data_stage02_quantification_analysis
    # query rows from data_stage02_quantification_analysis
    def get_experimentIDAndSampleNameAbbreviationAndTimePoint_analysisID_dataStage02QuantificationAnalysis(self,analysis_id_I):
        '''Query experiment_id, sample_name_abbreviation and time_point that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_analysis.time_point).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_abbreviation,
                    data_stage02_quantification_analysis.time_point).order_by(
                    data_stage02_quantification_analysis.experiment_id.asc(),
                    data_stage02_quantification_analysis.sample_name_abbreviation.asc(),
                    data_stage02_quantification_analysis.time_point.asc()).all();
            experiment_id_O = []
            sample_name_abbreviation_O = []
            time_point_O = []
            if data: 
                for d in data:
                    experiment_id_O.append(d.experiment_id);
                    sample_name_abbreviation_O.append(d.sample_name_abbreviation); 
                    time_point_O.append(d.time_point);               
            return  experiment_id_O,sample_name_abbreviation_O,time_point_O;
        except SQLAlchemyError as e:
            print(e);
    def get_experimentIDAndSampleNameShortAndTimePoint_analysisID_dataStage02QuantificationAnalysis(self,analysis_id_I):
        '''Query Query experiment_id, sample_name_short and time_point that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_short,
                    data_stage02_quantification_analysis.time_point).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.used_.is_(True)).group_by(
                    data_stage02_quantification_analysis.experiment_id,
                    data_stage02_quantification_analysis.sample_name_short,
                    data_stage02_quantification_analysis.time_point).order_by(
                    data_stage02_quantification_analysis.experiment_id.asc(),
                    data_stage02_quantification_analysis.sample_name_short.asc(),
                    data_stage02_quantification_analysis.time_point.asc()).all();
            experiment_id_O = []
            sample_name_short_O = []
            time_point_O = []
            if data: 
                for d in data:
                    experiment_id_O.append(d.experiment_id);
                    sample_name_short_O.append(d.sample_name_short); 
                    time_point_O.append(d.time_point);               
            return  experiment_id_O,sample_name_short_O,time_point_O;
        except SQLAlchemyError as e:
            print(e);

    #SPLIT 2:
    def add_dataStage02QuantificationAnalysis(self,table_I,data_I):
        '''add rows of data_stage02_quantification_analysis'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryinsert = sbaas_base_query_insert(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryinsert.add_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);
    def update_dataStage02QuantificationAnalysis(self,table_I,data_I):
        '''update rows of data_stage02_quantification_analysis'''
        if data_I:
            try:
                model_I = self.convert_tableString2SqlalchemyModel(table_I);
                queryupdate = sbaas_base_query_update(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
                queryupdate.update_rows_sqlalchemyModel(model_I,data_I);
            except Exception as e:
                print(e);
    def initialize_dataStage02_quantification_analysis(self,
            tables_I = [],):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            queryinitialize = sbaas_base_query_initialize(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                model_I = self.convert_tableString2SqlalchemyModel(table);
                queryinitialize.initialize_table_sqlalchemyModel(model_I);
        except Exception as e:
            print(e);
    def drop_dataStage02_quantification_analysis(self,
            tables_I = [],):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            querydrop = sbaas_base_query_drop(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                model_I = self.convert_tableString2SqlalchemyModel(table);
                querydrop.drop_table_sqlalchemyModel(model_I);
        except Exception as e:
            print(e);
    def reset_dataStage02_quantification_analysis(self,
            tables_I = [],
            analysis_id_I = None,
            warn_I=True):
        try:
            if not tables_I:
                tables_I = list(self.get_supportedTables().keys());
            querydelete = sbaas_base_query_delete(session_I=self.session,engine_I=self.engine,settings_I=self.settings,data_I=self.data);
            for table in tables_I:
                query = {};
                query['delete_from'] = [{'table_name':table}];
                query['where'] = [{
                        'table_name':table,
                        'column_name':'analysis_id',
                        'value':analysis_id_I,
                        #'value':self.convert_string2StringString(analysis_id_I),
		                'operator':'LIKE',
                        'connector':'AND'
                        }
	                ];
                table_model = self.convert_tableStringList2SqlalchemyModelDict([table]);
                query = querydelete.make_queryFromString(table_model,query);
                querydelete.reset_table_sqlalchemyModel(query_I=query,warn_I=warn_I);
        except Exception as e:
            print(e);
    def _get_rows_analysisID_dataStage02QuantificationAnalysis(self,
                analysis_id_I,
                query_I={},
                output_O='listDict',
                dictColumn_I=None):
        '''Query rows by analysis_id from data_stage02_quantification_analysis
        INPUT:
        analysis_id_I = string
        output_O = string
        dictColumn_I = string
        OPTIONAL INPUT:
        query_I = additional query blocks
        OUTPUT:
        data_O = output specified by output_O and dictColumn_I
        '''

        tables = ['data_stage02_quantification_analysis'];
        # get the listDict data
        data_O = [];
        query = {};
        query['select'] = [{"table_name":tables[0]}];
        query['where'] = [
            {"table_name":tables[0],
            'column_name':'analysis_id',
            'value':analysis_id_I,
            #'value':self.convert_string2StringString(analysis_id_I),
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
            'column_name':'sample_name_short',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'component_name',
            'order':'ASC',
            },
            {"table_name":tables[0],
            'column_name':'time_point',
            'order':'ASC',
            },
        ];

        #additional blocks
        for k,v in query_I.items():
            for r in v:
                query[k].append(r);
        
        data_O = self.get_rows_tables(
            tables_I=tables,
            query_I=query,
            output_O=output_O,
            dictColumn_I=dictColumn_I);
        return data_O;

    #SPLIT 1:   
    def get_rows_analysisID_dataStage02QuantificationAnalysis(self,analysis_id_I):
        '''Query rows that are used from the analysis'''
        try:
            data = self.session.query(data_stage02_quantification_analysis).filter(
                    data_stage02_quantification_analysis.analysis_id.like(analysis_id_I),
                    data_stage02_quantification_analysis.used_.is_(True)).all();
            rows_O = [];
            if data: 
                for d in data:
                    rows_O.append(d.__repr__dict__());
            return rows_O;
        except SQLAlchemyError as e:
            print(e);
    #def add_dataStage02QuantificationAnalysis(self, data_I):
    #    '''add rows of data_stage02_quantification_analysis'''
    #    if data_I:
    #        for d in data_I:
    #            try:
    #                data_add = data_stage02_quantification_analysis(
    #                    d['analysis_id'],
    #                    d['experiment_id'],
    #                    d['sample_name_short'],
    #                    d['sample_name_abbreviation'],
    #                    d['time_point'],
    #                    #d['time_point_units'],
    #                    d['analysis_type'],
    #                    d['used_'],
    #                    d['comment_']);
    #                self.session.add(data_add);
    #            except SQLAlchemyError as e:
    #                print(e);
    #        self.session.commit();
    #def update_dataStage02QuantificationAnalysis(self,data_I):
    #    '''update rows of data_stage02_quantification_analysis'''
    #    if data_I:
    #        for d in data_I:
    #            try:
    #                data_update = self.session.query(data_stage02_quantification_analysis).filter(
    #                        data_stage02_quantification_analysis.id==d['id']).update(
    #                        {
    #                        'analysis_id':d['analysis_id'],
    #                        'experiment_id':d['experiment_id'],
    #                        'sample_name_short':d['sample_name_short'],
    #                        'sample_name_abbreviation':d['sample_name_abbreviation'],
    #                        'time_point':d['time_point'],
    #                        #'time_point_units':d['time_point_units'],
    #                        'analysis_type':d['analysis_type'],
    #                        'used_':d['used_'],
    #                        'comment_':d['comment_']},
    #                        synchronize_session=False);
    #                if data_update == 0:
    #                    print('row not found.')
    #                    print(d)
    #            except IntegrityError as e:
    #                print(e);
    #            except SQLAlchemyError as e:
    #                print(e);
    #        self.session.commit();
    #def initialize_dataStage02_quantification_analysis(self):
    #    try:
    #        data_stage02_quantification_analysis.__table__.create(self.engine,True);
    #    except SQLAlchemyError as e:
    #        print(e);
    #def drop_dataStage02_quantification_analysis(self):
    #    try:
    #        data_stage02_quantification_analysis.__table__.drop(self.engine,True);
    #    except SQLAlchemyError as e:
    #        print(e);
    #def reset_dataStage02_quantification_analysis(self,analysis_id_I = None):
    #    try:
    #        if analysis_id_I:
    #            reset = self.session.query(data_stage02_quantification_analysis).filter(data_stage02_quantification_analysis.analysis_id.like(analysis_id_I)).delete(synchronize_session=False);
    #        else:
    #            reset = self.session.query(data_stage02_quantification_analysis).delete(synchronize_session=False);
    #        self.session.commit();
    #    except SQLAlchemyError as e:
    #        print(e);
   

