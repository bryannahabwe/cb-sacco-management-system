from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CbsLoanPayment(models.Model):
    _name = "cbs.loan.payment"
    _description = "Loan Payment"
    _rec_name = "member_id"

    member_id = fields.Many2one('cbs.member', 'Member', required=True)
    loan_amount = fields.Monetary('Loan Amount', required=True)
    amount_paid = fields.Monetary('Amount Paid', required=True)
    loan_balance = fields.Monetary('Loan Balance', compute='_compute_loan_balance', readonly=True, )
    amount_in_words = fields.Char('Amount In Words', compute='_amount_in_word', readonly=True, )
    date_of_payment = fields.Date('Date of Payment', required=True, default=fields.Date.today())
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    referee_ids = fields.Many2many('cbs.member', string='Referees', required=True)

    def _amount_in_word(self):
        for rec in self:
            rec.amount_in_words = str(rec.currency_id.amount_to_text(rec.amount_paid))

    @api.onchange('member_id')
    def onchange_classroom(self):
        total_loan_amount = 0
        if self.member_id:
            loan_application_records = self.env['cbs.loan.application'].search([('member_id', '=', self.member_id.id),
                                                                                ('state', '!=', 'cleared')])
            for record in loan_application_records:
                total_loan_amount += record.amount
        self.loan_amount = total_loan_amount

    @api.depends('amount_paid', 'loan_amount')
    def _compute_loan_balance(self):
        for record in self:
            record.loan_balance = record.loan_amount - record.amount_paid

    def action_confirm(self):
        self.state = 'submitted'

    def action_pay(self):
        self.state = 'paid'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'
