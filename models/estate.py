from odoo import models,fields,api
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.osv import expression


class TestModel(models.Model):
    _name = "estate"
    _description = "Estate Details"
    _order = "id desc"

    active = fields.Boolean('Active', default=False)
    state = fields.Selection(selection=[('new', 'New'), ('offer_recived', 'Offer recived'), ('offer_accepted', 'Offer accepted'),('sold','Sold'),('cancelled', 'Cancelled')], string='State')
    name = fields.Char(string="Proporety Name",required=True)
    description=fields.Text(string="Description")                       
    postcode=fields.Char(string="Postcode")          
    expected_price=fields.Float(string="Expected Price",required=True)           
    selling_price=fields.Float(string="Selling price",readonly=True)           
    bedrooms=fields.Integer(string="Bedrooms",default=2)                   
    living_area=fields.Integer(string="Living area")                    
    facades=fields.Integer(string="Facades")                
    garage=fields.Boolean(string="Garage")                    
    garden=fields.Boolean(string="Garden")                   
    garden_area=fields.Integer(string="Garden area")                    
    garden_orientation=fields.Selection(string='Type',
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')],
        help="Type is used to separate Leads and Opportunities") 
    part_id=fields.Many2one('res.partner',string="buyer")
    buyer_id=fields.Char(related="part_id.name",string="buyer")
    seller_id=fields.Many2one('res.users',string="seller",index=True, tracking=True, default=lambda self: self.env.user)
    type_id=fields.Many2one('p_type',string="type")
    tag_id=fields.Many2many('tag', string="tag")
    offer_ids = fields.One2many("offer", "property_id")
    total = fields.Float(compute="_compute_total")
    Color=fields.Integer()
    

    @api.depends("garden_area","living_area")
    def _compute_total(self):
        for record in self:
            record.total = record.garden_area + record.living_area


    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden == True:
            self.garden_orientation = "north"
            self.garden_area = 10
        if self.garden == False:
            self.garden_orientation = ""
            self.garden_area = 0

    @api.constrains('expected_price')
    def _expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError("The price date cannot be set in minus")

    @api.depends("state")
    def action_sold(self):
        for record in self:
            if record.state=="cancelled":
                return False
                break
            record.state = "sold"
        return True
        
    @api.depends("state")
    def action_cancel(self):
        for record in self:
            if record.state=="sold":
                return False
                break
            record.state = "cancelled"
        return True

    _sql_constraints = [
        ('expected_price', 'CHECK( expected_price > 0 AND  expected_price < 1000000)',
         'The percentage of an analytic distribution should be between 0 and 1000000.')
    ]




class Buyer(models.Model):
    _name = "buyer"
    _description = "buyer Details"
    
    name=fields.Char(string="name")

class Seller(models.Model):
    _name = "seller"
    _description = "seller Details"
    
    name=fields.Char(string="name")


class P_type(models.Model):
    _name = "p_type"
    _description = "type details"
    _order = "name desc"

    name=fields.Char(string="name")
    number=fields.Integer(string="number")
    property_ids=fields.One2many("estate", "type_id")
    offer_ids=fields.One2many('offer', 'p_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
                
    
class Tag(models.Model):
    _name = "tag"
    _description = "type details"
    _order = "name desc"

    name=fields.Char(string="name")
    tag=fields.Char(string="tag")
    color=fields.Integer()

class Offer(models.Model):
    _name = "offer"
    _description = "offer details"
    _order = "price desc"

    price=fields.Float(string="price")
    status=fields.Selection(string="status",selection=[('accepted', 'Accepted'),('rejected', 'Rejected')] )
    partner_id=fields.Many2one('res.partner', string="part")
    property_id=fields.Many2one('estate')
    date=fields.Date()
    p_type_id=fields.Many2one(related='property_id.type_id')



    def action_set_done(self):
        for record in self:
            if record.status=="rejected":
                return False
                break
            record.state = "accepted"
        return True

    def action_cancel(self):
        for record in self:
            if record.state=="accepted":
                return False
                break
            record.state = "rejected"
        return True

class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate','seller_id')


