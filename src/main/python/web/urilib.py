from urllib.parse import urlsplit

    
    
class URI(object):
    '''
    URI
    '''
        
    def __init__(self, uri):
        '''
        URI constructor
        '''
        self.__uri = uri
        self.__structure = urlsplit(uri)

    def scheme(self):
        return self.__structure.scheme
    
    def authority(self):
        return self.__structure.netloc
    
    def path(self):
        return self.__structure.__path
    
    def query(self):
        return self.__structure.query
    
    def fragment(self):
        return self.__structure.fragment
    
    def username(self):
        return self.__structure.username
    
    def password(self):
        return self.__structure.password
    
    def hostname(self):
        return self.__structure.hostname
    
    def port(self):
        return self.__structure.port

    


    def GET(self):
        pass
    
    def PUT(self):
        pass
    
    def POST(self):
        pass
    
    def HEAD(self):
        pass
    
    def OPTIONS(self):
        pass
    