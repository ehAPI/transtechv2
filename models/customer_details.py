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

	def create(self, cr, uid, vals, context=None):
		if vals.get('cust_code','/')=='/':
			vals['cust_code']=self.pool.get('ir.sequence').get(cr,uid,'customer.info') or '/'	
		return super(customer_details,self).create(cr, uid, vals, context=context)

customer_details()

class date_rate(osv.osv):
	_name = 'date.rate'
	_columns = {
	'cur' : fields.integer(),
	'dates' : fields.date('Date'),
	'rates' : fields.float('Rate'),
	}