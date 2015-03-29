var Reports = (function (){

    $(document).ready(function () {
        Reports.load_date_picker();
        Reports.load_listeners();
        Reports.load_data();
        Reports.draw_map();
    });

    return {

        current_start_date: moment().subtract(29, 'days'),
        current_end_date: moment(),
        map: new ol.Map({}),
        events_layer: new ol.layer.Vector({}),

        load_date_picker: function(){
            var that = this;
            $('#reportrange span').html(moment().subtract(29, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));
            $('#reportrange').daterangepicker({
                format: 'MM/DD/YYYY',
                startDate: that.current_start_date,
                endDate: that.current_end_date,
                minDate: '01/01/2012',
                maxDate: '12/31/2015',
                dateLimit: { days: 60 },
                showDropdowns: true,
                showWeekNumbers: true,
                timePicker: false,
                timePickerIncrement: 1,
                timePicker12Hour: true,
                ranges: {
                    'Today': [moment(), moment()],
                    'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                    'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                    'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                    'This Month': [moment().startOf('month'), moment().endOf('month')],
                    'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                },
                opens: 'right',
                buttonClasses: ['btn', 'btn-sm'],
                applyClass: 'btn-primary',
                cancelClass: 'btn-default',
                separator: ' to '
            }, function(start, end, label) {
                that.current_end_date = end;
                that.current_start_date = start;
                that.load_data();
            });
        },

        load_listeners: function(){
            var that = this;
            $(".filter_option").on("change", function(){
                that.load_data();
            })
        },

        draw_map: function(){

            this.map = new ol.Map({
                layers: [new ol.layer.Tile({ source: new ol.source.OSM() })],
                target: 'map',
                view: new ol.View({
                    center: [0, 0],
                    zoom: 3
                })
            });
        },

        refresh_map_events: function(data){
            var vectorSource = new ol.source.Vector({});

            //create a bunch of icons and add to source vector
            for (var i=0;i<50;i++){
                var iconFeature = new ol.Feature({
                    geometry: new
                        ol.geom.Point(ol.proj.transform([Math.random()*360-180, Math.random()*180-90], 'EPSG:4326',   'EPSG:3857')),
                    name: 'Null Island ' + i,
                    population: 4000,
                    rainfall: 500
                });
                vectorSource.addFeature(iconFeature);
            }

            //create the style
            var iconStyle = new ol.style.Style({
                image: new ol.style.Icon(({
                    anchor: [0.5, 46],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'pixels',
                    opacity: 0.75,
                    src: 'http://ol3js.org/en/master/examples/data/icon.png'
                }))
            });

            //add the feature vector to the layer vector, and apply a style to whole layer
            var vectorLayer = new ol.layer.Vector({
                source: vectorSource,
                style: iconStyle
            });

            this.events_layer = vectorLayer;
            this.map.addLayer(vectorLayer);
        },

        is_loading: function(){
            $(".privacy_tools_loading").show();
            $("#multi_series").empty();
            $(".click_drag_instructions").hide();
            this.map.removeLayer(this.events_layer);
        },

        done_loading: function(){
            $(".privacy_tools_loading").hide();
            $(".click_drag_instructions").show();
        },

        load_data: function(){
            var that = this;
            var params = this.get_params();
            this.is_loading();
            $.when(
                $.getJSON("/testjson")
            ).done(function (d) {
                    that.done_loading();
                    var data = [{"type 1": 19, "type 2": 0, "type 3": 7, "date": "20140310", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 12, "type 7": 0, "type 8": 4, "type 9": 7, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 36, "type 2": 0, "type 3": 12, "date": "20140314", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 25, "type 7": 0, "type 8": 7, "type 9": 11, "type 10": 0, "type 11": 5, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 30, "type 2": 0, "type 3": 3, "date": "20140319", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 22, "type 7": 0, "type 8": 2, "type 9": 8, "type 10": 0, "type 11": 1, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 17, "type 2": 0, "type 3": 5, "date": "20140320", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 12, "type 7": 0, "type 8": 4, "type 9": 5, "type 10": 0, "type 11": 1, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 19, "type 2": 0, "type 3": 3, "date": "20140321", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 14, "type 7": 0, "type 8": 2, "type 9": 5, "type 10": 0, "type 11": 1, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 17, "type 2": 0, "type 3": 5, "date": "20140322", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 13, "type 7": 0, "type 8": 3, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 17, "type 2": 0, "type 3": 5, "date": "20140323", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 13, "type 7": 0, "type 8": 3, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 18, "type 2": 0, "type 3": 4, "date": "20140324", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 14, "type 7": 0, "type 8": 2, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 142, "type 2": 0, "type 3": 18, "date": "20140328", "type 4": 10, "type 4": 0, "type 5": 0, "type 6": 83, "type 7": 0, "type 8": 13, "type 9": 49, "type 10": 0, "type 11": 5, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 21, "type 2": 0, "type 3": 12, "date": "20140329", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 27, "type 2": 0, "type 3": 12, "date": "20140330", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 12, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 12, "type 2": 0, "type 3": 10, "date": "20140331", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 8, "type 7": 0, "type 8": 8, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 21, "type 2": 0, "type 3": 12, "date": "20140401", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 21, "type 2": 0, "type 3": 12, "date": "20140402", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 21, "type 2": 0, "type 3": 12, "date": "20140403", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 21, "type 2": 0, "type 3": 12, "date": "20140404", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 21, "type 2": 0, "type 3": 12, "date": "20140405", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 21, "type 2": 0, "type 3": 12, "date": "20140406", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 21, "type 2": 0, "type 3": 12, "date": "20140407", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 15, "type 7": 0, "type 8": 9, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 19, "type 2": 0, "type 3": 14, "date": "20140408", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 13, "type 7": 0, "type 8": 11, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 23, "type 2": 0, "type 3": 10, "date": "20140409", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 17, "type 7": 0, "type 8": 7, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 12, "type 2": 0, "type 3": 10, "date": "20140410", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 8, "type 7": 0, "type 8": 8, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 14, "type 2": 0, "type 3": 8, "date": "20140411", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 10, "type 7": 0, "type 8": 6, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 14, "type 2": 0, "type 3": 8, "date": "20140412", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 10, "type 7": 0, "type 8": 6, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 14, "type 2": 0, "type 3": 8, "date": "20140413", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 10, "type 7": 0, "type 8": 6, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 14, "type 2": 0, "type 3": 8, "date": "20140414", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 10, "type 7": 0, "type 8": 6, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 26, "type 2": 0, "type 3": 9, "date": "20140415", "type 4": 2, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 14, "type 2": 0, "type 3": 8, "date": "20140416", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 10, "type 7": 0, "type 8": 6, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 14, "type 2": 0, "type 3": 8, "date": "20140417", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 10, "type 7": 0, "type 8": 6, "type 9": 4, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 22, "type 2": 0, "type 3": 11, "date": "20140418", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 16, "type 7": 0, "type 8": 8, "type 9": 6, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 60, "type 2": 0, "type 3": 16, "date": "20140425", "type 4": 6, "type 4": 0, "type 5": 0, "type 6": 36, "type 7": 0, "type 8": 12, "type 9": 18, "type 10": 0, "type 11": 4, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 30, "type 2": 0, "type 3": 0, "date": "20140428", "type 4": 4, "type 4": 0, "type 5": 0, "type 6": 16, "type 7": 0, "type 8": 0, "type 9": 10, "type 10": 0, "type 11": 0, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 27, "type 2": 0, "type 3": 8, "date": "20140429", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 9, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 27, "type 2": 0, "type 3": 8, "date": "20140430", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 9, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 16, "type 2": 0, "type 3": 6, "date": "20140501", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 10, "type 7": 0, "type 8": 6, "type 9": 6, "type 10": 0, "type 11": 0, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 25, "type 2": 0, "type 3": 9, "date": "20140502", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 7, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 25, "type 2": 0, "type 3": 9, "date": "20140503", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 7, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 27, "type 2": 0, "type 3": 8, "date": "20140504", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 9, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 27, "type 2": 0, "type 3": 8, "date": "20140505", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 9, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 20, "type 2": 0, "type 3": 4, "date": "20140506", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 13, "type 7": 0, "type 8": 3, "type 9": 7, "type 10": 0, "type 11": 1, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 27, "type 2": 0, "type 3": 8, "date": "20140507", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 9, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 57, "type 2": 0, "type 3": 8, "date": "20140508", "type 4": 4, "type 4": 0, "type 5": 0, "type 6": 34, "type 7": 0, "type 8": 6, "type 9": 19, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 34, "type 2": 0, "type 3": 12, "date": "20140509", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 23, "type 7": 0, "type 8": 9, "type 9": 11, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 28, "type 2": 0, "type 3": 7, "date": "20140510", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 20, "type 7": 0, "type 8": 4, "type 9": 8, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 28, "type 2": 0, "type 3": 7, "date": "20140511", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 20, "type 7": 0, "type 8": 4, "type 9": 8, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 28, "type 2": 0, "type 3": 7, "date": "20140512", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 20, "type 7": 0, "type 8": 4, "type 9": 8, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 29, "type 2": 0, "type 3": 6, "date": "20140513", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 20, "type 7": 0, "type 8": 4, "type 9": 9, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 29, "type 2": 0, "type 3": 6, "date": "20140514", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 20, "type 7": 0, "type 8": 4, "type 9": 9, "type 10": 0, "type 11": 2, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 28, "type 2": 0, "type 3": 7, "date": "20140515", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 20, "type 7": 0, "type 8": 4, "type 9": 8, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 26, "type 2": 0, "type 3": 9, "date": "20140516", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 8, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}, {"type 1": 26, "type 2": 0, "type 3": 9, "date": "20140517", "type 4": 0, "type 4": 0, "type 5": 0, "type 6": 18, "type 7": 0, "type 8": 6, "type 9": 8, "type 10": 0, "type 11": 3, "type 12": 0, "type 13": 0, "type 14": 0, "type 15": 0, "type 17": 0, "type 16": 0}];
                    that.refresh_visuals(data);
                }).fail(function () {
                    that.done_loading();$(".filter_option").trigger("change");
                });
        },

        get_params: function(){
            var filter_types = $(".filter_types input:checkbox:checked").map(function(){
                return this.value;
            }).get();
            var filter_sources = $(".filter_sources input:checkbox:checked").map(function(){
                return this.value;
            }).get();
            return {
                "types": filter_types.join(","),
                "sources": filter_sources.join(","),
                "date_range": [this.current_start_date, this.current_end_date]
            }
        },

        refresh_visuals: function(data){
            this.draw_graph(data);
            this.refresh_map_events(data)
        },

        draw_graph: function(data){
            var margin = {top: 20, right: 230, bottom: 100, left: 30},
                margin2 = {top: 430, right: 20, bottom: 20, left: 40},
                width = 940 - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom,
                height2 = 500 - margin2.top - margin2.bottom;

            var parseDate = d3.time.format("%Y%m%d").parse;
            var bisectDate = d3.bisector(function (d) {
                return d.date;
            }).left;

            var xScale = d3.time.scale().range([0, width]);
            var xScale2 = d3.time.scale().range([0, width]);

            var yScale = d3.scale.linear().range([height, 0]);
            var color = d3.scale.category20();
            var xAxis = d3.svg.axis().scale(xScale).orient("bottom");
            var xAxis2 = d3.svg.axis().scale(xScale2).orient("bottom");

            var yAxis = d3.svg.axis().scale(yScale).orient("left");

            var line = d3.svg.line()
                .interpolate("basis")
                .x(function (d) {
                    return xScale(d.date);
                })
                .y(function (d) {
                    return yScale(d.rating);
                })
                .defined(function (d) {
                    return d.rating;
                });

            var maxY;

            var svg = d3.select("#multi_series").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            svg.append("rect")
                .attr("width", width)
                .attr("height", height)
                .attr("x", 0)
                .attr("y", 0)
                .attr("id", "mouse-tracker")
                .style("fill", "white");

            var context = svg.append("g")
                .attr("transform", "translate(" + 0 + "," + 410 + ")")
                .attr("class", "context");

            svg.append("defs")
                .append("clipPath")
                .attr("id", "clip")
                .append("rect")
                .attr("width", width)
                .attr("height", height);

            color.domain(d3.keys(data[0]).filter(function (key) {
                return key !== "date";
            }));

            data.forEach(function (d) {
                d.date = parseDate(d.date);
            });

            var categories = color.domain().map(function (name) {

                return {
                    name: name,
                    values: data.map(function (d) {
                        return {
                            date: d.date,
                            rating: +(d[name])
                        };
                    }),
                    visible: true
                };
            });

            xScale.domain(d3.extent(data, function (d) {
                return d.date;
            }));
            yScale.domain([0, d3.max(categories, function (c) {
                return d3.max(c.values, function (v) {
                    return v.rating;
                });
            })]);
            xScale2.domain(xScale.domain());

            var brush = d3.svg.brush()
                .x(xScale2)
                .on("brush", brushed);

            context.append("g")
                .attr("class", "x axis1")
                .attr("transform", "translate(0," + height2 + ")")
                .call(xAxis2);

            var contextArea = d3.svg.area()
                .interpolate("monotone")
                .x(function (d) {
                    return xScale2(d.date);
                })
                .y0(height2)
                .y1(0);

            context.append("path")
                .attr("class", "area")
                .attr("d", contextArea(categories[0].values))
                .attr("fill", "#F1F1F2");

            context.append("g")
                .attr("class", "x brush")
                .call(brush)
                .selectAll("rect")
                .attr("height", height2)
                .attr("fill", "#E6E7E8");

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                .attr("y", 0)
                .attr("x", 420)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("")
                .style("font-size", "14px");

            var issue = svg.selectAll(".issue")
                .data(categories)
                .enter().append("g")
                .attr("class", "issue");

            issue.append("path")
                .attr("class", "line")
                .style("pointer-events", "none")
                .attr("id", function (d) {
                    return "line-" + d.name.replace(" ", "").replace("/", "");
                })
                .attr("d", function (d) {
                    return d.visible ? line(d.values) : null;
                })
                .attr("clip-path", "url(#clip)")
                .style("stroke", function (d) {
                    return color(d.name);
                });

            var legendSpace = height / categories.length;

            issue.append("rect")
                .attr("width", 10)
                .attr("height", 10)
                .attr("x", width + (margin.right / 3) - 45)
                .attr("y", function (d, i) {
                    return (legendSpace) + i * (legendSpace) - 9;
                })  // spacing
                .attr("fill", function (d) {
                    return d.visible ? color(d.name) : "#F1F1F2";
                })
                .attr("class", "legend-box")

                .on("click", function (d) {
                    d.visible = !d.visible;

                    maxY = findMaxY(categories);
                    yScale.domain([0, maxY]);
                    svg.select(".y.axis")
                        .transition()
                        .call(yAxis);

                    issue.select("path")
                        .transition()
                        .attr("d", function (d) {
                            return d.visible ? line(d.values) : null;
                        });
                    issue.select("rect")
                        .transition()
                        .attr("fill", function (d) {
                            return d.visible ? color(d.name) : "#F1F1F2";
                        });
                })

                .on("mouseover", function (d) {

                    d3.select(this)
                        .transition()
                        .attr("fill", function (d) {
                            return color(d.name);
                        });
                    d3.select("#line-" + d.name.replace(" ", "").replace("/", ""))
                        .transition()
                        .style("stroke-width", 2.5);
                })

                .on("mouseout", function (d) {

                    d3.select(this)
                        .transition()
                        .attr("fill", function (d) {
                            return d.visible ? color(d.name) : "#F1F1F2";
                        });
                    d3.select("#line-" + d.name.replace(" ", "").replace("/", ""))
                        .transition()
                        .style("stroke-width", 1.5);
                });

            issue.append("text")
                .attr("x", width + (margin.right / 3) - 30)
                .style("font-size", "13px")
                .attr("y", function (d, i) {
                    return (legendSpace) + i * (legendSpace);
                })
                .text(function (d) {
                    return d.name;
                });

            var hoverLineGroup = svg.append("g")
                .attr("class", "hover-line");

            hoverLineGroup
                .append("line")
                .attr("id", "hover-line")
                .attr("x1", 10).attr("x2", 10)
                .attr("y1", 0).attr("y2", height + 10)
                .style("pointer-events", "none")
                .style("opacity", 1e-6);

            var hoverDate = hoverLineGroup
                .append('text')
                .attr("class", "hover-text")
                .attr("y", height - (height - 40))
                .attr("x", width - 180)
                .style("fill", "#E6E7E8");

            var k = d3.keys(data[0]);
            var columnNames = [];
            for (var i = 0; i < k.length; i++) {
                if (k[i] != "date") {
                    columnNames.push(k[i]);
                }
            }

            var focus = issue.select("g")
                .data(columnNames)
                .enter().append("g")
                .attr("class", "focus");

            focus.append("text")
                .attr("class", "tooltip")
                .style("font-size", "13px")
                .attr("x", width + 190)
                .attr("y", function (d, i) {
                    return (legendSpace) + i * (legendSpace);
                });

            d3.select("#mouse-tracker")
                .on("mousemove", mousemove)
                .on("mouseout", function () {
                    hoverDate
                        .text(null);

                    d3.select("#hover-line")
                        .style("opacity", 1e-6);
                });

            function mousemove() {
                var mouse_x = d3.mouse(this)[0];
                var graph_x = xScale.invert(mouse_x);

                var format = d3.time.format('%e %b %Y');

                hoverDate.text(format(graph_x));

                d3.select("#hover-line")
                    .attr("x1", mouse_x)
                    .attr("x2", mouse_x)
                    .style("opacity", 1);

                var x0 = xScale.invert(d3.mouse(this)[0]),
                    i = bisectDate(data, x0, 1),
                    d0 = data[i - 1],
                    d1 = data[i],
                    d = x0 - d0.date > d1.date - x0 ? d1 : d0;


                focus.select("text").text(function (columnName) {
                    return (d[columnName]);
                });
            }

            function brushed() {

                xScale.domain(brush.empty() ? xScale2.domain() : brush.extent());

                svg.select(".x.axis")
                    .transition()
                    .call(xAxis);

                maxY = findMaxY(categories);
                yScale.domain([0, maxY]);

                svg.select(".y.axis")
                    .transition()
                    .call(yAxis);

                issue.select("path")
                    .transition()
                    .attr("d", function (d) {
                        return d.visible ? line(d.values) : null;
                    });

            }

            function findMaxY(data) {
                var maxYValues = data.map(function (d) {
                    if (d.visible) {
                        return d3.max(d.values, function (value) {
                            return value.rating;
                        })
                    }
                });
                return d3.max(maxYValues);
            }

            $(".context, .click_drag_instructions").mouseover(function () {
                $(".click_drag_instructions").fadeOut();
            });
        }
    }
})();