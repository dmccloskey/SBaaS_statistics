#SBaaS
from .stage02_quantification_enrichment_query import stage02_quantification_enrichment_query
#SBaaS base
from SBaaS_base.sbaas_template_io import sbaas_template_io
#Resources
from ddt_python.ddt_container_filterMenuAndChart2dAndTable import ddt_container_filterMenuAndChart2dAndTable
from listDict.listDict import listDict
from math import log10

class stage02_quantification_enrichment_io(stage02_quantification_enrichment_query,
                                    sbaas_template_io):
    
    def export_dataStage02QuantificationGeneSetEnrichment_js(self,analysis_id_I,
                query_I={},
                data_dir_I='tmp'):
        '''Export a joined table of geneSetEnrichment categories and FC levels
        Table
        '''
        
        data_O = self.get_rows_analysisID_dataStage02QuantificationGeneSetEnrichment(
            analysis_id_I,
            query_I = query_I);
        #dynamically add -log10(p-value)
        for d in data_O:
            d['log10(pvalue)']=-log10(d['pvalue']);

        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                    'experiment_id',
                    'sample_name_abbreviation',
                    'time_point',
                    'calculated_concentration_units',
                    'GO_id','GO_term',
                    'GO_database',
                    'GO_annotation',
                    'GO_annotation_mapping',
                    'GO_annotation_id',
                    'GO_ontology',
                    'enrichment_method',
                    'test_description'
                    ];
        data1_nestkeys = ['GO_term'];
        data1_keymap = {
            'xdata':'sample_name_abbreviation',
            'ydata':'log10(pvalue)',
            'serieslabel':'sample_name_abbreviation',
            'featureslabel':'GO_term',
            'rowslabel':'GO_term',
            'columnslabel':'pvalue',
            'tooltiplabel':'GO_definition',
            'tooltipdata':'pvalue',
            };     
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
                data_filtermenu=data_O,
                data_filtermenu_keys=data1_keys,
                data_filtermenu_nestkeys=data1_nestkeys,
                data_filtermenu_keymap=data1_keymap,
                data_svg_keys=None,
                data_svg_nestkeys=None,
                data_svg_keymap=None,
                data_table_keys=None,
                data_table_nestkeys=None,
                data_table_keymap=None,
                data_svg=None,
                data_table=None,
                svgtype='verticalbarschart2d_01',
                tabletype='responsivetable_01',
                svgx1axislabel='GO term',
                svgy1axislabel='log10(pvalue)',
                tablekeymap = [data1_keymap],
                svgkeymap = [data1_keymap], #calculated on the fly
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=[0], #calculated on the fly
                svgfilters=None,
                svgtileheader='Gene Set Enrichment Analysis',
                tablefilters=None,
                tableheaders=None,
                svgparameters_I= {
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 250, 'left': 50 },
                            "svgwidth":750,
                            "svgheight":450,
                            'colclass':"col-sm-12"
                            }
                );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());

    def import_dataStage02QuantificationEnrichmentClasses_COBRA(self,
        cobra_model_I,
        include_mets_I=True,
        include_rxns_I=True,
        include_genes_I=True,
        deformat_metID_I = True,
        ):
        '''
        map metabolite, reactions, and/or genes to model subsystems
        INPUT:
        OUTPUT:
        '''
        pass;

        #make the COBRA table
        from SBaaS_models.models_COBRA_query import models_COBRA_query
        qCOBRA01 = models_COBRA_query(self.session,self.engine,self.settings);
        qCOBRA01.initialize_supportedTables();

        data_mets_O = [];
        #query unique metabolites/subsystems
        if include_mets_I:
            data_mets_tmp = qCOBRA01.getGroup_subsystemsAndMetIDAndCount_modelID_dataStage02PhysiologyModelReactions(
                cobra_model_I,deformat_metID_I=deformat_metID_I)
            #rename columns
            for d in data_mets_tmp:
                tmp = {};
                tmp['enrichment_class']=d['subsystem']
                tmp['enrichment_class_description']=None
                tmp['enrichment_class_weight']=d['count']
                tmp['enrichment_class_database']="%s_%s"%(cobra_model_I,'metabolites');
                tmp['component_group_name']=d['met_id']
                tmp['component_name']=d['met_id']
                tmp['used_']=True
                tmp['comment_']=None
                data_mets_O.append(tmp);
        
        data_rxns_O = [];
        #query unique reactions/subsystems
        if include_rxns_I:
            data_rxns_tmp = qCOBRA01.getGroup_subsystemsAndRxnIDAndCount_modelID_dataStage02PhysiologyModelReactions(
                cobra_model_I)
            #rename columns
            for d in data_rxns_tmp:
                tmp = {};
                tmp['enrichment_class']=d['subsystem']
                tmp['enrichment_class_description']=None
                tmp['enrichment_class_weight']=d['count']
                tmp['enrichment_class_database']="%s_%s"%(cobra_model_I,'reactions');
                tmp['component_group_name']=d['rxn_id']
                tmp['component_name']=d['rxn_id']
                tmp['used_']=True
                tmp['comment_']=None
                data_rxns_O.append(tmp);
        
        data_genes_O = [];
        #query unique genes/subsystems
        if include_genes_I:
            data_genes_tmp = qCOBRA01.getGroup_subsystemsAndGenesAndCount_modelID_dataStage02PhysiologyModelReactions(
                cobra_model_I)
            #rename columns
            for d in data_genes_tmp:
                tmp = {};
                tmp['enrichment_class']=d['subsystem']
                tmp['enrichment_class_description']=None
                tmp['enrichment_class_weight']=d['count']
                tmp['enrichment_class_database']="%s_%s"%(cobra_model_I,'genes');
                tmp['component_group_name']=d['gene']
                tmp['component_name']=d['gene']
                tmp['used_']=True
                tmp['comment_']=None
                data_rxns_O.append(tmp);

        self.add_rows_table('data_stage02_quantification_enrichmentClasses',data_mets_O)
        self.add_rows_table('data_stage02_quantification_enrichmentClasses',data_rxns_O)
        self.add_rows_table('data_stage02_quantification_enrichmentClasses',data_genes_O)
    
    def export_dataStage02QuantificationPairWiseEnrichment_js(self,analysis_id_I,
                query_I={},
                data_dir_I='tmp'):
        '''Export a joined table of pairWiseEnrichment categories and FC levels
        Table
        '''
        
        data_O = self.get_rows_analysisID_dataStage02QuantificationPairWiseEnrichment(
            analysis_id_I,
            query_I = query_I);
        #dynamically add -log10(p-value)
        for d in data_O:
            if d['pvalue_corrected'] > 0.0:
                d['log10(pvalue)']=-log10(d['pvalue_corrected']);

        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                    'sample_name_abbreviation_1',
                    'sample_name_abbreviation_2',
                    'calculated_concentration_units',
                    'pvalue_corrected_description',
                    'enrichment_class',
                    'enrichment_method',
                    'enrichment_options',
                    'enrichment_class_database',
                    'test_description',
                    'pvalue_corrected_description',
                    ];
        data1_nestkeys = ['enrichment_class'];
        data1_keymap = {
            'xdata':'sample_name_abbreviation_2',
            'ydata':'log10(pvalue)',
            'serieslabel':'sample_name_abbreviation_2',
            'featureslabel':'enrichment_class',
            'rowslabel':'enrichment_class',
            'columnslabel':'pvalue_corrected',
            'tooltiplabel':'enrichment_class',
            'tooltipdata':'pvalue_corrected',
            };     
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
                data_filtermenu=data_O,
                data_filtermenu_keys=data1_keys,
                data_filtermenu_nestkeys=data1_nestkeys,
                data_filtermenu_keymap=data1_keymap,
                data_svg_keys=None,
                data_svg_nestkeys=None,
                data_svg_keymap=None,
                data_table_keys=None,
                data_table_nestkeys=None,
                data_table_keymap=None,
                data_svg=None,
                data_table=None,
                svgtype='verticalbarschart2d_01',
                tabletype='responsivetable_01',
                svgx1axislabel='enrichment_class',
                svgy1axislabel='log10(pvalue)',
                tablekeymap = [data1_keymap],
                svgkeymap = [data1_keymap], #calculated on the fly
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=[0], #calculated on the fly
                svgfilters=None,
                svgtileheader='Gene Set Enrichment Analysis',
                tablefilters=None,
                tableheaders=None,
                svgparameters_I= {
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 250, 'left': 50 },
                            "svgwidth":750,
                            "svgheight":450,
                            'colclass':"col-sm-12"
                            }
                );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());
    def export_dataStage02QuantificationPairWiseGeneSetEnrichment_js(self,analysis_id_I,
                query_I={},
                data_dir_I='tmp'):
        '''Export a joined table of geneSetEnrichment categories and FC levels
        Table
        '''
        
        data_O = self.get_rows_analysisID_dataStage02QuantificationPairWiseGeneSetEnrichment(
            analysis_id_I,
            query_I = query_I);
        #dynamically add -log10(p-value)
        for d in data_O:
            d['log10(pvalue)']=-log10(d['pvalue']);

        # make the tile objects  
        #data1 = filter menu and table    
        data1_keys = ['analysis_id',
                    'sample_name_abbreviation_1',
                    'sample_name_abbreviation_2',
                    'calculated_concentration_units',
                    'GO_id','GO_term',
                    'GO_database',
                    'GO_annotation',
                    'GO_annotation_mapping',
                    'GO_annotation_id',
                    'GO_ontology',
                    'enrichment_method',
                    'test_description'
                    ];
        data1_nestkeys = ['GO_term'];
        data1_keymap = {
            'xdata':'sample_name_abbreviation_2',
            'ydata':'log10(pvalue)',
            'serieslabel':'sample_name_abbreviation_2',
            'featureslabel':'GO_term',
            'rowslabel':'GO_term',
            'columnslabel':'pvalue',
            'tooltiplabel':'GO_definition',
            'tooltipdata':'pvalue',
            };     
        
        nsvgtable = ddt_container_filterMenuAndChart2dAndTable();
        nsvgtable.make_filterMenuAndChart2dAndTable(
                data_filtermenu=data_O,
                data_filtermenu_keys=data1_keys,
                data_filtermenu_nestkeys=data1_nestkeys,
                data_filtermenu_keymap=data1_keymap,
                data_svg_keys=None,
                data_svg_nestkeys=None,
                data_svg_keymap=None,
                data_table_keys=None,
                data_table_nestkeys=None,
                data_table_keymap=None,
                data_svg=None,
                data_table=None,
                svgtype='verticalbarschart2d_01',
                tabletype='responsivetable_01',
                svgx1axislabel='GO term',
                svgy1axislabel='log10(pvalue)',
                tablekeymap = [data1_keymap],
                svgkeymap = [data1_keymap], #calculated on the fly
                formtile2datamap=[0],
                tabletile2datamap=[0],
                svgtile2datamap=[0], #calculated on the fly
                svgfilters=None,
                svgtileheader='Gene Set Enrichment Analysis',
                tablefilters=None,
                tableheaders=None,
                svgparameters_I= {
                            "svgmargin":{ 'top': 50, 'right': 250, 'bottom': 250, 'left': 50 },
                            "svgwidth":750,
                            "svgheight":450,
                            'colclass':"col-sm-12"
                            }
                );

        if data_dir_I=='tmp':
            filename_str = self.settings['visualization_data'] + '/tmp/ddt_data.js'
        elif data_dir_I=='data_json':
            data_json_O = nsvgtable.get_allObjects_js();
            return data_json_O;
        with open(filename_str,'w') as file:
            file.write(nsvgtable.get_allObjects());
