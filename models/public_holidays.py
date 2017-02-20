from openerp.osv import fields, osv

class public_holidays(osv.osv):
	_name = 'public.holidays'
	_rec_name = 'cal_year'
	_description = 'Public Holidays'
	_columns = {
	'cal_year' : fields.char('Calendar Year', required=True),
	'public_holiday' : fields.one2many('public.holiday.days','dn','Public Holidays'),
	}

public_holidays()

class public_holiday_days(osv.osv):
	_name = 'public.holiday.days'
	_columns = {
	'dn' : fields.integer('Day', required= True),
	'date' : fields.date('Date', required= True),
	'name' : fields.char('Name', required= True),
	'date_may_change' : fields.boolean('Date May Change'),
	}