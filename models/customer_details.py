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
	_rec_name = 'name'
	_description = "Customer Setup"

	def write(self,cr,uid,ids,vals,context=None):
		obj = self.browse(cr,uid,ids)
		c_ids = self.pool.get('res.users').search(cr,uid,[('name','=',obj[0].name)])
		if c_ids:
			if 'name' in vals:
				self.pool.get('res.users').write(cr,uid,c_ids[0],{'name':vals['name']})
			if 'image' in vals:
				self.pool.get('res.users').write(cr,uid,c_ids[0],{'image':vals['image']})
				# user = self.pool.get('res.users').browse(cr,uid,c_ids)
				# p_id = self.pool.get('res.partner').search(cr,uid,[('id','=',user[0].partner_id.id)])
		return super(customer_details,self).write(cr,uid,ids,vals,context=context)

	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
		    result[obj.id] = tools.image_get_resized_images(obj.image)
		return result

	def _set_image(self, cr, uid, id, name, value, args, context=None):
	        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

	def _has_image(self, cr, uid, ids, name, args, context=None):
		result = {}
		for obj in self.browse(cr, uid, ids, context=context):
		    result[obj.id] = obj.image != False
		return result

	def _show_tasks(self, cr, uid, ids, name, args, context=None):
		res = {}
		c_ids = self.pool.get('atm.surverys.management').search(cr,uid,[('customer','=',ids[0])])
		for t_id in self.browse(cr,uid,ids):
			res[t_id.id] = c_ids
		return res

	_columns = {
		'customer_code' : fields.char('Customer Code', size = 20, readonly=True),
		"image" : fields.binary('Image',
		    help="This field holds the image used as avatar for this contact, limited to 1024x1024px"),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
		    string="Medium-sized image", type="binary", multi="_get_image",
		    store={
		        'customer.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
		    },
		    help="Medium-sized image of this contact. It is automatically "\
		         "resized as a 128x128px image, with aspect ratio preserved. "\
		         "Use this field in form views or some kanban views."),	
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
            		string="Small-sized image", type="binary", multi="_get_image",
            		store={
                	'customer.info': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
           		 },
           		 help="Small-sized image of this contact. It is automatically "\
                	 "resized as a 64x64px image, with aspect ratio preserved. "\
                 	"Use this field anywhere a small image is required."),
        'has_image': fields.function(_has_image, type="boolean"),
		'name' : fields.char('Customer Name', size = 20, required=True),
		'address' : fields.text('Address'),
		'country_id' : fields.many2one('res.country','Country', ondelete='set null'),
		'contact_person' : fields.char('Contact Person', size = 50),
		'contact_email' : fields.char('Contact Person Email 1', size = 50),
		'contact_email2' : fields.char('Contact Person Email 2', size = 50),
		'contact_email3' : fields.char('Contact Person Email 3', size = 50),
		'mobile_no' : fields.char('Contact Number', size = 64),
		'active' : fields.boolean('Active??', size = 5),
		'sla_start' : fields.datetime('SLA Start Date'),
		'sla_end' : fields.datetime('SLA End Date'),
		'display_mapping':fields.boolean('Dispaly Mapping'),
		'task_ids': fields.function(_show_tasks, relation='atm.surverys.management', type="many2many", string='My Tasks'),
		'account_manager' : fields.many2one('res.users', 'Account Manager', ondelete='set null', required=True),
		'other_1' :fields.many2one('res.users', 'Other1', ondelete='set null', required=True),
		'other_2' :fields.many2one('res.users', 'Other2', ondelete='set null', required=True),
		'is_customer':fields.boolean('Is Customer'),
	}
	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]
	
	_defaults ={
		'active': 1,
		'country_id':_default_country,
		'is_customer':1
	}

	_order = 'customer_code'

	def create(self, cr, uid, vals, context=None):
		if vals.get('customer_code','/')=='/':
			vals['customer_code']=self.pool.get('ir.sequence').get(cr,uid,'customer.info') or '/'	
		return super(customer_details,self).create(cr, uid, vals, context=context)

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'customer_code': self.pool.get('ir.sequence').get(cr, uid, 'customer.info'),
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