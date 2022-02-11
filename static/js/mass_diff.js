$(document).ready(function () {
    function calc() {
        var out = 0;
        var rm = 0;
        var n = 0;
        var fg_weight = 0;
        var rm_weight = 0;

        var fg = $("input[name^='detailproductionresults_set'][name$='hasil_jadi_qty']");
        var hd = $("input[name^='detailproductionresults_set'][name$='hold_qc_qty']");
        var bu = $("input[name^='detailproductionresults_set'][name$='berat_unit_sample']");
        var rj = $("input[name^='detailproductionresults_set'][name$='reject']");
        var tr = $("input[name^='detailproductionresults_set'][name$='trimming']");
        var ws = $("input[name^='detailproductionresults_set'][name$='waste']");

        fg = _.map(fg, 'value').map(i => Number(i));
        hd = _.map(hd, 'value').map(i => Number(i));
        bu = _.map(bu, 'value').map(i => Number(i));
        rj = _.map(rj, 'value').map(i => Number(i));
        tr = _.map(tr, 'value').map(i => Number(i));
        ws = _.map(ws, 'value').map(i => Number(i));

        var rm_init = $("input[name^='detailmaterialconsumption_set'][name$='qty_awal']");
        var rm_add = $("input[name^='detailmaterialconsumption_set'][name$='qty_tambahan']");
        var rm_fin = $("input[name^='detailmaterialconsumption_set'][name$='qty_akhir']");

        rm_init = _.map(rm_init, 'value').map(i => Number(i));
        rm_add = _.map(rm_add, 'value').map(i => Number(i));
        rm_fin = _.map(rm_fin, 'value').map(i => Number(i));

        /* Calculate FG */

        var i;
        for (i = 0; i < fg.length; i++) {
            fg_weight += bu[i] * fg[i];
        }
        fg_weight = fg_weight.toFixed(2);
        $("#fg_weight").val(fg_weight);
        
        /* Calculate RM */

        for (i = 0; i < rm_init.length; i++) {
            rm_weight += rm_init[i] + rm_add[i] - rm_fin[i];
        }
        rm_weight = rm_weight.toFixed(2);
        $("#rm_weight").val(rm_weight);

        /* Calculate Difference */
        for (i = 0; i < fg.length; i++) {
            out += bu[i] * (fg[i] + hd[i]) + rj[i] + tr[i] + ws[i];
        }
        
        for (i = 0; i < rm_init.length; i++) {
            rm += rm_init[i] + rm_add[i] - rm_fin[i];
        }
        n = (rm - out).toFixed(2);
        $("#selisih").val(n);
        
        /* Production Time */
        var initialTime = $("input[name^='start_time_']");
        var initialTimeDate = moment(initialTime[0].value, "DDMMYYYY");
        var initialTimeHr = moment(initialTime[1].value, "h:mm:ss");
        var endTime = $("input[name^='end_time_']");
        var endTimeDate = moment(endTime[0].value, "DDMMYYYY");
        var endTimeHr = moment(endTime[1].value, "h:mm:ss");
        var totalHours = endTimeDate.diff(initialTimeDate,"minutes") + endTimeHr.diff(initialTimeHr,"minutes");
        totalHours = (totalHours / 60).toFixed(2)
        $("#durasi").val( totalHours + " Jam");
        
        /* Downtime */
        var downtime_start = $("input[name^='detaildowntime_set-'][name$='-waktu_mulai']").not("[name*='__prefix__']");
        var downtime_end = $("input[name^='detaildowntime_set-'][name$='-waktu_selesai']").not("[name*='__prefix__']");
        var downtimeHours
        var downtimeStartObj
        var downtimeEndObj
        var downtimeTotal = 0
        for (i = 0; i < downtime_start.length; i++) {
            downtimeStartObj = moment(downtime_start[i].value, "h:mm:ss")
            downtimeEndObj = moment(downtime_end[i].value, "h:mm:ss")
            downtimeHours = downtimeEndObj.diff(downtimeStartObj, "minutes");
            if (downtimeHours < 0){
                downtimeHours += 24*60
            }
            downtimeTotal += downtimeHours
        }
        downtimeTotal = (downtimeTotal / 60).toFixed(2)
        $("#downtime").val( downtimeTotal + " Jam");

        $("#efektif").val( (totalHours - downtimeTotal) + " Jam");
    }
    $("body").keyup(calc);
    window.onload = calc
});
