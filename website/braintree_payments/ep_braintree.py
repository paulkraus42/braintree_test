import logging
from decimal import Decimal
import braintree
from flask import Blueprint, current_app, jsonify
# from flask_jwt_extended import current_user, jwt_optional, get_jwt_identity

from flask_restful import Api, Resource, abort, current_app, reqparse
from nameko.standalone.rpc import ClusterRpcProxy
import uuid

braintree_bp = Blueprint('braintree_bp', __name__)
api = Api(braintree_bp)

class CreateTransactionError(Exception):
    def __init__(self, message):
        self.message = message

class ErrorProcessingCard(Exception):
    def __init__(self, message):
        self.message = message

class Braintree(object):
    def __init__(self, nonce=None):
        if current_app.config['CONFIG_STATE'] in  ['development', 'localdev']:
            self.gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    braintree.Environment.Sandbox,
                    merchant_id=current_app.config['BRAINTREE_MERCHANT_ID'],
                    public_key=current_app.config['BRAINTREE_API_KEY_PUB'],
                    private_key=current_app.config['BRAINTREE_API_KEY_PRIV'],
                )
            )
        else:
            self.gateway = braintree.BraintreeGateway(
                braintree.Configuration(
                    braintree.Environment.Production,
                    merchant_id=current_app.config['BRAINTREE_MERCHANT_ID'],
                    public_key=current_app.config['BRAINTREE_API_KEY_PUB'],
                    private_key=current_app.config['BRAINTREE_API_KEY_PRIV'],
                )
            )
        self.rabbit_config = {'AMQP_URI': "pyamqp://guest:guest@rabbitmq"}
        self.nonce = nonce

    def _update_customer(self, customer_payload):
        customer_id = customer_payload['customer_id']
        del customer_payload['customer_id']
        self.gateway.customer.update(customer_id, customer_payload)

    def _update_payment(self, payment_payload):
        result = self.gateway.payment_method.create({
            'customer_id': payment_payload['customer_id'],
            'payment_method_nonce': payment_payload['payment_method_nonce']
        })
        return result.payment_method.token

    def update_customer(self, customer_payload, payment_payload):
        self._update_customer(customer_payload=customer_payload)
        token = self._update_payment(payment_payload=payment_payload)
        return token

    def create_customer(self, payload):
        with ClusterRpcProxy(self.rabbit_config) as cluster_rpc:
            return cluster_rpc.customer_services.create_customer(payload)

    def get_client_token(self, customer_id):
        if customer_id is not None:
            try:
                resp = self.gateway.client_token.generate({'customer_id': customer_id})
            except ValueError:
                self.gateway.customer.create({'id': customer_id})
                # self.create_customer({'id': customer_id})
                resp = self.gateway.client_token.generate({'customer_id': customer_id})
        else:
            resp = self.gateway.client_token.generate()
        logging.debug(resp)
        print(resp)
        return resp


class EPGetClientToken(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'customerId', 
            type=str, 
            required=True, 
            help='PaymentMethodNonce not in request body'
        )
        args = parser.parse_args()
        customer_id = args.get('customerId')
        bt = Braintree()
        token = bt.get_client_token(customer_id=customer_id)
        return jsonify({'clientToken': token, 'customer_id': customer_id})


class EPVaultCustomer(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'payload', type=dict, required=True, help='PaymentMethodNonce not in request body'
        )
        args = parser.parse_args()
        payload = args.get('payload')
        customer_id = payload['customer_id']
        payment_payload = {
            'customer_id': customer_id,
            'payment_method_nonce': payload['payment_method_nonce'],
            'street_address': payload['street_address'],
            'postal_code': payload['postal_code']
        }
        customer_payload = {
            'customer_id': customer_id,
            'first_name': payload['first_name'],
            'last_name': payload['last_name'],
        }
        bt = Braintree()
        token = bt.update_customer(
            customer_payload=customer_payload, payment_payload=payment_payload
        )
        logging.debug(token)
        return jsonify({'payment_token': token})
        
api.add_resource(EPGetClientToken, '/bt/get_client_token')
api.add_resource(EPVaultCustomer, '/bt/vault_customer')
