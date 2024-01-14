from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CbsLoanApplication(models.Model):
    _name = "cbs.loan.application"
    _description = "Loan Application"
    _rec_name = "display_name"

    display_name = fields.Char('Display Name', compute='_compute_display_name')
    member_id = fields.Many2one('cbs.member', 'Member', required=True,
                                domain=lambda self: self._get_default_members())
    amount = fields.Monetary('Principal', required=True)
    total_interest = fields.Monetary('Total Interest', required=True, default=0)
    total_amount = fields.Monetary('Total Amount', required=True, default=0,
                                   compute='_compute_total_amount', store=True)
    amount_in_words = fields.Char('Amount In Words', compute='_amount_in_word', readonly=True, )
    payment_period = fields.Integer('Payment Period', required=True, default=1)
    payment_length = fields.Selection(selection=[
        ('month', 'Month'),
        ('year', 'Year')],
        string='Payment Length',
        default='year', required=True)
    start_date_of_payment = fields.Date('Start Date of Payment', required=True, default=fields.Date.today())
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('cleared', 'Cleared'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True)
    referee_ids = fields.Many2many('cbs.member', string='Referees', required=True, ondelete='cascade',
                                   domain=lambda self: self._get_default_referees())
    total_referee_savings = fields.Monetary('Total Referee Savings', default=0,
                                            compute='_compute_total_referee_savings', store=True)
    interest_rate = fields.Float(string='Interest Rate', default=0.015)
    loan_payments = fields.One2many('cbs.loan.payment', 'loan_id', string='Loan Payments')
    terms_in_months = fields.Integer(string='Payment Period in Months', default=0)
    terms_in_months_text = fields.Char(string='Payment Period in Months', compute='_compute_terms_in_months_text',
                                       store=True)
    remaining_balance = fields.Monetary('Remaining Balance', default=0, compute='_compute_remaining_balance',
                                        store=True)

    @api.depends('member_id', 'amount')
    def _compute_display_name(self):
        for record in self:
            name = '%s' % (record.member_id.name or '')
            amount = '%s' % ("{:,.0f}".format(record.amount) or '')
            record.display_name = _("%s ( %s )") % (name, amount)

    def _amount_in_word(self):
        for rec in self:
            rec.amount_in_words = str(rec.currency_id.amount_to_text(rec.amount))

    def _get_default_members(self):
        self.env.cache.invalidate()
        members_with_loans = self.env['cbs.loan.application'].search([('state', '=', 'approved')]).mapped(
            'member_id.id')
        registered_members = self.env['cbs.member'].search([('state', '=', 'approved')])
        member_ids = []
        for registered_member in registered_members:
            if registered_member.id not in members_with_loans and registered_member.id not in member_ids:
                member_ids.append(registered_member.id)
        return [('id', 'in', member_ids)]

    def _get_default_referees(self):
        all_members = self.env['cbs.member'].search([('state', '=', 'approved')])
        member_ids = []
        for member in all_members:
            if member.id not in member_ids:
                member_ids.append(member.id)
        return [('id', 'in', member_ids)]

    @api.onchange('payment_length')
    def onchange_payment_length(self):
        total_terms_in_months = 0
        if self.payment_length == "year":
            total_terms_in_months = self.payment_period * 12
        else:
            total_terms_in_months = self.payment_period
        self.terms_in_months = total_terms_in_months

    @api.depends('terms_in_months')
    def _compute_terms_in_months_text(self):
        for record in self:
            if record.terms_in_months <= 1:
                record.terms_in_months_text = f"{record.terms_in_months} month"
            else:
                record.terms_in_months_text = f"{record.terms_in_months} months"

    @api.depends('referee_ids')
    def _compute_total_referee_savings(self):
        total_savings = 0
        for referee_id in self.referee_ids:
            if referee_id:
                total_savings += referee_id.monthly_savings.amount
            else:
                total_savings += 0
        self.total_referee_savings = total_savings

    @api.depends('amount')
    def _compute_remaining_balance(self):
        total = 0
        if self.amount:
            total = self.amount
        self.remaining_balance = total

    @api.depends('amount', 'total_interest')
    def _compute_total_amount(self):
        total = 0
        if self.amount:
            total = self.amount + self.total_interest
        self.total_amount = total

    @api.constrains('amount', 'total_referee_savings')
    def _check_amount(self):
        for rec in self:
            print(rec.state)
            if rec.state == 'draft':
                amount = rec.amount
                total_referee_savings = rec.total_referee_savings
                print(amount)
                print(total_referee_savings)
                if total_referee_savings < amount:
                    raise ValidationError(_(
                        "Total Referee Savings should greater than the loan amount requested"))

    def action_confirm(self):
        self.state = 'submitted'

    def action_approve(self):
        self.state = 'approved'

    def action_cleared(self):
        self.state = 'cleared'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'
