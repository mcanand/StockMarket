from odoo import fields, models, api, _


class StockTickerDayData(models.Model):
    _name = 'stock.ticker.day.data'
    _order = 'date_time DESC'

    ticker_data_id = fields.Many2one('stock.ticker.data')
    open = fields.Float()
    close = fields.Float()
    low = fields.Float()
    high = fields.Float()
    volume = fields.Float()
    date_time = fields.Datetime()
