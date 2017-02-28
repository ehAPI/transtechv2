from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
class atm_localization(osv.osv):
    _name = 'atm.move'   
    _columns = { 
                'longitude':fields.char('Longitude'),
                'latitude':fields.char('Latitude'),
                'date':fields.date('Date',readonly=True),
                'atm_branch_details':fields.char("ATM Branch Details"),  
                }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d')
    }

    def action_save(self,cr,uid,ids,context=None):
        atm_id = context['active_ids']
        data = self.read(cr, uid, ids)[0]
        atm_obj = self.pool.get('atm.details').browse(cr,uid,atm_id)[0]
        self.pool.get('atm.details').write(cr,uid,atm_id[0],
            {'child_ids':[[0, False, 
            {'latitude': atm_obj.latitude,
         'name': atm_obj.atm_branch_details, 
         'longitude': atm_obj.longitude,
         'date':atm_obj.date}]]},context=context)
        self.pool.get('atm.details').write(cr,uid,atm_id[0],data,context=context)
        # res = super(atm_localization,self).create(cr,uid,context=context)
        return True


atm_localization()

# class surveys_approve(osv.TransientModel):
#     _name="surveys.approve"

#     def approve_survey(self, cr, uid, ids, context=None):
#         data_inv = self.pool.get('survey.details').read(cr, uid, context['active_ids'], ['status'], context=context)

#         for record in data_inv:
#             if record['status'] not in ('waiting_approval'):
#                 raise osv.except_osv(_('Warning!'), _("Selected survey(s) cannot be approved as they are not in 'Waiting Approval' state."))
#         self.pool.get('survey.details').write(cr,uid,context['active_ids'],{'status':'approved'})
#         obj_list = self.pool.get('survey.details').browse(cr,uid,context['active_ids'])
#         for obj in obj_list:
#             self.pool.get('atm.surverys.management').write(cr, uid, obj.surv_task.id,{'status':'done'}, context)
#         return {'type': 'ir.actions.act_window_close'}

# surveys_approve()


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
    

#     def action_upload(self, cr, uid, ids, context=None):
#         # for i in range(0,5):
#         data = self.read(cr, uid, ids)[0]


#         vals = {}

#         if data['bfr_img_front']:
#             vals['bfr_img_front'] = data['bfr_img_front']

#         if data['bfr_img_side']:
#             vals['bfr_img_side'] = data['bfr_img_side']

#         if data['bfr_img_back']:
#             vals['bfr_img_back'] = data['bfr_img_back']

#         if data['after_img_front']:
#             vals['after_img_front'] = data['after_img_front']

#         if data['after_img_side']:
#             vals['after_img_side'] = data['after_img_side']

#         if data['after_img_back']:
#             vals['after_img_back'] = data['after_img_back']


#         if data['bfr_img_front2']:
#             vals['bfr_img_front2'] = data['bfr_img_front2']

#         if data['bfr_img_side2']:
#             vals['bfr_img_side'] = data['bfr_img_side2']

#         if data['bfr_img_back2']:
#             vals['bfr_img_back2'] = data['bfr_img_back2']

#         if data['after_img_front2']:
#             vals['after_img_front2'] = data['after_img_front2']

#         if data['after_img_side2']:
#             vals['after_img_side2'] = data['after_img_side2']

#         if data['after_img_back2']:
#             vals['after_img_back2'] = data['after_img_back2']


#         if data['bfr_img_front3']:
#             vals['bfr_img_front3'] = data['bfr_img_front3']

#         if data['bfr_img_side3']:
#             vals['bfr_img_side3'] = data['bfr_img_side3']

#         if data['after_img_front3']:
#             vals['after_img_front3'] = data['after_img_front3']
            
#         if data['after_img_side3']:
#             vals['after_img_side3'] = data['after_img_side3']

#         survey_ids = self.pool.get('survey.details').write(cr,uid,context['active_id'],vals)
#         return {
#                 'type': 'ir.actions.client',
#                 'tag': 'reload',  }

        
       

# surveys_print()