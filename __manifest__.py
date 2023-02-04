

{
    'name': "estate",
    'version': '1',
    'summary': """New custom module for testing""",
    'description': """This module records real estate info""",
    'author': "Ahmed Salah ",
    'category': 'Tools',
    'depends': ['base'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/estate.xml',
        'views/res.xml'],
    'demo': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}
