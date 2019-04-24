#!/usr/bin/python3

import requests
from json import dumps
import sys
import argparse
import time
from forex_python.converter import CurrencyCodes

#Python program to get the real-time
# currency exchange rate

class Converter():


    def CliParser(self):
        self._args = argparse.ArgumentParser(prog='Converter', add_help=False)
        self._required = self._args.add_argument_group('Required arguments')
        self._required.add_argument('--amount', help='Amount of currency to convert', required=True, type=float)
        self._required.add_argument('--input_currency', help='Currency to convert', required=True)

        self._optional = self._args.add_argument_group('Optional arguments')
        self._optional.add_argument('-h', '--help', action="help", help='This is help for Currency Converter')
        self._optional.add_argument('--output_currency', help='To which currency you want to convert, when none is given all known currencies are printed')

        parsed_args = vars(self._args.parse_args())

        return parsed_args
    # Function to get real time currency exchange


    def RealTimeConvert(self, input_currency, output_currency, amount):


        codeses = ["AED", "AFN", "ALL", "AMD", "ANG", "ARS", "AUD", "AWG",
                "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD",
                "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BZD", "CAD",
                "CDF", "CHF", "CLF", "CLP", "CNH", "CNY", "COP", "CUP",
                "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN",
                "ETB", "EUR", "FJD", "FKP", "GBP", "GEL", "GHS", "GIP",
                "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG",
                "HUF", "IDR", "ILS", "INR", "IQD", "IRR", "ISK", "JEP",
                "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "LKR",
                "KPW", "KRW", "KWD", "KYD", "KZT", "LAK", "LBP", "LRD",
                "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT",
                "MOP", "MRO", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR",
                "MZN", "NAD", "NGN", "NOK", "NPR", "NZD", "OMR", "PAB",
                "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON",
                "RSD", "RUB", "RUR", "RWF", "SAR", "SBD", "SCR", "SDG",
                "SEK", "SGD", "SHP", "SLL", "SOS", "SRD", "SYP", "SZL",
                "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TWD",
                "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VND", "VUV",
                "WST", "XAF", "XAG", "XCD", "XDR", "XOF", "XPF", "YER",
                "ZAR", "ZMW", "ZWL"]



        codes = ["CZK", "EUR", "USD", "CNY"]

        symbol = dict()
        listOfKeys = list()
        c = CurrencyCodes()
        #print(c)
        for code in codeses:
            symbol[code] = c.get_symbol(code)

        bool = True
        self.input_currency = input_currency.upper()
        self.output_currency = output_currency
        self.amount = amount
        c = Converter()
        array = dict()


        for k, v in symbol.items():
            if self.input_currency == v:
                self.input_currency = k

        if self.input_currency not in codeses:
            print("This is invalid input currency, please try it again")
            sys.exit(-1)

        if self.output_currency is None:
            bool = False
            #for code in codeses:
            for code in codes:
                output = code
                page = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
                # main_url variable store complete url
                main_url = page + "&from_currency=" + self.input_currency + "&to_currency=" + output + "&apikey=ZTXBPQH814OH3060"
                req_ob = requests.get(main_url)
                result = req_ob.json()
                if "Note" in result:
                    message = result["Note"]
                    print("\n" + message + "\n")
                    sys.exit(-1)
                # parsing the required information
                Exchange_Rate = float(result["Realtime Currency Exchange Rate"]
                                                          ['5. Exchange Rate'])
                # calculation for the conversion
                new_amount = str(round(self.amount * Exchange_Rate, 2))
                array[code] = new_amount
                #time.sleep(12)

            result = dict()
            result['input'] = {'amount' : self.amount, 'currency': self.input_currency}
            result['output'] = {}
            result['output'] = array
            return result



        elif self.output_currency.upper() not in codeses:
            print("This is invalid output currency, please try it again")
            sys.exit()


        if bool == True:
            output = self.output_currency.upper()
            page = r"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
            # main_url variable store complete url
            main_url = page + "&from_currency=" + self.input_currency + "&to_currency=" + output + "&apikey=ZTXBPQH814OH3060"
            req_ob = requests.get(main_url)
            result = req_ob.json()
            if "Note" in result:
                message = result["Note"]
                print("\n" + message + "\n")
                sys.exit(-1)
            # parsing the required information
            Exchange_Rate = float(result["Realtime Currency Exchange Rate"]
                                                      ['5. Exchange Rate'])
            # calculation for the conversion
            new_amount = str(round(self.amount * Exchange_Rate, 2))
            result = dict()
            result['input'] = {'amount' : self.amount, 'currency': self.input_currency}
            result['output'] = {self.output_currency : new_amount}
            return result


# Driver code
if __name__ == "__main__" :

    convert = Converter()
    args = convert.CliParser()
    json = convert.RealTimeConvert(args['input_currency'], args['output_currency'], args['amount'])
    print(dumps(json, indent=4))
