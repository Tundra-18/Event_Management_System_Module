import re

from odoo import fields, models, api, exceptions


class Participants(models.Model):
    _name = 'event.hosts'
    _description = 'Event Hosts'
    _table = 'hosts'

    name = fields.Char(string='Host Name', required=True)
    image = fields.Binary(string="Image", required=True)
    age = fields.Integer(string="Age", required=True)
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
        ], string="Gender", required=True
    )

    nrc = fields.Char(string='NRC', required=True)
    address = fields.Char(string="Address")
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone Number", required=True)
    reg_date = fields.Date(string='Registration Date', default=fields.Datetime.now)

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

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 10 or record.age > 99:
                raise exceptions.ValidationError("Age must be between 10 to 99!")

    # _sql_constraints = ('email_unique', 'unique(email)', 'Participant Email must be unique!')
