from odoo import models, fields


class CbsLoanApplication(models.Model):
    _name = "cbs.loan.application"
    _description = "Loan Application"
    _rec_name = "member_id"

    member_id = fields.Many2one('cbs.member', 'Member', required=True)
    amount = fields.Monetary('Amount', required=True)
    amount_in_words = fields.Char('Amount In Words', compute='_amount_in_word', readonly=True, )
    payment_period = fields.Integer('Payment Period', required=True)
    start_date_of_payment = fields.Date('Start Date of Payment', required=True, default=fields.Date.today())
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', required=True)
    referee_ids = fields.Many2many('cbs.member', string='Referees', required=True)

    def _amount_in_word(self):
        for rec in self:
            rec.amount_in_words = str(rec.currency_id.amount_to_text(rec.amount))

    def action_confirm(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'
