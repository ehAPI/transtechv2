from openerp.osv import fields, osv
<<<<<<< HEAD
import time

import time

=======
from openerp.tools.translate import _
import datetime
import time
import urllib
import random
>>>>>>> 7ab66f4f40370e99e9866130e63441eadf4e4fd1

# atm details class

class atm_details(osv.osv):
	_name = 'atm.details'
	_rec_name = 'atm_branch_details'
	_description = 'ATM Details'
	_columns = {
	'atm_image' : fields.binary('ATM Image', widget='image'),
	'atm_code' : fields.char('ATM Code', readonly=True),
	'atm_branch_details' :fields.char('ATM Branch Details',required=True),
	'bank_atm_id' :fields.char('Bank ATM ID (proved by bank)',required=True),
	'customer' :fields.many2one('customer.info','Customer',required=True, onchange='onchange_customer(customer)', ondelete='set null'),
	'atm_type' :fields.selection([('atm_only','ATM Only'),
								  ('atm_cash_deposit','ATM and Cash Deposit'),
								  ('drive', 'Drive Through'),
								  ('walk', 'Walk Through'),
								  ('lobby', 'Lobby'),
								  ('ttw', 'TTW')],'ATM Type',required=True),
	'visits_done' :fields.integer('Visits Done'),
	'visits_left' :fields.integer('Visits Left'),
	'visits_required' :fields.integer('Required Visits', ondelete='set null'),
	'date' : fields.date('Date'),
	'country' : fields.many2one('res.country','Country', ondelete='set null'),
	'state' : fields.many2one('res.country.state', 'State', required=True, ondelete='set null'),
	'sla_start_date' : fields.datetime('SLA Start Date'),
	'sla_end_date' : fields.datetime('SLA End Date'),
	'sic' : fields.text('Special Instructions/Conditions'),
	'longitude' : fields.char('Longitude'),
	'latitude' : fields.char('Latitude'),
	'child_ids' : fields.one2many('atm.old','parent_id', readonly=True),
	'atm_id' :fields.char('ATM ID'),
	'atm_model' :fields.char('ATM Model'),
	'atm_serial_no' :fields.char('ATM Serial No.'),
	'atm_make' :fields.char('ATM Make'),
	'atm_functionality' :fields.char('ATM Functionality'),
	'base_height' :fields.char('Base Height'),
<<<<<<< HEAD
=======
	'no_tasks':fields.integer('No. of Tasks',readonly=True),
>>>>>>> 7ab66f4f40370e99e9866130e63441eadf4e4fd1
	'location_category' :fields.selection([('offsite','Offsite'),('onsite','Onsite')],'Location Category'),
	'onsite_category' :fields.selection([('branch','Branch'),
										 ('csu','CSU'),
										 ('mall_branch','Mall Branch')],'Onsite Category', invisible=[['location_category','=','offsite']]),
	'offsite_category' :fields.selection([('sm','Shopping Mall'),
										  ('other','Other'),
										  ('govt_inst','Govt. Institution'),
										  ('fuel_station','Fuel Station')],'Offsite Category',invisible=[['location_category','=','onsite']]),
	'kiosk_type' :fields.char('Kiosk Type'),
	'branding_details' :fields.text('Branding Details'),
	'installation_date' :fields.date('Installation Date'),
	'removed_from' :fields.char('Removed From'),
	'd1' :fields.char('Device 1'),
	'd2' :fields.char('Device 2'),
	'd3' :fields.char('Device 3'),
	'd4' :fields.char('Device 4'),
	'd5' :fields.char('Device 5'),
	'escorting_company' :fields.char('Escorting Company'),
	'ded_no' :fields.char('DED Number'),
	'make' :fields.char('Make'),
	'model' :fields.char('Model'),
	'capacity' :fields.char('Capacity'),
	'detail1' :fields.char('Detail 1'),
	'detail2' :fields.char('Detail 2'),
	}
	def _default_country(self, cr, uid, context=None):
		cid = self.pool.get('res.country').search(cr, uid, [('code', '=', 'AE')], context=context)
		return cid[0]

	_defaults = {
		'date': lambda *a: time.strftime('%Y-%m-%d'),
		'country':_default_country,
	}
	_order = 'atm_code'
<<<<<<< HEAD
	
=======

	def open_map(self, cr, uid, ids, context=None):
		address_obj= self.pool.get('atm.details')
		partner = address_obj.browse(cr, uid, ids, context=context)[0]
		url="http://maps.google.com/maps?oi=map&q="
		if partner.longitude:
			url+=partner.longitude.replace(' ','+')
		if partner.latitude:
			url+= ',' + partner.latitude.replace(' ','+')
		return {
			'type': 'ir.actions.act_url','url':url,'target': 'new'}
	
	def geo_localize(self, cr, uid, ids, context=None):

		partner = self.browse(cr,uid,ids)
		latitude = partner[0].latitude
		longitude = partner[0].longitude
		geo = {}
		if latitude or longitude:
			geo['lat'] = latitude
			geo['lng'] = longitude
			return float(geo['lat']), float(geo['lng'])
		return True

	def name_get(self,cr,uid,ids,context=None):
		if context is None:
			context ={}
		res=[]
		record_name=self.browse(cr,uid,ids,context)
		for object in record_name:

			# if object.name:
			if object.latitude and object.longitude:
				  # name for contact_address_id field
				res.append((object.id,object.atm_branch_details+', '+object.bank_atm_id+', '+'%%'+object.latitude+'%%'+object.longitude))
			else:
			   # //name for contact_id field                     
				res.append((object.id,object.atm_branch_details+', '+object.bank_atm_id))
		return res
>>>>>>> 7ab66f4f40370e99e9866130e63441eadf4e4fd1

atm_details()

class atm_old(osv.osv):
	_name = 'atm.old'    
	_columns = { 
				'parent_id':fields.many2one('atm.details','ATM', ondelete='set null'),
				'longitude':fields.char('Longitude'),
				'latitude':fields.char('Latitude'),
				'date':fields.date('Date'),
				'name':fields.char('ATM Branch Details'),
				}

