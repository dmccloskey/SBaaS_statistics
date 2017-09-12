import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Documents/GitHub/SBaaS_base')
#sys.path.append('C:/Users/dmccloskey/Documents/GitHub/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_settings/settings_metabolomics.ini';
#filename = 'C:/Users/dmccloskey/Google Drive/SBaaS_settings/settings_metabolomics_remote.ini';
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
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_COBRA')
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

#make the pairWiseCorrelation tables
from SBaaS_statistics.stage02_quantification_pairWiseCorrelation_execute import stage02_quantification_pairWiseCorrelation_execute
pairWiseCorrelation01 = stage02_quantification_pairWiseCorrelation_execute(session,engine,pg_settings.datadir_settings);
#pairWiseCorrelation01.drop_dataStage02_quantification_pairWiseCorrelation();
pairWiseCorrelation01.initialize_supportedTables();
pairWiseCorrelation01.initialize_tables();

#make the analysis table
from SBaaS_statistics.stage02_quantification_analysis_execute import stage02_quantification_analysis_execute
analysis01 = stage02_quantification_analysis_execute(session,engine,pg_settings.datadir_settings);
analysis01.initialize_supportedTables();
analysis01.initialize_tables();

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

#make the count tables 
from SBaaS_statistics.stage02_quantification_count_execute import stage02_quantification_count_execute
count01 = stage02_quantification_count_execute(session,engine,pg_settings.datadir_settings);
count01.initialize_supportedTables();
count01.initialize_tables();

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

#make the histogram table
from SBaaS_statistics.stage02_quantification_histogram_execute import stage02_quantification_histogram_execute
hist01 = stage02_quantification_histogram_execute(session,engine,pg_settings.datadir_settings);
hist01.initialize_supportedTables();
hist01.initialize_tables();

#make the outliers tables
from SBaaS_statistics.stage02_quantification_outliers_execute import stage02_quantification_outliers_execute
outliers01 = stage02_quantification_outliers_execute(session,engine,pg_settings.datadir_settings);
outliers01.initialize_supportedTables();
outliers01.initialize_tables();

#make the pairWiseTest table
from SBaaS_statistics.stage02_quantification_pairWiseTest_execute import stage02_quantification_pairWiseTest_execute
pwt01 = stage02_quantification_pairWiseTest_execute(session,engine,pg_settings.datadir_settings);
pwt01.initialize_supportedTables();
pwt01.initialize_tables();

#make the dataPreProcessing tables
from SBaaS_statistics.stage02_quantification_dataPreProcessing_pairWiseTest_execute import stage02_quantification_dataPreProcessing_pairWiseTest_execute
dpppwt01 = stage02_quantification_dataPreProcessing_pairWiseTest_execute(session,engine,pg_settings.datadir_settings);
dpppwt01.initialize_supportedTables();
#dpppwt01.drop_tables();
dpppwt01.initialize_tables();

# Load R once
from r_statistics.r_interface import r_interface
r_calc = r_interface();

##Custom analysis tests:
#################################################################
#sys.path.append(pg_settings.datadir_settings['workspace']+'/sbaas_shared')
#from ALEsKOs01_shared.ALEsKOs01_commonRoutines import *

