/**
 * Copyright (c) 2021 José Hbez. All rights reserved 
 */
(function ($) {

    function GetHistorical (){
        $("#request-container").hide();
        $("#start-container").show();

        var hc = document.getElementById('historical-chart');
        if (hc !== null){
            var ctx = hc.getContext('2d');
            fetch('/api/historical').then( response => response.json()).then( data=>{                
                if (data.success == true){
                    var hcConfig = {
                        type: 'line',
                        data: {
                            labels: data.payload.labels,
                            datasets:data.payload.datasets
                        },
                        options: {
                            responsive: true,
                            title: {
                                display: true,
                                text: 'Histórico'
                            },
                            tooltips: {
                                mode: 'index',
                                intersect: false,
                            },
                            hover: {
                                mode: 'nearest',
                                intersect: true
                            },
                            scales: {
                                xAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Día'
                                    }
                                }],
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Valor'
                                    }
                                }]
                            }
                        }
                    };
                    new Chart(ctx, hcConfig);
                    ShowAlert(null)
                }else{
                    ShowAlert(data.message);
                }
            }).catch((error)=>{
                console.error(error)
            });
        }
    }

    function CleanBySerie( from ){
        $("#rc-min-max-avg").hide();
        $("#rc-min").text(0)
        $("#rc-max").text(0)
        $("#rc-avg").text(0)

        if (from === "menu"){
            $("#rc-date-from").val("");
            $("#rc-date-to").val("");
        }
        
    }
    function GetBySerie(menu, from){
        
        CleanBySerie(from);

        var path = null; 
        var title = null; 
        var showMinMaxAvg = true;
        
        

        if ( menu ===  "DOLAR"){
            title = "Tipo de Cambio";
            path = "/api/dollar";            
        }else if ( menu ===  "UDIS"){
            title ="Valor de UDIS";
            path ="/api/udis"
        }else if ( menu ===  "TIIE"){
            title ="Tasas de Interés Interbancarias";
            path ="/api/tiie";
            showMinMaxAvg = false;

        }else{
            return 0 
        }
        
        var getMinMaxAvg = function(arr) {
            var max = arr[0];
            var min = arr[0];
            var sum = arr[0]; 
            for (var i = 1; i < arr.length; i++) {
                if (arr[i] > max) {
                    max = arr[i];
                }
                if (arr[i] < min) {
                    min = arr[i];
                }
                sum = sum + arr[i];
            }
            return [ min, max, sum/arr.length]; 
        }

        $("#start-container").hide();
        $("#request-container").show();
        $("#rc-content-chart").hide();        
    
        $("#rc-title").text(title);

        var rc = document.getElementById('request-chart');

        if (rc !== null){

            var ctx = rc.getContext('2d');
            ctx.clearRect(0, 0, rc.width, rc.height);
            
            fetch(path,{
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    "X-CSRFToken":$("input[name='csrfmiddlewaretoken']").val(),
                },
                method: 'POST', 
                body: JSON.stringify({
                    'dt-from': $("#rc-date-from").val(),
                    'dt-to':$("#rc-date-to").val(),
                })
            }).then( response => response.json()).then( data=>{                
                
                if (data.success == true){
                    
                    $("#rc-content-chart").show();

                    if (showMinMaxAvg){
                        if (data.payload.datasets.length>0){
                            $("#rc-min-max-avg").show();
                            var valMinMaxAvg = getMinMaxAvg(data.payload.datasets[0].data)
                            var decPart = (valMinMaxAvg[0]+"").split(".")[1];
                            $("#rc-min").text(valMinMaxAvg[0])
                            $("#rc-max").text(valMinMaxAvg[1])
                            $("#rc-avg").text(valMinMaxAvg[2].toFixed(decPart.length))
                        }
                    }
                    var rcConfig = {
                        type: 'line',
                        data: {
                            labels: data.payload.labels,
                            datasets:data.payload.datasets
                        },
                        options: {
                            responsive: true,
                            //title: {
                            //    display: true,
                            //    text: title
                            //},
                            tooltips: {
                                mode: 'index',
                                intersect: false,
                            },
                            hover: {
                                mode: 'nearest',
                                intersect: true
                            },
                            scales: {
                                xAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Día'
                                    }
                                }],
                                yAxes: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Valor'
                                    }
                                }]
                            }
                        }
                    };
                    
                    new Chart(ctx, rcConfig);
                    ShowAlert(null)
                }else{
                    ShowAlert(data.message)
                }
            }).catch((error)=>{
                console.error( error)
            });

        }
    }

    function ShowAlert(msg){
        if (msg === null){
            $(".alert").hide();
        }else{
            $("#alert-message").text(msg);
            $(".alert").show();
        }
    }
    $(document).ready(function () {
        ShowAlert(null)
        GetHistorical();
        $('.nav-item').on('click', function (e) {
            e.preventDefault();
            var menu = this.innerText;
            if (menu ===  "INICIO"){
                GetHistorical();
            }else{
                GetBySerie(menu, "menu");
            }
            $('.nav-item').removeClass('active');
            var athis = this;
            $(athis).addClass('active');

        });        
        $('#rc-button').on('click', function (e) {
            e.preventDefault();
            $.each( $('.nav-item'), function( key, value ) {
                if ($(value).hasClass('active')){
                    GetBySerie(value.innerText,"button");
                }
            });
        });
        
    });

})(window.jQuery);