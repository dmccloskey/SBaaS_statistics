import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings_metabolomics.ini';
pg_settings = postgresql_settings(filename);

# connect to the database from the settings file
pg_orm = postgresql_orm();
pg_orm.set_sessionFromSettings(pg_settings.database_settings);
session = pg_orm.get_session();
engine = pg_orm.get_engine();

# your app...
# SBaaS paths:
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_base')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_LIMS')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_visualization')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_resequencing')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_rnasequencing')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_physiology')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_quantification')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_isotopomer')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_models')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_MFA')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_thermodynamics')
# SBaaS dependencies paths:
sys.path.append(pg_settings.datadir_settings['github']+'/sequencing_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/thermodynamics')
sys.path.append(pg_settings.datadir_settings['github']+'/component-contribution')
sys.path.append(pg_settings.datadir_settings['github']+'/io_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/sequencing_analysis')
sys.path.append(pg_settings.datadir_settings['github']+'/matplotlib_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/MDV_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/molmass')
sys.path.append(pg_settings.datadir_settings['github']+'/python_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/r_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/listDict')
sys.path.append(pg_settings.datadir_settings['github']+'/ddt_python')

#make the analysis table
from SBaaS_statistics.stage02_quantification_analysis_execute import stage02_quantification_analysis_execute
analysis01 = stage02_quantification_analysis_execute(session,engine,pg_settings.datadir_settings);
analysis01.initialize_supportedTables();
analysis01.initialize_dataStage02_quantification_analysis();
#read the analyses from .csv
#analysis01.import_rows_table_add_csv('data_stage02_quantification_analysis',pg_settings.datadir_settings['workspace_data']+'/_input/151128_Quantification_ALEsKOs01_analysis01_test.csv');
#analysis01.reset_dataStage02_quantification_analysis("ALEsKOs01_0_test");
#analysis01.export_rows_tables_table_js(
#    tables_I=['data_stage02_quantification_analysis'],
#    query_I ={
#            #'select':{'data_stage02_quantification_analysis':'analysis_id'},
#            'select':[{'table_name':'data_stage02_quantification_analysis'}],
#              'where':[{'table_name':'data_stage02_quantification_analysis',
#                        'column_name':'analysis_id',
#                        'value':"'ALEsKOs01_0'",
#                        'operator':'LIKE',
#                        'connector':'AND'
#                        },
#                        ],
#              #'group_by':{'data_stage02_quantification_analysis':'analysis_id'},
#              'order_by':[{'table_name':'data_stage02_quantification_analysis',
#                            'column_name':'analysis_id',
#                            'order':'ASC',
#                            },
#                        ],
#              'limit':10.0,
#               },
#    data_dir_I = 'tmp',
#    );

#make the outliers tables
from SBaaS_statistics.stage02_quantification_outliers_execute import stage02_quantification_outliers_execute
outliers01 = stage02_quantification_outliers_execute(session,engine,pg_settings.datadir_settings);
outliers01.initialize_dataStage02_quantification_outliers();

#make the normalization methods table
from SBaaS_statistics.stage02_quantification_normalization_execute import stage02_quantification_normalization_execute
norm01 = stage02_quantification_normalization_execute(session,engine,pg_settings.datadir_settings);
norm01.initialize_dataStage02_quantification_glogNormalized();

#make the descriptiveStats methods table
from SBaaS_statistics.stage02_quantification_descriptiveStats_execute import stage02_quantification_descriptiveStats_execute
descstats01 = stage02_quantification_descriptiveStats_execute(session,engine,pg_settings.datadir_settings);
descstats01.initialize_dataStage02_quantification_descriptiveStats();

#make the pairWiseTest table
from SBaaS_statistics.stage02_quantification_pairWiseTest_execute import stage02_quantification_pairWiseTest_execute
pwt01 = stage02_quantification_pairWiseTest_execute(session,engine,pg_settings.datadir_settings);
pwt01.initialize_dataStage02_quantification_pairWiseTest();

#make the heatmap tables
from SBaaS_statistics.stage02_quantification_heatmap_execute import stage02_quantification_heatmap_execute
heatmap01 = stage02_quantification_heatmap_execute(session,engine,pg_settings.datadir_settings);
heatmap01.initialize_supportedTables();
heatmap01.initialize_dataStage02_quantification_heatmap();

