import json

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CbsLoanPayment(models.Model):
    _name = "cbs.loan.payment"
    _description = "Loan Payment"
    _rec_name = "member_id"

    member_id = fields.Many2one('cbs.member', 'Member', required=True)
    loan_amount = fields.Monetary('Loan Amount + Interest', required=True)
    amount_paid = fields.Monetary('Amount Paid', required=True)
    interest_amount = fields.Float(string='Interest Amount', store=True)
    loan_balance = fields.Monetary('Loan Balance', compute='_compute_loan_balance', readonly=True, store=True)
    amount_in_words = fields.Char('Amount In Words', compute='_amount_in_word', readonly=True, store=True)
    date_of_payment = fields.Date('Date of Payment', required=True, default=fields.Date.today())
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    loan_id = fields.Many2one('cbs.loan.application', string='Loan')
    loan_id_domain = fields.Char(compute="_compute_loan_id_domain", readonly=True, store=False)

    @api.depends('amount_paid')
    def _amount_in_word(self):
        for rec in self:
            rec.amount_in_words = str(rec.currency_id.amount_to_text(rec.amount_paid))

    @api.depends('member_id')
    def _compute_loan_id_domain(self):
        for rec in self:
            rec.loan_id_domain = json.dumps([('member_id', '=', rec.member_id.id), ('state', '!=', 'cleared')])

    @api.onchange('loan_id')
    def onchange_loan_id(self):
        interest_amount = 0
        total_loan_amount = 0
        if self.loan_id:
            loan_application_records = self.env['cbs.loan.application'].search([('id', '=', self.loan_id.id),
                                                                                ('state', '=', 'approved')])
            for record in loan_application_records:
                if record.remaining_balance == 0:
                    total_loan_amount = record.amount
                    interest_amount = (record.amount * record.interest_rate)
                else:
                    interest_amount = (record.remaining_balance * record.interest_rate)
                    total_loan_amount = record.remaining_balance + interest_amount
            self.loan_amount = total_loan_amount
            self.interest_amount = interest_amount

    @api.depends('amount_paid')
    def _compute_loan_balance(self):
        for record in self:
            record.loan_balance = record.loan_amount - record.amount_paid

    @api.constrains('amount_paid')
    def _check_amount_paid(self):
        for rec in self:
            if rec.state == 'draft':
                amount = rec.amount_paid
                if amount > rec.loan_amount:
                    raise ValidationError(_(
                        "Amount Paid should not be greater than the loan balance"))

    def action_confirm(self):
        self.state = 'submitted'

    def action_pay(self):
        if self.loan_id and self.date_of_payment:
            loan = self.loan_id
            # Update the remaining balance in the loan
            principal_amount = self.loan_amount - self.amount_paid
            loan.remaining_balance = principal_amount
            loan.total_interest += self.interest_amount
            if loan.remaining_balance <= 0:
                loan.state = 'cleared'
                loan.remaining_balance = 0
        self.state = 'paid'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'
