from openerp.osv import fields, osv

class site_inspection(osv.osv):

	_name = 'site.inspection'
	_columns = {
			'name':fields.char('Inspection ID', readonly=True),
			'site_type':fields.selection([('ttw','TTW'),
				('lobby','LOBBY'),
				('other','Other'),
				('walkup','Walk Up'),
				('driveup','Drive Up')],'Site Type'),
			'acc_manager' : fields.many2one('res.users', 'Site Inspector Name', required=True),
			#'site_inspector_name':fields.many2one('site.inspector','Site Inspector Name',ondelete='set null'),
			#'surveyor':fields.many2one('res.users','Site Indpector Name',required=True),
			'date_assigned':fields.datetime('Date Assigned', required=True),
			'date_of_visit':fields.datetime('Date of Visit', required=True),

			'customer_name':fields.many2one('customer.info','Customer Name',required=True),
			'site_address':fields.text('Site Address'),
			'latitude':fields.char('Latitude'),
			'longitude':fields.char('Longitude'),
			'contact':fields.char('Contact Person Name'),
			'mobile':fields.integer('Mobile Number'),
			'job_description':fields.text('Job Description'),
			'atm_brand':fields.char('ATM Brand/Model/Class'),
			'hole_height_in':fields.char('Hole Height from inside'),
			'hole_height_cust':fields.char('Hole Height from Customer standing area', ),
			'hole_height_out':fields.char('Hole height from Outside'),
			'access_truck':fields.selection([('yes','Yes'),
				('no','No')],'Access For Truck'),
            'access_truck_crane':fields.selection([('yes','Yes'),
				('no','No')],'Access For Truck'),
            'hole_height_in_repeated':fields.char('Hole Height from inside'),
	}

	def create(self, cr, uid, vals, context=None):
		if vals.get('name','/')=='/':
			vals['name']=self.pool.get('ir.sequence').get(cr, uid, 'site.inspection') or '/'
		return super(site_inspection,self).create(cr, uid, vals, context=context)

site_inspection()


