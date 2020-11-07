/* Main */
var config = {{ conf }}
var updates = {{ update }}
document.getElementById("logsheader").innerHTML = 'Logs <br><small>Loglevel: ' + config.loglevel + '</small>';
if (updates) {
  document.getElementById("updates").innerHTML = "(Updates are Availible)";
  $('#buttonUpdate').append('<br><form action="/settings" method="post"><button class="btn btn-block btn-primary" name="update" value="update"><i class="material-icons" style="vertical-align: middle;">system_update_alt</i> Update dzga</button></form>');
};

// Add Active Class to Current Element sidebar
var btnContainer = document.getElementById("sidebar");
var btns = btnContainer.getElementsByClassName("nav-item");
for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    if (current.length > 0) {
      current[0].className = current[0].className.replace(" active", "");
    }
    this.className += " active";
  });
}

if (config.auth_user == 'admin' || config.auth_pass == 'admin'){
    $('#messageModal').modal('show')
};
message = '{{ message }}'
if (message != '') {
    document.getElementById("modalLabel").innerHTML = "Information!";
    document.getElementById("message").innerHTML = message;
    $('#messageModal').modal('show')
};

/* Device page */
function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("deviceTable");
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TD")[n];
          y = rows[i + 1].getElementsByTagName("TD")[n];
          if (dir == "asc") {
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
              shouldSwitch = true;
              break;
            }
          } else if (dir == "desc") {
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
              shouldSwitch = true;
              break;
            }
          }
        }
        if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount ++;
        } else {
          if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
          }
        }
    }
}
function sortIdxTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("deviceTable");
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TH")[n];
          y = rows[i + 1].getElementsByTagName("TH")[n];
          if (dir == "asc") {
            if (Number(x.innerHTML) > Number(y.innerHTML)) {
              shouldSwitch = true;
              break;
            }
          } else if (dir == "desc") {
            if (Number(x.innerHTML) < Number(y.innerHTML)) {
              shouldSwitch = true;
              break;
            }
          }
        }
        if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount ++;
        } else {
          if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
          }
        }
    }
}

function readDevices(){
    var devicelist = {{ list }}

    var xl, i, nicknames = "";
    for (i in devicelist){
        if (devicelist[i][4] == undefined) {
            devicelist[i][4] = " "
        }
        if (devicelist[i][5] == undefined) {
            nicknames = " ";
        }else{ nicknames = " <small><i>(" + devicelist[i][5] + ")</i></small>"}
        xl += "<tr><th scope='row'>" + devicelist[i][1] + "</th><td>" + devicelist[i][0] +  nicknames + "</td><td>" + devicelist[i][2] + "</td><td>" + devicelist[i][3] + "</td><td>" + devicelist[i][4] + "</td></tr>";
    };
    if (typeof xl !== "undefined"){
        $('#deviceList_idx').html(xl.replace('undefined',''));
    }else{
        document.getElementById("modalLabel").innerHTML = "Check configuration.";
        document.getElementById("message").innerHTML = "Connection to Domoticz refused! Check configuration.";
        $('#messageModal').modal('show')
    };    
}
readDevices()

/* config page */
var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    mode: "yaml",
    autoRefresh:true
});
editor.setOption("extraKeys", {
  Tab: function(cm) {
    var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
    cm.replaceSelection(spaces);
  }
});
editor.on("change", function() {
    textTosave = editor.getValue();
    document.getElementById("save").value = textTosave;
 });
 
document.getElementById("save").value = document.getElementById("code").value
 
/* Logs page */
function readTextFile(){
    var x = document.getElementById("autoScroll").checked; //if autoscrool is checked
    if(x==true){
     document.getElementById("logs").scrollTop = document.getElementById("logs").scrollHeight; //autoscroll
    }

    var filePath = "/log"

    $.ajax({
    dataType: "text",
    success : function (data) {
            $("#logs").load(filePath);
            }
    });

}
readTextFile()
setInterval(readTextFile, 5000);
