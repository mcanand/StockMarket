from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

import yfinance as yf


class StockTickers(models.Model):
    _name = 'stock.ticker'

    name = fields.Char()
    ticker_symbol = fields.Char()
    address1 = fields.Char()
    address2 = fields.Char()
    city = fields.Char()
    zip = fields.Char()
    phone = fields.Char()
    country_id = fields.Many2one('res.country')
    currency_id = fields.Many2one('res.currency')
    website = fields.Char()
    industry = fields.Char()
    sector = fields.Char()
    summary = fields.Char()
    employee_count = fields.Integer()
    price_hint = fields.Char()
    float_share = fields.Char()
    share_outstanding = fields.Char()
    implied_share_outstanding = fields.Char()

    mail_extra_content = fields.Char()
    bo_volume = fields.Float()
    bo_perc = fields.Float()


    company_id = fields.Many2one('res.company')
    prev_close = fields.Float()
    open = fields.Float()
    day_low = fields.Float()
    day_high = fields.Float()
    dividend_rate = fields.Float()
    dividend_yield = fields.Float()
    x_dividend_date = fields.Datetime()
    payout_ratio = fields.Float()
    trailing_pe = fields.Float()
    volume = fields.Float()
    avg_volume = fields.Float()
    avg_volume_10_day = fields.Float()
    market_cap = fields.Float()
    fifty_two_week_low = fields.Float()
    fifty_two_week_high = fields.Float()
    price_to_sales_twelve_months = fields.Float()
    fifty_day_avg = fields.Float()
    two_hundred_day_avg = fields.Float()
    book_value = fields.Float()
    price_book = fields.Float()
    earnings_quarterly_growth = fields.Float()
    exchange = fields.Char()
    quote_type = fields.Char()
    current_price = fields.Float()
    total_cash = fields.Float()
    total_cash_per_share = fields.Float()
    total_debt = fields.Float()
    total_revenue = fields.Float()

    def get_currency(self, currency):
        currency = self.env['res.currency'].search([('name', '=', currency)])
        currency_usd = self.env['res.currency'].search([('name', '=', 'USD')])
        return currency.id or currency_usd.id

    def get_country(self, currency):
        currency = self.env['res.currency'].search([('name', '=', currency)], limit=1)
        country = self.env['res.country'].search([('currency_id', '=', currency.id)], limit=1)
        return country.id or False

    def get_stock_ticker_info(self, symbol):
        stock = yf.Ticker(symbol)
        info = stock.info
        vals_list = {}
        vals_list['ticker_symbol'] = symbol
        if info:
            vals_list['name'] = info.get('longName')
            vals_list['address1'] = info.get('address1')
            vals_list['address2'] = info.get('address2')
            vals_list['zip'] = info.get('zip')
            vals_list['phone'] = info.get('phone')
            vals_list['city'] = info.get('city')
            vals_list['industry'] = info.get('industry')
            vals_list['summary'] = info.get('longBusinessSummary')
            vals_list['sector'] = info.get('sector')
            vals_list['employee_count'] = info.get('fullTimeEmployees')
            vals_list['website'] = info.get('website')
            vals_list['prev_close'] = info.get('previousClose')
            vals_list['open'] = info.get('open')
            vals_list['day_low'] = info.get('dayLow')
            vals_list['day_high'] = info.get('dayHigh')
            vals_list['dividend_rate'] = info.get('dividendRate')
            vals_list['dividend_yield'] = info.get('dividendYield')
            vals_list['x_dividend_date'] = datetime.fromtimestamp(info.get('exDividendDate')) if info.get(
                'exDividendDate') else False
            vals_list['payout_ratio'] = info.get('payoutRatio')
            vals_list['trailing_pe'] = info.get('trailingPE')
            vals_list['volume'] = info.get('volume')
            vals_list['avg_volume'] = info.get('averageVolume')
            vals_list['avg_volume_10_day'] = info.get('averageVolume10days')
            vals_list['market_cap'] = info.get('marketCap')
            vals_list['fifty_two_week_low'] = info.get('fiftyTwoWeekLow')
            vals_list['fifty_two_week_high'] = info.get('fiftyTwoWeekHigh')
            vals_list['price_to_sales_twelve_months'] = info.get('priceToSalesTrailing12Months')
            vals_list['fifty_day_avg'] = info.get('fiftyDayAverage')
            vals_list['two_hundred_day_avg'] = info.get('twoHundredDayAverage')
            vals_list['book_value'] = info.get('bookValue')
            vals_list['price_book'] = info.get('priceToBook')
            vals_list['earnings_quarterly_growth'] = info.get('earningsQuarterlyGrowth')
            vals_list['exchange'] = info.get('exchange')
            vals_list['quote_type'] = info.get('quoteType')
            vals_list['current_price'] = info.get('currentPrice')
            vals_list['total_cash'] = info.get('totalCash')
            vals_list['total_cash_per_share'] = info.get('totalCashPerShare')
            vals_list['total_debt'] = info.get('totalDebt')
            vals_list['total_revenue'] = info.get('totalRevenue')
            vals_list['company_id'] = self.env.company.id
            vals_list['currency_id'] = self.get_currency(info.get('currency'))
            vals_list['country_id'] = self.get_country(info.get('currency'))
            vals_list['price_hint'] = info.get('priceHint')
            vals_list['float_share'] = info.get('floatShares')
            vals_list['share_outstanding'] = info.get('sharesOutstanding')
            vals_list['implied_share_outstanding'] = info.get('impliedSharesOutstanding')
        return vals_list

    @api.model_create_single
    def create(self, vals_list):
        if vals_list['ticker_symbol']:
            vals_list = self.get_stock_ticker_info(vals_list['ticker_symbol'])
        res = super(StockTickers, self).create(vals_list)
        return res

    def get_stock_vals(self):
        vals_list = {}
        if self.ticker_symbol:
            stock = yf.Ticker(self.ticker_symbol)
            info = stock.info
            vals_list['prev_close'] = info.get('previousClose')
            vals_list['open'] = info.get('open')
            vals_list['day_low'] = info.get('dayLow')
            vals_list['day_high'] = info.get('dayHigh')
            vals_list['dividend_rate'] = info.get('dividendRate')
            vals_list['dividend_yield'] = info.get('dividendYield')
            vals_list['x_dividend_date'] = datetime.fromtimestamp(info.get('exDividendDate')) if info.get(
                'exDividendDate') else False
            vals_list['payout_ratio'] = info.get('payoutRatio')
            vals_list['trailing_pe'] = info.get('trailingPE')
            vals_list['volume'] = info.get('volume')
            vals_list['avg_volume'] = info.get('averageVolume')
            vals_list['avg_volume_10_day'] = info.get('averageVolume10days')
            vals_list['market_cap'] = info.get('marketCap')
            vals_list['fifty_two_week_low'] = info.get('fiftyTwoWeekLow')
            vals_list['fifty_two_week_high'] = info.get('fiftyTwoWeekHigh')
            vals_list['price_to_sales_twelve_months'] = info.get('priceToSalesTrailing12Months')
            vals_list['fifty_day_avg'] = info.get('fiftyDayAverage')
            vals_list['two_hundred_day_avg'] = info.get('twoHundredDayAverage')
            vals_list['book_value'] = info.get('bookValue')
            vals_list['price_book'] = info.get('priceToBook')
            vals_list['earnings_quarterly_growth'] = info.get('earningsQuarterlyGrowth')
            vals_list['exchange'] = info.get('exchange')
            vals_list['quote_type'] = info.get('quoteType')
            vals_list['current_price'] = info.get('currentPrice')
            vals_list['total_cash'] = info.get('totalCash')
            vals_list['total_cash_per_share'] = info.get('totalCashPerShare')
            vals_list['total_debt'] = info.get('totalDebt')
            vals_list['total_revenue'] = info.get('totalRevenue')
            vals_list['price_hint'] = info.get('priceHint')
            vals_list['float_share'] = info.get('floatShares')
            vals_list['share_outstanding'] = info.get('sharesOutstanding')
            vals_list['implied_share_outstanding'] = info.get('impliedSharesOutstanding')
            return vals_list

    def check_break_out(self):
        """current volume grater than avg 10 day volume x 3 then considered as breakout"""
        # TODO add 3 in company to get percentage conditional wise
        check_price = ((self.open * self.bo_perc) / 100)
        if self.volume >= (self.avg_volume_10_day * self.bo_volume) and self.current_price >= (self.open + check_price):
            self.mail_extra_content = "self.volume >= (self.avg_volume_10_day * 3) and self.current_price >= (self.open + check_price)"
            self.trigger_breakout_mail()

    def trigger_breakout_mail(self):
        """Send mail to all existing partners"""
        # Todo can be added which are the partners who is subscribed for this update
        mail_template = self.env.ref('stock_market.email_stock_breakout_info')
        if self.company_id.email:
            mail_template.email_from = self.company_id.email
            partners = [x for x in self.env['res.partner'].search([]) if x.email]
            for partner in partners:
                if partner.email:
                    mail_template.email_to = partner.email
                    mail_template.send_mail(self.id, force_send=True)

    def update_stock(self):
        """Crone Function to fetch data"""
        for rec in self.env['stock.ticker'].search([]):
            vals_list = rec.get_stock_vals()
            rec.write(vals_list)
            rec.check_break_out()
