
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
from datetime import date, datetime, timedelta




class doctor_list_report_odontologia(osv.osv):

	_name= 'doctor.list_report_odontologia'


	_columns = {
		'professional_id': fields.many2one('doctor.professional', 'Doctor'),
		'attentions_odontology_ids': fields.one2many('doctor.hc.odontologia', 'list_report_odontologia_id', 'Attentions'),
		'patient_id': fields.many2one('doctor.patient', 'Paciente', required=True),
		'fecha_inicio':fields.datetime('Inicio Atención'),
		'fecha_fin':fields.datetime('Fin Atención'),
		'especialidad_id':fields.many2one('doctor.speciality', 'Especialidad'),
		'ultimas_citas' :fields.boolean('Ultima Cita'),
	}

	_defaults = {
		'patient_id' : lambda self, cr, uid, context: context.get('default_patient_id', False),
		'professional_id' : lambda self, cr, uid, context: context.get('default_professional_id', False),
		'ultimas_citas' : lambda self, cr, uid, context: context.get('default_ultimas_citas', False),
		#'fecha_fin' : lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
	}	

	#Funcion para cargar la especialidad del profesional en la salud
	def onchange_cargar_especialidad_doctor(self, cr, uid, ids, patient_id, professional_id, date_begin, date_end, context=None):

		if patient_id and professional_id:
			return self.cargar_datos_impresion_atencion(cr, uid, patient_id, professional_id, None, date_begin, date_end, "1", context=context)

		return False

	#Funcion para cargar las atenciones por especialidad
	def onchange_cargar_por_especialidad(self, cr, uid, ids, patient_id, professional_id, especialidad_id, date_begin, date_end, context=None):

		if especialidad_id and patient_id and professional_id:
			return self.cargar_datos_impresion_atencion(cr, uid, patient_id, professional_id, especialidad_id, date_begin, date_end, "1", context=context)

		return False

	#Funcion para cargar las atenciones por fecha inicio y fecha fin
	def onchange_cargar_por_fechas(self, cr, uid, ids, patient_id, professional_id, date_begin, date_end, context=None):

		return False

	def cargar_datos_impresion_atencion(self, cr, uid, patient_id, professional_id, especialidad_id, date_begin, date_end, opcion, context=None):
		atenciones=''
		atenciones_psicologia=''
		nombre_especialidad=''
		fecha_inicial=''
		fecha_final=''
		nombre_especialidad_id=''

		#Almacenamos la fecha en la variable fecha_inicial dependiendo si tiene o no el date_begin
		if date_begin:
			fecha_inicial=date_begin
		else:
			fecha_inicial= "2010-11-30 00:27:09"

		#Almacenamos la fecha en la variable fecha_final dependiendo si tiene o no el date_begin
		if date_end:
			fecha_final=date_end
		else:
			fecha_final= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		#Almacenamos el nombre de la especialidad en la varianle nombre_especialidad dependiendo si ha escogido un doctor o no
		if professional_id:
			nombre_especialidad = self.pool.get('doctor.professional').browse(cr, uid, professional_id ).speciality_id.name
			nombre_especialidad_id= self.pool.get('doctor.professional').browse(cr, uid, professional_id ).speciality_id.id
		else:
			nombre_especialidad = self.pool.get('doctor.speciality').browse(cr, uid, especialidad_id ).name
			nombre_especialidad_id = especialidad_id

		#Opcion donde hay paciente y doctor, como tambien la posible fecha inicial y final
		if opcion == "1":
			_logger.info('Capturando desde cualquier historia')
			atenciones = self.pool.get('doctor.hc.odontologia').search(cr, uid, [('patient_id', '=', patient_id), ('professional_id', '=', professional_id), ('date_attention', '>=', fecha_inicial), ('date_attention', '<=', fecha_final)])
			return {'value': {'attentions_odontology_ids': atenciones, 'especialidad_id': nombre_especialidad_id}}

		return False	



	#Funcion para cargar las ultimas atenciones
	def onchange_cargar_ultimas_atenciones(self, cr, uid, ids, patient_id, professional_id, ultimas_citas, context=None):

		_logger.info('aqui')
		if ultimas_citas:

			atenciones=''
			if patient_id and professional_id:

				atenciones = self.pool.get('doctor.hc.odontologia').search(cr, uid, [('patient_id', '=', patient_id), ('professional_id', '=', professional_id)])
				atenciones_id=[]
				if len(atenciones) > 4:
					for x in range(1, 4):
						_logger.info(atenciones[x])
						atenciones_id.append(atenciones[x])
					return {'value': {'attentions_odontology_ids': atenciones_id}}
				else:
					for x in range(len(atenciones)):
						atenciones_id.append(atenciones[x])
					return {'value': {'attentions_odontology_ids': atenciones_id}}		

		return False


	#Funcion que permite cargar las ultimas tres atenciones que tenga el paciente en el momento.
	def button_cargar_ultimas_atenciones(self, cr, uid, ids, context=None):

		_logger.info('Estamos imprimiendo ultimas tres atenciones: ')
		data = self.read(cr, uid, ids)[0]
		if data['attentions_odontology_ids']:
			return self.export_report_print(cr, uid, ids, 'doctor_attention_odontologia_report')


		return False


	def button_imprimir_algunos_informes(self, cr, uid, ids, context=None):

		data = self.read(cr, uid, ids)[0]

		if data['attentions_odontology_ids']:
			return self.export_report_print(cr, uid, ids, 'doctor_attention_odontologia_report')

		return False
		
	

	def export_report_print(self, cr, uid, ids, name_report, context=None):
		if context is None:
			context = {}
		data = self.read(cr, uid, ids)[0]
		_logger.info('entro')
		_logger.info(data)
		return {
			'type': 'ir.actions.report.xml',
			'report_name': name_report,

		}
	
doctor_list_report_odontologia()