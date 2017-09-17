odoo.define('ebmerchant_posfront.posfront', function (require) {
    "use strict";
    var Class   = require('web.Class');
    var Model   = require('web.Model');
    var bus = require('bus.bus').bus;

    var screens = require('point_of_sale.screens');
    var PaymentScreenWidget = screens.PaymentScreenWidget;
    var OrderWidget = screens.OrderWidget;
    var ProductScreenWidget = screens.ProductScreenWidget;

    bus.on('notification', null, function(notifications) {
        _.each(notifications, function (notification) {
            var model = notification[0][1];
            var message = notification[1];
            if (model === 'ebmerchant_posfront') {
                var event = message[0];
                var data = message[1];
                if(event == 'select_payment') {
                    var payment_id = data.id;
                    jQuery('.paymentmethod[data-id="'+payment_id+'"]').click();
                }
            }
        });
    });


    var posfront_refresh = function() {
        var pos = this.pos;
        var order = pos.get_order();
        var methods = pos.cashregisters;
        var payment_lines = order.get_paymentlines();
        var lines = order.get_orderlines();
        var total = order.get_total_with_tax();
        var taxes = total - order.get_total_without_tax();
        if(!pos.config.posfront_config_id[0]) return;

        var order_info = {
            id: order.name,
            total: total,
            taxes: taxes,
            current_screen: pos.gui.get_current_screen(),
            lines: [],
            payment_methods: [],
            payment_lines: []
        };

        for(var i = 0;i<methods.length;i++) {
            var method = methods[i];
            var name = method.journal_id[1];
            var id = method.journal_id[0];
            var payment_method = {
                id: id,
                name: name
            };
            order_info.payment_methods.push(payment_method);
        }

        for(var i = 0;i<payment_lines.length;i++) {
            var payment_line = payment_lines[i];
            var tmp = {
                id: payment_line.cid,
                name: payment_line.name,
                amount: payment_line.amount,
                bitpay_config_id: payment_line.cashregister.journal.bitpay_config_id,
                mercury_config_id: payment_line.cashregister.journal.pos_mercury_config_id
            };
            order_info.payment_lines.push(tmp);
        }

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
        model.call('send', [pos.config.posfront_config_id[0],order_data], undefined, {timeout: 2000}).then(function (data) {
        });
    };

    PaymentScreenWidget.include({
        show: function() {
            this._super();
            posfront_refresh.call(this);
        },

        click_paymentmethods: function(id) {
            this._super(id);
            posfront_refresh.call(this);
        },

        click_delete_paymentline: function(cid) {
            this._super(cid);
            posfront_refresh.call(this);
        },

        payment_input: function(input) {
            this._super(input);
            posfront_refresh.call(this);
        }
    });

    OrderWidget.include({

        renderElement: function(scrollbottom){
            this._super();
            posfront_refresh.call(this);
        },

        set_value: function(value) {
            this._super(value);
            posfront_refresh.call(this);
        }
    });

    ProductScreenWidget.include({
        show: function() {
            this._super();
            posfront_refresh.call(this);
        }
    });
});
