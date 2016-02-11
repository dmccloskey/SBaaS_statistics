#system
import numpy
#resources
from python_statistics.calculate_correlation import calculate_correlation

class stage02_quantification_correlation_dependencies():
    def convert_profileStr2DataList(self,profiles_I):
        '''Convert a string list of profiles into a data object for plotting
        INPUT:
        profiles_I = [] of string profile_matches
        OUTPUT
        profiles_O = [{"profile_match":,
                       "profile_int":,
                       "profile_index":,
                       },...
                      ];
        '''        
        
        #convert each profile into its own data set
        calculatecorrelation = calculate_correlation();
        profiles_O=[];
        for profile in profiles_I:
            profile_int = calculatecorrelation.convert_profileStr2List(profile);
            for i,p_int in enumerate(profile_int):
                tmp={};
                tmp['profile_match']=profile;
                tmp['profile_int']=p_int;
                tmp['profile_index']=i;
                profiles_O.append(tmp);
        return profiles_O;
    def convert_trendStr2DataList(self,trends_I):
        '''Convert a string list of trends into a data object for plotting
        INPUT:
        trends_I = [] of string trend_matches
        OUTPUT
        trends_O = [{"trend_match":,
                       "trend_int":,
                       "trend_index":,
                       },...
                      ];
        '''        
        
        #convert each trend into its own data set
        calculatecorrelation = calculate_correlation();
        trends_O=[];
        for trend in trends_I:
            trend_int = calculatecorrelation.convert_profileStr2List(trend);
            for i,p_int in enumerate(trend_int):
                tmp={};
                tmp['trend_match']=trend;
                tmp['trend_int']=p_int;
                tmp['trend_index']=i;
                trends_O.append(tmp);
        return trends_O;
    def convert_patternStr2DataList(self,patterns_I):
        '''Convert a string list of patterns into a data object for plotting
        INPUT:
        patterns_I = [] of string pattern_matches
        OUTPUT
        patterns_O = [{"pattern_match":,
                       "pattern_int":,
                       "pattern_index":,
                       },...
                      ];
        '''        
        
        #convert each pattern into its own data set
        calculatecorrelation = calculate_correlation();
        patterns_O=[];
        for pattern in patterns_I:
            pattern_int = calculatecorrelation.convert_profileStr2List(pattern);
            for i,p_int in enumerate(pattern_int):
                tmp={};
                tmp['pattern_match']=pattern;
                tmp['pattern_int']=p_int;
                tmp['pattern_index']=i;
                patterns_O.append(tmp);
        return patterns_O;
