from openerp.osv import fields, osv

class internal_alerts(osv.osv):
	_name = 'internal.alerts'
	_inherit="cust.alerts"
	_description = 'Internal Alerts'
	_columns = {
	'customer' : fields.many2one('customer.info', 'Customer', ondelete='set null'),
	'created_by' : fields.many2one('res.users','Created By', ondelete='set null'),
	'assigned_to' : fields.many2one('res.users','Assigned To', ondelete='set null'),
	}

	_defaults = {
        'created_by': lambda obj, cr, uid, context: uid,
		'status': 'assigned'
	}

	# _order = "name desc"

	def status_resolve(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'resolved'},context=context)
		return True

	def status_close(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'closed'},context=context)
		return True


internal_alerts()
