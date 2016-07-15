import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Documents/GitHub/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_settings/settings_metabolomics.ini';
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



#make the descriptiveStats methods table
from SBaaS_statistics.stage02_quantification_descriptiveStats_execute import stage02_quantification_descriptiveStats_execute
descstats01 = stage02_quantification_descriptiveStats_execute(session,engine,pg_settings.datadir_settings);
descstats01.initialize_supportedTables();
descstats01.initialize_tables();

#make the heatmap tables
from SBaaS_statistics.stage02_quantification_heatmap_execute import stage02_quantification_heatmap_execute
heatmap01 = stage02_quantification_heatmap_execute(session,engine,pg_settings.datadir_settings);
heatmap01.initialize_supportedTables();
heatmap01.initialize_tables();

#make the pca tables
from SBaaS_statistics.stage02_quantification_pca_execute import stage02_quantification_pca_execute
pca01 = stage02_quantification_pca_execute(session,engine,pg_settings.datadir_settings);
pca01.initialize_supportedTables();
pca01.initialize_tables();

#make the pls tables
from SBaaS_statistics.stage02_quantification_pls_execute import stage02_quantification_pls_execute
pls01 = stage02_quantification_pls_execute(session,engine,pg_settings.datadir_settings);
pls01.initialize_supportedTables();
pls01.initialize_tables();

#make the svd tables
from SBaaS_statistics.stage02_quantification_svd_execute import stage02_quantification_svd_execute
svd01 = stage02_quantification_svd_execute(session,engine,pg_settings.datadir_settings);
#svd01.drop_dataStage02_quantification_svd();
svd01.initialize_supportedTables();
svd01.initialize_tables();

#make the pairWiseTable tables
from SBaaS_statistics.stage02_quantification_pairWiseTable_execute import stage02_quantification_pairWiseTable_execute
pairWiseTable01 = stage02_quantification_pairWiseTable_execute(session,engine,pg_settings.datadir_settings);
#pairWiseTable01.drop_dataStage02_quantification_pairWiseTable();
pairWiseTable01.initialize_supportedTables();
pairWiseTable01.initialize_tables();

#make the pairWiseCorrelation tables
from SBaaS_statistics.stage02_quantification_pairWiseCorrelation_execute import stage02_quantification_pairWiseCorrelation_execute
pairWiseCorrelation01 = stage02_quantification_pairWiseCorrelation_execute(session,engine,pg_settings.datadir_settings);
#pairWiseCorrelation01.drop_dataStage02_quantification_pairWiseCorrelation();
pairWiseCorrelation01.initialize_supportedTables();
pairWiseCorrelation01.initialize_tables();

#make the dataPreProcessing tables
from SBaaS_statistics.stage02_quantification_dataPreProcessing_replicates_execute import stage02_quantification_dataPreProcessing_replicates_execute
dpprep01 = stage02_quantification_dataPreProcessing_replicates_execute(session,engine,pg_settings.datadir_settings);
dpprep01.initialize_supportedTables();
#dpprep01.drop_tables();
dpprep01.initialize_tables();

#make the dataPreProcessing tables
from SBaaS_statistics.stage02_quantification_dataPreProcessing_averages_execute import stage02_quantification_dataPreProcessing_averages_execute
dppave01 = stage02_quantification_dataPreProcessing_averages_execute(session,engine,pg_settings.datadir_settings);
dppave01.initialize_supportedTables();
#dppave01.drop_tables();
dppave01.initialize_tables();

#make the covariance tables
from SBaaS_statistics.stage02_quantification_covariance_execute import stage02_quantification_covariance_execute
covariance01 = stage02_quantification_covariance_execute(session,engine,pg_settings.datadir_settings);
covariance01.initialize_supportedTables();
#covariance01.drop_tables();
covariance01.initialize_tables();

#make the tree tables
from SBaaS_statistics.stage02_quantification_tree_execute import stage02_quantification_tree_execute
tree01 = stage02_quantification_tree_execute(session,engine,pg_settings.datadir_settings);
tree01.initialize_supportedTables();
#tree01.drop_tables();
tree01.initialize_tables();

