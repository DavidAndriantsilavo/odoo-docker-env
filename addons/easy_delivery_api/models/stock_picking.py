# -*- coding: utf-8 -*-

import requests
from odoo import models
from werkzeug.urls import url_join

from odoo.exceptions import UserError, ValidationError


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
            'parcels': [
                {
                    'weight': line.product_id.weight,
                    'shipper_reference': self.carrier_id.name,
                    'comment': line.description_picking,
                    'value': line.product_id.lst_price * line.quantity,
                } for line in self.move_ids_without_package
            ],
            'printtype': 'zpl',
        }

        return delivery_params

    def easy_delivery_retrieve_label(self):
        """
        Retrieve the necessary information for printing the shipping label.
        Creates 1 ir.attachment if the response has data['pdf'], or 1 zpl for each data['labels']
        :return:
        """
        self.ensure_one()
        active_config = self.easy_delivery_get_active_config()
        if active_config:
            request_url = url_join(active_config.url, '/api/order')
            request_response = requests.post(request_url, json=self.easy_delivery_get_delivery_data(),
                                             headers=get_request_headers(active_config.auth_token))
            json_response = request_response.json()
            if json_response['status'] == 'success':
                datas = []
                if json_response['data']['pdf']:
                    datas.append({
                        'name': json_response['data']['parcel_ref'] + '.pdf',
                        'datas': json_response['data']['pdf'],
                        'type': 'binary',
                        'mimetype': 'application/pdf',
                        'res_model': 'stock.picking',
                        'res_id': self.id,
                    })
                else:
                    for label in json_response['data']['labels']:
                        datas.append({
                            'name': label['shipper_ref'],
                            'raw': label['zpl'],
                            'res_model': 'stock.picking',
                            'res_id': self.id,
                        })
                self.env['ir.attachment'].create(datas)
            else:
                raise ValidationError(json_response['error']['type'] + ': ' + json_response['error']['message'])
