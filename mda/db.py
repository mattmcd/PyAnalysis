from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database
from docker import Client
from docker.utils import create_host_config

class Database():
    
    def __init__(self):
        db_port = 5432
        proxy_port = 5432
        self.db_name = 'db'
        self.proxy_name = 'db_proxy'
        proxy_config = create_host_config( 
            links={'db':'db'}, port_bindings={db_port:('127.0.0.1',proxy_port)} )
        self.db_kwargs = {'image': 'postgres:9.4', 'detach': True, 
            'name': self.db_name }
        self.proxy_kwargs = { 'image': 'svendowideit/ambassador', 
            'host_config': proxy_config, 'detach': True, 
            'name': self.proxy_name, 'ports': [proxy_port] }
        self.cli = Client(base_url='unix://var/run/docker.sock')
        self.db_container = []
        self.proxy_container = []

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
    
    def stop_app(self):
        self.cli.stop( self.db_container )
        self.cli.stop( self.proxy_container )

    def remove_app(self):
        self.cli.remove_container( self.proxy_name )
        self.cli.remove_container( self.db_name )

    def get_engine(self):
        '''Return engine connection to postgres db'''
        engine = create_engine('postgresql://postgres@localhost:5432/postgres')
        return engine
