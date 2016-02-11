import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base')
from SBaaS_base.postgresql_settings import postgresql_settings
from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings_1.ini';
#filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_base/settings_metabolomics.ini';
pg_settings = postgresql_settings(filename);

# connect to the database from the settings file
pg_orm = postgresql_orm();
pg_orm.set_sessionFromSettings(pg_settings.database_settings);
session = pg_orm.get_session();
engine = pg_orm.get_engine();

# your app...
# SBaaS paths:
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_base')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_LIMS')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_statistics')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_visualization')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_resequencing')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_rnasequencing')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_physiology')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_quantification')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_isotopomer')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_statistics')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_models')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_MFA')
sys.path.append(pg_settings.datadir_settings['drive']+'/SBaaS_thermodynamics')
# SBaaS dependencies paths:
sys.path.append(pg_settings.datadir_settings['github']+'/sequencing_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/thermodynamics')
sys.path.append(pg_settings.datadir_settings['github']+'/component-contribution')
sys.path.append(pg_settings.datadir_settings['github']+'/io_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/sequencing_analysis')
sys.path.append(pg_settings.datadir_settings['github']+'/calculate_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/matplotlib_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/MDV_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/molmass')

#make the analysis table
from SBaaS_statistics.stage02_quantification_analysis_execute import stage02_quantification_analysis_execute
analysis01 = stage02_quantification_analysis_execute(session,engine,pg_settings.datadir_settings);
analysis01.drop_dataStage02_quantification_analysis();
analysis01.initialize_dataStage02_quantification_analysis();
analysis01.reset_dataStage02_quantification_analysis();
analysis01.import_dataStage02QuantificationAnalysis_add('data/tests/analysis_statistics/150805_Quantification_chemoCLim01_dataStage02_analysis01.csv')

#make the normalization methods table
from SBaaS_statistics.stage02_quantification_normalization_execute import stage02_quantification_normalization_execute
norm01 = stage02_quantification_normalization_execute(session,engine,pg_settings.datadir_settings);
norm01.drop_dataStage02_quantification_glogNormalized();
norm01.initialize_dataStage02_quantification_glogNormalized();
norm01.reset_dataStage02_quantification_glogNormalized('chemoCLim01');
norm01.execute_glogNormalization('chemoCLim01');
norm01.execute_getDataStage01PhysiologicalRatios('chemoCLim01');
norm01.execute_getDataStage01ReplicatesMI('chemoCLim01');
 #TODO:
 #export .csv
 #export .js (plot of normalized and un-normalized)

#make the descriptiveStats methods table
from SBaaS_statistics.stage02_quantification_descriptiveStats_execute import stage02_quantification_descriptiveStats_execute
descstats01 = stage02_quantification_descriptiveStats_execute(session,engine,pg_settings.datadir_settings);
descstats01.drop_dataStage02_quantification_descriptiveStats();
descstats01.initialize_dataStage02_quantification_descriptiveStats();
descstats01.reset_dataStage02_quantification_descriptiveStats('chemoCLim01');
descstats01.execute_descriptiveStats('chemoCLim01');
descstats01.export_dataStage02QuantificationDescriptiveStats_js('chemoCLim01');

#make the pairWiseTest table
from SBaaS_statistics.stage02_quantification_pairWiseTest_execute import stage02_quantification_pairWiseTest_execute
pwt01 = stage02_quantification_pairWiseTest_execute(session,engine,pg_settings.datadir_settings);
pwt01.drop_dataStage02_quantification_pairWiseTest();
pwt01.initialize_dataStage02_quantification_pairWiseTest();
pwt01.reset_dataStage02_quantification_pairWiseTest('chemoCLim01');
pwt01.execute_pairwiseTTest('chemoCLim01',concentration_units_I=['mM_glog_normalized','height_ratio_glog_normalized','ratio']);
pwt01.export_dataStage02QuantificationPairWiseTest_js('chemoCLim01');

#TODO: anova also computes a pairwise test (combine anova and pairWiseTest modules?)
#make the anova table 
from SBaaS_statistics.stage02_quantification_anova_execute import stage02_quantification_anova_execute
anova01 = stage02_quantification_anova_execute(session,engine,pg_settings.datadir_settings);
anova01.drop_dataStage02_quantification_anova();
anova01.initialize_dataStage02_quantification_anova();
anova01.reset_dataStage02_quantification_anova('chemoCLim01');
anova01.execute_anova('chemoCLim01',concentration_units_I=['mM_glog_normalized','height_ratio_glog_normalized','ratio']);
# TODO:
# export to .csv
# export to .js

#make the pca tables
from SBaaS_statistics.stage02_quantification_pca_execute import stage02_quantification_pca_execute
pca01 = stage02_quantification_pca_execute(session,engine,pg_settings.datadir_settings);
pca01.drop_dataStage02_quantification_pca();
pca01.initialize_dataStage02_quantification_pca();
pca01.reset_dataStage02_quantification_pca_scores('chemoCLim01');
pca01.reset_dataStage02_quantification_pca_loadings('chemoCLim01');
pca01.execute_pca('chemoCLim01',concentration_units_I=['mM_glog_normalized','height_ratio_glog_normalized']);
pca01.export_dataStage02QuantificationPca_js('chemoCLim01');

#make the heatmap tables
from SBaaS_statistics.stage02_quantification_heatmap_execute import stage02_quantification_heatmap_execute
heatmap01 = stage02_quantification_heatmap_execute(session,engine,pg_settings.datadir_settings);
heatmap01.drop_dataStage02_quantification_heatmap();
heatmap01.initialize_dataStage02_quantification_heatmap();
heatmap01.reset_dataStage02_quantification_heatmap('chemoCLim01');
heatmap01.reset_dataStage02_quantification_dendrogram('chemoCLim01');
heatmap01.execute_heatmap('chemoCLim01',concentration_units_I=['mM_glog_normalized','height_ratio_glog_normalized','ratio']);
heatmap01.export_dataStage02QuantificationHeatmap_js('chemoCLim01');