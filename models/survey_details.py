from openerp.osv import fields, osv
from openerp.tools.translate import _
import datetime
import time
from openerp import tools
import random
import smtplib
import os
import base64
from PIL import Image
from os.path import expanduser
from lxml import etree
from openerp import workflow


class survey_details(osv.osv):

	_name = 'survey.details'


	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
			'name': self.pool.get('ir.sequence').get(cr, uid, 'survey.details'),
		})
		return super(survey_details, self).copy(cr, uid, id, default, context=context)

	def _check_customer(self, cr, uid, ids, name, args, context=None):

		result = {}

		groups_id = self.pool.get('res.users').read(cr, uid, uid)['groups_id']
		for obj in self.browse(cr, uid, ids):
			if len(groups_id) == 1:
				c_name = self.pool.get('res.users').read(cr, uid, uid)['name']
				if 'NBAD' in c_name:
					result[obj.id] = True

				else:
					result[obj.id] = False
			else:
				result[obj.id] = True

		return result
	
	_columns = {
		'name':fields.char('Survey id', readonly=True),
		'atm_report':fields.many2one('view.plan.tasks','ATM Report Task ID'),
	
		'month':fields.selection([('Jan','January'),
			('Feb','February'),
			('March','March'),
			('April','April'),
			('May','May'),
			('June','June'),
			('July','July'),
			('August','August'),
			('Sept','September'),
			('Oct', 'October'),
			('Nov','November'),
			('Dec','December')],'Month'),
		'remarks_category' : fields.many2one('remark.category','Remarks Category'),
		'atm' : fields.many2one('atm.details', 'ATM'),
		'customer_name':fields.many2one('customer.info','Customer'),
		'acc_manager' : fields.many2one('res.users', 'Surveyor'),
		'is_nbad': fields.function(_check_customer, type='boolean', string='Is NBAD', method=True, store=False, multi=False),
		
		#'surveyor':fields.many2one('res.users','Site Indpector Name',required=True),
		'visit_time':fields.datetime('Visit Time'),
		#'customer':fields.many2one('customer.info','Customer Name'),
		'current_longitude':fields.char('Current Longitude'),
		'current_latitude':fields.char('Current Latitude'),
		'next_survey_distance':fields.integer('Next Survey Distance'),
		'next_task_id':fields.many2one('view.plan.tasks','Next Task ID'),
		'state' : fields.many2one('res.country.state', 'State'),
		'status': fields.selection([
		('waiting_approval', 'Waiting for Approval'),
		('approved', 'Approved')], 'Status'),

		'no_comments':fields.boolean('No Comments'),
		'col_cash':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Collect Cash'),
		'col_receipt':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Collect Receipt'),
		'ins_card':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Insert Card'),
		'ins_cheq':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Insert Cheque'),
		'cables':fields.selection([('required','Required'),
			('completed','Completed')],'Cables Securing'),
		'trash':fields.selection([('required','Required')],'Trash bin Keys'),
		'mach':fields.selection([('required','Required')],'Machine Surround Maintenance'),
		'card_pic':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Insert Card'),
		'trans_receipt':fields.selection([('na','Not Available')],'Transaction Receipt'),
		'do_dont':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],"Do's and Don'ts sticker"),
		'cash_deposit':fields.selection([('nw','Not Working')],'Cash Deposit'),
		'touch_errors':fields.selection([('nw','Touch function not working'),
			('dd','Display Distorted')],'Touch Screen Errors'),
		'screen':fields.selection([('blank','Blank'),('frozen','Frozen')],'Screen'),
		'ac_issues':fields.selection([('nw','Not Working')],'AC Issues'),
		'surround_locks':fields.selection([('nw_lock_damaged','Network Lock Box Damaged'),
			('nw_lock_required','Network Box Lock Required'),
			('vl_damaged','Vault Lock Damaged'),
			('lock_req','Lock Required')],'Surround Locks'),
		'lights':fields.selection([('off','Off'),('on','On')],'Main Board Lights'),
		'sec_cam':fields.selection([('exp','Exposed')],'Security Camera Cables'),
		'out_cont':fields.selection([('yes','Yes'),('no','No')],'Outdated Contact no.on the Surround'),
		'card_reader':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Card Reader'),
		'side_frames':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Side Frames/Posters on the Surround'),

		'atm_vault':fields.selection([('open','Open'),('damaged','Damaged')],'ATM Vault Door'),
		'ded':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'DED Number'),
		'atm_notices':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'ATM Notices'),
		'keypad':fields.selection([('displaced','Displaced'),
			('damaged','Damaged'),
			('faded','Number Faded')],'Keypad Condition'),
		'atm_status':fields.selection([('offline','Offline'),
			('off','Powered Off'),
			('out_of_service','Out of Service')],'ATM Status'),
		'atm_screen_protector':fields.selection([('damaged','Damaged')],'ATM Screen Protector'),
		'trashbin_repairs':fields.selection([('required','Required'),
			('keys_required','Keys Required'),
			('damaged','Damaged'),('replaced','Replaced')],
			'Trash Bin Repairs/ replacement to be completed(as per the agreed contract'),
		'ttw_branding':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'TTW Branding'),
		'protective_box':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Protective Box for Power Crcuit'),
		'machine_cam':fields.selection([('glass_mining','Glass Mining'),
			('glass_broken','Glass Broken'),
			('out_of_focus','Out of Focus')],'Machine Security Camera'),
		'fascia':fields.selection([('faded_from_edges','Faded from Edges'),
			('faded_from_keypad','Faded from Keypad'),
			('damaged','Damaged')],'Fascia Condition'),	
		'ins_cash':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Insert Cash'),
		'network_sticker':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Network Sticker'),
		'instruction_sticker':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Instruction Sticker'),
		'vault_branding':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Vault Branding'),
		'terminal_id':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Terminal ID'),
		'spot_lights':fields.selection([('off','Off'),
			('missing','Missing'),
			('replaced','Replaced')],'Spot Lights'),
		'machine_surround':fields.selection([
			('damaged','Damaged')],'Machine Surround Branding'),
		'canopy':fields.selection([
			('damaged','Damaged')],'Canopy Branding'),
		'pin_guard':fields.selection([('required','Required'),
			('damaged','Damaged'),
			],'Pin Guard'),
		'privacy_flap':fields.selection([('required','Required'),
			('damaged','Damaged'),
			],'Privacy Flap'),
		'kiosk_door':fields.selection([('open','Open'),
			('damaged','Damaged'),
			],'Kiosk Door'),
		'kiosk_lights':fields.selection([('off','Off'),
			('left_off','Left Off'),('top_off','Top Off'),
			('right_off','Right Off'),
			],'Kiosk Lights'),
		'fascia_light':fields.selection([('off','Off'),
			('missing','Missing'),
			('replaced','Replaced')],'Fascia Light'),
		'boom_sign':fields.selection([('off','Off'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Boom Sign'),
		'image1_b':fields.binary('image1'),
		'image2_b':fields.binary('image2'),
		'image3_b':fields.binary('image3'),
		'image4_b':fields.binary('image4'),
		'image5_b':fields.binary('image5'),
		'image6_b':fields.binary('image6'),
		'image7_b':fields.binary('image7'),
		'image8_b':fields.binary('image8'),
		'image1_a':fields.binary('image1'),
		'image2_a':fields.binary('image2'),
		'image3_a':fields.binary('image3'),
		'image4_a':fields.binary('image4'),
		'image5_a':fields.binary('image5'),
		'image6_a':fields.binary('image6'),
		'image7_a':fields.binary('image7'),
		'image8_a':fields.binary('image8'),


		}

	_order = "visit_time desc"

	_defaults={

		'status': 'waiting_approval',
		'visit_time': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),

		}

	def onchange_taskid(self, cr, uid, ids, atm_report, context=None):
		res = {'value': {}}
		if atm_report:
			part = self.pool.get('view.plan.tasks').browse(
				cr, uid, atm_report, context)
			# print part.atm.id
			res['value'].update({'month': part.task_month})
			res['value'].update({'atm': part.atm.id})
			res['value'].update({'acc_manager': part.surveyor.id})

			res['value'].update({'customer_name': part.customer.id})
			res['value'].update({'visit_time': part.visit_time})
			res['value'].update({'state': part.state.id})

		return res

	def __resize__image(self, cr, uid, image, context=None):

		imgdata1 = base64.b64decode(image)
		home = expanduser("~")

		dir_name = home + '/temp_img/%s' % (str(uid))

		if os.path.exists(dir_name):
			full_path = dir_name + '/temp_img.jpeg'

		else:
			os.makedirs(dir_name)
			full_path = dir_name + '/temp_img.jpeg'

		with open(full_path, 'wb') as f:
			f.write(imgdata1)
			f.close()

		im = Image.open(full_path)
		im.save(full_path, quality=20)

		f = open(full_path, 'r')

		photo_data = f.read()

		n_data = base64.b64encode(photo_data)

		# print tools.human_size(n_data)

		return n_data

	def __create_dir(self, cr, uid, cid, atm_id, month, context=None):

		customer = self.pool.get('customer.info').browse(cr, uid, cid).name
		atm = self.pool.get('atm.details').browse(cr, uid, atm_id).atm_id

		dir_name = '/var/www/html/ERP/%s/%s/%s' % (
			str(month), str(customer), str(atm))

		return dir_name

	def __write_image_file(self, cr, uid, imgdata1, vals, counter, context=None):

		file_loc = self.__create_dir(
			cr, uid, vals['customer_name'], vals['atm'], vals['month'], context=None)

		if os.path.exists(file_loc):
			full_path = file_loc + '/%s_%s.jpeg' % (vals['name'], str(counter))

		else:
			os.makedirs(file_loc)
			full_path = file_loc + '/%s_%s.jpeg' % (vals['name'], str(counter))

		with open(full_path, 'wb') as f:
			f.write(imgdata1)
			f.close()

		return full_path

	def add_line(self, cr, uid, ids, context):

		this = self.browse(cr, uid, ids, context=context)[0]
		# tree_id = self.pool.get('ir.model.data').get_object_reference(
		search_view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'atm', 'view_atm_surverys_filter')[1]
		form_id = self.pool.get('ir.model.data').get_object_reference(
			cr, uid, 'atm', 'view_atm_view_plan_tasks_form')[1]

		res = {
			'type': 'ir.actions.act_window',
			'name': 'Test',
			'view_type': 'form',
			'view_mode': 'form,tree',
			'res_model': 'view.plan.tasks',
			'domain': [('id', '=', 290)],
			# 'context':{'search_default_Current': 1, 'search_default_solu': 1, 'search_default_traj':1},
			'views': [(tree_id, 'tree'), (form_id, 'form')],
			# 'search_view_id': search_view_id
		}

		return res


	def cover_print(self, cr, uid, ids, context=None):
		# for i in range(0,5):
		survey_ids = self.search(cr, uid, [('status', '=', 'approved')])
		'''
		This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
		'''
		assert len(
			ids) == 1, 'This option should only be used for a single id at a time'
		datas = {
			'model': 'survey.details',
			'ids': survey_ids,
			'form': self.read(cr, uid, survey_ids, context=context),
		}
		return {'type': 'ir.actions.report.xml', 'report_name': 'survey.details', 'datas': datas, 'nodestroy': True}



	def status_approve(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'approved'},context=context)
		return True 

	def write(self, cr, uid, ids, vals, context=None):
		return super(survey_details, self).write(cr, uid, ids, vals, context)

	# def create(self, cr, uid, vals, context=None):
 #   		vals['name']= self.pool.get('ir.sequence').get(cr, uid, 'survey.det')
 #   		return super(Survey_Details, self).create(cr, uid, vals, context=context)

	def create(self, cr, uid, vals, context=None):

		if vals.get('name', '/') == '/':
			vals['name'] = self.pool.get('ir.sequence').get(
				cr, uid, 'survey.details') or '/'

		vals['visit_time'] = datetime.datetime.now()
		s_ids = self.search(cr, uid, [('month', '=', vals['month']), ('atm', '=', vals[
							'atm']), ('atm_report', '=', vals['atm_report'])], context=None)

		if s_ids:
			self.unlink(cr, uid, s_ids, context=None)

		survey_id = super(survey_details, self).create(
			cr, uid, vals, context=context)

		values = {}

		part = self.pool.get('view.plan.tasks').browse(
			cr, uid, vals['atm_report'], context)

		self.pool.get('view.plan.tasks').write(cr, uid, vals['atm_report'], {'status': 'done'}, context)

		approve_surveys = self.status_approve(cr,uid,survey_id,context=None)
		
		values.update({'state': part.state.id})

		if vals['current_longitude'] and vals['current_latitude']:
			self.pool.get('atm.details').write(cr, uid, vals['atm'], {
				'latitude': vals['current_latitude'], 'longitude': vals['current_longitude']})

		self.write(cr, uid, survey_id, values)
		return survey_id  

	

	# def print_survey(self, cr, uid, ids, context=None):
	# 	'''
	# 	This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
	# 	'''
	# 	assert len(ids) == 1, 'This option should only be used for a single id at a time'
	# 	self.signal_workflow(cr, uid, ids, 'quotation_sent')
	# 	return self.pool['report'].get_action(cr, uid, ids, 'atm.print_survey', context=context)
	 
	

	def create(self, cr, uid, vals, context=None):
		if vals.get('name','/')=='/':
			vals['name']=self.pool.get('ir.sequence').get(cr, uid, 'survey.details') or '/'
		return super(survey_details,self).create(cr, uid, vals, context=context)

