# -*- coding: utf-8 -*-
##############################################################################
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

{
    'name' : 'doctor_hc_odontologia',
    'version' : '1.0',
    'summary': 'Modulo de historia clinica para odontologia.',
    'description': """
Historia Clinica Para Odontologia. 
=================================================================

""",
    'category' : '',
    'author' : 'PROYECTO EVOLUZION',
    'website': 'http://www.proyectoevoluzion.com/',
    'license': 'AGPL-3',
    'depends' : ['doctor', 'knowledge', 'account_voucher', 'l10n_co_doctor'],
    'data' : [
        'security/ir.model.access.csv',
        'views/inherit_doctor_view.xml',
        'views/doctor_co_prescripcion_medica.xml',
        'views/doctor_hc_odontologia_diente_view.xml',
        'views/doctor_patient_inherit_view.xml',
        'data/doctor_hc_odontologia_diente_data.xml',
        'data/tipocita_odontologica.sql'
    ],
    'installable': True,
    'qweb': ['static/src/xml/custom_access_login.xml'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