#analysis_ids_Metabolomics_str = 'ALEsKOs01_Metabolomics_0_evo04_0_11_evo04gndEvo01,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04gndEvo02,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04gndEvo03,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04sdhCBEvo01,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04sdhCBEvo02,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04sdhCBEvo03,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04tpiAEvo01,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04tpiAEvo02,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04tpiAEvo03,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04tpiAEvo04,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04ptsHIcrrEvo01,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04ptsHIcrrEvo02,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04ptsHIcrrEvo03,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04ptsHIcrrEvo04,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04pgiEvo01,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04pgiEvo02,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04pgiEvo03,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04pgiEvo04,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04pgiEvo05,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04pgiEvo06,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04pgiEvo07,\
#ALEsKOs01_Metabolomics_0_evo04_0_11_evo04pgiEvo08'
#analysis_ids_RNASequencing_str = 'ALEsKOs01_RNASequencing_0_evo04_0_11_evo04gndEvo01,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04gndEvo02,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04gndEvo03,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04sdhCBEvo01,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04sdhCBEvo02,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04sdhCBEvo03,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04tpiAEvo01,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04tpiAEvo02,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04tpiAEvo03,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04tpiAEvo04,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04ptsHIcrrEvo01,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04ptsHIcrrEvo02,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04ptsHIcrrEvo03,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04ptsHIcrrEvo04,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04pgiEvo01,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04pgiEvo02,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04pgiEvo03,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04pgiEvo04,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04pgiEvo05,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04pgiEvo06,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04pgiEvo07,\
#ALEsKOs01_RNASequencing_0_evo04_0_11_evo04pgiEvo08'
#analysis_ids_sampledFluxes_str = 'ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04gndEvo01,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04gndEvo02,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04gndEvo03,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04sdhCBEvo01,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04sdhCBEvo02,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04sdhCBEvo03,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04tpiAEvo01,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04tpiAEvo02,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04tpiAEvo03,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04tpiAEvo04,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04ptsHIcrrEvo01,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04ptsHIcrrEvo02,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04ptsHIcrrEvo03,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04ptsHIcrrEvo04,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04pgiEvo01,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04pgiEvo02,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04pgiEvo03,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04pgiEvo04,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04pgiEvo05,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04pgiEvo06,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04pgiEvo07,\
#ALEsKOs01_sampledFluxes_0_evo04_0_11_evo04pgiEvo08'

#sigMets,sigExpression,sigFluxes = execute_getSignificantComponents(
#    session,
#    analysis_ids_Metabolomics_str,
#    analysis_ids_RNASequencing_str,
#    analysis_ids_sampledFluxes_str
#    )
#sigComponents = {};
#sigComponents.update(sigMets);
#sigComponents.update(sigExpression);
#sigComponents.update(sigFluxes);

#filename_I = pg_settings.datadir_settings['workspace_data']+\
#    '/ALEsKOs01_impFeats/ALEsKOs01_0_11_correlationPatterns.csv'
    
#iobase = base_importData();
#iobase.read_csv(filename_I);
#analysis_table_I = iobase.data;  

#fitnessVsCorrelationPatterns,\
#    fitnessVsCorrelationPatterns_aid_stats,\
#    fitnessVsCorrelationPatterns_rnp_stats = execute_fitnessVsCorrelationPatterns(
#    session,
#    analysis_table_I,
#    pvalue_I = None,
#    correlation_coefficient_I = 0.88,
#    sigComponents_I=sigComponents,
#    optional_constraint_I=None,
#    )

#filename_O = pg_settings.datadir_settings['workspace_data']+\
#    '/_output/ALEsKOs01_0_11_fitnessVsCorrelationPatterns.csv'
    
#iobase = base_exportData(fitnessVsCorrelationPatterns);
#iobase.write_dict2csv(filename_O);

#filename_O = pg_settings.datadir_settings['workspace_data']+\
#    '/_output/ALEsKOs01_0_11_fitnessVsCorrelationPatterns_aid_stats.csv'
    
#iobase = base_exportData(fitnessVsCorrelationPatterns_aid_stats);
#iobase.write_dict2csv(filename_O);

#filename_O = pg_settings.datadir_settings['workspace_data']+\
#    '/_output/ALEsKOs01_0_11_fitnessVsCorrelationPatterns_rnp_stats.csv'
    
#iobase = base_exportData(fitnessVsCorrelationPatterns_rnp_stats);
#iobase.write_dict2csv(filename_O);

