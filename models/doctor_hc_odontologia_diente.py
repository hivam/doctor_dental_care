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


class diente(osv.osv):
	"""doctor_hc_odontologia_diente"""
	_name = 'doctor.hc.odontologia.diente'

	_columns = {
		'name' : fields.char(u'Número diente', size = 5 ,required =True),
		'descripcion_diente' : fields.char(u'Descripción diente', required=False),
	}

	_sql_constraints = [('numerodiente_constraint', 'unique(numero_diente)', 'El número del diente que intenta crear ya existe en la base de datos.')]

diente()