#make the svm tables
from SBaaS_statistics.stage02_quantification_svm_execute import stage02_quantification_svm_execute
svm01 = stage02_quantification_svm_execute(session,engine,pg_settings.datadir_settings);
svm01.initialize_supportedTables();
#svm01.drop_tables();
svm01.initialize_tables();

#make the anova table 
from SBaaS_statistics.stage02_quantification_anova_execute import stage02_quantification_anova_execute
anova01 = stage02_quantification_anova_execute(session,engine,pg_settings.datadir_settings);
anova01.initialize_supportedTables();
anova01.initialize_tables();

#make the enrichment table 
from SBaaS_statistics.stage02_quantification_enrichment_execute import stage02_quantification_enrichment_execute
enrichment01 = stage02_quantification_enrichment_execute(session,engine,pg_settings.datadir_settings);
enrichment01.initialize_supportedTables();
enrichment01.initialize_tables();

#make the correlation tables 
from SBaaS_statistics.stage02_quantification_correlation_execute import stage02_quantification_correlation_execute
corr01 = stage02_quantification_correlation_execute(session,engine,pg_settings.datadir_settings);
corr01.initialize_supportedTables();
corr01.initialize_tables();

#make the spls table 
from SBaaS_statistics.stage02_quantification_spls_execute import stage02_quantification_spls_execute
spls01 = stage02_quantification_spls_execute(session,engine,pg_settings.datadir_settings);
spls01.initialize_supportedTables();
spls01.initialize_tables();

#make the pairWisePLS tables
from SBaaS_statistics.stage02_quantification_pairWisePLS_execute import stage02_quantification_pairWisePLS_execute
pairWisePLS01 = stage02_quantification_pairWisePLS_execute(session,engine,pg_settings.datadir_settings);
pairWisePLS01.initialize_supportedTables();
#pairWisePLS01.drop_tables();
pairWisePLS01.initialize_tables();



