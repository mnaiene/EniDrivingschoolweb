from flask import Flask, request, jsonify
from portalsdk import APIContext, APIMethodType, APIRequest
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin for frontend

@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    msisdn = data.get("msisdn")
    amount = data.get("amount")

    api_context = APIContext()
    api_context.api_key = 'p1ftma1jvwwzybyvk54ua312r10mmjea'
    api_context.public_key = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAmptSWqV7cGUUJJhUBxsMLonux24u+FoTlrb+4Kgc6092JIszmI1QUoMohaDDXSVueXx6IXwYGsjjWY32HGXj1iQhkALXfObJ4DqXn5h6E8y5/xQYNAyd5bpN5Z8r892B6toGzZQVB7qtebH4apDjmvTi5FGZVjVYxalyyQkj4uQbbRQjgCkubSi45Xl4CGtLqZztsKssWz3mcKncgTnq3DHGYYEYiKq0xIj100LGbnvNz20Sgqmw/cH+Bua4GJsWYLEqf/h/yiMgiBbxFxsnwZl0im5vXDlwKPw+QnO2fscDhxZFAwV06bgG0oEoWm9FnjMsfvwm0rUNYFlZ+TOtCEhmhtFp+Tsx9jPCuOd5h2emGdSKD8A6jtwhNa7oQ8RtLEEqwAn44orENa1ibOkxMiiiFpmmJkwgZPOG/zMCjXIrrhDWTDUOZaPx/lEQoInJoE2i43VN/HTGCCw8dKQAwg0jsEXau5ixD0GUothqvuX3B9taoeoFAIvUPEq35YulprMM7ThdKodSHvhnwKG82dCsodRwY428kg2xM/UjiTENog4B6zzZfPhMxFlOSFX4MnrqkAS+8Jamhy1GgoHkEMrsT5+/ofjCx0HjKbT5NuA2V/lmzgJLl3jIERadLzuTYnKGWxVJcGLkWXlEPYLbiaKzbJb2sYxt+Kt5OxQqC1MCAwEAAQ=='
    api_context.ssl = True
    api_context.method_type = APIMethodType.POST
    api_context.address = 'api.sandbox.vm.co.mz'
    api_context.port = 18352
    api_context.path = '/ipg/v1x/c2bPayment/singleStage/'
    
    api_context.add_header('Origin', '*')
    api_context.add_parameter('input_TransactionReference', 'TX12345ENI')
    api_context.add_parameter('input_CustomerMSISDN', msisdn)
    api_context.add_parameter('input_Amount', amount)
    api_context.add_parameter('input_ThirdPartyReference', '1J3MPE')
    api_context.add_parameter('input_ServiceProviderCode', '171717')

    api_request = APIRequest(api_context)
    result = api_request.execute()

    return jsonify({
        "status": result.status_code,
        "response": result.body
    })

if __name__ == '__main__':
    app.run(port=4242)