survey_details()


# class upload_images(osv.osv):
#     _name = 'upload_images.tutorial'
#     _description = 'Tutorial image uploading'
 
#     _columns = {
#     'upload_name': fields.char('Name', required=True, translate=True),
#     'image': fields.binary("Image",
#             help="This field holds the image used as image for our customers, limited to 1024x1024px."),
#     'image_medium': fields.function(_get_image, fnct_inv=_set_image,
#             string="Image (auto-resized to 128x128):", type="binary", multi="_get_image",
#             store={
#                 'upload_images.tutorial': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
#             },help="Medium-sized image of the category. It is automatically "\
#                  "resized as a 128x128px image, with aspect ratio preserved. "\
#                  "Use this field in form views or some kanban views."),
#     'image_small': fields.function(_get_image, fnct_inv=_set_image,
#             string="Image (auto-resized to 64x64):", type="binary", multi="_get_image",
#             store={
#                 'upload_images.tutorial': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
#             },
#             help="Small-sized image of the category. It is automatically "\
#                  "resized as a 64x64px image, with aspect ratio preserved. "\
#                  "Use this field anywhere a small image is required."),
#     }

#     def _get_image(self, cr, uid, ids, name, args, context=None):
#         result = dict.fromkeys(ids, False)
#         for obj in self.browse(cr, uid, ids, context=context):
#             result[obj.id] = tools.image_get_resized_images(obj.image)
#         return result

