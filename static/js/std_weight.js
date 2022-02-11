$(document).ready(function () {
    function wt_update() {
        var row_id = this.id.match(/\d+/)[0];
        var item_name = this.options[this.selectedIndex].innerText;
        var item_wt = item_name.match(/((?:\d*\.)?\d+)(?!.*((?:\d*\.)?\d+))/)[0]
        var wt_field = "detailproductionresults_set-" + row_id + "-berat_unit_sample"
        $("input[name="+wt_field+"]").val(item_wt);
        console.log("row_id"); 
    }

    function trigger_update(){
        $("select[name^='detailproductionresults_set'][name$='produk']").on("change", wt_update)
    }
    $("#detailproductionresults_set-group").click(trigger_update)
});
