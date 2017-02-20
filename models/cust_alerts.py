from openerp.osv import fields, osv

class cust_alerts(osv.osv):
	_name = 'cust.alerts'
	_description = 'Customer Alerts'
	_columns = {
	'alert_id' : fields.char('Alert ID', readonly=True),
	'customer' : fields.many2one('customer.info', 'Customer', ondelete='set null'),
	'atm' : fields.many2one('atm.details', 'ATM', required=True, ondelete='set null'),
	'category' : fields.selection([('complaint','Complaint'),('issue','Issue')],'Category', required=True),
	'priority' : fields.selection([('low','Low'),('medium','Medium'),('high','High'),('critical','Critical')],'Priority', required=True),
	'country' : fields.many2one('res.country', 'Country', ondelete='set null'),
	'state' : fields.many2one('res.country.state', 'State', ondelete='set null'),
	'submitted_by' : fields.many2one('res.users','Submitted by', readonly=True, ondelete='set null'),
	'status': fields.selection([('assigned','Assigned'),('resolved','Resolved'),('closed','Closed')]),
	'reason_code_id' : fields.many2one('reason.code.setup','Reason Code', ondelete='set null'),
	'reason_description' : fields.text('Reason Descriptions'),
	'summary' : fields.char('Summary', size=100),
	'description' : fields.text('Description'),
	'img1' : fields.binary('Image', widget='image'),
	'img2' : fields.binary('Image', widget='image'),
	'img3' : fields.binary('Image', widget='image'),
	}

cust_alerts()

