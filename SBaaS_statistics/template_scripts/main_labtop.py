import sys
sys.path.append('C:/Users/dmccloskey/Documents/Github/SBaaS_base')

from SBaaS_base.postgresql_settings import postgresql_settings
#from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey/Google Drive/SBaaS_settings/settings_metabolomics_labtop.ini';
pg_settings = postgresql_settings(filename);

## connect to the database from the settings file
## NOTES: inital user settings
##        data directories specified in the settings will be used after database session and engine
##        are updated after login
#pg_orm = postgresql_orm();
#pg_orm.set_sessionFromSettings(pg_settings.database_settings);
#session = pg_orm.get_session();
#engine = pg_orm.get_engine();

# your app...
# SBaaS paths:
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_base')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_webServer')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_LIMS')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_ale')
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
sys.path.append(pg_settings.datadir_settings['github']+'/genomeScale_MFA')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_models')
sys.path.append(pg_settings.datadir_settings['github']+'/SBaaS_COBRA')
sys.path.append(pg_settings.datadir_settings['github']+'/genomeScale_MFA_INCA')
# SBaaS dependencies paths:
sys.path.append(pg_settings.datadir_settings['github']+'/sequencing_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/thermodynamics')
sys.path.append(pg_settings.datadir_settings['github']+'/component-contribution')
sys.path.append(pg_settings.datadir_settings['github']+'/io_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/sequencing_analysis')
sys.path.append(pg_settings.datadir_settings['github']+'/quantification_analysis')
sys.path.append(pg_settings.datadir_settings['github']+'/matplotlib_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/MDV_utilities')
sys.path.append(pg_settings.datadir_settings['github']+'/molmass')
sys.path.append(pg_settings.datadir_settings['github']+'/python_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/r_statistics')
sys.path.append(pg_settings.datadir_settings['github']+'/listDict')
sys.path.append(pg_settings.datadir_settings['github']+'/ddt_python')

from SBaaS_webServer.server import server
server.run(port_I=8080,public_I=False,webServer_settings_filename_I=filename);
