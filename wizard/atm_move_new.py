from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
class atm_localization(osv.osv):
    _name = 'atm.move'   
    _columns = { 
                'longitude':fields.char('Longitude'),
                'latitude':fields.char('Latitude'),
                'date':fields.date('Date',readonly=True),
                'name':fields.char("ATM Branch Details"),  
                }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d')
    }

    def action_save(self,cr,uid,ids,context=None):
        atm_id = context['active_ids']
        data = self.read(cr, uid, ids)[0]
        atm_obj = self.pool.get('atm.info').browse(cr,uid,atm_id)[0]
        self.pool.get('atm.info').write(cr,uid,atm_id[0],
            {'child_ids':[[0, False, 
            {'latitude': atm_obj.latitude,
         'name_': atm_obj.name, 
         'longitude': atm_obj.longitude,
         'date':atm_obj.date}]]},context=context)
        self.pool.get('atm.info').write(cr,uid,atm_id[0],data,context=context)
        # res = super(atm_localization,self).create(cr,uid,context=context)
        return True


atm_localization()

# class surveys_print(osv.TransientModel):

#     _name = "print.survey"

#     _columns = {
#     'customer_id':fields.many2one('customer.info','Customer/Bank'),
#     'month':fields.selection([
#             ('jan','January'),
#             ('feb', 'February'),
#             ('mar', 'March'),
#             ('apr', 'April'),
#             ('may', 'May'),
#             ('june','June'),
#             ('jul', 'July'),
#             ('aug', 'August'),
#             ('sep', 'September'),
#             ('oct', 'October'),
#             ('nov', 'November'),
#             ('dec', 'December'),
#             ], 'Month'),

#     'bfr_img_front':fields.binary('Front View'),
#     'bfr_img_side':fields.binary('Side View'),
#     'bfr_img_back':fields.binary('Back View'),
#     'after_img_front':fields.binary('Front View After'),
#     'after_img_side':fields.binary('Side View After'),
#     'after_img_back':fields.binary('Back View After'),

#     'bfr_img_front2':fields.binary('Front View 2'),
#     'bfr_img_side2':fields.binary('Side View 2'),
#     'bfr_img_back2':fields.binary('Back View 2'),
#     'after_img_front2':fields.binary('Front View After 2'),
#     'after_img_side2':fields.binary('Side View After 2'),
#     'after_img_back2':fields.binary('Back View After 2'),


#     'bfr_img_front3':fields.binary('Front View 3'),
#     'bfr_img_side3':fields.binary('Front View Side 3'),
#     'after_img_front3':fields.binary('Front View After 3'),
#     'after_img_side3':fields.binary('Side View After 3'),

#     }


#     def action_print(self, cr, uid, ids, context=None):
#         # for i in range(0,5):
#         data = self.read(cr, uid, ids)[0]
#         survey_ids = self.pool.get('survey.details').search(cr,uid,[('status','=','approved'),('customer_surv','=',data['customer_id'][0]),('month','=',data['month'])])
        
#         if not survey_ids:
#             raise osv.except_osv(_('Warning!'), _("Selected survey(s) cannot be printed as they are not in Portal."))

#         '''
#         This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
#         '''
#         assert len(ids) == 1, 'This option should only be used for a single id at a time'
#         datas = {
#                 'model': 'survey.details',
#                 'ids': survey_ids,
#                 'form': self.read(cr, uid, survey_ids, context=context),
#             }
#         return {'type': 'ir.actions.report.xml', 'report_name': 'survey.details', 'datas': datas, 'nodestroy': True}