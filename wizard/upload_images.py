from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
class upload_images(osv.TransientModel):

    _name = "upload.images"

    _columns = {
    'customer_id':fields.many2one('customer.info','Customer/Bank'),
    'month':fields.selection([
            ('jan','January'),
            ('feb', 'February'),
            ('mar', 'March'),
            ('apr', 'April'),
            ('may', 'May'),
            ('june','June'),
            ('jul', 'July'),
            ('aug', 'August'),
            ('sep', 'September'),
            ('oct', 'October'),
            ('nov', 'November'),
            ('dec', 'December'),
            ], 'Month'),

    'image1_b':fields.binary('Front View'),
    'image2_b':fields.binary('Side View'),
    'image3_b':fields.binary('Back View'),
    'image1_a':fields.binary('Front View After'),
    'image2_a':fields.binary('Side View After'),
    'image3_a':fields.binary('Back View After'),

    'image4_b':fields.binary('Front View 2'),
    'image5_b':fields.binary('Side View 2'),
    'image6_b':fields.binary('Back View 2'),
    'image4_a':fields.binary('Front View After 2'),
    'image5_a':fields.binary('Side View After 2'),
    'image6_a':fields.binary('Back View After 2'),


    'image7_b':fields.binary('Front View 3'),
    'image8_b':fields.binary('Front View Side 3'),
    'image7_a':fields.binary('Front View After 3'),
    'image8_a':fields.binary('Side View After 3'),

    }


    # def action_print(self, cr, uid, ids, context=None):
    #     # for i in range(0,5):
    #     data = self.read(cr, uid, ids)[0]
    #     survey_ids = self.pool.get('survey.details').search(cr,uid,[('status','=','approved'),('customer_surv','=',data['customer_id'][0]),('month','=',data['month'])])
        
    #     if not survey_ids:
    #         raise osv.except_osv(_('Warning!'), _("Selected survey(s) cannot be printed as they are not in Portal."))

    #     '''
    #     This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
    #     '''
    #     assert len(ids) == 1, 'This option should only be used for a single id at a time'
    #     datas = {
    #             'model': 'survey.details',
    #             'ids': survey_ids,
    #             'form': self.read(cr, uid, survey_ids, context=context),
    #         }
    #     return {'type': 'ir.actions.report.xml', 'report_name': 'survey.details', 'datas': datas, 'nodestroy': True}
    

    def action_upload(self, cr, uid, ids, context=None):
        # for i in range(0,5):
        data = self.read(cr, uid, ids)[0]


        vals = {}

        if data['image1_b']:
            vals['image1_b'] = data['image1_b']

        if data['image2_b']:
            vals['image2_b'] = data['image2_b']

        if data['image3_b']:
            vals['image3_b'] = data['image3_b']

        if data['image1_a']:
            vals['image1_a'] = data['image1_a']

        if data['image2_a']:
            vals['image2_a'] = data['image2_a']

        if data['image3_a']:
            vals['image3_a'] = data['image3_a']

        if data['image4_b']:
            vals['image4_b'] = data['image4_b']

        if data['image5_b']:
            vals['image5_b'] = data['image5_b']

        if data['image6_b']:
            vals['image6_b'] = data['image6_b']

        if data['image4_a']:
            vals['image4_a'] = data['image4_a']

        if data['image5_a']:
            vals['image5_a'] = data['image5_a']

        if data['image6_a']:
            vals['image6_a'] = data['image6_a']


        if data['image7_b']:
            vals['image7_b'] = data['image7_b']

        if data['image8_b']:
            vals['image8_b'] = data['image8_b']

        if data['image7_a']:
            vals['image7_a'] = data['image7_a']
            
        if data['image8_a']:
            vals['image8_a'] = data['image8_a']

        survey_ids = self.pool.get('survey.details').write(cr,uid,context['active_id'],vals)
        return {
                'type': 'ir.actions.client',
                'tag': 'reload',  }

        
       

upload_images()