##Pipeline tests:
#################################################################
#pipelines = [
#    'ALEsKOs01_0_11_crossUnits'
#]
##build the connections for the pipeline
#for pipeline in pipelines:
#    print("running pipeline " + pipeline)
#    analysis01.execute_analysisPipeline(
#        pipeline_id_I = pipeline,
#        r_calc_I = r_calc,
#        )

##Analysis tests:
#################################################################
analysis_ids_run = [
    #'BloodProject01',
    #"BloodProject01_P_pre-post_02",
    #'BloodProject01_S01_D01_P_25C',
'BloodProject01_S01_0-D01_P_25C',
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

##TODO: update notebook...
#add in spls pipelines
data_O=[
    {'pipeline_id':'plsda_R_scaleAndCenter',
    'pipeline_order':1,
    'used_':True,'comment_':None,
    'pipeline_model':"plsda",
    'pipeline_method':"R",
    'pipeline_parameters':{
        'method':"cppls",
        'ncomp':7,
        'Y_add':"NULL",
        'scale':"TRUE",
        'validation':"none",
        'segments':0, #no CV
        'stripped':"FALSE",
        'lower':0.5,
        'upper':0.5, 
        'trunc_pow':"FALSE", 
        'weights':"NULL",
        }
    },
    {'pipeline_id':'svdPca_R_scaleAndCenter',
    'pipeline_order':1,
    'used_':True,'comment_':None,
    'pipeline_model':"pca",
    'pipeline_method':"R",
    'pipeline_parameters':{
        'method':"svd",
        'ncomp':7,
        'imputeMissingValues':"FALSE",
        'scale':"uv",
        'center':"TRUE",
        'cv':"none",
        'segments':0, #no CV
        'nruncv':1.0, 
        'type':"krzanowski", 
        }
    },
    {'pipeline_id':'beysianPca_R_scaleAndCenter',
    'pipeline_order':1,
    'used_':True,'comment_':None,
    'pipeline_model':"pca",
    'pipeline_method':"R",
    'pipeline_parameters':{
        'method':"bpca",
        'ncomp':7,
        'imputeMissingValues':"FALSE",
        'scale':"uv",
        'center':"TRUE",
        'cv':"none",
        'segments':0, #no CV
        'nruncv':1.0, 
        'type':"krzanowski", 
        }
    },
    {'pipeline_id':'robustPca_R_scaleAndCenter',
    'pipeline_order':1,
    'used_':True,'comment_':None,
    'pipeline_model':"robustPca",
    'pipeline_method':"R",
    'pipeline_parameters':{
        'robust':True,
        'cor':"FALSE",
        'scores':"TRUE",
        'covmat':"NULL",
        'na_action':'na.omit',
        'center':"TRUE",
        'scale':"TRUE",
        'ncomp':7,
        }
    },
]
#spls01.add_rows_table('data_stage02_quantification_spls_pipeline',data_O)

#define the different hyperparameter searches
#PLSDA using pls
splsHyperparameters = [
    {'pipeline_id':'plsda_R_scaleAndCenter',
     'param_dist':{"ncomp":7},
     'metric_method':['msep','rmsep','r2','r2x','q2'],
     'metric_options':None,
     'crossval_method':'CV',
     'crossval_options':{'validation':'CV','segments':10},
     'hyperparameter_method':'GridSearchCV',
     'hyperparameter_options':{},
     },
#PCA using pcaMethods
    {'pipeline_id':'svdPca_R_scaleAndCenter',
     'param_dist':{"ncomp":7},
     'metric_method':['msep','rmsep','r2','q2'],
     'metric_options':None,
     'crossval_method':'CV',
     'crossval_options':{'type':"krzanowski",'segments':10,'cv':'q2','nruncv':1.0},
     'hyperparameter_method':'GridSearchCV',
     'hyperparameter_options':{},
     },
    {'pipeline_id':'beysianPca_R_scaleAndCenter',
     'param_dist':{"ncomp":7},
     'metric_method':['msep','rmsep','r2','q2'],
     'metric_options':None,
     'crossval_method':'CV',
     'crossval_options':{'type':"krzanowski",'segments':10,'cv':'q2','nruncv':1.0},
     'hyperparameter_method':'GridSearchCV',
     'hyperparameter_options':{},
     },
    ];
#define svd models
svd_method = {
    'svd',
    'robustSvd',
    };

# analyses to run:
analysis_ids_run = [
# "IndustrialStrains01_0",
"IndustrialStrains0103_EColi_BL21",
"IndustrialStrains0103_EColi_C",
"IndustrialStrains0103_EColi_Crooks",
"IndustrialStrains0103_EColi_DH5a",
"IndustrialStrains0103_EColi_MG1655",
"IndustrialStrains0103_EColi_W",
"IndustrialStrains0103_EColi_W3110",
# "IndustrialStrains03_0"
        ];

for analysis_id in analysis_ids_run:
    print("running analysis " + analysis_id);  

    #pairWiseCorrelation01.reset_dataStage02_quantification_pairWiseCorrelation(
    #        tables_I = ['data_stage02_quantification_pairWiseCorrelation'], 
    #        analysis_id_I = analysis_id,
    #        warn_I=False);
    #pairWiseCorrelation01.execute_pairwiseCorrelationAverages(analysis_id,
    #    calculated_concentration_units_I=[
    #        'umol*gDW-1',
    #        'umol*gDW-1_glog_normalized'
    #    ],
    #    redundancy_I=False,
    #        query_object_descStats_I = 'stage02_quantification_descriptiveStats_query',
    #        query_func_descStats_I = 'get_rows_analysisIDAndOrAllColumns_dataStage02QuantificationDescriptiveStats',
    #    r_calc_I=r_calc);
    #pairWiseCorrelation01.clear_data()

    ##TODO: update notebooks...
    ##search for the optimal spls parameters
    #spls01.reset_dataStage02_quantification_spls(
    #    tables_I = ['data_stage02_quantification_spls_hyperparameter'],
    #    analysis_id_I=analysis_id,
    #    warn_I=False,
    #    );
    ##spls hyperparameter search (DEBUGGING spls methods)
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
    #    calculated_concentration_units_I=['mM_glog_normalized'],
    #    experiment_ids_I=[],
    #    sample_name_abbreviations_I=[],
    #    sample_name_shorts_I=[],
    #    component_names_I=[],
    #    component_group_names_I=[],
    #    time_points_I=[],
    #    r_calc_I=r_calc
    #    );
    ##pls hyperparameter search
    #for row in splsHyperparameters:
    #    spls01.execute_splsHyperparameter(
    #        analysis_id_I=analysis_id,
    #        pipeline_id_I=row['pipeline_id'],
    #        param_dist_I=row['param_dist'],
    #        test_size_I = 0.,
    #        metric_method_I = row['metric_method'],
    #        metric_options_I = row['metric_options'],
    #        crossval_method_I = row['crossval_method'],
    #        crossval_options_I = row['crossval_options'],
    #        hyperparameter_method_I = row['hyperparameter_method'],
    #        hyperparameter_options_I = row['hyperparameter_options'],
    #        calculated_concentration_units_I=['mM_glog_normalized'],
    #        experiment_ids_I=[],
    #        sample_name_abbreviations_I=[],
    #        sample_name_shorts_I=[],
    #        component_names_I=[],
    #        component_group_names_I=[],
    #        time_points_I=[],
    #        r_calc_I=r_calc
    #        );
    ##perform a spls analysis
    #spls01.reset_dataStage02_quantification_spls(
    #    tables_I = ['data_stage02_quantification_spls_impfeat',
    #                'data_stage02_quantification_spls_scores',
    #                'data_stage02_quantification_spls_loadings',
    #                'data_stage02_quantification_spls_loadingsResponse',
    #                'data_stage02_quantification_spls_axis'],
    #    analysis_id_I=analysis_id,
    #    warn_I=False,
    #    );
    ##PLSDA
    #spls01.execute_spls(
    #    analysis_id_I=analysis_id,
    #    pipeline_id_I='plsda_R_scaleAndCenter',
    #    test_size_I = 0.,
    #    loadings_methods_I=[
    #        {'metric_method':'loadings','metric_options':None},
    #        {'metric_method':'correlations','metric_options':None}],
    #    impfeat_methods_I=[
    #        {'impfeat_method':'coefficients','impfeat_options':None},
    #        {'impfeat_method':'VIP','impfeat_options':None},],
    #    scores_methods_I=[
    #        {'metric_method':'scores','metric_options':None},
    #        {'metric_method':'scores_response','metric_options':None},
    #        #{'metric_method':'explained_variance','metric_options':None},
    #        ],
    #    loadings_response_methods_I=[
    #        {'metric_method':'loadings_response','metric_options':None},
    #        {'metric_method':'correlations_response','metric_options':None},
    #        ],
    #    axis_metric_methods_I=[
    #        {'metric_method':'var_proportional','metric_options':None},
    #        {'metric_method':'var_cumulative','metric_options':None},
    #        ],
    #    calculated_concentration_units_I=['mM_glog_normalized'],
    #    experiment_ids_I=[],
    #    sample_name_abbreviations_I=[],
    #    sample_name_shorts_I=[],
    #    component_names_I=[],
    #    component_group_names_I=[],
    #    time_points_I=[],
    #    r_calc_I=r_calc
    #    )
    ##PCA
    #for pipeline_id in [
    #    'svdPca_R_scaleAndCenter',
    #    #'robustPca_R_scaleAndCenter',
    #    'beysianPca_R_scaleAndCenter']:
    #    spls01.execute_spls(
    #        analysis_id_I=analysis_id,
    #        pipeline_id_I=pipeline_id,
    #        test_size_I = 0.,
    #        loadings_methods_I=[
    #            {'metric_method':'loadings','metric_options':None},
    #            #{'metric_method':'correlations','metric_options':None}
    #            ],
    #        impfeat_methods_I=[],
    #        scores_methods_I=[
    #            {'metric_method':'scores','metric_options':None},
    #            ],
    #        loadings_response_methods_I=[],
    #        axis_metric_methods_I=[
    #            {'metric_method':'var_proportional','metric_options':None},
    #            {'metric_method':'var_cumulative','metric_options':None},
    #            ],
    #        calculated_concentration_units_I=['mM_glog_normalized'],
    #        experiment_ids_I=[],
    #        sample_name_abbreviations_I=[],
    #        sample_name_shorts_I=[],
    #        component_names_I=[],
    #        component_group_names_I=[],
    #        time_points_I=[],
    #        r_calc_I=r_calc
    #        )

##Analysis export tests:
#################################################################
    
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

##data export tests
######################################################
#covariance01.export_dataStage02QuantificationCovarianceSamples_js(analysis_id)
pairWiseCorrelation01.export_dataStage02QuantificationPairWiseCorrelation_js('IndustrialStrains03_0')
#pairWiseTable01.export_dataStage02QuantificationPairWiseTable_js('IndustrialStrains0103_EColi_W3110')

#heatmap01.export_dataStage02QuantificationDendrogramDescriptiveStats_js('ALEsKOs01_DNAResequencing_11_evo04pgi')
#descstats01.export_dataStage02QuantificationDescriptiveStats_js("ALEsKOs01_0-1-2-11_evo04pgiEvo01",plot_points_I=True,vertical_I = False)

#enrichment01.export_dataStage02QuantificationPairWiseGeneSetEnrichment_js('ALEsKOs01_0_evo04_0_11_evo04pgi');
#dpprep01.export_dataStage02QuantificationDataPreProcessingReplicatesCrossTable_js('BloodProject01_PLT');