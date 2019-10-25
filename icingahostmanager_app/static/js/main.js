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
        /* Allow multiple selection.
        console.log($(this).hasClass('selected'));

        $($(this).siblings()).each(function(i,row){
            $(row).removeClass('selected');
        });*/
    } );
});

const TOTALNUMFIELDS = 16;

function showedithostmodal(){
    $("#edithostsmodal_table_body").empty();
    // for each host, get the properties to fill the table in the modal.
    $("#edithoststable tbody tr.selected").each(function(index,hostrow){
        var rowcopy = $(hostrow).clone().prop('id','edithostsmodal_host_id_' + $(hostrow).attr('id'));
        $($(rowcopy).children()).each(function(i,c){
            $(c).prop('contenteditable','true');
        });
        $("#edithostsmodal_table_body").append(rowcopy);
    });
    $("#edithostmodal").modal('show');
    /* Return original table to simpler view, don't show every column; */
    for (var i = 0 ; i < TOTALNUMFIELDS; i ++){ // TOTALNUMFIELDS fields total
        if (i >= 6){
            var column = edithoststable.column(i);
             column.visible(false);
        }
    }
}

function edit_hosts(){
    // create json dict of host id : { k : val, k: val...}
    var hosts = {};
    var hostid;
    var fields = [];
    $("#edithostsmodal_table thead th").each(function(i,heading){
        fields.push($(heading).html())
    });

    $("#edithostsmodal_table_body tr").each(function(index, row){
        hostid = $(row).attr('id');
        hosts[hostid]= {};
        $($(row).children()).each(function(i,cell){
            hosts[hostid][fields[i]] = $(cell).html();
        });
    });
    console.log(hosts);
    $.ajax({
        url: "/edit_hosts/",
        type: "POST",
        data: {
            'hosts': JSON.stringify(hosts),
        },
        dataType: 'json',
        success: function(data){
            if (data['res'] == 'success')
                $("#edithostmodal .modal-body").html("<h4 style='color:green'>Your hosts were edited successfully!</h4>");
            else
                $("#edithostmodal .modal-body").html("<h4 style='color:red'>Edits were not successful.</h4>");
            setTimeout(function(){
                    window.location.href = "/";
            }, 2000);

        }
    });
}
function showdeletehostmodal(){
    $("#deletehostsmodal_table_body").empty();
    $("#edithoststable tbody tr.selected").each(function(index,hostrow){
       var rowcopy = $(hostrow).clone().prop('id','deletehostsmodal_host_id_' + $(hostrow).attr('id'));
       $("#deletehostsmodal_table_body").append(rowcopy);
    });
    $("#deletehostmodal").modal('show');
    for (var i = 0 ; i < TOTALNUMFIELDS; i ++){ // TOTALNUMFIELDS fields total
        if (i >= 6){
            var column = edithoststable.column(i);
             column.visible(false);
        }
    }
}
function delete_hosts(){
    // create json dict of host id : { k : val, k: val...}
    var hosts_to_delete = [];
    var hostid;
    $("#deletehostsmodal_table_body tr").each(function(index, row){
        hostid = $(row).attr('id');
        hosts_to_delete.push(hostid);
    });
    console.log(hosts_to_delete);
    $.ajax({
        url: "/delete_hosts/",
        type: "POST",
        data: {
            'hosts_to_delete': JSON.stringify(hosts_to_delete),
        },
        dataType: 'json',
        success: function(data){
            if (data['res'] == 'success')
                $("#deletehostmodal .modal-body").html("<h4 style='color:green'>Your hosts were deleted successfully!</h4>");
            else
                $("#deletehostmodal .modal-body").html("<h4 style='color:red'>Deletions were not successful.</h4>");
            setTimeout(function(){
                    window.location.href = "/";
            }, 2000);

        }
    });
}
function modal_prep_work(_callback){
    // enable all columns so no values are missed first.
    // for each column

    if ($(".dataTable tr.selected").length == 0) {
        alert("You need to select at least one host first!")
        return;
    }
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
