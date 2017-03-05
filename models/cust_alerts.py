from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from openerp import workflow


class cust_alerts(osv.osv):
	_name = 'cust.alerts'
	_inherit = ['mail.thread']
	_rec_name = 'alert_id'
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
	'status': fields.selection([('assigned','Assigned'),('resolved','Resolved'),('closed','Closed')],'Status'),
	'reason_code_id' : fields.many2one('reason.code.setup','Reason Code', ondelete='set null'),
	'reason_description' : fields.text('Reason Descriptions'),
	'summary' : fields.char('Summary', size=100),
	'description' : fields.text('Description'),
	'img1' : fields.binary('Image', widget='image'),
	'img2' : fields.binary('Image', widget='image'),
	'img3' : fields.binary('Image', widget='image'),
	}

	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	def _default_customer(self, cr, uid, context=None):

		cid = []

		user = self.pool.get('res.users').browse(cr,uid,uid)
		cid = self.pool.get('customer.info').search(cr,uid,[('cust_name','=',user.name)])

		if cid:
			return cid[0]

		return cid

	def status_resolve(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'resolved'},context=context)
		return True

	def status_close(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'closed'},context=context)
		return True
		

	_defaults = {
		'status':'assigned',
		'country_id':_default_country,
		'customer':_default_customer,
	}

	_order = "alert_id desc"

	def create(self,cr,uid,vals,context=None):
		if vals.get('alert_id','/') == '/': 
			vals['alert_id'] = self.pool.get('ir.sequence').get(cr, uid, 'cust.alerts') or '/'
		alert_id = super(cust_alerts, self).create(cr, uid, vals, context=context)
		alert_info = self.browse(cr,uid,[alert_id],context=None)[0]
		alertnumber = alert_info.alert_id
		
		if alert_id != False and alertnumber[0:5]=='Alert':
			self.send_alert_invitation_customer(cr,uid,[alert_id],context=None)
			self.send_alert_invitation_teamleader(cr,uid,[alert_id],context=None)
		return alert_id

	def action_alert_send(self,cr,uid,ids,context=None):
		'''
		This function opens a window to compose an email, with the edi sale template message loaded by default
		'''
		assert len(ids) == 1, 'This option should only be used for a single id at a time.'
		ir_model_data = self.pool.get('ir.model.data')
		try:
			template_id = ir_model_data.get_object_reference(cr, uid, 'atm', 'email_template_edi_atm')[1]
		except ValueError:
			template_id = False
		try:
			compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
		except ValueError:
			compose_form_id = False 
		ctx = dict()
		ctx.update({
			'default_model': 'cust.alerts',
			'default_res_id': ids[0],
			'default_use_template': bool(template_id),
			'default_template_id': template_id,
			# 'default_composition_mode': 'summary',
			# 'default_composition_mode': 'comment',
			'mark_so_as_sent': True
		})
		return{
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views': [(compose_form_id,'form')],
			'view_id': compose_form_id,
			'target': 'new',
			'context': ctx,
		}

	# def send_alert_invitation_customer(self,cr,uid,ids,context=None):
	# 	alert_obj = self.browse(cr,uid,ids,context=None)[0]
	# 	customer_id =  self.pool.get('customer.info').browse(cr,uid,alert_obj.customer.id)
	# 	customer_name = customer_id.cust_name
	# 	affectedATM =self.pool.get('atm.details').browse(cr,uid,alert_obj.atm.id)
	# 	atm_name = affectedATM.atm_branch_details
	# 	if not customer_id.cont_per:
	# 		raise osv.except_osv(_('No Email Provided for this customer'),_("Please give a Valid email address !") )
	# 		return False
	# 	# mail_ids = self.pool.get('ir.mail_server').search(cr,uid,[('active','=','True')])
	# 	# mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,mail_ids)[0]
	# 	# username = mail_obj.smtp_user
	# 	# pwd = 'd2dddaf6-caea-4d61-90e0-90aa58d88b98'
	# 	# host = mail_obj.smtp_host
	# 	# port = mail_obj.smtp_port
	# 	# fromaddr = username
	# 	# server = smtplib.SMTP(host+':'+'2525')
	# 	# server.ehlo()
	# 	# server.starttls()
	# 	# server.ehlo()
	# 	# server.login(username, pwd)
	# 	# SMTP
	# 	msg = MIMEMultipart()
	# 	TO = customer_id.cont_per
	# 	msg['To'] = TO
	# 	FROM = 'info@transtech.ae'
	# 	msg['From'] = FROM
	# 	# msg['Subject'] = 'email subject'
	# 	send = smtplib.SMTP('smtp.elasticemail.com', 2525)
	# 	send.starttls()
	# 	send.login('rethish.kumar@transtech.ae', 'd2dddaf6-caea-4d61-90e0-90aa58d88b98')
		
	# 	# msg['From'] = fromaddr
	# 	msg['Subject'] = 'Regarding Alert in TransTech Portal'
	# 	toaddr = customer_id.cont_per
	# 	msg['To'] = toaddr
	# 	text = ('<p><h2>Dear %s,</h2><p>\
	# 		<p>An error alert is recorded in TransTech portal. Details are as follows:</p>\
	# 		<p><b>Alert Category</b>: %s</p>\
	# 		<p><b>Priority</b>: %s</p>\
	# 		<p><b>ATM Location</b>: %s</p>\
	# 		<p><b>ATM ID</b>: %s</p>\
	# 		<p><b>Subject</b>: %s</p>\n \
	# 		<p><b>Description</b>: %s</p>\n Thanks')\
	# 	%(customer_id.cust_name,
	# 		str(alert_obj.category).title(),
	# 		str(alert_obj.priority).title(),
	# 		affectedATM.atm_branch_details,
	# 		affectedATM.bank_atm_id,
	# 		alert_obj.summary,
	# 		alert_obj.description)
	# 	body = MIMEText(text,_subtype='html')
	# 	msg.attach(body)
	# 	# res = server.sendmail(fromaddr, toaddr, msg.as_string())
	# 	# server.quit()
	# 	send.sendmail(FROM, TO, msg.as_string())
	# 	send.quit()
	# 	return True

	# def send_alert_invitation_teamleader(self,cr,uid,ids,context=None):
	# 	alert_obj = self.browse(cr,uid,ids,context=None)[0]
	# 	customer_id =  self.pool.get('customer.info').browse(cr,uid,alert_obj.customer.id)
	# 	customer_name = customer_id.cust_name
	# 	affectedATM =self.pool.get('atm.details').browse(cr,uid,alert_obj.atm_id.id)
	# 	atm_name = affectedATM.atm_branch_details
	# 	user_ids = self.pool.get('res.users').browse(cr,uid,customer_id.acc_manager.id)
	# 	temail_id = user_ids.email
	# 	if not temail_id:
	# 		raise osv.except_osv(_('No Email Provided for this Team Leader'),_("Please give a Valid email address !") )
	# 		return False
	# 	tname= user_ids.name
	# 	# mail_ids = self.pool.get('ir.mail_server').search(cr,uid,[('active','=','True')])
	# 	# mail_obj = self.pool.get('ir.mail_server').browse(cr,uid,mail_ids)[0]
	# 	# username = mail_obj.smtp_user
	# 	# pwd = mail_obj.smtp_pass
	# 	# host = mail_obj.smtp_host
	# 	# port = mail_obj.smtp_port
	# 	# fromaddr = username
	# 	# server = smtplib.SMTP(host+':'+'2525')
	# 	# server.ehlo()
	# 	# server.starttls()`
	# 	# server.ehlo()
	# 	# server.login(username, pwd)
	# 	send = smtplib.SMTP('smtp.elasticemail.com', 2525)
	# 	send.starttls()
	# 	send.login('rethish.kumar@transtech.ae', 'd2dddaf6-caea-4d61-90e0-90aa58d88b98')
	# 	msg = MIMEMultipart()
	# 	FROM = 'info@transtech.ae'
	# 	msg['From'] = FROM
	# 	# msg['From'] = 'info@transtech.ae'
	# 	msg['Subject'] = 'New Customer Alert in Transtech Portal'
	# 	TO = temail_id
	# 	msg['To'] = TO
	# 	text = ('<p><h2>Hello %s,</h2>\
	# 	 One Customer Alert has been recorded in Transtech Portal</p>\
	# 	 <p><b>Details of generated alert is given below:</b></p>\
	# 	 <p><b>Genrated By </b>: %s</p>\
	# 	 <p><b>Alert ID</b> :  %s</p>\
	# 	 <p><b>Alert Category </b> : %s</p>\
	# 	 <p><b>Priority </b>: %s</p>\
	# 	 <p><b>ATM </b>: %s,%s</p>\
	# 	 <p><b>Summary </b>: %s</p>\
	# 	 <p><b>Description </b>: %s</p>')\
	# 	%(tname,
	# 		customer_id.name,
	# 		alert_obj.name,
	# 		alert_obj.category,
	# 		alert_obj.priority,
	# 		atm_name,
	# 		affectedATM.atm_id,
	# 		alert_obj.summary,
	# 		alert_obj.description)
	# 	body = MIMEText(text, _subtype='html')
	# 	msg.attach(body)
	# 	# res = server.sendmail(fromaddr, toaddr, msg.as_string())
	# 	# server.quit()
	# 	send.sendmail(FROM, TO, msg.as_string())
	# 	send.quit()

	# 	return True

cust_alerts()

# class mail_compose_message(osv.Model):
# 	_inherit = 'mail.compose.message'

# 	def send_mail(self, cr, uid, ids, context=None):
# 		context = context or {}
# 		if context.get('default_model') == 'cust.alerts' and context.get('default_res_id') and context.get('mark_so_as_sent'):
# 			context = dict(context, mail_post_autofollow=True)
# 			self.pool.get('cust.alerts').signal_workflow(cr, uid, [context['default_res_id']], 'quotation_sent')
# 		return super(mail_compose_message, self).send_mail(cr, uid, ids, context=context)

