from openerp.osv import fields, osv

class Tasks_status_dashboard(osv.osv):

	_name = 'tasks.status'

	_inherit="tasks.queue"
	_columns={
	'status_id':fields.char('Task ID'),
	}

	def create(self, cr, uid, vals, context=None):
   		vals['status_id']= self.pool.get('ir.sequence').get(cr, uid, 'task.status')
   		return super(Tasks_status_dashboard, self).create(cr, uid, vals, context=context)

Tasks_status_dashboard()