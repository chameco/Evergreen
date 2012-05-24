class coreError(Exception): pass
class serverError(coreError): pass
class drawError(coreError): pass
class configError(coreError): pass
class invalidRequestError(coreError): pass
class netError(coreError): pass
class dbError(coreError): pass