#     def _set_image(self, cr, uid, id, name, value, args, context=None):
#         return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

# upload_images()
# class images_calss(osv.osv):

# 	def image1_bfr(self, cr, uid, ids, name, arg, context=None):
# 		result = {}
# 		for obj in self.browse(cr, uid, ids, context=context):
# 			result[obj.id] = obj.image1_b
# 		return result

# 	def image3_bfr(self, cr, uid, ids, name, arg, context=None):
# 		result = {}
# 		for obj in self.browse(cr, uid, ids, context=context):
# 			result[obj.id] = obj.image3_b
# 		return result

# 	def image2_bfr(self, cr, uid, ids, name, arg, context=None):
# 		result = {}
# 		for obj in self.browse(cr, uid, ids, context=context):
# 			result[obj.id] = obj.image2_bfr
# 		return result

# 	def image6_afr(self, cr, uid, ids, name, arg, context=None):
# 		result = {}
# 		for obj in self.browse(cr, uid, ids, context=context):
# 			result[obj.id] = obj.image6_a
# 		return result

# 	def image8_afr(self, cr, uid, ids, name, arg, context=None):
# 		result = {}
# 		for obj in self.browse(cr, uid, ids, context=context):
# 			result[obj.id] = obj.image8_a
# 		return result

# 	def image7_afr(self, cr, uid, ids, name, arg, context=None):
# 		result = {}
# 		for obj in self.browse(cr, uid, ids, context=context):
# 			result[obj.id] = obj.image7_a
# 		return result

# 	_inherit = 'survey.details'

# 	_columns = {

# 		'bfr_img_front_r': fields.function(image1_bfr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'bfr_img_side_r': fields.function(image3_bfr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'bfr_img_back_r': fields.function(image2_bfr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'after_img_side_r': fields.function(image8_afr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'after_img_front_r': fields.function(image6_afr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'after_img_back_r': fields.function(image7_afr, type='binary', string='Image', method=True, store=False, multi=False),

# 	}
# images_calss()

