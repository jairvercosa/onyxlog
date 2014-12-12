from fabric.api import *
#Default release - 0.0.1

env.release = '0.0.1'

def production():
    """Confgs da producao"""
    env.hosts = ['54.201.128.71']
    env.user = 'ubuntu'
    env.key_filename = '/Users/jairvercosa/Projects/python/gopipeserver.pem'
    env.settings = 'production'
    env.path = '/home/ubuntu/gopipe'
    env.port = 22

def deploy():
    """Deploy da ultima versao"""
    checkout_latest()
    symlink_current_release()
    migrate()
    restart_server()

def checkout_latest():
    """Atualiza ultimo codigo no repositorio"""
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    
    run("cd %(path)s; rm -rf repository" % env)
    run("cd %(path)s; mkdir repository" % env)
    run("cd %(path)s/repository; git clone https://jairvercosa@bitbucket.org/jairvercosa/gopipe.git" % env)
    #run("cd %(path)s/repository; git pull origin master" % env)
    run("cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/gopipe/.git*" % env)

def symlink_current_release():
    """carrega arquivos de setting"""
    with settings(warn_only=True):
        run('cd %(path)s/releases; rm -rf previous; mkdir previous; cp -r releases/current/* releases/previous;' % env)

    run('cd %(path)s; rm -rf releases/current/*' % env)
    run('cd %(path)s; cp -R releases/%(release)s/gopipe/* releases/current' % env)
    run('cd %(path)s; cp -R releases/current/gopipe/* gopipe;' % env)
    run('cd %(path)s/releases/current/gopipe/; mv settings_%(settings)s.py %(path)s/gopipe/settings.py' % env)
    run('%(path)s/bin/python %(path)s/manage.py collectstatic' % env)

def migrate():
    """Executa migrates do sistema"""
    run('cd %(path)s; bin/python %(path)s/manage.py migrate gopipe.acesso' % env)
    run('cd %(path)s; bin/python %(path)s/manage.py migrate gopipe.cliente' % env)
    run('cd %(path)s; bin/python %(path)s/manage.py migrate gopipe.core' % env)
    run('cd %(path)s; bin/python %(path)s/manage.py migrate gopipe.equipe' % env)
    run('cd %(path)s; bin/python %(path)s/manage.py migrate gopipe.oportunidade' % env)

def restart_server():
    """Reinicia servicos"""
    with settings(warn_only=True):
        run('sudo service nginx stop')
        run('sudo supervisorctl stop gopipe')
    
    run('sudo supervisorctl start gopipe')
    run('sudo service nginx start')

def rollback():
    run('cd %(path)s; mv releases/current releases/_previous;' % env)
    run('cd %(path)s; mv releases/previous releases/current;' % env)
    run('cd %(path)s; mv releases/_previous releases/previous;' % env)
    restart_server()