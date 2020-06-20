import re

# TODO REVIEW THIS https://stackoverflow.com/questions/6259443/how-to-match-a-line-not-containing-a-word

date_regex = re.compile(r'^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$' # match mm/dd/yyyy
                        r'|'
                        r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$' # match dd-mm-yyyy
                        r'|'
                        r'^([^\s]+) (\d{2}),? ?(\d{4})$' # match Month D, Yr (i.e. February 17, 2009 or February 17,2009)
                        r'|'
                        r'^\d{4}$' # match year (i.e. 2011)
                        r'|'
                        'Fiscal\d{4}'
                        r'|'
                        r'^Change$'
                        r'|'
                        r'(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})')

balance_sheet_regex = r'(balance ?sheet|condition)'
cash_flow_statement_regex = r'(Consolidated(.*?)cash flow)|(cash( ?)flow(s?) statement(s?))'
income_statement_regex = r'(Consolidated(.*?)statements of earnings)|(Income Statement)'

cash_flow_investing_activities = {

    # Plant, Property, and Equipment
    'Payments to Acquire Productive Assets': r'Capital expenditures – excluding equipment leased to others',
    'Payments to Acquire Equipment on Lease': r'Expenditures for equipment leased to others',
    'Payments to Acquire Property, Plant, and Equipment': r'(Purchase(s?) of property[ ?](, leasehold improvements )?and equipment)'
                                                                     r'|'
                                                                     r'(Payments for acquisition of property, plant and equipment)',
    'Proceeds from Sale of Property, Plant, and Equipment': r'Proceeds from disposals of leased assets and property, plant and equipment',

    # Loans and Leases
    # 'Issuance Short Term Loans To Subsidiaries Net': r'',
    'Payments for (Proceeds from) Loans and Leases': r'Loans, net \(excluding loans held for sale\)',

    # Business Acquisitions
    'Payments to Acquire Businesses, Net of Cash Acquired': r'(Investments and acquisitions \(net of cash acquired\))'
                                                                       r'|'
                                                                       r'Payments made in connection with business acquisitions, net',
    'Proceeds from divestiture of businesses net of cash divested': r'Proceeds from sale of businesses and investments \(net of cash sold\)',

    # Finance Receivables
    'Payments to acquire finance receivables': r'Additions to finance receivables',
    'Proceeds from collection of finance receivables': r'Collections of finance receivables',
    'Proceeds from sale of finance receivables': r'Proceeds from sale of finance receivables',

    # Marketable Securities
    'Marketable Securities': {
        'Payments to Acquire Marketable Securities': r'(Purchases of|Investments in)( marketable?) securities',
        'Proceeds from sale and maturity of marketable securities': {
            'Proceeds from Sale of Debt Securities, Available-for-sale': r'(Proceeds from )?sale(s?) of( marketable?) securities',
            'Proceeds from Maturities, Prepayments and Calls of Debt Securities, Available-for-sale': r'(Proceeds from )?Maturities of marketable securities',
        }
    },

    # Investments
    'Proceeds from Sale of Investment Projects': r'Purchase of investments',
    'Payments to Acquire Investments': r'Proceeds from sales and paydowns of investments',

    # Other
    # 'Payments to Acquire Other Investments': r'',
    # 'Proceeds from Sale and Maturity of Other Investments': r'',

    'Payments for (Proceeds from) Other Investing Activities': r'Other( – net)?',
    'Net Cash Provided by (Used in) Investing Activities': r'(Net cash provided by \(used for\) investing activities) |'
                                                                      r'(Cash generated by/\(used in\) investing activities)'
}

cash_flow_operating_activities = {
    'Net Income (Loss)': r'(Net Earnings)|(Profit \(loss\) of consolidated and affiliated companies)',
    'Adjustments for non-cash items': {
        'Depreciation, Depletion and Amortization, Nonproduction': r'Depreciation and amortization',
        'DefinedBenefitPlanActuarialGainLoss': r'Actuarial \(gain\) loss on pension and postretirement benefits',
        'Deferred Income Tax Expense (Benefit)': r'(Provision \(benefit\) for )?deferred income taxes',
        'Share-based Compensation': r'Share-based compensation',
        'Gain (Loss) on Extinguishment of Debt': r'Gain related to extinguishment of unsecured borrowings',
        'Provision for Loan, Lease, and Other Losses': r'Provision for credit losses',
        'OtherNoncashIncomeExpense': r'Other'
    },
    'Changes in assets, net of acquisitions and diverstitures': {
        'Increase (Decrease) in Receivables': r'Receivables',
        'Increase (Decrease) in Inventories': r'Inventories',
        'Increase (Decrease) in Other Operating Assets': r'Other assets – net',
    },
    'Changes in liabilities, net of acquisitions and diverstitures': {
        'Increase (Decrease) in Accounts Payable': r'Accounts payable',
        'Increase (Decrease) in Accrued Liabilities': r'Accrued expenses',
        'Increase (Decrease) in Employee Related Liabilities': r'Accrued wages, salaries and employee benefits',
        'Increase (Decrease) in Customer Advances': r'Customer advances',
        'Increase (Decrease) in Other Operating Liabilities': r'Other liabilities – net'
    },
    'Net Cash Provided by (Used in) Operating Activities': r'Net cash provided by \(used for\) operating activities',

}

