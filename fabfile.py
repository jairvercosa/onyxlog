from fabric.api import *
#Default release - 0.0.1

env.release = '0.0.1'

def production():
    """Confgs da producao"""
    env.hosts = ['177.55.104.109']
    env.user = 'root'
    env.password = '2fC@+Zh%tx'
    env.settings = 'production'
    env.path = '/onyxlog'
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
    run("cd %(path)s/repository; git clone https://github.com/jairvercosa/onyxlog.git" % env)
    #run("cd %(path)s/repository; git pull origin master" % env)
    run("cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/onyxlog/.git*" % env)

def symlink_current_release():
    """carrega arquivos de setting"""
    with settings(warn_only=True):
        run('cd %(path)s/releases; rm -rf previous; mkdir previous; cp -r releases/current/* releases/previous;' % env)

    run('cd %(path)s; rm -rf releases/current/*' % env)
    run('cd %(path)s; cp -R releases/%(release)s/onyxlog/* releases/current' % env)
    run('cd %(path)s; cp -R releases/current/onyxlog/* onyxlog;' % env)
    run('cd %(path)s/releases/current/onyxlog/; mv settings_%(settings)s.py %(path)s/onyxlog/settings.py' % env)
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
    if env.settings!='testenv':
        with settings(warn_only=True):
            run('/etc/init.d/nginx stop')
            run('kill -8 `cat %(path)s/uwsgi_pid.pid`' % env)
            run('rm -f %(path)s/onyxlog.sock' % env)
            
        run('source %(path)s/bin/activate; uwsgi --ini %(path)s/uwsgi.ini' % env)
    run('/etc/init.d/nginx start')