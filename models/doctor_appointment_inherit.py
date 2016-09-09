# -*- encoding: utf-8 -*-
# #############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)
import base64
import sys, os

class doctor_appointment(osv.osv):
	_name = "doctor.appointment"
	_inherit = "doctor.appointment"

	_columns = {}

	def generate_attentiont(self, cr, uid, ids, context={}):
		doctor_appointment = self.browse(cr, uid, ids, context=context)[0]
		attentiont_id = self.create_attentiont(cr, uid, doctor_appointment, context=context)
		# Update appointment state
		appointment_state = doctor_appointment.state
		if appointment_state != 'invoiced':
			self.write(cr, uid, doctor_appointment.id, {'state': 'attending'}, context=context)
		self.write(cr, uid, doctor_appointment.id, {'attended': True}, context=context)
		# Get appoinment type
		appointment_type = doctor_appointment.type_id.name

		profesional_id = doctor_appointment.schedule_id.professional_id.id

		#GET model of the viewpg 
		data_obj = self.pool.get('ir.model.data')

		

		#condition
		if appointment_type == u'Odontológica':
			result = data_obj._get_id(cr, uid, 'doctor_dental_care', 'view_doctor_hc_odonto_form')
			view_id = data_obj.browse(cr, uid, result).res_id
			context['default_patient_id'] = context.get('patient_id')
			context['default_professional_id'] = profesional_id
			return {
				'type': 'ir.actions.act_window',
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': 'doctor.hc.odontologia',
				'res_id': False,
				'view_id': [view_id] or False,
				'type': 'ir.actions.act_window',
				'context' : context or None,
				'nodestroy': True,
				'target' : 'current',
			}

		else:
			# Get view to show
			result = data_obj._get_id(cr, uid, 'doctor', 'view_doctor_attentions_form')
			view_id = data_obj.browse(cr, uid, result).res_id

			return {
				'view_type': 'form',
				'view_mode': 'form',
				'res_model': 'doctor.attentions',
				'res_id': attentiont_id or False,
				'view_id': [view_id],
				'type': 'ir.actions.act_window',
				'context' : context,
				'nodestroy': True,
				'target' : 'current',
			}
