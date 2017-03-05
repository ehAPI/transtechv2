from openerp.osv import fields, osv

class internal_alerts(osv.osv):
	_name = 'internal.alerts'
	_inherit="cust.alerts"
	_rec_name = 'alert_id'
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

	def create(self,cr,uid,vals,context=None):
		if vals.get('alert_id','/') == '/': 
			vals['alert_id'] = self.pool.get('ir.sequence').get(cr, uid, 'internal.alerts') or '/'
		alert_id = super(internal_alerts, self).create(cr, uid, vals, context=context)
		alert_info = self.browse(cr,uid,[alert_id],context=None)[0]
		alertnumber = alert_info.alert_id
		
		if alert_id != False and alertnumber[0:5]=='Alert':
			self.send_alert_invitation_customer(cr,uid,[alert_id],context=None)
			self.send_alert_invitation_teamleader(cr,uid,[alert_id],context=None)
		return alert_id


internal_alerts()