#make the pls tables
from SBaaS_statistics.stage02_quantification_pls_execute import stage02_quantification_pls_execute
pls01 = stage02_quantification_pls_execute(session,engine,pg_settings.datadir_settings);
#pls01.drop_dataStage02_quantification_pls();
pls01.initialize_dataStage02_quantification_pls();

#make the histogram table
from SBaaS_statistics.stage02_quantification_histogram_execute import stage02_quantification_histogram_execute
hist01 = stage02_quantification_histogram_execute(session,engine,pg_settings.datadir_settings);
hist01.initialize_dataStage02_quantification_histogram();

#make the count table
from SBaaS_statistics.stage02_quantification_count_execute import stage02_quantification_count_execute
count01 = stage02_quantification_count_execute(session,engine,pg_settings.datadir_settings);
count01.initialize_dataStage02_quantification_count();

#make the pca tables
from SBaaS_statistics.stage02_quantification_pca_execute import stage02_quantification_pca_execute
pca01 = stage02_quantification_pca_execute(session,engine,pg_settings.datadir_settings);
pca01.initialize_dataStage02_quantification_pca();

#make the svd tables
from SBaaS_statistics.stage02_quantification_svd_execute import stage02_quantification_svd_execute
svd01 = stage02_quantification_svd_execute(session,engine,pg_settings.datadir_settings);
#svd01.drop_dataStage02_quantification_svd();
svd01.initialize_supportedTables();
svd01.initialize_tables();
#svd01.initialize_dataStage02_quantification_svd();

analysis_ids_run = [
        #"ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01",
        #'ALEsKOs01_0',
        #"rpomut02",
        "chemoCLim01",
        "chemoNLim01",
        "rpomut01",
        ];
pls_model_method = {
    #'PCR-DA':'svdpc',
    'PLS-DA':"cppls"
    };
pca_model_method = {
    #'PCA':'bpca',
    'PCA':"svd",
    #'PCA':"robustPca",
    };
svd_method = {
    'svd',
    'robustSvd',
    };
features_histogram = ['mean','cv','var','median','calculated_concentration'];
#feature_units = ['umol*gDW-1_glog_normalized','umol*gDW-1'];
feature_units = ['mM_glog_normalized','mM'];
n_bins_histogram = [];
features_countCorrelationProfile = ['profile_match', 'component_match', 'profile_match_description'];
features_countCorrelationTrend = ['trend_match', 'component_match', 'trend_match_description'];
features_countCorrelationPattern = ['pattern_match', 'component_match', 'pattern_match_description'];
distance_measures=[
    #'spearman',
    'pearson'
    ];
correlation_coefficient_thresholds={'>':0.8,'<':-0.8,} #correlation_coefficient > 0.88 = pvalue < 0.05

## Load R once
#from r_statistics.r_interface import r_interface
#r_calc = r_interface();

