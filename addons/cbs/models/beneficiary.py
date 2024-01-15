from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CbsBeneficiary(models.Model):
    _name = "cbs.beneficiary"
    _description = "Beneficiary"

    member_id = fields.Many2one('cbs.member', 'Member', required=True)
    name = fields.Char('Beneficiary Name', required=True)
    phone_number = fields.Char('Telephone Number', required=True)
    relationship = fields.Char('Relationship', required=True)
    percentage = fields.Float('Percentage', required=True, default=0.0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', required=True)

    @api.constrains('percentage')
    def check_percentage(self):
        for record in self:
            if record.member_id:
                total_percentage = sum(record.member_id.beneficiaries.mapped('percentage'))
                if total_percentage > 1:
                    raise ValidationError("Total percentage for all beneficiaries of this member cannot exceed 100%.")

    def action_confirm(self):
        self.state = 'submitted'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'
