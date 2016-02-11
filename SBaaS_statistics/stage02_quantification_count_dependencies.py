class stage02_quantification_count_dependencies():
    def record_count(self,analysis_id,feature_id,feature_units,element_ids,element_counts,elements_count_fraction):
        '''make the count listDict
        INPUT:
        OUTPUT:
        '''
        data_O = [];
        for i,e in enumerate(element_ids):
            tmp = {
                'analysis_id':analysis_id,
                'feature_id':feature_id,
                'feature_units':feature_units,
                'element_id':e,
                'frequency':int(element_counts[i]),
                'fraction':elements_count_fraction[i],
                'used_':True,
                'comment_':None};
            data_O.append(tmp);
        return data_O;
    def record_count_correlation(self,
            analysis_id,feature_id,feature_units,
            distance_measure,correlation_coefficient_threshold,
            element_ids,element_counts,elements_count_fraction):
        '''make the count listDict
        INPUT:
        OUTPUT:
        '''
        data_O = [];
        for i,e in enumerate(element_ids):
            tmp = {
                'analysis_id':analysis_id,
                'feature_id':feature_id,
                'feature_units':feature_units,
                'distance_measure':distance_measure,
                'correlation_coefficient_threshold':correlation_coefficient_threshold,
                'element_id':e,
                'frequency':int(element_counts[i]),
                'fraction':elements_count_fraction[i],
                'used_':True,
                'comment_':None};
            data_O.append(tmp);
        return data_O;
    def make_pvalueThresholdStr(self,comparator,pvalue):
        '''make a string representation of a comparator and pvalue
        INPUT:
        comparator = string, e.g. '>'
        pvalue = float, e.g. 0.8
        OUTPUT:
        pvalueThresholdStr_O = string
        STATUS:
        only simple comparators are currently supported
        '''
        pvalueThresholdStr_O = comparator + str(pvalue);
        return pvalueThresholdStr_O;
    def make_correlationCoefficientThresholdStr(self,comparator,correlation_coefficient):
        '''make a string representation of a comparator and correlation_coefficient
        INPUT:
        comparator = string, e.g. '>'
        correlation_coefficient = float, e.g. 0.8
        OUTPUT:
        correlationCoefficientThresholdStr_O = string
        STATUS:
        only simple comparators are currently supported
        '''
        correlationCoefficientThresholdStr_O = comparator + str(correlation_coefficient);
        return correlationCoefficientThresholdStr_O;