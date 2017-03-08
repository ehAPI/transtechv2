from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID

class view_plan_tasks(osv.osv):

	_name = 'view.plan.tasks'
	_columns = {
	        'name':fields.char('Task ID', readonly=True),
			'month':fields.selection([('Jan','January'),
				('Feb','February'),
				('March','March'),
				('April','April'),
				('May','May'),
				('June','June'),
				('July','July'),
				('August','August'),
				('Sept','September'),
				('Oct', 'October'),
				('Nov','November'),
				('Dec','December')],'Month'),
			# 'surveyor':fields.many2one('res.users','Site Indpector Name',required=True),
			'customer_name':fields.many2one('customer.info','Customer',required=True),
			'state' : fields.many2one('res.country.state', 'State', required=True),
			'atm' : fields.many2one('atm.details', 'ATM', required=True),
			'visit_shift':fields.selection([('day','Day'),
				('night','Night')],'Visit Shift',required=True),
			'country' : fields.many2one('res.country','Country'),
			'surveyor' : fields.many2one('res.users', 'Surveyor', required=True),
			'visit_date_time':fields.datetime('Visit Date and Time', required=True),
			#'customer':fields.many2one('customer.info','Customer Name'),
			'add_instr':fields.text('Additional instructions'),
			'bulk_insert' : fields.boolean('Bulk Insert',size=5),
			'visit_type': fields.selection([('daily','Daily'),
				('weekly','Weekly'),
				('monthly','Monthly'),
				('twice','Twice'),
				('3_times','3 times'),
				('4_times','4 times'),
				('5_times','5 times'),
				('6_times','6 times'),
				('7_times','7 times'),
				('8_times','8 times'),
				('9_times','9 times'),
				('10_times','10 times'),
				('12_times','12 times'),
				('13_times','13 times'),
				('16_times','16 times')],'Visit Type'),
			'visit_details':fields.char('Visit Details',readonly=True),
			'assigned_by':fields.many2one('res.users','Assigned By' ,readonly=True),
			'remarks_category' : fields.many2one('remarks.category','Remarks Category'),
			'remarks':fields.text('Remarks'),
			'act_date_time':fields.datetime('Actual Date Time'),
			'status':fields.selection([('assigned','Assigned'),
									   ('pending','Pending'),
									   ('cancel','Cancelled'),
									   ('progress','Progess'),
									   ('waiting_approve','Waiting for Approval'),
									   ('done','Done')],'Status')

	}
	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	_defaults = {
	'assigned_by':lambda obj, cr, uid, ctx=None: uid,
	'status':'assigned',
	'visit_shift':'day',
	'country':_default_country,
	}

	_order = "name desc"

	def status_done(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'done'},context=context)
		return True

	def status_cancel(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'cancel'},context=context)
		return True

	def create(self, cr, uid, vals, context=None):
		visit_date = vals['visit_date_time']
		if vals.get('name','/')== '/':
			vals['name']=self.pool.get('ir.sequence').get(cr,uid,'view.plan.tasks') or '/'
		return super(view_plan_tasks,self).create(cr, uid, vals, context=context)		


view_plan_tasks	()