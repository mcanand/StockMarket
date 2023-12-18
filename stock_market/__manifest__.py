
{
    'name': 'Stock Market',
    'version': '17.0.0.1',
    'sequence': 1,
    'summary': '',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/mail_template.xml',
        'views/ticker.xml',
        'views/ticker_data.xml',
        'views/ticker_day_data.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {

    },
    'license': 'LGPL-3',
}
