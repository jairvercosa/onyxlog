from fabric.api import *
#Default release - 0.0.1

env.release = '0.0.2'

def production():
    """Confgs da producao"""
    env.hosts = ['177.55.104.109']
    env.user = 'root'
    env.password = '2fC@+Zh%tx'
    env.settings = 'production'
    env.server = 'production'
    env.path = '/onyxlog'
    env.port = 22

def offlineProduction():
    """Confgs da producao offline"""
    env.hosts = ['ubuntu-VirtualBox']
    env.user = 'onyxlog'
    env.password = 'onyxlog!@#'
    env.settings = 'production'
    env.server = 'offline'
    env.path = '/onyxlog'
    env.port = 22

def deploy():
    """Deploy da ultima versao"""
    checkout_latest()
    symlink_current_release()
    #migrate()
    #restart_server()

def checkout_latest():
    """Atualiza ultimo codigo no repositorio"""
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    
    run("cd %(path)s; rm -rf repository" % env)
    run("cd %(path)s; mkdir repository" % env)
    run("cd %(path)s/repository; git clone https://github.com/jairvercosa/onyxlog.git" % env)
    #run("cd %(path)s/repository; git pull origin master" % env)
    run("cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/onyxlog/.git*" % env)

def symlink_current_release():
    """carrega arquivos de setting"""
    with settings(warn_only=True):
        run('cd %(path)s/releases; rm -rf previous; mkdir previous; cp -r releases/current/* releases/previous;' % env)

    run('cd %(path)s; rm -rf releases/current/*' % env)
    run('cd %(path)s; cp -R releases/%(release)s/onyxlog/* releases/current' % env)
    #run('cd %(path)s; sudo chmod 777 releases/current' % env)
    run('cd %(path)s/releases/current/onyxlog/; mv settings_%(settings)s.py settings.py' % env)
    run('cd %(path)s; cp -R releases/current/* /onyxlog;' % env)

    run('%(path)s/bin/python %(path)s/manage.py collectstatic' % env)

def migrate():
    """Executa migrates do sistema"""
    run('cd %(path)s; bin/python %(path)s/manage.py migrate' % env)

def rollback():
    run('cd %(path)s; mv releases/current releases/_previous;' % env)
    run('cd %(path)s; mv releases/previous releases/current;' % env)
    run('cd %(path)s; mv releases/_previous releases/previous;' % env)
    restart_server()

def restart_server():
    """Reinicia servicos"""
    if env.server == 'offline':
        with settings(warn_only=True):
            run('sudo /etc/init.d/nginx stop')
            run('sudo supervisorctl stop onyxlog')
            run('sudo supervisorctl start onyxlog')
            run('sudo /etc/init.d/nginx start')
            
            #run('rm -rf %(path)s/tmp/supervisor.sock' % env)
            #run('rm -rf %(path)s/tmp/supervisord.pid' % env)
            #run('sudo fuser -k 8002/tcp')
            #run('rm -rf %(path)s/tmp/gunicorn.pid' % env)

        #run('source %(path)s/bin/activate; cd %(path)s/onyxlog; supervisord;' % env)
        
    elif env.settings!='testenv':
        with settings(warn_only=True):
            run('/etc/init.d/nginx stop')
            run('kill -8 cat %(path)s/uwsgi_pid.pid' % env)
            run('rm -f %(path)s/onyxlog.sock' % env)
            
        run('source %(path)s/bin/activate; uwsgi --ini %(path)s/uwsgi.ini' % env)

    run('/etc/init.d/nginx start')