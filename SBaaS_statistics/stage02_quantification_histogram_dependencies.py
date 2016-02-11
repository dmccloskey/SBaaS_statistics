class stage02_quantification_histogram_dependencies():
    def record_histogram(self,analysis_id,feature_id,feature_units,bin,bin_width,frequency):
        '''make the histogram listDict
        INPUT:
        OUTPUT:
        '''
        data_O = [];
        for i,b in enumerate(bin):
            tmp = {
                'analysis_id':analysis_id,
                'feature_id':feature_id,
                'feature_units':feature_units,
                'bin':b,
                'bin_width':bin_width[i],
                'frequency':int(frequency[i]),
                'used_':True,
                'comment_':None};
            data_O.append(tmp);
        return data_O;