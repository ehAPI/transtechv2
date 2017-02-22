from openerp.osv import fields, osv
import time
import openerp
from openerp.tools.translate import _
from openerp import api


class pricing_wizard_selection(osv.TransientModel):

    _name = 'survey.report'

    _columns = {

        'from_date': fields.date('From Date'),
        'to_date': fields.date('To Date'),
        'Bank/Customer': fields.many2one('customer.info', 'Bank/Customer'),
    }

    # def action_save(self, cr, uid, ids, context=None):
    #     survey_report_obj = self.pool.get('atm.details').browse(cr, uid, context['active_id'])
    #     input_data = self.read(cr, uid, ids[0])
    #     message = input_data['cancel_message']

    #     user_obj = self.pool.get('res.users').browse(cr, uid, uid)

    #     # Logging the message in chatter
    #     msg_vals = {
    #     'author_id': user_obj.partner_id.id,
    #     'type':'comment',
    #     'model':'atm.details',
    #     'res_id':context['active_id'],
    #     'sub_type_id':1,
    #     'body': message,
    #     }
    #     self.pool.get('mail.message').create(cr, uid,msg_vals)

    #     self.pool.get('atm.details').write(cr, uid, context['active_id'], {'status':'cancelled'})

    #     return True