for analysis_id in analysis_ids_run:
    print("running analysis " + analysis_id);
    ## normalize the data using a glog normalization
    #norm01.reset_dataStage02_quantification_glogNormalized(analysis_id);
    #norm01.execute_glogNormalization(analysis_id,r_calc_I=r_calc);
    ## load in quantified data
    #norm01.execute_getDataStage01PhysiologicalRatios(analysis_id);
    #norm01.execute_getDataStage01ReplicatesMI(analysis_id);
    ## calculate the mean, variance, lb/ub, etc. of the normalized data
    #descstats01.reset_dataStage02_quantification_descriptiveStats(analysis_id);
    #descstats01.execute_descriptiveStats(analysis_id,r_calc_I=r_calc);
    ## check for outliers
    #outliers01.reset_dataStage02_quantification_outliersDeviation(analysis_id);
    #outliers01.execute_calculateOutliersDeviation(analysis_id,
    #            component_names_I = ['23dpg.23dpg_1.Light'],
    #            concentration_units_I = ['umol*gDW-1'],
    #            deviation_I = 0.2,
    #            method_I = 'var');
    #outliers01.execute_calculateOutliersPCA(analysis_id,
    #            concentration_units_I = ['umol*gDW-1'],
    #            r_calc_I=r_calc);
    ## check for outliers using SVD
    #svd01.reset_dataStage02_quantification_svd(
    #        tables_I = [], 
    #        analysis_id_I = analysis_id,
    #        );
    #for k in svd_method:
    #    svd01.execute_svd(analysis_id,
    #        concentration_units_I=['umol*gDW-1_glog_normalized'],
    #        r_calc_I=r_calc,
    #        svd_method_I = k,
    #        );
    ## check for groupings of samples and outliers in the normalized data set using PCA
    #pca01.reset_dataStage02_quantification_pca_scores(analysis_id);
    #pca01.reset_dataStage02_quantification_pca_loadings(analysis_id);
    #pca01.reset_dataStage02_quantification_pca_validation(analysis_id);
    #for k,v in pca_model_method.items():
    #    pca01.execute_pca(analysis_id,
    #        #concentration_units_I=['umol*gDW-1_glog_normalized'],
    #        concentration_units_I=['mM_glog_normalized'],
    #        r_calc_I=r_calc,             
    #        pca_model_I = k,
    #        pca_method_I = v,
    #        imputeMissingValues="TRUE",
    #        cv="q2",
    #        ncomps="7",
    #        #scale="none",
    #        #center="FALSE",
    #        scale="uv",
    #        center="TRUE",
    #        segments="10",
    #        nruncv="1",
    #        crossValidation_type="krzanowski",
    #        );
    ## perform a pair-wise comparison of each sample in the normalized data set
    #pwt01.reset_dataStage02_quantification_pairWiseTest(analysis_id);
    #pwt01.execute_pairwiseWilcoxonRankSumTest(analysis_id,
    #    concentration_units_I=[
    #        'mM_glog_normalized',
    #        'height_ratio_glog_normalized',
    #        'ratio',
    #        'mM',
    #        'height_ratio',
    #    ],
    #    r_calc_I=r_calc);
    #pwt01.execute_pairwiseTTest(analysis_id,
    #    concentration_units_I=[
    #        'mM_glog_normalized',
    #        'height_ratio_glog_normalized',
    #        'ratio',
    #        'mM',
    #        'height_ratio',
    #    ],
    #    r_calc_I=r_calc);
    ## bin the data
    #hist01.reset_dataStage02_quantification_histogram(analysis_id_I = analysis_id);
    #hist01.execute_binFeatures(
    #    analysis_id_I = analysis_id,
    #    features_I = features_histogram,
    #    feature_units_I = feature_units,
    #    n_bins_I = n_bins_histogram,
    #    );
    ## count the data
    #count01.reset_dataStage02_quantification_countCorrelationProfile(analysis_id_I = analysis_id);
    #count01.execute_countElementsInFeatures_correlationProfile(
    #    analysis_id_I = analysis_id,
    #    features_I = features_countCorrelationProfile,
    #    feature_units_I = feature_units,
    #    distance_measures_I = distance_measures,
    #    correlation_coefficient_thresholds_I = correlation_coefficient_thresholds,
    #    );
    #count01.reset_dataStage02_quantification_countCorrelationTrend(analysis_id_I = analysis_id);
    #count01.execute_countElementsInFeatures_correlationTrend(
    #    analysis_id_I = analysis_id,
    #    features_I = features_countCorrelationTrend,
    #    feature_units_I = feature_units,
    #    distance_measures_I = distance_measures,
    #    correlation_coefficient_thresholds_I = correlation_coefficient_thresholds,
    #    );
    #count01.reset_dataStage02_quantification_countCorrelationPattern(analysis_id_I = analysis_id);
    #count01.execute_countElementsInFeatures_correlationPattern(
    #    analysis_id_I = analysis_id,
    #    features_I = features_countCorrelationPattern,
    #    feature_units_I = feature_units,
    #    distance_measures_I = distance_measures,
    #    correlation_coefficient_thresholds_I = correlation_coefficient_thresholds,
    #    );
    ## perform a pls-da analysis
    #pls01.reset_dataStage02_quantification_pls_scores(analysis_id);
    #pls01.reset_dataStage02_quantification_pls_loadings(analysis_id);
    #pls01.reset_dataStage02_quantification_pls_validation(analysis_id);
    #pls01.reset_dataStage02_quantification_pls_vip(analysis_id_I=analysis_id);
    #pls01.reset_dataStage02_quantification_pls_loadingsResponse(analysis_id_I=analysis_id);
    #pls01.reset_dataStage02_quantification_pls_coefficients(analysis_id_I=analysis_id);
    #for k,v in pls_model_method.items():
    #    pls01.execute_plsda(
    #        analysis_id_I = analysis_id,
    #        #concentration_units_I=['umol*gDW-1_glog_normalized'],
    #        concentration_units_I=['mM_glog_normalized'],
    #        r_calc_I=r_calc,
    #        pls_model_I = k,
    #        method = v,
    #        response_I = None,
    #        factor_I= "sample_name_abbreviation",
    #        ncomp = 7,
    #        Y_add = "NULL",
    #        scale = "TRUE",
    #        validation = "CV",
    #        segments = 5,
    #        #segments = 10,
    #        stripped = "FALSE",
    #        lower = 0.5,
    #        upper = 0.5, 
    #        trunc_pow = "FALSE", 
    #        weights = "NULL",
    #        p_method = "fdr",
    #        nperm = 999);
    ## perform a correlation analysis
    #heatmap01.reset_dataStage02_quantification_heatmap(analysis_id);
    #heatmap01.reset_dataStage02_quantification_dendrogram(analysis_id);
    #heatmap01.execute_heatmap(
    #    analysis_id,
    #    #concentration_units_I=['umol*gDW-1_glog_normalized'],
    #    concentration_units_I=['mM_glog_normalized'],
    #    sample_name_shorts_I=[],
    #    #component_names_I=['cit.cit_2.Light',
    #    #                   'akg.akg_1.Light',
    #    #                   'fum.fum_1.Light',
    #    #                   'glx.glx_1.Light',
    #    #                   'icit.icit_2.Light',
    #    #                   'mal-L.mal-L_1.Light',
    #    #                   'succ.succ_1.Light',
    #    #                   'acon-C.acon-C_1.Light'],
    #    order_componentNameBySampleNameShort_I = True,
    #    );
    #heatmap01.reset_dataStage02_quantification_heatmap_descriptiveStats(analysis_id);
    #heatmap01.reset_dataStage02_quantification_dendrogram_descriptiveStats(analysis_id);
    #heatmap01.execute_heatmap_descriptiveStats(
    #    analysis_id,
    #    #concentration_units_I=['umol*gDW-1_glog_normalized'],
    #    concentration_units_I=['mM_glog_normalized'],
    #    sample_name_abbreviations_I=[],
    #    #component_names_I=['cit.cit_2.Light',
    #    #                   'akg.akg_1.Light',
    #    #                   'fum.fum_1.Light',
    #    #                   'glx.glx_1.Light',
    #    #                   'icit.icit_2.Light',
    #    #                   'mal-L.mal-L_1.Light',
    #    #                   'succ.succ_1.Light',
    #    #                   'acon-C.acon-C_1.Light'],
    #    order_componentNameBySampleNameAbbreviation_I = True,
    #    value_I = 'mean'
    #    );
    
