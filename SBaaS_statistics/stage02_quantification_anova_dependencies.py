# Resources
from math import log

class stage02_quantification_anova_dependencies():
    def format_dataAnovaPlot(self,data_I):
        '''Reformat the data for an anova plot'''
        data_O = data_I;

        #add in -log10(pvalue)
        component_names_all = [];
        for d in data_O:
            # add in -log10(pvalue)
            d['pvalue_negLog10']=None;
            if not d['pvalue'] is None:
                d['pvalue_negLog10'] = -log(d['pvalue'],10);
            d['pvalue_corrected_negLog10'] = None;
            if not d['pvalue_corrected'] is None:
                d['pvalue_corrected_negLog10'] = -log(d['pvalue_corrected'],10);
            # get the component_name
            component_names_all.append(d['component_name']);

        #add in index for each component
        component_names_unique = list(set(component_names_all));
        component_names_unique.sort();
        component_names_dict = {};
        for i,cn in enumerate(component_names_unique):
            component_names_dict[cn]=i;
        for d in data_O:
            d['component_index']=component_names_dict[d['component_name']];

        return data_O;