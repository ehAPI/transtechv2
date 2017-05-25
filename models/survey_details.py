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

class survey_details_info(osv.osv):

	_name = 'survey.info'


	def copy(self, cr, uid, id, default=None, context=None):
		if not default:
			default = {}
		default.update({
			'name': self.pool.get('ir.sequence').get(cr, uid, 'survey.info'),
		})
		return super(survey_details_info, self).copy(cr, uid, id, default, context=context)

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
		'surv_task':fields.many2one('atm.surverys.management','ATM Report Task ID'),
		'month': fields.selection([
            ('jan', 'January'),
            ('feb', 'February'),
            ('mar', 'March'),
            ('apr', 'April'),
            ('may', 'May'),
            ('june', 'June'),
            ('jul', 'July'),
            ('aug', 'August'),
            ('sep', 'September'),
            ('oct', 'October'),
            ('nov', 'November'),
            ('dec', 'December'),
        ], 'Month'),
		'remarks_survey' : fields.many2one('remarks.category','Remarks Category'),
		'atm_surv' : fields.many2one('atm.info', 'ATM'),
		'customer_surv':fields.many2one('customer.info','Customer'),
		'surveyor_surv' : fields.many2one('res.users', 'Surveyor'),
		'is_nbad':fields.function(_check_customer, type='boolean', string='Is NBAD', method=True, store=False, multi=False),
		
		#'surveyor':fields.many2one('res.users','Site Indpector Name',required=True),
		'visit_tm':fields.datetime('Visit Time'),
		#'customer':fields.many2one('customer.info','Customer Name'),
		'cur_longitude':fields.char('Current Longitude'),
		'cur_latitude':fields.char('Current Latitude'),
		'nxt_survey_distance':fields.integer('Next Survey Distance'),
		'nxt_taskid':fields.many2one('atm.surverys.management','Next Task ID'),
		'state' : fields.many2one('res.country.state', 'State'),
		'status': fields.selection([
		('waiting_approval', 'Waiting for Approval'),
		('approved', 'Approved')], 'Status'),

		'check_list1':fields.boolean('No Comments'),
		'check_list3':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Collect Cash'),
		'check_list4':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Collect Receipt'),
		'check_list5':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Insert Card'),
		'insert_chq':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Insert Cheque'),
		'check_list11':fields.selection([('required','Required'),
			('completed','Completed')],'Cables Securing'),
		'check_list13':fields.selection([('required','Required')],'Trash bin Keys'),
		'check_list15':fields.selection([('required','Required')],'Machine Surround Maintenance'),
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
		'check_list21':fields.selection([('nw_lock_damaged','Network Lock Box Damaged'),
			('nw_lock_required','Network Box Lock Required'),
			('vl_damaged','Vault Lock Damaged'),
			('lock_req','Lock Required')],'Surround Locks'),
		'check_list23':fields.selection([('off','Off'),('on','On')],'Main Board Lights'),
		'check_list25':fields.selection([('exp','Exposed')],'Security Camera Cables'),
		'check_list26':fields.selection([('yes','Yes'),('no','No')],'Outdated Contact no.on the Surround'),
		'check_list27':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Card Reader'),
		'side_frames':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Side Frames/Posters on the Surround'),

		'check_list28':fields.selection([('open','Open'),('damaged','Damaged')],'ATM Vault Door'),
		'check_list29':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'DED Number'),
		'black_notices':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'ATM Notices'),
		'keypad_condition':fields.selection([('displaced','Displaced'),
			('damaged','Damaged'),
			('faded','Number Faded')],'Keypad Condition'),
		'atm_status':fields.selection([('offline','Offline'),
			('off','Powered Off'),
			('out_of_service','Out of Service')],'ATM Status'),
		'scree_protector':fields.selection([('damaged','Damaged')],'ATM Screen Protector'),
		'trash_bin_repairs':fields.selection([('required','Required'),
			('keys_required','Keys Required'),
			('damaged','Damaged'),('replaced','Replaced')],
			'Trash Bin Repairs/ replacement to be completed(as per the agreed contract'),
		'ttw_branding':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'TTW Branding'),
		'protective_box':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Protective Box for Power Crcuit'),
		'machine_security_camera':fields.selection([('glass_mining','Glass Mining'),
			('glass_broken','Glass Broken'),
			('out_of_focus','Out of Focus')],'Machine Security Camera'),
		'fascia_condition':fields.selection([('faded_from_edges','Faded from Edges'),
			('faded_from_keypad','Faded from Keypad'),
			('damaged','Damaged')],'Fascia Condition'),	

		
        # Branding Audit Check List sheet-1

        'dl_brochure_holder':fields.selection([('updated_inventory', ' Updated inventory available'),
                                                ('outdated_inventory',
                                                 'Outdated inventory available'),
                                                ('low_inventory',
                                                 'Low inventory - To be ordered'),
                                                ], 'DL Brochure Holder'),

        'brochure_holder_19x19':fields.selection([('updated_inventory', ' Updated inventory available'),
                                                   ('outdated_inventory',
                                                    'Outdated inventory available'),
                                                   ('low_inventory',
                                                    'Low inventory - To be ordered'),
                                                   ], 'Brochure holder - 19 x 19'),

        'application_form': fields.selection([('updated_inventory', ' Updated inventory available'),
                                              ('outdated_inventory',
                                               'Outdated inventory available'),
                                              ('low_inventory',
                                               'Low inventory - To be ordered'),
                                              ], 'Application form'),

        'poster_frames': fields.selection([('current_compaign', 'Current campaigns available'),
                                           ('outdated', 'Outdated/old available - Reported')],
                                          'Poster Frames'),
        'internal_window_graphics': fields.selection([('current_compaign', 'Current campaigns available'), ('outdated', 'Outdated/old available - Reported')], 'Internal window graphics'),

        'advertising_stands': fields.selection([('current_compaign', 'Current campaigns available'), ('outdated', 'Outdated/old available - Reported')], 'Advertising stands'),
        'push/pull_stickers': fields.selection([('running', 'In running condition'),
                                                ('req_replacement',
                                                 'Require replacement'),
                                                ('missing', 'Missing'),
                                                ], 'Push/Pull stickers'),

        'stationary_calendars': fields.selection([('updated_inventory', ' Updated inventory available'),
                                                  ('outdated_inventory',
                                                   'Outdated inventory available'),
                                                  ('low_inventory',
                                                   'Low inventory - To be ordered'),
                                                  ], 'Stationary - Calendars, annual reports, tissue boxes'),

        'store_inventory_cur_campaigns': fields.selection([('updated_inventory', ' Updated inventory available'),
                                                           ('outdated_inventory',
                                                            'Outdated inventory available'),
                                                           ('low_inventory',
                                                            'Low inventory - To be ordered'),
                                                           ], 'Store inventory - Current campaigns'),

        'led_screen_ad': fields.selection([('current_compaign', 'Current campaigns available'), ('outdated', 'Outdated/old available - Reported')], 'LED Screen advertisement'),
        'palm_leaf_strip_sticker': fields.selection([('running', 'In running condition'),
                                                     ('req_replacement',
                                                      'Require replacement'),
                                                     ('missing', 'Missing'),
                                                     ], 'Palm Leaf Strip Sticker'),
        'branding_conditions': fields.selection([('running', 'In running condition'),
                                                 ('req_replacement',
                                                  'Require replacement'),
                                                 ('missing', 'Missing'),
                                                 ], 'Branding condition (internal) -  Dusty/faded colors/torn'),
        'led_conditions': fields.selection([('running_updated_campaign', 'Running with updated campaigns'),
                                            ('damaged', 'Not working/Damaged'),
                                            ('running_outdated_campaign',
                                             'Running with outdated campaigns'),
                                            ], 'LED screen condition - Report in case damaged or not running'),

        'external_br_condition': fields.selection([('running', 'In running condition'),
                                                   ('req_replacement',
                                                    'Require replacement'),
                                                   ('missing', 'Missing'),
                                                   ], 'External branch branding condition'),

        'onsite_atm_branding': fields.selection([('running', 'In running condition'),
                                                 ('req_replacement',
                                                  'Require replacement'),
                                                 ('missing', 'Missing'),
                                                 ], 'Branding of on-site ATM'),

        'personal_loan_compaign': fields.selection([('available', 'Available'),
                                                    ('outdated',
                                                     'Not available/Outdated'),
                                                    ], 'Personal Loan Campaign'),

        'real_madrid_compaign': fields.selection([('available', 'Available'),
                                                  ('outdated',
                                                   'Not available/Outdated'),
                                                  ], 'Real-madrid Campaign'),
        'mobile_app_campaign': fields.selection([('available', 'Available'),
                                                 ('outdated',
                                                  'Not available/Outdated'),
                                                 ], 'Mobile App Campaign'),
        'mortgage_loan_campaign': fields.selection([('available', 'Available'),
                                                    ('outdated',
                                                     'Not available/Outdated'),
                                                    ], 'Mortgage Loan Campaign'),
        'other_compaign': fields.selection([('available', 'Available'),
                                            ('outdated',
                                             'Not available/Outdated'),
                                            ], 'Any other campaign except ML,PL, RM & Mobile app'),

        # Branding Audit Check List sheet-2

        # 'initial_observations': fields.boolean('Initial observations'),
        # 'record_observations': fields.boolean('Recording the observations, record any thing unusual found on the site'),
        # 'take_pic_before_cleaning': fields.boolean('Taking picture before cleaning initiation'),
        # 'cleaning_atm_surround': fields.boolean('Cleaning the ATM and surround/enclosure/topper'),
        # 'cleaning_skirting': fields.boolean('Cleaning the skirting'),
        # 'cleaning_machine_base': fields.boolean('Cleaning the machine Base'),
        # 'cleaning_machine_top': fields.boolean('Cleaning the machine top'),
        # 'cleaning_ad_material': fields.boolean('Cleaning the advertisement material (frames and plastic covers)'),
        # 'inspecting_kiosk_lightings': fields.selection([('faulty', 'Faulty'),
        #                                                 ('ok', 'Ok'),
        #                                                 ], 'Inspecting the lightings for the Kiosk/Topper and External Board Lighting for off-site machines where applicable'),

        # 'cleaning_window_glass': fields.boolean('Cleaning the window glass, where applicable'),
        # 'cleaning_floor': fields.boolean('Cleaning the floor'),
        # 'mopping_floor': fields.boolean('Mopping the floor'),
        # 'remove_trash': fields.boolean('Removing the trash and emptying it in the municipality garbage'),

        # 'logo_stickers': fields.selection([('faded', 'Faded'),
        #                                    ('missing', 'Missing'),
        #                                    ('peeloff', 'Peeloff'),
        #                                    ('required', 'Required'),
        #                                    ('replaced', 'Replaced'),
        #                                    ('fine', 'In fine Condition'),
        #                                    ], 'Logo Stickers (model wise)'),

        # 'chk_card_reader': fields.selection([('cleaned', 'Cleaned'),
        #                                      ('faulty',
        #                                       'Faulty, Reported'),
        #                                      ], 'Check Card Reader & report'),

        # 'taking_pics_upon_completion': fields.boolean('Taking picture upon completion'),
        # 'rechecking_all_above_chklist': fields.boolean('Rechecking all the above checklist'),
        # 'surround_side_branding': fields.selection([('required', 'Required'),
        #                                             ('not_required',
        #                                              'Not Required'),
        #                                             ('replaced',
        #                                              'Replaced'),
        #                                             ('n/a', 'N/A'),
        #                                             ], 'Surround side branding (left/ right)'),

        # 'side_frames_posters_kiosk': fields.selection([('required', 'Required'),
        #                                                ('not_required',
        #                                                 'Not Required'),
        #                                                ('replaced',
        #                                                 'Replaced'),
        #                                                ('n/a', 'N/A'),
        #                                                ], 'Side frames/ posters on the kiosk'),

        # 'wall_branding': fields.selection([('required', 'Required'),
        #                                    ('not_required',
        #                                     'Not Required'),
        #                                    ('replaced', 'Replaced'),
        #                                    ('n/a', 'N/A'),
        #                                    ], 'Wall Branding'),


        #''' Branding Audit Check List sheet-3



        # 'cur_longitude': fields.char('Current Longitude'),
        # 'cur_latitude': fields.char('Current Latitude'),
        # 'nxt_survey_distance': fields.integer('Next Survey Distance'),
        # 'nxt_taskid': fields.many2one('atm.surverys.management', 'Next Task ID'),
        # 'visits_done': fields.integer('Visits Done'),
        # 'visits_left': fields.integer('Visits Left'),
        # 'total_visits': fields.integer('Total Visits'),

        # 'image_medium': fields.function(_get_image, fnct_inv=_set_image,
        # 	string="Medium-sized image", type="binary", multi="_get_image",
        # 	store={
        # 		'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_front'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_side'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_back'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_front'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_side'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_back'], 10),
        # 	},
        # 	help="Medium-sized image of this contact. It is automatically "
        # 		 "resized as a 128x128px image, with aspect ratio preserved. "
        # 		 "Use this field in form views or some kanban views."),
        # 'image_small': fields.function(_get_image, fnct_inv=_set_image,
        # 			string="Small-sized image", type="binary", multi="_get_image",
        # 			store={
        # 			'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_front'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_side'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['bfr_img_back'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_front'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_side'], 10),
        # 	'survey.info': (lambda self, cr, uid, ids, c={}: ids, ['after_img_back'], 10),
        # 		 },
        # 		 help="Small-sized image of this contact. It is automatically "
        # 			 "resized as a 64x64px image, with aspect ratio preserved. "
        # 			"Use this field anywhere a small image is required."),
        # 	'has_image': fields.function(_has_image, type="boolean"),

        # 'file': fields.function(_get_image,
        #                               fnct_inv=_set_image,
        #                               type="binary",
        #                               string="File",
        #                               filters='*.jpeg,*.jpeg,*.gif'),

        # 'status': fields.selection([
        #     ('waiting_approval', 'Waiting for Approval'),
        #     ('approved', 'Approved')], 'Status'),

        # 'is_nbad': fields.function(_check_customer, type='boolean', string='Is NBAD', method=True, store=False, multi=False),

		'check_list6':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Insert Cash'),
		'check_list7':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Network Sticker'),
		'check_list8':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Instruction Sticker'),
		'check_list9':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Vault Branding'),
		'check_list10':fields.selection([('required','Required'),
			('damaged','Damaged'),
			('replaced','Replaced')],'Terminal ID'),
		'check_list17':fields.selection([('off','Off'),
			('missing','Missing'),
			('replaced','Replaced')],'Spot Lights'),
		'check_list19':fields.selection([
			('damaged','Damaged')],'Machine Surround Branding'),
		'check_list20':fields.selection([
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
		'bfr_img_front': fields.binary('Front View'),
        'bfr_img_side': fields.binary('Side View'),
        'bfr_img_back': fields.binary('Back View'),
        'after_img_front': fields.binary('Front View After'),
        'after_img_side': fields.binary('Side View After'),
        'after_img_back': fields.binary('Back View After'),

        'bfr_img_front2': fields.binary('Front View 2'),
        'bfr_img_side2': fields.binary('Side View 2'),
        'bfr_img_back2': fields.binary('Back View 2'),
        'after_img_front2': fields.binary('Front View After 2'),
        'after_img_side2': fields.binary('Side View After 2'),
        'after_img_back2': fields.binary('Back View After 2'),


        'bfr_img_front3': fields.binary('Front View 3'),
        'bfr_img_side3': fields.binary('Front View Side 3'),
        'after_img_front3': fields.binary('Front View After 3'),
        'after_img_side3': fields.binary('Side View After 3'),


		}

	_order = "visit_tm"

	_defaults={

		'status': 'waiting_approval',
		'visit_tm': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),

		}

	def onchange_taskid(self, cr, uid, ids, surv_task, context=None):
		res = {'value': {}}
		if surv_task:
			part = self.pool.get('atm.surverys.management').browse(
				cr, uid, surv_task, context)
			# print part.atm.id
			res['value'].update({'month': part.task_month})
			res['value'].update({'atm_surv': part.atm.id})
			res['value'].update({'surveyor_surv': part.surveyor.id})


			res['value'].update({'customer_surv': part.customer.id})
			res['value'].update({'visit_tm': part.visit_time})
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
		atm = self.pool.get('atm.info').browse(cr, uid, atm_id).atm_id

		dir_name = '/var/www/html/ERP/%s/%s/%s' % (
			str(month), str(customer), str(atm))

		return dir_name

	def __write_image_file(self, cr, uid, imgdata1, vals, counter, context=None):

		file_loc = self.__create_dir(
			cr, uid, vals['customer_surv'], vals['atm_surv'], vals['month'], context=None)

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
			cr, uid, 'atm', 'view_atm_surveys_management_form')[1]

		res = {
			'type': 'ir.actions.act_window',
			'name': 'Test',
			'view_type': 'form',
			'view_mode': 'form,tree',
			'res_model': 'atm.surverys.management',
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
			'model': 'survey.info',
			'ids': survey_ids,
			'form': self.read(cr, uid, survey_ids, context=context),
		}
		return {'type': 'ir.actions.report.xml', 'report_name': 'survey.info', 'datas': datas, 'nodestroy': True}



	def status_approve(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'approved'},context=context)
		return True 

	def write(self, cr, uid, ids, vals, context=None):
		return super(survey_details_info, self).write(cr, uid, ids, vals, context)

	# def create(self, cr, uid, vals, context=None):
 #   		vals['name']= self.pool.get('ir.sequence').get(cr, uid, 'survey.det')
 #   		return super(Survey_Details, self).create(cr, uid, vals, context=context)

	def create(self, cr, uid, vals, context=None):

		if vals.get('name', '/') == '/':
			vals['name'] = self.pool.get('ir.sequence').get(
				cr, uid, 'survey.info') or '/'

		vals['visit_tm'] = datetime.datetime.now()
		s_ids = self.search(cr, uid, [('month', '=', vals['month']), ('atm_surv', '=', vals[
							'atm_surv']), ('surv_task', '=', vals['surv_task'])], context=None)

		if s_ids:
			self.unlink(cr, uid, s_ids, context=None)

		survey_id = super(survey_details_info, self).create(
			cr, uid, vals, context=context)

		values = {}

		part = self.pool.get('atm.surverys.management').browse(
			cr, uid, vals['surv_task'], context)

		self.pool.get('atm.surverys.management').write(cr, uid, vals['surv_task'], {'status': 'done'}, context)


		approve_surveys = self.status_approve(cr,uid,survey_id,context=None)
		values.update({'state': part.state.id})

		if vals['cur_longitude'] and vals['cur_latitude']:
			self.pool.get('atm.info').write(cr, uid, vals['atm_surv'], {
				'latitude': vals['cur_latitude'], 'longitude': vals['cur_longitude']})

		self.write(cr, uid, survey_id, values)
		return survey_id  

	

	def print_survey(self, cr, uid, ids, context=None):
		'''
		This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
		'''
		assert len(ids) == 1, 'This option should only be used for a single id at a time'
		self.signal_workflow(cr, uid, ids, 'quotation_sent')
		return self.pool['report'].get_action(cr, uid, ids, 'atm.print_survey', context=context)
	 
	


	def create(self, cr, uid, vals, context=None):
		if vals.get('name','/')=='/':
			vals['name']=self.pool.get('ir.sequence').get(cr, uid, 'survey.info') or '/'
		return super(survey_details_info,self).create(cr, uid, vals, context=context)

survey_details_info()


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

# 	_inherit = 'survey.info'

# 	_columns = {

# 		'bfr_img_front_r': fields.function(image1_bfr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'bfr_img_side_r': fields.function(image3_bfr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'bfr_img_back_r': fields.function(image2_bfr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'after_img_side_r': fields.function(image8_afr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'after_img_front_r': fields.function(image6_afr, type='binary', string='Image', method=True, store=False, multi=False),
# 		'after_img_back_r': fields.function(image7_afr, type='binary', string='Image', method=True, store=False, multi=False),

# 	}
# images_calss()