#norm01.export_dataStage02QuantificationGlogNormalizedCrossTable_js('ALEsKOs01_0');
#heatmap01.export_dataStage02QuantificationHeatmap_js('ALEsKOs01_0');
#pca01.export_dataStage02QuantificationPCAScoresAndLoadings_js('ALEsKOs01_0');
#pca01.export_dataStage02QuantificationPCABiPlotAndValidation_js('ALEsKOs01_0');
#pls01.export_dataStage02QuantificationPLSScoresAndLoadings_js('ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01');
#pls01.export_dataStage02QuantificationPLSBiPlotAndValidation_js('ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01');
#count01.export_dataStage02QuantificationCountCorrelationPattern_js('ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01');
#pls01.export_dataStage02QuantificationPLSSPlot_js('ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01');
#descstats01.export_dataStage02QuantificationDescriptiveStats_js('ALEsKOs01_0',plot_points_I=True);

#svd01.export_dataStage02QuantificationSVDV_js("ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01");
#svd01.export_dataStage02QuantificationSVDU_js("ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01");
#svd01.export_dataStage02QuantificationSVDD_js("ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01");
#svd01.export_rows_analysisID_dataStage02QuantificationSVD_csv(
#    tables_I=['data_stage02_quantification_svd_d'],
#    analysis_id_I = "ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01",
#    filename_O = 'tmp.csv'
#    );
#svd01.export_dataStage02QuantificationSVDScoresAndLoadings_js("ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01");
#svd01.export_dataStage02QuantificationSVDScoresAndLoadingsAndMethods_js("ALEsKOs01_0-1-2-3-11_evo04pgiEvo02");
