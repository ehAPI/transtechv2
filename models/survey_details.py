from openerp.osv import fields, osv
import datetime
import time

class survey_details(osv.osv):

	_name = 'survey.details'
	
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
			'out_cont':fields.selection([('yes','Yes'),('no','No')],'OUtdated Contact no.on the Surround'),
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
				('replaced','Replaced')],'Protective Box for Power Circuit'),
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
			'image1_b':fields.binary('image1',filters='*.png,*.gif', widget = 'image'),
			'image2_b':fields.binary('image2',filters='*.png,*.gif', widget = 'image'),
			'image3_b':fields.binary('image3',filters='*.png,*.gif', widget = 'image'),
			'image4_b':fields.binary('image4',filters='*.png,*.gif', widget = 'image'),
			'image5_b':fields.binary('image5',filters='*.png,*.gif', widget = 'image'),
			'image6_b':fields.binary('image6',filters='*.png,*.gif', widget = 'image'),
			'image7_b':fields.binary('image7',filters='*.png,*.gif', widget = 'image'),
			'image8_b':fields.binary('image8',filters='*.png,*.gif', widget = 'image'),
			'image1_a':fields.binary('image1',filters='*.png,*.gif', widget = 'image'),
			'image2_a':fields.binary('image2',filters='*.png,*.gif', widget = 'image'),
			'image3_a':fields.binary('image3',filters='*.png,*.gif', widget = 'image'),
			'image4_a':fields.binary('image4',filters='*.png,*.gif', widget = 'image'),
			'image5_a':fields.binary('image5',filters='*.png,*.gif', widget = 'image'),
			'image6_a':fields.binary('image6',filters='*.png,*.gif', widget = 'image'),
			'image7_a':fields.binary('image7',filters='*.png,*.gif', widget = 'image'),
			'image8_a':fields.binary('image8',filters='*.png,*.gif', widget = 'image'),


		}

	_order = "visit_time desc"

	_defaults={

		'status': 'waiting_approval',
		'visit_time': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),

		}

	def status_approve(self,cr,uid,ids,context=None):
		self.write(cr,uid,ids,{'status':'approved'},context=context)
		return True 

	def write(self, cr, uid, ids, vals, context=None):
		return super(survey_details, self).write(cr, uid, ids, vals, context)

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
		
	# def create(self, cr, uid, vals, context=None):
	# 	if vals.get('name','/')=='/':
	# 		vals['name']=self.pool.get('ir.sequence').get(cr, uid, 'survey.details') or '/'
	# 	return super(survey_details,self).create(cr, uid, vals, context=context)

survey_details()