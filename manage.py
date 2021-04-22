import time
from flask_script import Manager
from website import create_app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config_name', required=True)

if __name__ == '__main__':
    manager.run()
