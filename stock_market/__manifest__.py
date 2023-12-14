
{
    'name': 'Stock Market',
    'version': '15.0.0.1.0.1',
    'sequence': 1,
    'summary': '',
    'depends': ['mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/mail_template.xml',
        'views/ticker.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {

    },
    'license': 'LGPL-3',
}
