from odoo import fields, models, api, _
from datetime import datetime, timedelta

import yfinance as yf


class StockTickerData(models.Model):
    _name = 'stock.ticker.data'
    _order = 'date DESC'

    stock_ticker_day_data_ids = fields.One2many('stock.ticker.day.data', 'ticker_data_id')
    ticker_id = fields.Many2one('stock.ticker')
    open = fields.Float()
    close = fields.Float()
    low = fields.Float()
    high = fields.Float()
    volume = fields.Float()
    date = fields.Date()

    def prepare_ticker_day_data_vals(self, data):
        ticker_data_list = []
        day_entries = []
        if self.stock_ticker_day_data_ids:
            day_entries += self.stock_ticker_day_data_ids.mapped('date_time')
        for i, (key, value) in enumerate(data.items()):
            timestamp_str = key.strftime('%Y-%m-%d %H:%M:%S')  # Replace this with your timestamp string
            format_str = '%Y-%m-%d %H:%M:%S'
            datetime_obj = datetime.strptime(timestamp_str, format_str)
            if self.env.user.tz == 'Asia/Calcutta':
                datetime_obj = datetime_obj - timedelta(hours=5, minutes=30)
            if not datetime_obj in day_entries:
                vals = {}
                vals['date_time'] = datetime_obj
                vals['open'] = value.get('Open')
                vals['close'] = value.get('Close')
                vals['low'] = value.get('Low')
                vals['high'] = value.get('High')
                vals['volume'] = value.get('Volume')
                ticker_data_list.append((0, 0, vals))
        return ticker_data_list

    def get_intraday_data(self):
        intraday_data = yf.download(self.ticker_id.ticker_symbol, start=self.date.strftime('%Y-%m-%d'),
                                    interval='1m').to_dict(orient='index')
        if intraday_data:
            data = self.prepare_ticker_day_data_vals(intraday_data)
            return data

    def action_get_day_data(self):
        self.stock_ticker_day_data_ids = []
        data = self.get_intraday_data()
        if data:
            self.stock_ticker_day_data_ids = data
