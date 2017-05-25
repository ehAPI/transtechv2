from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID

class transtech_site_inspection(osv.osv):

	_name = 'transtech.site.inspection'

	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
            'name': self.pool.get('ir.sequence').get(cr, uid, 'transtech.site.inspection'),
        })
		return super(atm_surverys_management, self).copy(cr, uid, id, default, context=context)

	_columns = {
			'name':fields.char('Inspection ID', readonly=True),
			'site_type':fields.selection([('ttw','TTW'),
				('lobby','LOBBY'),
				('other','Other'),
				('walkup','Walk Up'),
				('driveup','Drive Up')],'Site Type'),
			'surveyor' : fields.many2one('res.users', 'Site Inspector Name', required=True),
			#'site_inspector_name':fields.many2one('site.inspector','Site Inspector Name',ondelete='set null'),
			#'surveyor':fields.many2one('res.users','Site Indpector Name',required=True),
			'date_assigned':fields.datetime('Date Assigned', required=True),
			'date_of_visit':fields.datetime('Date of Visit', required=True),

			'customer':fields.many2one('customer.info','Customer Name',required=True),
			'site_address':fields.text('Site Address'),
			'site_lat':fields.char('site_lat'),
			'site_long':fields.char('site_long'),
			'contact_person':fields.char('contact Person Name'),
			'contact_mobile':fields.integer('Mobile Number'),
			'job_description':fields.text('Job Description'),
			'atm_brand':fields.char('ATM Brand/Model/Class'),
			'hole_height':fields.char('Hole Height from Customer standing area', ),
			'access_for_truck':fields.selection([('yes','Yes'),
				('no','No')],'Access For Truck'),
            'access_for_truck_crane':fields.selection([('yes','Yes'),

				('no','No')],'Access For Truck with Crane'),

		'hole_inside_height':fields.char("Hole Height from inside"),
		'inside_outside':fields.char("Hole Height from inside"),
		'hole_height_outside':fields.char("Hole height from Outside"),
            
	}

	_order = "name desc"

	def create(self, cr, uid, vals, context=None):
		if vals.get('name','/')=='/':
			vals['name']=self.pool.get('ir.sequence').get(cr, uid, 'transtech.site.inspection') or '/'
		return super(transtech_site_inspection,self).create(cr, uid, vals, context=context)

transtech_site_inspection()


