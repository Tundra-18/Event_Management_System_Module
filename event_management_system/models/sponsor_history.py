from odoo import fields, models

class SponsorHistory(models.Model):
    _name = "sponsor.history"
    _description = "Sponsor History"
    _table = "sponsor_history"

    event_id = fields.Many2one('event.management', string="Event Name", required=True)
    sponsor_id = fields.Many2one('event.sponsor', string="Sponsor Name", required=True)
