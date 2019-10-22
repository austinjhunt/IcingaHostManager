$(document).ready(function () {
    $("#body").fadeIn();
    $("#loader").fadeOut();
    $("#whitebg").fadeOut();
    $("#checksTable").DataTable();
    $("#checksTable2").DataTable();
    $("#availablefields").DataTable({
        "order": [[ 2, "desc" ]]
    });
    $('#checksTable tbody').on( 'click', 'tr', function () {

        var selectedcheck = $($(this).children()[0]).html();
        console.log(selectedcheck);
        // if going from unselected -> selected, append to container, else remove
        if (!$(this).hasClass('selected')) {
            var newcheck = $("<div></div>").addClass("selectedcheck").html(selectedcheck);
            $(".selectedcheckscontainer").append(newcheck);
            $("#checks_to_execute").val($("#checks_to_execute").val() + "," + selectedcheck);
        }
        else {
            // remove selectedcheck in container matching selectedcheck
            $(".selectedcheckscontainer .selectedcheck:contains(\"" + selectedcheck + "\")").remove();
            deleteValue("," +selectedcheck,"checks_to_execute");
        }
        console.log("New checks val: " + $("#checks_to_execute").val());
        $(this).toggleClass('selected');
    } );


    $('#edithoststable tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
        console.log($(this).hasClass('selected'));
        $($(this).siblings()).each(function(i,row){
            $(row).removeClass('selected');
        });
    } );
});

const TOTALNUMFIELDS = 16;

function showedithostmodal(){
    var hostid = $("#edithoststable tbody tr.selected").attr('id');
    $("#host_id").val(hostid);
    var value_array = [];
    $("#edithoststable tbody tr.selected td").each(function(i,cell){
        value_array.push($(cell).html());
    });

    $("#edithostmodal input[type!='hidden']").each(function(i, inputfield){
        var val = value_array[i];
        if (val === "True" || val === "False"){
            $(inputfield).attr('type','checkbox');
            if (val == "True"){
                $(inputfield).prop('checked',true);
            } else{
                $(inputfield).prop('checked',false);
            }
        }
       $(inputfield).val(value_array[i]);
    });
    $("#edithostmodal").modal('show');
    for (var i = 0 ; i < TOTALNUMFIELDS; i ++){ // TOTALNUMFIELDS fields total
        if (i >= 6){
            var column = edithoststable.column(i);
             column.visible(false);
        }
    }


}
function modal_prep_work(_callback){
    // enable all columns so no values are missed first.
    // for each column
    console.log(edithoststable);
    for (var i = 0; i < TOTALNUMFIELDS; i ++){
        var column = edithoststable.column(i);
        column.visible(true);
    }

    // after doing above, now execute callback
    _callback();
}


// add replaceAll func to String object to remove all occurences of specific text (e.g. removing strings from textarea
(function() {
    if (!String.replaceAll) {
        String.prototype.replaceAll = function replaceAll(replace, value) {
            return this.replace(new RegExp(replace, 'g'), value);
        };
}
}());
// And modify delete function should look like this:

function deleteValue(strtoremove,textareaid) {
    var textarea = document.getElementById(textareaid);
    var data = textarea.value;
    textarea.value = textarea.value.replaceAll(strtoremove, "");
}

function openbulkuploadform(){
    $("#singlehostformcontainer").fadeOut();
    $("#bulkuploadformcontainer").fadeIn();

}
function openaddhostform(){
    $("#singlehostformcontainer").fadeIn();
    $("#bulkuploadformcontainer").fadeOut();
}

function toggleconfirmpage(btn){
    $("#successfulhosts").toggle('slow');
    $("#failedhosts").toggle('slow');
    $(btn).toggleClass("showfailed showsuccess");
}

