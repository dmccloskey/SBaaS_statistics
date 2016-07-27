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