from odoo import fields, models, api, exceptions
import re


class Sponsor(models.Model):
    _name = 'event.sponsor'
    _description = 'Event Sponsor'
    _table = 'sponsor'

    name = fields.Char(string="Name", required=True)
    image = fields.Binary(string="Logo", required=True)
    reg_date = fields.Date(string="Registration Date", required=True)
    website = fields.Char(string="Website")

    contact_person = fields.Char(string="Contact Person", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone", required=True)
    address = fields.Char(string="Address")

    level = fields.Selection(
        [
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum'),
        ], string="Level", required=True
    )
    amount_contributed = fields.Integer(string="Amount Contributed")
    currency_id = fields.Many2one('res.currency',
                                  string="Currency",
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'MMK')], limit=1))

    support = fields.Text(string="In-Kind Support")
    note = fields.Text(string="Notes")

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('done', 'Done'),
            ('confirm', 'Confirmed'),
            ('cancel', 'Canceled'),
        ], string="Status", default="draft", tracking=True
    )

    def action_draft(self):
        for record in self:
            record.state = 'draft'

    def action_confirm(self):
        for record in self:
            record.state = 'confirm'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

    @api.constrains('phone')
    def _check_hotline_number(self):
        for record in self:
            if record.phone:
                if not re.match(r'^\d{9,11}$', record.phone):
                    raise exceptions.ValidationError("Phone number must be a numeric value between 9 and 11 digits!")

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', record.email):
                    raise exceptions.ValidationError("Please enter a valid email address!")

    @api.onchange('level')
    def _onchange_bronze(self):
        if self.level == 'bronze':
            return {
                'warning': {
                    'title': 'Notice',
                    'message': 'Bronze level sponsorship must provide at least "In-kind" support!'
                               '\nSo, please fill out "In-Kind Support" field!'
                }
            }

    @api.constrains('level', 'support')
    def _check_support_required(self):
        for record in self:
            if record.level == 'bronze' and not record.support:
                raise exceptions.ValidationError('The "In-Kind Support" field is required when the level is "Bronze".')

    @api.constrains('level', 'amount_contributed')
    def _check_amount_contributed(self):
        for record in self:
            if record.level == 'silver' and (record.amount_contributed < 100000
                                             or record.amount_contributed > 500000):
                raise exceptions.ValidationError("Silver level sponsorship is between 1 Lakh to 5 Lakhs!")

            if record.level == 'gold' and (record.amount_contributed < 600000
                                           or record.amount_contributed > 1000000):
                raise exceptions.ValidationError("Gold level sponsorship is between 6 Lakhs to 10 Lakhs!")

            if record.level == 'platinum' and (record.amount_contributed < 1100000
                                               or record.amount_contributed > 2000000):
                raise exceptions.ValidationError("Platinum level sponsorship is between 11 Lakhs to 20 Lakhs!")
