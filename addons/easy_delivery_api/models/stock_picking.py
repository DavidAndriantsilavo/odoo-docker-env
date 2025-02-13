# -*- coding: utf-8 -*-

import requests
from werkzeug.urls import url_join

from odoo import models


def get_request_headers(auth_token):
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}',
        'Cache-Control': 'no-cache',
    }


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def easy_delivery_get_active_config(self):
        return self.env['easy.delivery.api.configuration'].search([], limit=1)

    def easy_delivery_get_delivery_data(self):
        company_partner = self.env.company.partner_id
        partner = self.partner_id
        delivery_params = {
            'shipper': {
                'name': company_partner.name,
                'street': company_partner.contact_address,
                'country': company_partner.country_id.code,
                'postal_code': company_partner.zip or '-',
                'city': company_partner.city,
                'tel': company_partner.phone,
                'email': company_partner.email,
            },
            'recipient': {
                'name': partner.name,
                'street': partner.contact_address,
                'country': partner.country_id.code,
                'postal_code': partner.zip,
                'city': partner.city,
                'tel': partner.phone,
                'email': partner.email,
            },
            'parcels': [],
            'printtype': 'zpl',
        }

        return delivery_params

    def easy_delivery_retrieve_label(self):
        """
        Retrieve the necessary information for printing the shipping label
        :return:
        """
        self.ensure_one()
        active_config = self.easy_delivery_get_active_config()
        if active_config:
            request_url = url_join(active_config.url, '/api/order')
            request_response = requests.post(request_url, json=self.easy_delivery_get_delivery_data(),
                                             headers=get_request_headers(active_config.auth_token))
            json_response = request_response.json()
