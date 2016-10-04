import sys
sys.path.append('/usr/local/lib/SBaaS/SBaaS_base')

from SBaaS_base.postgresql_settings import postgresql_settings

# read in the settings file
filename = '/home/user/settings/settings_metabolomics_docker.ini';
pg_settings = postgresql_settings(filename);

# your app...
# SBaaS paths:
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_base')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_webServer')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_LIMS')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_ale')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_statistics')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_visualization')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_resequencing')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_rnasequencing')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_physiology')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_quantification')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_isotopomer')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_statistics')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_models')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_MFA')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_thermodynamics')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/genomeScale_MFA')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_models')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/SBaaS_COBRA')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/genomeScale_MFA_INCA')
# SBaaS dependencies paths:
sys.path.append(pg_settings.datadir_settings['sbaas']+'/sequencing_utilities')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/thermodynamics')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/component-contribution')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/io_utilities')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/sequencing_analysis')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/quantification_analysis')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/matplotlib_utilities')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/MDV_utilities')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/molmass')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/python_statistics')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/r_statistics')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/listDict')
sys.path.append(pg_settings.datadir_settings['sbaas']+'/ddt_python')

from SBaaS_webServer.server import server
server.run(port_I=8088,public_I=True,webServer_settings_filename_I=filename);
