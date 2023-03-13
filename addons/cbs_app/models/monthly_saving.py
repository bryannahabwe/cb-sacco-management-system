from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CbsMonthlySaving(models.Model):
    _name = "cbs.monthly.saving"
    _description = "Monthly Saving"
    _rec_name = "member_id"

    member_id = fields.Many2one('cbs.member', 'Member', required=True)
    paid_for = fields.Selection([
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ], string='Paid for', required=True)
    year = fields.Selection(selection='years_selection', string='Year', required=True, default='2022')
    amount = fields.Monetary('Amount', required=True)
    amount_in_words = fields.Char('Amount In Words', compute='_amount_in_word', readonly=True, )
    date_of_payment = fields.Date('Date of Payment', required=True, default=fields.Date.today())
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft', required=True)

    def _amount_in_word(self):
        for rec in self:
            rec.amount_in_words = str(rec.currency_id.amount_to_text(rec.amount))

    def years_selection(self):
        year = 2022  # replace 2000 with your start year
        year_list = []
        while year != 2030:  # replace 2030 with your end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    def action_confirm(self):
        self.state = 'submitted'

    def action_pay(self):
        self.state = 'paid'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'