analysis_ids_run = [
    #"ALEsKOs01_DNAResequencing_0_11",
    #'ALEsKOs01_0_evo04_0_11_evo04gndEvo01',
        'ALEsKOs01_RNASequencing_0_11_evo04Evo01',
        #"ALEsKOs01_0_evo04_0-1-2-11_evo04pgiEvo01",
        #'ALEsKOs01_0_11_evo04pgi',
        #"ALEsKOs01_0-1-2-11_evo04pgiEvo01",
        #'ALEsKOs01_0_evo04_0_11_evo04pgi',
        #'ALEsKOs01_0',
        #'ALEsKOs01_0_11',
        #'ALEsKOs01',
        #"rpomut02",
        #"chemoCLim01",
        #"chemoNLim01",
        #"rpomut01",
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

#RNAsequencing
mv_value_operator = [
    {'value':None,'operator':'NA','feature':'mean'},
    #{'value':0.0,'operator':'<='},
    ]
features_histogram = ['calculated_concentration'];
feature_units = ['FPKM','FPKM_log2_normalized'];
n_bins_histogram = [];

covariance_model = [
    {'data_matrix_shape':'featuresBySamples','model':"MinCovDet",'method':"MinCovDet",'options':None},
    {'data_matrix_shape':'featuresBySamples','model':"EmpiricalCovariance",'method':"EmpiricalCovariance",'options':None},
    {'data_matrix_shape':'samplesByFeatures','model':"MinCovDet",'method':"MinCovDet",'options':None},
    {'data_matrix_shape':'samplesByFeatures','model':"EmpiricalCovariance",'method':"EmpiricalCovariance",'options':None},
    ];

tree_model = [
    {'pipeline_id':"AdaBoostClassifier_scikit-learn_centerAndScale",
     'impfeat_methods':[
         {'impfeat_method':'feature_importance','impfeat_options':None},
         {'impfeat_method':'RFECV','impfeat_options':{'step':1, 'cv':2, 'scoring':None, 'estimator_params':None, 'verbose':0}},
        ],
     'response_class_methods':[
         {'response_class_method':'class_probability','response_class_options':None},
         #{'response_class_method':'decision_function','response_class_options':None},
         ],
     },
    {'pipeline_id':"RandomForestClassifier_scikit-learn_centerAndScale",
     'impfeat_methods':[
         {'impfeat_method':'RFECV','impfeat_options':{'step':1, 'cv':2, 'scoring':None, 'estimator_params':None, 'verbose':0}},
         {'impfeat_method':'feature_importance','impfeat_options':None},
        ],
     'response_class_methods':[
         {'response_class_method':'class_probability','response_class_options':None},
         #{'response_class_method':'decision_function','response_class_options':None},
         ],
     },
    {'pipeline_id':"DecisionTreeClassifier_scikit-learn_centerAndScale",
     'impfeat_methods':[
         {'impfeat_method':'RFECV','impfeat_options':{'step':1, 'cv':2, 'scoring':None, 'estimator_params':None, 'verbose':0}},
         {'impfeat_method':'feature_importance','impfeat_options':None},
        ],
     'response_class_methods':[
         {'response_class_method':'class_probability','response_class_options':None},
         #{'response_class_method':'decision_function','response_class_options':None},
         ],
     },
    #{'model':"ExtraTreesClassifier",'method':"scikit-learn",'parameters':{'n_estimators':100, 'criterion':'gini', 'max_depth':None, 'min_samples_split':2, 'min_samples_leaf':1, 'min_weight_fraction_leaf':0.0, 'max_features':'auto', 'max_leaf_nodes':None, 'bootstrap':False, 'oob_score':False, 'n_jobs':1, 'random_state':None, 'verbose':0, 'warm_start':False, 'class_weight':None},
    # 'impfeat_methods':[
    #     {'impfeat_method':'RFECV','impfeat_options':{'step':1, 'cv':2, 'scoring':None, 'estimator_params':None, 'verbose':0}},
    #     {'impfeat_method':'feature_importance','impfeat_options':None},
    #    ],
    # 'response_class_methods':[
    #     {'response_class_method':'class_probability','response_class_options':None},
    #     #{'response_class_method':'decision_function','response_class_options':None},
    #     ],
    # },
    ];
tree_hyperparameters = [
    {'pipeline_id':'AdaBoostClassifier_scikit-learn_centerAndScale',
     'param_dist':{"AdaBoostClassifier__n_estimators": [25,50,100],"AdaBoostClassifier__learning_rate": [.1, 1, 10]},
     'metric_method':'accuracy','metric_options':None,
     'crossval_method':'LabelKFold','crossval_options':{'n_folds':2},
     'hyperparameter_method':'GridSearchCV','hyperparameter_options':{'fit_params':None, 'n_jobs':1, 'iid':True, 'refit':True, 'verbose':0, 'error_score':'raise'},
     },
    {'pipeline_id':'RandomForestClassifier_scikit-learn_centerAndScale',
     'param_dist':{"RandomForestClassifier__max_depth": [3, None],"RandomForestClassifier__max_features": [1, 10],"RandomForestClassifier__min_samples_split": [1, 10],"RandomForestClassifier__min_samples_leaf": [1, 10],"RandomForestClassifier__bootstrap": [True, False],"RandomForestClassifier__criterion": ["gini", "entropy"]},
     'metric_method':'accuracy','metric_options':None,
     'crossval_method':'LabelKFold','crossval_options':{'n_folds':2},
     'hyperparameter_method':'RandomizedSearchCV','hyperparameter_options':{'n_iter':10, 'fit_params':None, 'n_jobs':1, 'iid':True, 'refit':True, 'verbose':0,  'random_state':None, 'error_score':'raise'},
     },
    ];

svm_model = [
    {'pipeline_id':"SVC_scikit-learn_centerAndScale",
     'impfeat_methods':[
         {'impfeat_method':'coefficients','impfeat_options':None},
         {'impfeat_method':'RFECV','impfeat_options':{'step':1, 'cv':2, 'scoring':None, 'estimator_params':None, 'verbose':0}},
        ],
     'response_class_methods':[
         {'response_class_method':'decision_function','response_class_options':None},
         ],
     },
    #Fails:
    #{'pipeline_id':"BaggingClassifier_scikit-learn_centerAndScale",
    # 'impfeat_methods':[
    #     {'impfeat_method':'RFECV','impfeat_options':{'step':1, 'cv':2, 'scoring':None, 'estimator_params':None, 'verbose':0}},
    #     {'impfeat_method':'coefficients','impfeat_options':None},
    #    ],
    # 'response_class_methods':[
    #     {'response_class_method':'class_probability','response_class_options':None},
    #     {'response_class_method':'decision_function','response_class_options':None},
    #     ],
    # },
    {'pipeline_id':"SGDClassifier_scikit-learn_centerAndScale",
     'impfeat_methods':[
         {'impfeat_method':'RFECV','impfeat_options':{'step':1, 'cv':2, 'scoring':None, 'estimator_params':None, 'verbose':0}},
         {'impfeat_method':'coefficients','impfeat_options':None},
        ],
     'response_class_methods':[
         {'response_class_method':'class_probability','response_class_options':None},
         {'response_class_method':'decision_function','response_class_options':None},
         ],
     },
    ];
svm_hyperparameters = [
    {'pipeline_id':'SVC_scikit-learn_centerAndScale',
     'param_dist':{"SVC__C": [.1, 1, 10]},
     'metric_method':'accuracy','metric_options':None,
     'crossval_method':'LabelKFold','crossval_options':{'n_folds':2},
     'hyperparameter_method':'GridSearchCV','hyperparameter_options':{'fit_params':None, 'n_jobs':1, 'iid':True, 'refit':True, 'verbose':0, 'error_score':'raise'},
     },
    #{'pipeline_id':'BaggingClassifier_scikit-learn_centerAndScale',
    # 'param_dist':{},
    # 'metric_method':'accuracy','metric_options':None,
    # 'crossval_method':'LabelKFold','crossval_options':{'n_folds':2},
    # 'hyperparameter_method':'RandomizedSearchCV','hyperparameter_options':{'n_iter':10, 'fit_params':None, 'n_jobs':1, 'iid':True, 'refit':True, 'verbose':0,  'random_state':None, 'error_score':'raise'},
    # },
    #{'pipeline_id':'SGDClassifier_scikit-learn_centerAndScale',
    # 'param_dist':{},
    # 'metric_method':'accuracy','metric_options':None,
    # 'crossval_method':'LabelKFold','crossval_options':{'n_folds':2},
    # 'hyperparameter_method':'RandomizedSearchCV','hyperparameter_options':{'n_iter':10, 'fit_params':None, 'n_jobs':1, 'iid':True, 'refit':True, 'verbose':0,  'random_state':None, 'error_score':'raise'},
    # },
    ];

algorithm_test = [
    #{'enrichment_algorithm':'weight01','test_description':'globaltest'},
    #{'enrichment_algorithm':'classic','test_description':'globaltest'},
    #{'enrichment_algorithm':'classic','test_description':'fisher'},
    #{'enrichment_algorithm':'elim','test_description':'globaltest'},
    {'enrichment_algorithm':'elim','test_description':'fisher'},
    {'enrichment_algorithm':'weight','test_description':'fisher'},
    {'enrichment_algorithm':'weight01','test_description':'fisher'},
    {'enrichment_algorithm':'parentchild','test_description':'fisher'},
    ]


## Load R once
#from r_statistics.r_interface import r_interface
#r_calc = r_interface();#get RNAsequencing data

for analysis_id in analysis_ids_run:
    print("running analysis " + analysis_id);

    # perform a correlation analysis
    heatmap01.reset_dataStage02_quantification_heatmap(analysis_id);
    heatmap01.reset_dataStage02_quantification_dendrogram(analysis_id);
    heatmap01.execute_heatmap(
        analysis_id,
        calculated_concentration_units_I=['count_cuffnorm_log2_normalized'],
        sample_name_shorts_I=[],
        component_names_I=[],
        order_componentNameBySampleNameShort_I = False,
        order_sample_name_shorts_I=False,
        order_component_names_I=False,);
    
    ##search for the optimal spls parameters
    #spls01.reset_dataStage02_quantification_spls(
    #    tables_I = ['data_stage02_quantification_spls_hyperparameter'],
    #    analysis_id_I=analysis_id,
    #    warn_I=False,
    #    );
    #spls01.execute_splsHyperparameter(
    #    analysis_id_I=analysis_id,
    #    pipeline_id_I='splsda_R_scaleAndCenter',
    #    param_dist_I={"kappa": 0.5,
    #                    "K": [1,2,3,4,5],
    #                    "eta": [0.1,.3,.5,.7,.9],
    #                    "classifier":'lda',
    #                'scale_x':"FALSE",
    #                    },
    #    test_size_I = 0.,
    #    metric_method_I = 'error_rate',
    #    metric_options_I = None,
    #    crossval_method_I = 'v-fold',
    #    crossval_options_I = {'fold':5
    #                            },
    #    hyperparameter_method_I = 'GridSearchCV',
    #    hyperparameter_options_I = {
    #        'plot_it':"FALSE", 'n_core':2,
    #        },
    #    calculated_concentration_units_I=['umol*gDW-1_glog_normalized'],
    #    experiment_ids_I=[],
    #    sample_name_abbreviations_I=[],
    #    sample_name_shorts_I=[],
    #    component_names_I=[],
    #    component_group_names_I=[],
    #    time_points_I=[],
    #    r_calc_I=r_calc
    #    );
    ##perform a spls analysis
    #spls01.reset_dataStage02_quantification_spls(
    #    tables_I = ['data_stage02_quantification_spls_impfeat',
    #                'data_stage02_quantification_spls_scores',
    #                'data_stage02_quantification_spls_loadings',
    #                'data_stage02_quantification_spls_loadingsResponse'],
    #    analysis_id_I=analysis_id,
    #    warn_I=False,
    #    );
    #spls01.execute_spls(
    #    analysis_id_I=analysis_id,
    #    pipeline_id_I='splsda_mixOmics_R_scaleAndCenter',
    #    test_size_I = 0.,
    #    impfeat_methods_I=[
    #        {'coefficients':'feature_importance','impfeat_options':None},
    #        {'VIP':'feature_importance','impfeat_options':None}],
    #    response_class_methods_I=[],
    #    calculated_concentration_units_I=['umol*gDW-1_glog_normalized'],
    #    experiment_ids_I=[],
    #    sample_name_abbreviations_I=[],
    #    sample_name_shorts_I=[],
    #    component_names_I=[],
    #    component_group_names_I=[],
    #    time_points_I=[],
    #    r_calc_I=r_calc
    #    )

    ##perform a gene_set_enrichment analysis:
    #enrichment01.reset_dataStage02_quantification_enrichment(
    #    tables_I = ['data_stage02_quantification_geneSetEnrichment'],
    #    analysis_id_I = analysis_id,
    #    warn_I = False,
    #    );

    #for row in algorithm_test:
    #    print("running algorithm " + row['enrichment_algorithm']);
    #    print("running statistic " + row['test_description']);        
    #    enrichment01.execute_geneSetEnrichment(
    #        analysis_id_I = analysis_id,
    #        calculated_concentration_units_I=['log2(FC)'],
    #        experiment_ids_I=[],
    #        time_points_I=[],
    #        sample_name_abbreviations_I=[],
    #        component_names_I=[],
    #        enrichment_method_I='topGO',
    #        enrichment_options_I={
    #            'pvalue_threshold':0.05,
    #            'GO_database':'GO.db',
    #            'enrichment_algorithm':row['enrichment_algorithm'],
    #            'test_description':row['test_description'],
    #            'GO_ontology':"BP",
    #            'GO_annotation':"annFUN.org",
    #            'GO_annotation_mapping':"org.EcK12.eg.db",
    #            'GO_annotation_id' :'alias'},
    #        pvalue_threshold_I = 0.05,
    #        pvalue_corrected_description_I = "bonferroni",
    #        query_object_descStats_I = 'stage02_quantification_dataPreProcessing_averages_query',
    #        r_calc_I=r_calc
    #        );
    
#pairWiseTable01.export_dataStage02QuantificationPairWiseTableReplicates_js(
#    "ALEsKOs01_RNASequencing_0_evo04_11_evo04Evo01",
#    #query_I = {},
#    query_I = {'where':[
#        {"table_name":'data_stage02_quantification_pairWiseTable_replicates',
#        'column_name':'sample_name_abbreviation_1',
#        'value':'OxicEvo04EcoliGlc',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#        {"table_name":'data_stage02_quantification_pairWiseTable_replicates',
#        'column_name':'sample_name_abbreviation_2',
#        'value':'OxicEvo04EcoliGlc',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#        {"table_name":'data_stage02_quantification_pairWiseTable_replicates',
#        'column_name':'calculated_concentration_units',
#        'value':'FPKM_log2_normalized',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#    ]
#    },
#    single_plot_I=True
#    );

#pairWiseTable01.export_dataStage02QuantificationPairWiseTableReplicates_chordDiagram_js(
#    "ALEsKOs01_0_evo04_0_11_evo04pgi",
#    query_I = 
#    {'where':[
#        {"table_name":'data_stage02_quantification_pairWiseTable_replicates',
#        'column_name':'sample_name_abbreviation_1',
#        'value':'OxicEvo04EcoliGlc',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#        {"table_name":'data_stage02_quantification_pairWiseTable_replicates',
#        'column_name':'sample_name_abbreviation_2',
#        'value':'OxicEvo04EcoliGlc',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#        {"table_name":'data_stage02_quantification_pairWiseTable_replicates',
#        'column_name':'calculated_concentration_units',
#        'value':'umol*gDW-1_glog_normalized',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#        {"table_name":'data_stage02_quantification_pairWiseTable_replicates',
#        'column_name':'component_group_name',
#        'value':"('{atp}'::text[])",
#        'operator':'=ANY',
#        'connector':'AND'
#            },#
#    ]
#    },
#    );

#pairWiseCorrelation01.export_dataStage02QuantificationPairWiseCorrelationReplicates_js("ALEsKOs01_RNASequencing_0_evo04_11_evo04Evo01",
#    query_I = 
#    {'where':[
#        {"table_name":'data_stage02_quantification_pairWiseCorrelation_replicates',
#        'column_name':'sample_name_abbreviation_1',
#        'value':'OxicEvo04EcoliGlc',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#        {"table_name":'data_stage02_quantification_pairWiseCorrelation_replicates',
#        'column_name':'sample_name_abbreviation_2',
#        'value':'OxicEvo04EcoliGlc',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#        {"table_name":'data_stage02_quantification_pairWiseCorrelation_replicates',
#        'column_name':'calculated_concentration_units',
#        'value':'FPKM_log2_normalized',
#        'operator':'LIKE',
#        'connector':'AND'
#            },
#    ]
#    },
#    );

#covariance01.export_dataStage02QuantificationCovarianceSamples_js('ALEsKOs01_RNASequencing_0_evo04_11_evo04Evo01')
#pairWiseCorrelation01.export_dataStage02QuantificationPairWiseCorrelation_js('ALEsKOs01_RNASequencing_0_evo04_0_11_evo04gnd')
#pairWiseTable01.export_dataStage02QuantificationPairWiseTable_js('ALEsKOs01_RNASequencing_0_evo04_0_11_evo04gnd')