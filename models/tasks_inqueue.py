from openerp.osv import fields, osv

class Tasks_in_queue(osv.osv):

	_name = 'tasks.queue'

	_columns = {
		'name':fields.char('Task ID'),
		'task_month':fields.selection([('jan','January'),
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
									   ('dec', 'December')], 'Month'),
		'customer':fields.many2one('customer.info','Customer'),
		'state':fields.many2one('res.country.state','State'),
		'atm':fields.many2one('atm.info','ATM'),
		'country':fields.many2one('res.country','Country', domain="[('code','=','AE')]"),
		'surveyor':fields.many2one('res.users','Surveyor'),
		'visit_time':fields.datetime('Visit Date And Time'),
		'additional_info':fields.text('Additional instructions'),
		'status': fields.selection([('assigned','Assigned'),
									('pending', 'Pending'),
									('cancel', 'Cancelled'),
									('progress', 'Progress'),
									('waitnig_approve','Waiting for Approval'),
									('done', 'Done'),], 'Status'),
		'bulk_insert':fields.boolean('Bulk Insert'),
		'nos':fields.integer('Number of records for Bulk Insert '),
		'remarks_id':fields.many2one('remarks.category', 'Remarks Category'),
		'remarks':fields.text('Remarks'),
		'act_visit_time':fields.datetime('Actual Date Time'),
		'assigned_by':fields.many2one('res.users','Assigned By'),
		'visit_type': fields.selection([('daily','Daily'),
										('weekly', 'Weekly'),
										('monthly', 'Monthly'),
										('2', 'Twice'),
										('3', '3 times'),
										('4', '4 times'),
										('5', '5 times'),
										('6', '6 times'),
										('7', '7 times'),
										('8', '8 times'),
										('9', '9 times'),
										('10', '10 times'),
										('12', '12 times'),
										('13', '13 times'),
										('16', '16 times')], 'Visit Type'),
		'next_visit':fields.datetime('Next Visit'),
		'visit_shift':fields.selection([('day','Day'),
										('night','Night')] ,'Visit Shift'),
	}


	# code to get default country name
	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	_defaults = {
		'status':'assigned',
		'visit_shift':'day',
		'country':_default_country,
	}
	def create(self, cr, uid, vals, context=None):
   		vals['name']= self.pool.get('ir.sequence').get(cr, uid, 'tasks.queue')
   		return super(Tasks_in_queue, self).create(cr, uid, vals, context=context)	

	def status_done(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'done'},context=context)
		return True

	def status_cancel(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'cancel'},context=context)
		return True
Tasks_in_queue()