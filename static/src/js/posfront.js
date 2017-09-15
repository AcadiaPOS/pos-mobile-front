odoo.define('ebmerchant_posfront.posfront', function (require) {
    "use strict";
    var Class   = require('web.Class');
    var Model   = require('web.Model');

    var screens = require('point_of_sale.screens');
    var PaymentScreenWidget = screens.PaymentScreenWidget;
    var OrderWidget = screens.OrderWidget;
    var disableRefresh = false;

    OrderWidget.include({

        posfront_refresh: function() {
            var order = this.pos.get_order();
            var lines = order.get_orderlines();
            var total = order.get_total_with_tax();
            var taxes = total - order.get_total_without_tax();

            var order_info = {
                id: order.name,
                total: total,
                taxes: taxes,
                lines: []
            };
            for (var i = 0;i<lines.length;i++) {
                var line = lines[i];
                var line_info = {
                    id: line.id,
                    price: line.price,
                    quantity: line.quantity,
                    name: line.product.display_name,
                    discount: line.discount
                };
                order_info.lines.push(line_info);
            }
            var model = new Model('posfront.configuration');
            var order_data = JSON.stringify(order_info);
            model.call('broadcast', [order_data], undefined, {timeout: 2000}).then(function (data) {
            });
        },

        renderElement: function(scrollbottom){
            this._super();
            this.posfront_refresh();
        },

        set_value: function(value) {
            this._super(value);
            this.posfront_refresh();
        }


    });
});
