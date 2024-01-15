/* @odoo-module */

import {ListRenderer} from "@web/views/list/list_renderer";
import {patch} from "@web/core/utils/patch";

patch(ListRenderer.prototype, {
    freezeColumnWidths() {
        const table = this.tableRef.el;
        const child_table = table.firstElementChild.firstElementChild;
        if (!$(child_table.firstChild).hasClass("o_list_row_count_sheliya")) {
            const a = $(child_table).prepend(
                '<th class="o_list_row_number_header o_list_row_count_sheliya" style="width: 4% !important;">'
            );
            a.find("th.o_list_row_count_sheliya").html("#");
        }
        return super.freezeColumnWidths();
    },
});
