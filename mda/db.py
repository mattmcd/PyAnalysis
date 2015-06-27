from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database, database_exists
from docker import Client
from docker.utils import create_host_config

class Database():
    
    def __init__(self, name='testdb'):
        db_port = 5432
        proxy_port = 5432
        self.db_name = 'db' # Name of db container
        self.proxy_name = 'db_proxy'
        self.db = name # Name of database on db app
        proxy_config = create_host_config( 
            links={'db':'db'}, port_bindings={db_port:('127.0.0.1',proxy_port)} )
        self.db_kwargs = {'image': 'postgres:9.4', 'detach': True, 
            'name': self.db_name }
        self.proxy_kwargs = { 'image': 'svendowideit/ambassador', 
            'host_config': proxy_config, 'detach': True, 
            'name': self.proxy_name, 'ports': [proxy_port] }
        self.cli = Client(base_url='unix://var/run/docker.sock')
        self.db_container = None
        self.proxy_container = None

    def up(self):
        '''Startup db and proxy, creating containers if required'''
        self.create_app()
        self.start_app()

    def down(self, remove=True):
        '''Stop db and proxy, remove containers'''
        self.stop_app()
        if remove:
            self.remove_app()

    def __create_container(self, c_name, c_field, c_args ):
        try:
            c_res = self.cli.inspect_container( getattr(self,c_name) )
            setattr(self, c_field, {'Id': c_res['Id'], 'Warnings': None })
        except:
            setattr(self, c_field, 
                self.cli.create_container(**getattr(self,c_args)) )

    def create_app(self):
        '''Create the database and proxy'''
        self.__create_container( 'db_name', 'db_container', 'db_kwargs')
        self.__create_container( 'proxy_name', 'proxy_container', 'proxy_kwargs')

    def start_app(self):
        self.cli.start( self.db_container )
        self.cli.start( self.proxy_container )
    
    def __stop_container(self, c_name, c_field):
        if getattr(self, c_field) is None:
            try:
                c_res = self.cli.inspect_container( getattr(self,c_name) )
                setattr(self, c_field, {'Id': c_res['Id'], 'Warnings': None })
            except:
                # Container does not exist
                pass
        self.cli.stop( getattr(self, c_field))                

    def stop_app(self):
        self.__stop_container( 'db_name', 'db_container' )
        self.__stop_container( 'proxy_name', 'proxy_container' )

    def remove_app(self):
        self.cli.remove_container( self.proxy_name )
        self.cli.remove_container( self.db_name )

    def get_engine(self):
        '''Return engine connection to postgres db'''
        db_url = 'postgresql://postgres@localhost:5432/' + self.db
        if not(database_exists( db_url )):
            create_database( db_url )
        engine = create_engine( db_url )
        return engine

if __name__ == '__main__':
    '''Usage: mda.db up to start'''
    import sys
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        action = 'up'

    db = Database()
    getattr(db, action)() 
