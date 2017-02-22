from openerp.osv import fields, osv
import time
import openerp
from openerp.tools.translate import _
from openerp import api


class pricing_wizard_selection(osv.TransientModel):

    _name = 'survey.request.message'

    _columns = {

        'cancel_message': fields.text('Enter your message'),
    }

    def action_cancel_request(self, cr, uid, ids, context=None):
        survey_report_obj = self.pool.get('survey.request').browse(cr, uid, context['active_id'])
        input_data = self.read(cr, uid, ids[0])
        message = input_data['cancel_message']

        user_obj = self.pool.get('res.users').browse(cr, uid, uid)

        # Logging the message in chatter
        msg_vals = {
        'author_id': user_obj.partner_id.id,
        'type':'comment',
        'model':'survey.request',
        'res_id':context['active_id'],
        'sub_type_id':1,
        'body': message,
        }
        self.pool.get('mail.message').create(cr, uid,msg_vals)

        self.pool.get('survey.request').write(cr, uid, context['active_id'], {'status':'cancelled'})

        return True