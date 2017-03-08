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
	_description = "Customer Setup"

	def write(self,cr,uid,ids,vals,context=None):
		obj = self.browse(cr,uid,ids)
		c_ids = self.pool.get('res.users').search(cr,uid,[('name','=',obj[0].cust_name)])
		if c_ids:
			if 'cust_name' in vals:
				self.pool.get('res.users').write(cr,uid,c_ids[0],{'name':vals['cust_name']})
			if 'cust_image' in vals:
				self.pool.get('res.users').write(cr,uid,c_ids[0],{'image':vals['cust_image']})
				# user = self.pool.get('res.users').browse(cr,uid,c_ids)
				# p_id = self.pool.get('res.partner').search(cr,uid,[('id','=',user[0].partner_id.id)])
		return super(customer_details,self).write(cr,uid,ids,vals,context=context)

	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
		    result[obj.id] = tools.image_get_resized_images(obj.cust_image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
	        return self.write(cr, uid, [id], {'cust_image': tools.image_resize_image_big(value)}, context=context)

	def _has_image(self, cr, uid, ids, name, args, context=None):
		result = {}
		for obj in self.browse(cr, uid, ids, context=context):
		    result[obj.id] = obj.image != False
		return result

	def _show_tasks(self, cr, uid, ids, name, args, context=None):
		res = {}
		c_ids = self.pool.get('view.plan.tasks').search(cr,uid,[('customer_name','=',ids[0])])
		for t_id in self.browse(cr,uid,ids):
			res[t_id.id] = c_ids
		return res

	_columns = {
		'cust_code' : fields.char('Customer Code', size = 20, readonly=True),
		"cust_image" : fields.binary('Image',
		    help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
		    string="Medium-sized image", type="binary", multi="_get_image",
		    store={
		        'customer.info': (lambda self, cr, uid, ids, c={}: ids, ['cust_image'], 10),
		    },
		    help="Medium-sized image of this contact. It is automatically "\
		         "resized as a 128x128px image, with aspect ratio preserved. "\
		         "Use this field in form views or some kanban views."),	
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            		string="Small-sized image", type="binary", multi="_get_image",
            		store={
                	'customer.info': (lambda self, cr, uid, ids, c={}: ids, ['cust_image'], 10),
           		 },
           		 help="Small-sized image of this contact. It is automatically "\
                	 "resized as a 64x64px image, with aspect ratio preserved. "\
                 	"Use this field anywhere a small image is required."),
        'has_image': fields.function(_has_image, type="boolean"),
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
		'display_mapping':fields.boolean('Dispaly Mapping'),
		'task_ids': fields.function(_show_tasks, relation='view.plan.tasks', type="many2many", string='My Tasks'),
		'acc_manager' : fields.many2one('res.users', 'Account Manager', ondelete='set null', required=True),
		'other1' :fields.many2one('res.users', 'Other1', ondelete='set null', required=True),
		'other2' :fields.many2one('res.users', 'Other2', ondelete='set null', required=True),
		'is_customer':fields.boolean('Is Customer'),
	}
	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]
	
	_defaults ={
		'active': 1,
		'country':_default_country,
		'is_customer':1
	}

	_order = 'cust_code'

	def create(self, cr, uid, vals, context=None):
		if vals.get('cust_code','/')=='/':
			vals['cust_code']=self.pool.get('ir.sequence').get(cr,uid,'customer.info') or '/'	
		return super(customer_details,self).create(cr, uid, vals, context=context)

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'cust_code': self.pool.get('ir.sequence').get(cr, uid, 'customer.info'),
        })
		return super(customer_details, self).copy(cr, uid, id, default, context=context)


customer_details()

class date_rate(osv.osv):
	_name = 'date.rate'
	_columns = {
	'cur' : fields.integer(),
	'dates' : fields.date('Date'),
	'rates' : fields.float('Rate'),
	}