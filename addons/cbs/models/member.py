from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CbsMember(models.Model):
    _name = "cbs.member"
    _description = "Members"

    name = fields.Char('Member Name', required=True)
    display_name = fields.Char('Display Name', compute='_compute_display_name')
    phone_number = fields.Char('Telephone Number', required=True)
    email = fields.Char('Email')
    address = fields.Char('Address')
    dob = fields.Date('Date of Birth', date_format='%d/%m/%Y')
    cbs_number = fields.Char('CBS Number', help="CBS Member Number", required=True)
    date_created = fields.Datetime('Date Created', readonly=True, default=fields.Datetime.now)
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female')], string='Gender', required=True)
    nin = fields.Char('NIN', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('cancelled', 'Cancelled'),
        ('approved', 'Active')],
        'State', default='draft')
    referees = fields.Char('List of Referees')
    beneficiaries = fields.One2many('cbs.beneficiary', 'member_id', string='Beneficiaries')
    monthly_savings = fields.One2many('cbs.monthly.saving', 'member_id', string='Monthly Savings')
    loan_applications = fields.One2many('cbs.loan.application', 'member_id', string='Loan Applications')
    loan_payments = fields.One2many('cbs.loan.payment', 'member_id', string='Loan Payments')

    @api.depends('name', 'cbs_number')
    def _compute_display_name(self):
        for record in self:
            name = '%s' % (record.name or '')
            cbs_number = '%s' % (record.cbs_number or '')
            record.display_name = _("%s ( %s )") % (name, cbs_number)

    @api.constrains('dob')
    def _check_birthdate(self):
        for record in self:
            if record.dob > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    def submit_form(self):
        self.state = 'submitted'

    def approve_member(self):
        self.state = 'approved'

    def confirm_to_draft(self):
        self.state = 'draft'

    def confirm_cancel(self):
        self.state = 'cancelled'
