from openerp.osv import fields, osv

class internal_alerts(osv.osv):
	_name = 'internal.alerts'
	_description = 'Internal Alerts'
	_columns = {
	'alert_id' : fields.char('Alert ID', readonly=True),
	'customer' : fields.many2one('customer.info', 'Customer', ondelete='set null'),
	'created_by' : fields.many2one('res.users','Created By', ondelete='set null'),
	'atm' : fields.many2one('atm.details', 'ATM', required=True, ondelete='set null'),
	'category' : fields.selection([('complaint','Complaint'),('issue','Issue')],'Category', required=True),
	'priority' : fields.selection([('low','Low'),('medium','Medium'),('high','High'),('critical','Critical')],'Priority', required=True),
	'country' : fields.many2one('res.country','Country', ondelete='set null'),
	'state' : fields.many2one('res.country.state', 'State', ondelete='set null'),
	'assigned_to' : fields.many2one('res.users','Assigned To', ondelete='set null'),
	'status': fields.selection([('assigned','Assigned'),('resolved','Resolved'),('closed','Closed')]),
	'reason_code_id' : fields.many2one('reason.code.setup','Reason Code', ondelete='set null'),
	'reason_description' : fields.text('Reason Descriptions'),
	'summary' : fields.char('Summary', size=100),
	'description' : fields.text('Description'),
	}

internal_alerts()