cash_flow_financing_activities = {

}

financial_entries_regex_dict = {
    'Balance Sheet': {
        'Assets': {
            'Current Assets': {
                'Cash and Short Term Investments': {

                    'Cash and Cash Equivalents': {
                        'Cash and Due from Banks': r'(?=.*cash)(?=.*due from banks)',
                        'Interest-bearing Deposits in Banks and Other Financial Institutions': r'(?=.*interest[- ]bearing deposits)',
                        'Restricted Cash': r'(?=.*cash)(?=.*restricted)',
                        'Other Cash and Cash Equivalents': r'(?!(?=.*cash)(?=.*due from banks))'
                                                           r'(?!(?=.*interest[- ]bearing deposits))'
                                                           r'(?!(?=.*cash)(?=.*restricted))'
                                                            # it means if pattern's name is cash and cash equivalents (the underscore and $ constrain that)
                                                           # do not include it in 'others'
                                                           r'(?!.*marketable securities)(?=.*_cash and cash equivalents$)(?!.*marketable securities)',
                        'Cash and Cash Equivalents': r'(?!.*marketable securities)(?=.*cash and cash equivalents)(?!.*marketable securities)',
                    },

                    'Marketable Securities Current': r'(?!.*non-current)(?=.*(current|short-term))(?=.*(marketable securities|investments))',
                    'Cash and Short Term Investments': r'(?=.*cash)(?=.*(marketable securities|short-term investments))'
                },
                'Accounts Receivable': {
                    'Gross Accounts Receivable': r'$^', # TODO
                    'Allowances for Doubtful Accounts': r'(?=.*Receivable)(?=.*allowances of \$(\d+))',
                    'Other Receivables': r'(?!(?=.*Receivable)(?=.*allowances of \$(\d+)))'
                                         r'(?!(?=.*Receivable)(?=.*net))'
                                         r'(?=.*Receivable)'
                                         r'(?!(?=.*Receivable)(?=.*allowances of \$(\d+)))'
                                         r'(?!(?=.*Receivable)(?=.*net))',
                    'Net Accounts Receivable': r'(?=.*Receivable)(?=.*(allowances|net))',
                },
                'Prepaid Expense, Current': r'Prepaid expenses',
                'Inventory, Net': r'(?=.*Inventor(y|ies))',
                'Income Taxes Receivable, Current': r'Income taxes receivable',
                'Assets Held-for-sale': r'Assets Held[- ]for[- ]sale',
                # taxes that have been already paid despite not yet having been incurred
                'Deferred Tax Assets, Current': r'(?=.*(Deferred tax(es)? (assets)|(on income))|(Prepaid taxes))',

                'Other Assets, Current': r'(?!.*non[- ]?current)(?=.*other)(?=.*assets)',
                'Total Assets, Current': r'(?!.*non[- ]?current)(?=.*total)(?=.*assets)',
            },
            'Non Current Assets': {

                'Marketable Securities Non Current': r'^(?!.*short-term)((?!.*current)|(?=.*non[- ]?current))(?=.*marketable securities|investments)',

                'Property, Plant and Equipment': {
                    'Gross Property, Plant and Equipment': r'(?=.*Property)(?=.*(Plant|Land))(?=.*Equipment)(?=.*Gross)',
                    'Accumulated Depreciation and Amortization': r'(?=.*Depreciation)(?=.*Amortization)',
                    'Property, Plant and Equipment, Net': r'(?=.*Property)(?=.*(Plant|Land))(?=.*Equipment)(?=.*Net)',
                },
                'Operating Lease Right-of-use Assets': r'Operating lease right-of-use assets',
                'Deferred Tax Assets Non Current': r'(?=.*non[- ]?current)(?=.*deferred tax assets)',
                'Intangible Assets': {
                    'Goodwill': r'(?!.*net)(?=.*Goodwill)(?!.*net)',
                    'Intangible Assets, Net (Excluding Goodwill)': r'(?=.*(other|net))(?=.*intangible assets)',
                    'Total Intangible Assets': r'(?!.*other)(?!.*goodwill)(?!.*net)(?=.*intangible assets)(?!.*goodwill)(?!.*other)(?!.*net)',
                },
                'Other Non Current Assets': r'((?=.*non[- ]?current)|(?!.*current))(?=.*other)(?=.*assets)', # the space before current is on purpose
                'Total Non Current Assets': r'((?=.*non[- ]?current)|(?!.*current))(?=.*total)(?=.*assets)',
            },
            'Total Assets': r'(?!.*non[- ]?current)(?!.*current)(?=.*total assets)(?!.*non[- ]?current)(?!.*current)'
        },
        'Liabilities and Shareholders\' Equity': {
            'Liabilities': {
                'Current Liabilities': {
                    'Short-Term Debt': r'(?=.*(Commercial Paper|Current Debt))',
                    'Long-term Debt, Current Maturities': r'(?=.*(Long-)?Term Debt|Loans and notes payable)',
                    'Accounts Payable, Current': r'(?=.*Accounts Payable)(?!(?=.*non-?current))',
                    'Accounts Payable, Trade, Current': r'(?=.*Partners Payable)',
                    'Operating Lease, Liability, Current': r'(?=.*Operating lease liabilities, current)',
                    'Current Deferred Revenues': r'(?=.*(Deferred Revenue)|(Short-term unearned revenue))',
                    'Employee-related Liabilities, Current': r'(?=.*Accrued Compensation)',
                    'Accrued Income Taxes': r'Accrued(?=.*Income)(?=.*Taxes)',
                    'Accrued Liabilities, Current': r'(?=.*Accrued)(?=.*(Expense|Liabilities))',
                    'Income Taxes Payable': r'(?=.*Income taxes payable)|(?=.*Short-term Income taxes)',
                    'Other Current Liabilities': r'(?!non-?current)(?=.*other)(?=.*liabilities)(?!.*non-?current)',
                    'Total Current Liabilities': r'(?=.*Total Current Liabilities)',
                },
                'Non Current Liabilities': {
                    'Deferred Tax Liabilities': r'(Deferred(?=.*Income)(?=.*Taxes))|(Deferred tax liabilities)',
                    # this debt is due after one year in contrast to current maturities which are due within this year
                    'Long-term Debt, Noncurrent Maturities': r'Long-term debt(?!.*?within)',
                    'Operating Lease, Liability, Noncurrent': r'(Operating lease liabilities(?!.*? current))',
                    'Liability, Defined Benefit Plan, Noncurrent': r'Employee related obligations',
                    'Accrued Income Taxes, Noncurrent': r'(Long-term ((income taxes)|(taxes payable)))',
                    'Deferred Revenue, Noncurrent': r'Deferred revenue(.*?)non-?current',
                    'Long-Term Unearned Revenue': r'(Long-term unearned revenue)',
                    'Other Liabilities, Noncurrent': r'(?=.*other)(?=.*liabilities)(?!.*[a-zA-Z]current)',
                    'Total Long-Term Liabilities': r'(?=.*Non-current liabilities)' # total liabilities - total current liabilities
                },
                'Total Liabilities': r'(?=.*Total Liabilities)(?!.*Equity$)'
            },
            'Shareholders\' Equity': {
                'Preferred Stock, Value, Issued': r'Preferred stock(?!.*treasury)',
                'Common Stock and Additional Paid in Capital': {
                    'Common Stock, Value, Issued': r'(?=.*Common stock)(?!.*treasury)(?!.*additional paid[- ]in capital)',
                    'Additional Paid in Capital': r'(?!.*Common stock)(?=.*additional paid[- ]in capital)',
                    'Common Stocks, Including Additional Paid in Capital': r'(?=.*Common stock and additional paid[- ]in capital)'
                },

                'Treasury Stock, Value': r'Treasury stock',
                'Retained Earnings (Accumulated Deficit)': r'(?=.*Accumulated deficit)|(Retained earnings)',
                'Accumulated Other Comprehensive Income': r'(?=.*Accumulated other comprehensive income)',
                'Deferred Stock Compensation': r'(?=.*Deferred stock compensation)',
                'Minority Interest': r'(?=.*Noncontrolling interests)',
                'Stockholders\' Equity Attributable to Parent': r'(?=.*Total shareholders[’\'] equity)',
            },
            'Total Liabilities and Shareholders\' Equity': r'(?=.*Total Liabilities)(?=.*Equity)'
        },
    },
    'Income Statement': {
        'Revenues': {
            'Net Sales': r'((Net|Product) sales)|(Revenue)',
            'Gross Margin': r'Gross margin'
        },
        'Cost of Goods and Services Sold': r'Cost of (goods sold|sales|revenue)',
        'Operating Expenses': {
            'Research and Development': r'Research and development',
            'Selling, General and Administrative': {
                'Sales and Marketing': r'Sales and Marketing',
                'General and Administrative': r'General and Administrative',
                'Selling, General and Administrative': r'Selling, general and administrative',
            },
            'Total Operating Expenses': r'Total operating expenses'
        },
        'Operating Income (Loss) / EBIT': r'Operating income',
        # 'Non-Operating Income (Expenses)': r'',
        # 'Net Income (Loss)': r'',
        # 'Net Income Loss Attributable to Noncontrolling Interest': r''
    },
    'Cash Flow Statement': {
        'Operating Activities': r'{}(.*?)Operating activities:(.*?)'.format(cash_flow_statement_regex),
        'Investing Activities': r'{}(.*?)Investing activities:(.*?)'.format(cash_flow_statement_regex),
        'Financing Activities': r'{}(.*?)Financing activities:(.*?)'.format(cash_flow_statement_regex),
    }
}
