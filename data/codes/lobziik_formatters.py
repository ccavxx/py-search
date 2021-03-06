# coding: utf-8import loggingimport getpassfrom socket import gethostname
from ._compat import json, text_type

class JSONFormatter(logging.Formatter):
 def format(self, record):        data = record.__dict__.copy()
 if record.args:            msg = record.msg % record.args else:            msg = record.msg
        data.update( username=getpass.getuser(), host=gethostname(), msg=msg, args=tuple(text_type(arg) for arg in record.args)        )
 if 'exc_info' in data and data['exc_info']:            data['exc_info'] = self.formatException(data['exc_info'])
 return json.dumps(data)