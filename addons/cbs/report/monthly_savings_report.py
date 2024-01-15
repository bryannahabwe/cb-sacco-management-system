from odoo import models, fields, api


class ReportMonthlySavings(models.AbstractModel):
    _name = 'report.cbs.report_monthly_savings'
    _description = 'Monthly Savings'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['cbs.monthly.saving'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'cbs.monthly.saving',
            'docs': docs
        }
