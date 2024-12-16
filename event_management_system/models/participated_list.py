from odoo import fields, models, api, exceptions


class ParticipatedList(models.Model):
    _name = 'participated.list'
    _description = 'Participated List'
    _table = 'participated_list'

    event_id = fields.Many2one('event.management', string="Event Name", required=True)
    participant_id = fields.Many2one('event.participants', string="Participant Name", required=True)
    reg_date = fields.Date(string="Registered Date", required=True)
    is_agree = fields.Boolean(string="I agree the policies of the event!", required=True)

    participant_fees = fields.Integer(
        string="Fees",
        related="event_id.amount",
    )

    participant_image = fields.Binary(
        string="Image",
        related="participant_id.image",
    )

    participant_age = fields.Integer(
        string="Age",
        related="participant_id.age",
    )

    participant_gender = fields.Selection(
        string="Gender",
        related="participant_id.gender",
    )

    participant_nrc = fields.Char(
        string="NRC",
        related="participant_id.nrc",
    )

    participant_address = fields.Char(
        string="Address",
        related="participant_id.address",
    )

    participant_email = fields.Char(
        string="Email",
        related="participant_id.email",
    )

    participant_phone = fields.Char(
        string="Phone",
        related="participant_id.phone",
    )

    payment_status = fields.Selection(
        [
            ('pending', 'Pending'),
            ('partial', 'Partially Paid'),
            ('paid', 'Paid'),
        ], string="Payment Status"
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


