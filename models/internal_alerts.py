from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
from openerp import  tools
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

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

	def create(self,cr,uid,vals,context=None):
		print vals
		if vals.get('cust_name','/') == '/': 
			vals['cust_name'] = self.pool.get('ir.sequence').get(cr, uid, 'internal.alerts') or '/'
		user_id= super(internal_alerts, self).create(cr, uid, vals, context=context)
		if user_id != False:
			self.send_alert_invitation(cr,uid,[user_id],context=None)
			return user_id

	def send_alert_invitation(self,cr,uid,ids,context=None):
		alert_obj = self.browse(cr,uid,ids,context=None)[0]
		print alert_obj
		customer_id =  self.pool.get('customer.info').browse(cr,uid,alert_obj.customer.id)
		customer_name = customer_id.cust_name
		atm_id1 =self.pool.get('atm.details').browse(cr,uid,alert_obj.atm.id)
		atm_name = atm_id1.atm_branch_details
		user_ids = self.pool.get('res.users').browse(cr,uid,alert_obj.assigned_to.id)
		# print user_ids.name_tl
		teamleader_find = self.pool.get('res.users').browse(cr,uid,user_ids.name_tl.id)
		print teamleader_find
		temail_id = teamleader_find.email
		print temail_id
		if not temail_id:
			raise osv.except_osv(_('No Email Provided for this Teamleader'),_("<P></P>lease give a Valid email address !") )
			return False
		tname= teamleader_find.name
		mail_ids = self.pool.get('ir.mail_server').search(cr,uid,[('active','=','True')])
		mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,mail_ids)[0]
		username = mail_obj.smtp_user
		pwd = mail_obj.smtp_pass
		host = mail_obj.smtp_host
		port = mail_obj.smtp_port
		fromaddr = username
		server = smtplib.SMTP(host+':'+'587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(username, pwd)
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['Subject'] = 'New Internal Alert in Transtech Portal'
		toaddr = teamleader_find.email
		msg['To'] = toaddr
		text = ('<p><h2>Hello, %s</h2> One internal alert is generate in Transtech Portal</p><p><b>Details of generate alerts is given below:-</b></p><p><b>Genrated By </b>: %s</p><p><b>Alert ID</b> :  %s</p><p><b>Customer</b> :  %s</p><p><b>Alert Category </b> : %s</p><p><b>Priority </b>:%s</p><p><b>ATM </b>:%s,%s</p>')%(tname,user_ids.alert_id,alert_obj.alert_id,customer_id.alert_id,alert_obj.category,alert_obj.priority,atm_name,atm_id1.atm)
		body = MIMEText(text, _subtype='html')
		msg.attach(body)
		res = server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()

		return True


internal_alerts()
