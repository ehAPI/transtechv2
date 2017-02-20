from openerp.osv import fields, osv

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
			#'surveyor':fields.many2one('res.users','Site Indpector Name',required=True),
			'customer_name':fields.many2one('customer.info','Customer',required=True),
			'state' : fields.many2one('res.country.state', 'State', required=True),
			'atm' : fields.many2one('atm.details', 'ATM', required=True),
			'visit_shift':fields.selection([('day','Day'),
				('night','Night')],'Visit Shift',required=True),
			'country' : fields.many2one('res.country','Country'),
			'acc_manager' : fields.many2one('res.users', 'Surveyor', required=True),
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
			
			'remarks_category' : fields.many2one('remarks.category','Remarks Category'),
			'remarks':fields.text('Remarks'),
			'act_date_time':fields.datetime('Actual Date Time'),
			'status':fields.char('Status')
	
	}

view_plan_tasks	()