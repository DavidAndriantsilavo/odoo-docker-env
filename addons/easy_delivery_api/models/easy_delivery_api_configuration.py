# -*- coding: utf-8 -*-


from odoo import models, fields, api


class EasyDeliveryApiConfiguration(models.Model):
    _name = 'easy.delivery.api.configuration'
    _description = 'Easy Delivery API Configuration'

    url = fields.Char(string='URL', required=True)
    auth_token = fields.Char(string='Auth Token', required=True)
    active = fields.Boolean(string='Active', default=False)

    _sql_constraints = [('uniq_active', 'unique(active)', "There can only be one active API configuration.")]
