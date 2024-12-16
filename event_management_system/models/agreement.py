from odoo import fields, api, models, exceptions


class Agreement(models.Model):
    _name = 'sponsor.agreement'
    _description = 'Sponsor Agreement'
    _table = 'sponsor_agreement'

    event_id = fields.Many2one('event.management', string="Event Name", required=True)
    sponsor_id = fields.Many2one('event.sponsor', string="Sponsor Name", required=True)

    sponsor_logo = fields.Binary(
        string="Logo",
        related="sponsor_id.image",
    )

    sponsor_level = fields.Selection(
        string="Level",
        related="sponsor_id.level",
    )

    sponsor_phone = fields.Char(
        string="Phone",
        related="sponsor_id.phone",
    )

    sponsor_email = fields.Char(
        string="Email",
        related="sponsor_id.email",
    )

    sponsor_address = fields.Char(
        string="Address",
        related="sponsor_id.address",
    )

    sponsor_contact_person = fields.Char(
        string="Contact Person",
        related="sponsor_id.contact_person",
    )

    sponsor_amount_contributed = fields.Integer(
        string="Amount Contributed",
        related="sponsor_id.amount_contributed",
    )

    agreed_date = fields.Date(string="Agreement Date", required=True)
    contract = fields.Binary(string="Signed Contract",
                             attachment=True,
                             required=True,
                             help="Upload the PDF file of the signed contract!")
    is_agree = fields.Boolean(string="I agree the policies of the event!", required=True)

    payment_status = fields.Selection(
        [
            ('pending', 'Pending'),
            ('partial', 'Partially Paid'),
            ('paid', 'Paid'),
        ], string="Payment Status",
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

    def is_agree_confirm(self):
        for record in self:
            if not record.is_agree:
                raise exceptions.ValidationError("You must agree to the event policies to got to confirm state!")
            record.state = 'confirm'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancel'

