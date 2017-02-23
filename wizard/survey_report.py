from openerp.osv import fields, osv
from openerp.tools.translate import _
import time



class survey_report(osv.TransientModel):

    _name = 'survey.report'

    _columns = {

        'from_date': fields.date('From Date'),
        'to_date': fields.date('To Date'),
        'Bank/Customer': fields.many2one('customer.info','Bank/Customer'),

    }

    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d')
    }
    def action_survey_details(self,cr,uid,ids,values,context=None):
    	from_date = values.get('from_date')
    	to_date = values.get('to_date')
    	
    	return True



 
survey_report()  
