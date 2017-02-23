from openerp.osv import fields, osv

class schedule_tasks(osv.osv):

	_name = 'schedule.tasks'
	_columns = {
	        'name':fields.char('Scheduled Task ID', readonly=True),
	        'customer_name':fields.many2one('customer.info','Customer',required=True),
			'state' : fields.many2one('res.country.state', 'State', required=True),
			'atm' : fields.many2one('atm.details', 'ATM', required=True),
		
			#'surveyor':fields.many2one('res.users','Site Indpector Name',required=True),
			'visit_shift':fields.selection([('day','Day'),
				('night','Night')],'Visit Shift',required=True),

			'country' : fields.many2one('res.country','Country',required=True),
			'acc_manager' : fields.many2one('res.users', 'Surveyor', required=True),
			'start_date':fields.datetime('Start Date', required=True),
			#'customer':fields.many2one('customer.info','Customer Name'),
			'add_instr':fields.text('Additional instructions'),
			'bulk_insert' : fields.boolean('Bulk Insert',size=5),
			'visit_type/': fields.selection([
				('monthly/1','Monthly/1 visit'),
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
				('16_times','16 times')],'Visit Type/ No. of Visits to be done',required=True),
			'visit_details':fields.char('Visit Details',readonly=True),

            'remarks_category' : fields.many2one('remark.category','Remarks Category'),
			'remarks':fields.text('Remarks'),
			'next_execution':fields.char('Next Execution',readonly=True),
			'no_of_visits':fields.integer('No. of visits per month'),
			'status': fields.selection([
			('assigned','Assigned'),
			('cancel', 'Cancelled')],'Status',readonly=True, track_visibility='always')
	
	}

	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	_defaults = {
	'visit_shift':'day',
	'bulk_insert': True,
	'status':'assigned'
	# 'country':_default_country,
	}

schedule_tasks	()

