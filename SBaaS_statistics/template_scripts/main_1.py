import sys
sys.path.append('C:/Users/dmccloskey-sbrg/Documents/GitHub/SBaaS_base')
#sys.path.append('C:/Users/dmccloskey/Google Drive/SBaaS_base')

from SBaaS_base.postgresql_settings import postgresql_settings
#from SBaaS_base.postgresql_orm import postgresql_orm

# read in the settings file
filename = 'C:/Users/dmccloskey-sbrg/Google Drive/SBaaS_settings/settings_metabolomics_WY.ini';
pg_settings = postgresql_settings(filename);

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
server.run(port_I=8088,public_I=True,webServer_settings_filename_I=filename);
