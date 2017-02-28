from openerp.osv import fields, osv

class Alerts_for_you(osv.osv):

	_name = 'alerts.dashboard'

	_columns = {
		'names':fields.char('Alert ID'),
		'customer':fields.many2one('customer.info','Customer'),
		'created_by':fields.many2one('res.users','Created By'),
		'atm_id':fields.many2one('atm.info','ATM'),
		'category':fields.selection([('complaint','Complaint'),
									 ('issue','Issue')],'Category'),
		'priority':fields.selection([('low','Low'),
									 ('medium','Medium'), 
									 ('high','High'),
									 ('critical','Critical')],'Priority'),
		'country_id':fields.many2one('res.country','Country',domain="[('code','=','AE')]"),
		'state_id':fields.many2one('res.country.state','State'),
		'assign_to':fields.many2one('res.users','Assign To'),
		'status':fields.selection([('assigned','Assigned'),
								   ('resolved','Resolved'), 
								   ('closed','Closed')],'Status'),
		'summary':fields.char('Summary', size=100),
		'description':fields.text('Description'),
		'reason_id':fields.many2one('reason.code','Reason Code'),
		'reason_disc':fields.text('Reason Descriptions'),
	

	}

	def create(self, cr, uid, vals, context=None):
   		vals['name']= self.pool.get('ir.sequence').get(cr, uid, 'alert.you')
   		return super(Alerts_for_you, self).create(cr, uid, vals, context=context)

	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]
		
	_defaults = {
		'status':'assigned',
		'country_id':_default_country,    
		'created_by': lambda obj, cr, uid, context: uid,
 	
	}

	def status_resolve(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'resolved'},context=context)
		return True

	def status_close(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'closed'},context=context)
		return True

	def unlink(self, cr, uid, ids, context=None):
        	alert_obj = self.pool.get('alert.info').browse(cr,uid,ids[0])
		if alert_obj.status in ('resolved','closed'):
			raise osv.except_osv(_('Invalid Action!'), _("You can't delete an Alert which is either in 'Resolved state' or in 'Closed state' "))
        	return super(alert_section, self).unlink(cr, uid, ids, context=context)

Alerts_for_you()


