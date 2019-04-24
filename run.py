from flask import Flask, request, jsonify
from currency_converter import Converter


app = Flask(__name__)
app.config["DEBUG"] = True
c = Converter()

@app.route('/currency_converter', methods=["GET"])

def API():
    args = dict()
    if request.method =='GET':
        args['input'] = request.args.get("input_currency", type=str)
        args['output'] = request.args.get("output_currency", type=str)
        args['amount'] = request.args.get("amount", type=float)

        if args['amount'] is None:
            response = jsonify({"error": "amount not entered"})
            response.status_code = 400
            return response

        if args['input'] is None:
            response = jsonify({"error": "input currency not entered"})
            response.status_code = 400
            return response

        result = c.RealTimeConvert(args['input'], args['output'], args['amount'])
        return jsonify(result)

    else:
        response = jsonify({"error": "wrong http method"})
        response.status_code = 405
        return response


if __name__ == '__main__':
    app.run()
