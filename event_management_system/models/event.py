import re

from odoo import models, fields, api, exceptions


class Event(models.Model):
    _name = "event.management"
    _description = "Event Management"
    _table = "events"

    image = fields.Binary(string="Event Logo")
    organizer = fields.Char(string="Organizer", required=True)
    host = fields.Many2one('event.hosts', string="Host Name", required=True)
    name = fields.Char(string="Event Name", required=True)
    event_description = fields.Text(string="Description", help="Tell something about the event!")
    agreement_id = fields.One2many('sponsor.agreement', 'event_id', string="Sponsors")
    participated_list_id = fields.One2many('participated.list', 'event_id', string="Participated List")
    event_type = fields.Selection(
        [
            ('conference', 'Conference'),
            ('workshop', 'Workshop'),
            ('meeting', 'Meeting'),
            ('webinar', 'Webinar'),
            ('staffparty', 'Staff Party'),
            ('gathering', 'Gathering'),
        ], string="Event Type", required=True
    )
    max_person = fields.Integer(string="Attendants", required=True)
    event_date = fields.Date(string="Event Date")
    start_time = fields.Char(string="Start Time")
    duration = fields.Char(string="Duration")
    location = fields.Char(string="Location")
    website = fields.Char(string="Website")
    hotline = fields.Char(string="Hotline", required=True)
    fees = fields.Selection(
        [
            ('foc', 'FOC'),
            ('charged', "Charged"),
        ], string="Fees", required=True
    )
    amount = fields.Integer(string="Amount")
    currency_id = fields.Many2one('res.currency',
                                  string="Currency",
                                  default=lambda self: self.env['res.currency'].search([('name', '=', 'MMK')], limit=1))

    payment = fields.Selection(
        [
            ('kpay', 'KBZ Pay'),
            ('wave', 'Wave Pay'),
            ('ayapay', 'AYA Pay'),
            ('cbpay', 'CB Pay'),
            ('awallet', 'A+ Wallet'),
        ], string="Acceptable Payments"
    )

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

    @api.constrains('hotline')
    def _check_hotline_number(self):
        regex = r'^\d{9,11}$'
        for record in self:
            if not re.match(regex, record.hotline):
                raise exceptions.ValidationError("Hotline must be a numeric value between 9 and 11 digits!")

    @api.constrains('max_person', 'event_type')
    def _check_attendants(self):
        for record in self:
            if record.event_type == 'conference' and record.max_person < 100:
                raise exceptions.ValidationError("A conference must have at least 100 attendants!")
            if record.event_type == 'workshop' and record.max_person < 10:
                raise exceptions.ValidationError("A workshop must have at least 10 attendants")
            if record.event_type == 'meeting' and record.max_person < 5:
                raise exceptions.ValidationError("A meeting must have at least 10 attendants")
            if record.event_type == 'webinar' and record.max_person < 10:
                raise exceptions.ValidationError("A webinar must have at least 10 attendants")
            if record.event_type == 'staffparty' and record.max_person < 30:
                raise exceptions.ValidationError("A staff party must have at least 30 attendants")
            if record.event_type == 'gathering' and record.max_person < 10:
                raise exceptions.ValidationError("A gathering must have at least 10 attendants")

    @api.constrains('start_time')
    def _check_start_time(self):
        for record in self:
            if record.start_time:
                if not re.match(r'^(0[1-9]|1[0-2]):([0-5][0-9])\s?(AM|PM)$', record.start_time):
                    raise exceptions.ValidationError("Start time must be in the format (XX:XX AM/PM)")

    @api.constrains('duration')
    def _check_duration(self):
        for record in self:
            if record.duration:
                if not re.match(
                        r'^([1-24]):([0-5][0-9])\s?(Hr|Hrs|hr|hrs)$'
                        r'|^([1-9]|1[0-9]|2[0-4])\s?(Hr|Hrs|hr|hrs)$'
                        r'|^([0-5][0-9])\s?(Min|Mins|min|mins)$', record.duration):
                    raise exceptions.ValidationError(
                        "Duration must be in the format:\n"
                        "(XX Min/min/Mins/mins)\n"
                        "(XX Hr/hr/Hrs/hrs)\n"
                        "(XX:XX Hrs/hrs)"
                    )


