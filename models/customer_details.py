from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
import random
import re
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from openerp import  tools

# customer details class
class customer_details(osv.osv):
	_name = "customer.info"
	_rec_name = 'cust_name'
	_description = "Customer Details"
	_columns = {
		'cust_code' : fields.char('Customer Code', size = 20, readonly=True),
		"cust_image" : fields.binary('Image'),
		'cust_name' : fields.char('Customer Name', size = 20, required=True),
		'address' : fields.text('Address'),
		'country' : fields.many2one('res.country','Country', ondelete='set null'),
		'cont_per' : fields.char('Contact Person', size = 20),
		'cont_per_e1' : fields.char('Contact Person Email 1', size = 20),
		'cont_per_e2' : fields.char('Contact Person Email 2', size = 20),
		'cont_per_e3' : fields.char('Contact Person Email 3', size = 20),
		'cont_no' : fields.char('Contact Number', size = 64),
		'active' : fields.boolean('Active??', size = 5),
		'sla_start_date' : fields.datetime('SLA Start Date'),
		'sla_end_date' : fields.datetime('SLA End Date'),
		'acc_manager' : fields.many2one('res.users', 'Account Manager', ondelete='set null', required=True),
		'other1' :fields.many2one('res.users', 'Other1', ondelete='set null', required=True),
		'other2' :fields.many2one('res.users', 'Other2', ondelete='set null', required=True),
	}
	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]
	
	_defaults ={
		'active': 1,
		'country':_default_country,
	}
	

	def send_invitation(self,cr,uid,ids,context=None):
		cust_obj = self.browse(cr,uid,ids,context=None)[0]
		if not cust_obj.cont_per_e1:
			raise osv.except_osv(_('No Email Provided for this customer'),_("Please give a Valid email address !") )
			return False
		name=cust_obj.cust_name
		if re.search(r'\s',cust_obj.cust_name):
			name=cust_obj.cust_name.replace(" ", "_")
		chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
		password = ''.join(random.choice(chars) for i in xrange(6))
		c_id = self.pool.get('res.users').search(cr,uid,[('name','=',cust_obj.cust_name)])
		gr_id = self.pool.get('res.groups').search(cr,uid,[('name','=','Customer')])
		del_id = self.pool.get('res.groups').search(cr,uid,[('name','=','Employee')])
		if c_id:
			raise osv.except_osv(_('You are already created a User for this customer'),_("Please recheck your users list via Users Menu.") )
			return False
		val={'name':cust_obj.cust_name,'login':name,'password':str(password),'role':'Customer'}
		new_id = self.pool.get('res.users').create(cr,uid,val,context=None)
		cr.execute('insert into  res_groups_users_rel (uid, gid) values(%s,%s)', (new_id, gr_id[0]))
		cr.execute('DELETE from  res_groups_users_rel where uid = %s and gid = %s', (new_id, del_id[0]))
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
		msg['Subject'] = 'Regarding Account Details For TransTechERP'
		toaddr = cust_obj.contact_email
		msg['To'] = toaddr
		text = ('<p><h2>Hello, %s</h2> Your account has been created in Transtech ERP as User</p><p><b>Your login credentials are given below:-</b></p><p>Username: %s</p><p>Password: %s</p><p>To login click on below link</p><p><a href="http://162.243.21.15:8069/">Click Here</a></p>')%(cust_obj.cust_name,name,password)
		body = MIMEText(text, _subtype='html')
		msg.attach(body)
		res = server.sendmail(fromaddr, toaddr, msg.as_string())
		server.quit()

		return True

customer_details()

class date_rate(osv.osv):
	_name = 'date.rate'
	_columns = {
	'cur' : fields.integer(),
	'dates' : fields.date('Date'),
	'rates' : fields.float('Rate'),
	}