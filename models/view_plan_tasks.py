from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID

class view_plan_tasks(osv.osv):

	_name = 'view.plan.tasks'

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
			'name': self.pool.get('ir.sequence').get(cr, uid, 'view.plan.tasks'),
		})
		return super(view_plan_tasks, self).copy(cr, uid, id, default, context=context)

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
			'state' : fields.many2one('res.country.state', 'State', required=True,domain="[('country_id','=',country)]"),
			'atm' : fields.many2one('atm.details', 'ATM', domain="[('customer','=',customer_name),('state_id','=',state)]",required=True),
			'visit_shift':fields.selection([('day','Day'),
				('night','Night')],'Visit Shift',required=True),
			'country' : fields.many2one('res.country','Country',domain="[('code','=','AE')]",required=True),
			'surveyor' : fields.many2one('res.users', 'Surveyor', required=True,domain="[('name_tl','!=',False)]"),
			'visit_time':fields.datetime('Visit Date and Time', required=True),
			#'customer':fields.many2one('customer.info','Customer Name'),
			'add_instr':fields.text('Additional instructions'),
			'bulk_insert' : fields.boolean('Bulk Insert',size=5),
			'task_month':fields.selection([
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
			'nos':fields.integer('Number of records for Bulk Insert '),
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
		visit_date = vals['visit_time']
		if vals.get('name','/')== '/':
			vals['name']=self.pool.get('ir.sequence').get(cr,uid,'view.plan.tasks') or '/'
		return super(view_plan_tasks,self).create(cr, uid, vals, context=context)	


	def create_task(self,cr,uid,context=None):
		today = datetime.datetime.now().date()
		ids1 = self.search(cr,uid,[('next_visit','!=',False),('status','in',('done','assigned','progress','pending','waitnig_approve'))])
		# print ids1
		task_list = self.browse(cr,uid,ids1,context=None)
		vals = {}
		for i in task_list:
			# if i.next_visit.split(' ')[0] == str(today) and i.nos > 1:
				# if i.status == 'assigned' or i.status == 'progress' or i.status == 'pending' or i.status== 'done':
				vals = {'customer':i.customer_name.id, 'atm':i.atm.id, 'country':i.country.id, 'state':i.state.id, 'surveyor':i.surveyor.id,'visit_time':i.next_visit,'additional_info':i.additional_info,'bulk_insert':i.bulk_insert, 'visit_type':i.visit_type,'act_visit_time':i.act_visit_time,'nos':i.nos-1}
				
				if i.visit_type == 'daily':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit']  = visit_date + datetime.timedelta(days=1)

				if i.visit_type == 'weekly':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit']  = visit_date + datetime.timedelta(days=7)

				if i.visit_type == 'monthly':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(months=1)

				if i.visit_type == '2':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=15)

				if i.visit_type == '3':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=9)

				if i.visit_type == '4':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=7.5)


				if i.visit_type == '5':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=6)

				if i.visit_type == '6':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=5)

				if i.visit_type == '7':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=4)

				if i.visit_type == '8':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=3.75)

				if i.visit_type == '9':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=3.333)

				if i.visit_type == '10':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=3)

				if i.visit_type == '12':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=2.5)


				if i.visit_type == '13':
					visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=2.30)

				# if i.visit_type == '16':
				# 	visit_date = datetime.datetime.strptime(i.visit_time, "%Y-%m-%d %H:%M:%S")
				# 	vals['next_visit'] = visit_date+ relativedelta(days=1.875)

				if visit_date.month == 1:
						vals['task_month'] = 'jan'
				if visit_date.month == 2:
						vals['task_month'] = 'feb'
				if visit_date.month == 3:
						vals['task_month'] = 'mar'
				if visit_date.month == 4:
						vals['task_month'] = 'apr'
				if visit_date.month == 5:
						vals['task_month'] = 'may'
				if visit_date.month == 6:
						vals['task_month'] = 'june'
				if visit_date.month == 7:
						vals['task_month'] = 'jul'
				if visit_date.month == 8:
						vals['task_month'] = 'aug'
				if visit_date.month == 9:
						vals['task_month'] = 'sep'
				if visit_date.month == 10:
						vals['task_month'] = 'oct'
				if visit_date.month == 11:
						vals['task_month'] = 'nov'
				if visit_date.month == 12:
						vals['task_month'] = 'dec'
				# print vals
				# if datetime.datetime.today().weekday() != 4:
					# print i.id
				print self.pool.get('view.plan.tasks').create(cr,uid,vals,context=None)
				self.pool.get('view.plan.tasks').write(cr,uid,i.id,{'nos':i.nos-1},context=None)
		return True	


	def change_task_status(self,cr,uid,context=None):
		today =  str(datetime.datetime.now()).split()[0]
		all_tasks = self.search(cr,uid,[('visit_time','!=',False),('status','in',('assigned','progress'))])
		task_list1 = self.browse(cr,uid,all_tasks,context=None)
		for obj in task_list1:
			if obj.visit_time.split()[0] == today:
				self.pool.get('view.plan.tasks').write(cr,uid,obj.id,{'status':'progress'},context=None)
			if obj.visit_time.split()[0] < today:
				self.pool.get('view.plan.tasks').write(cr,uid,obj.id,{'status':'pending'},context=None)

		return True



	def write(self,cr,uid,ids,vals,context=None):
		if isinstance(ids, (int, long)):
			ids = [ids]

		if 'visit_time' in vals or 'atm' in vals:
			atm_lst = self.browse(cr,uid,ids)
			if 'visit_time' in vals:
				visit_date = datetime.datetime.strptime(vals['visit_time'], "%Y-%m-%d %H:%M:%S")
			else:
				visit_date = datetime.datetime.strptime(atm_lst[0].visit_time, "%Y-%m-%d %H:%M:%S")
			d1 = datetime.datetime.strftime(visit_date.date(), "%Y-%m-%d %H:%M:%S")
			d2 = datetime.datetime.strftime(visit_date.date(), "%Y-%m-%d 23:59:59")
			if 'atm' not in vals:
				lines = self.search(cr,uid, [('atm','=',atm_lst[0].atm.id),('visit_time','>=',d1), ('visit_time','<=',d2),('status','in',('pending','progress','assigned'))])
			else:
				lines = self.search(cr,uid, [('atm','=',vals['atm']),('visit_time','>=',d1), ('visit_time','<=',d2),('status','in',('pending','progress','assigned'))])
			# print lines
			if lines:
				if ids[0] not in lines:
					raise osv.except_osv(_('Error !'),_("One Task has been already created with this ATM & with the same visit date !") )

		result = super(view_plan_tasks,self).write(cr,uid,ids,vals,context=None)
		lst = self.browse(cr,uid,ids)
		for obj in lst:
			if obj.nos > 1:
				if obj.visit_type == 'daily':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit']  = visit_date + datetime.timedelta(days=1)
				if obj.visit_type == 'weekly':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit']  = visit_date + datetime.timedelta(days=7)
				if obj.visit_type == 'monthly':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(months=1)

				if obj.visit_type == '2':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=14)

				if obj.visit_type == '3':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=9)

				if obj.visit_type == '4':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=7.5)

				if obj.visit_type == '5':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=6)

				if obj.visit_type == '6':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=5)

				if obj.visit_type == '7':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=4)

				if obj.visit_type == '8':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=3.75)

				if obj.visit_type == '9':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=3.33)


				if obj.visit_type == '10':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=3)


				if obj.visit_type == '12':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=2.5)

				if obj.visit_type == '13':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=2.30)

				if obj.visit_type == '16':
					visit_date = datetime.datetime.strptime(obj.visit_time, "%Y-%m-%d %H:%M:%S")
					vals['next_visit'] = visit_date+ relativedelta(days=1.875)

				if  obj.bulk_insert == False:
					vals['next_visit'] = None
					vals['nos'] = 0
					vals['visit_type'] = None
				super(view_plan_tasks,self).write(cr,uid,ids,vals,context=None)

		return True


	def unlink(self, cr, uid, ids, context=None):
		# prod_obj = self.pool.get('atm.surverys.management').browse(cr,uid,ids[0])
		# if prod_obj.status in ('progress','done'):
		# 	raise osv.except_osv(_('Invalid Action!'), _("You can't delete a task which is either in 'Pending' or in 'Progress' or in 'Done'"))
			
		return super(view_plan_tasks, self).unlink(cr, uid, ids, context=context)


	def onchange_month(self,cr,uid,ids,task_month,context=None):
		res = {'value':{}}
		today = datetime.datetime.now()
		s = str(today).split(' ')[0]

		if task_month == 'jan':
			d = s.replace(s.split('-')[1], "01")
		elif task_month == 'feb':
			d = s.replace(s.split('-')[1], "02")
		elif task_month == 'mar':
			d = s.replace(s.split('-')[1], "03")
		elif task_month == 'apr':
			d = s.replace(s.split('-')[1], "04")
		elif task_month == 'may':
			d = s.replace(s.split('-')[1], "05")
		elif task_month == 'june':
			d = s.replace(s.split('-')[1], "06")
		elif task_month == 'jul':
			d = s.replace(s.split('-')[1], "07")
		elif task_month == 'aug':
			d = s.replace(s.split('-')[1], "08")
		elif task_month == 'sep':
			d = s.replace(s.split('-')[1], "09")
		elif task_month == 'oct':
			d = s.replace(s.split('-')[1], "10")
		elif task_month == 'nov':
			d = s.replace(s.split('-')[1], "11")
		else:
			d = s.replace(s.split('-')[1], "12")
		res['value'].update({'visit_time':d+' 12:30:00'})
		return res



view_plan_tasks	()