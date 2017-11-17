define(['knockout', 'underscore', 'viewmodels/widget', 'jquery', 'fpan'], function (ko, _, WidgetViewModel, $, fpan) {
    /**
    * registers a text-widget component for use in forms
    * @function external:"ko.components".text-widget
    * @param {object} params
    * @param {string} params.value - the value being managed
    * @param {function} params.config - observable containing config object
    * @param {string} params.config().label - label to use alongside the text input
    * @param {string} params.config().placeholder - default text to show in the text input
    */
    return ko.components.register('scout-widget', {
        viewModel: function(params) {
            params.configKeys = ['options','placeholder'];
            WidgetViewModel.apply(this, [params]);
            var self = this;
            self.availableScouts = ko.observableArray();
            self.selectedScout = ko.observable();

            $.ajax(fpan.urls.scouts_dropdown, {
                dataType: "json"
            }).done(function(data) {
                $.each(data, function() {
                    self.availableScouts.push(this.user_id);
                    console.log(this);
                });
            });
            
        },
        template: { require: 'text!templates/views/components/widgets/scout-widget.htm' }
    });
});
