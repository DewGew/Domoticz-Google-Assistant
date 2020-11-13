/* Main */
var config = {{ conf }}
var updates = {{ update }}

$('#notes').hide()
$('#logsheader').html('Logs <br><small>Loglevel: ' + config.loglevel + '</small>');

if (updates) {
  $('#updates').html("Updates are Availible");
  $('#notes').show()
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


$('#user').append(config.auth_user)

message = '{{ message }}'
if (message != '') {
    $('#modalLabel').html("Information!");
    $('#message').html(message);
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

function readDevices(devicelist){
    $.ajax({
      type: 'GET',
      url: '/states',
      success: function(response) {
        devicelist = JSON.parse(response)
        var xl, i, nicknames = "";
        for (i in devicelist){
            if (devicelist[i][4] == undefined) {
                devicelist[i][4] = " "
            }
            if (devicelist[i][5] == undefined) {
                nicknames = " ";
            }else{ nicknames = " <small><i>(" + devicelist[i][5] + ")</i></small>"}
            xl += "<tr><th scope='row'>" + devicelist[i][1] + "</th>"
            xl += "<td>" + devicelist[i][0] +  nicknames + "</td>";
            xl += "<td>" + devicelist[i][2] + "</td>";
            if (devicelist[i][3] == "Off" | devicelist[i][3] == "Closed"){
                xl += "<td><button type='button' class='btn btn-danger btn-sm'>" + devicelist[i][3] + "</button></td>";
            }else if (devicelist[i][3] == "On" | devicelist[i][3] == "Open" | devicelist[i][3] == "Normal"){
                xl += "<td><button type='button'class='btn btn-success btn-sm'>" + devicelist[i][3] + "</button></td>";
            }else if (devicelist[i][3] == "Mixed"){
                xl += "<td><button type='button'class='btn btn-warning btn-sm'>" + devicelist[i][3] + "</button></td>";
            }else {
                 xl += "<td><button type='button'class='btn btn-info btn-sm' disabled>" + devicelist[i][3] + "</button></td>";
            }
            xl += "<td>" + devicelist[i][4] + "</td></tr>";
        };
        if (typeof xl !== "undefined"){
            $('#deviceList_idx').html(xl.replace('undefined',''));
        }else{
            $('#modalLabel').html("Check configuration.");
            $('#message').html("Connection to Domoticz refused! Check configuration.");
            $('#messageModal').modal('show')
        };             
      },
      error: function() {
        console.log('Error, states not availible');
      }
    });    
}
readDevices()
setInterval(readDevices, 2000);

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
function getlogs(){
    var x = document.getElementById("autoScroll").checked; //if autoscrool is checked
    if(x==true){
     document.getElementById("logs").scrollTop = document.getElementById("logs").scrollHeight; //autoscroll
    }
    
    $.ajax({
      type: 'GET',
      url: '/log',
      success: function(response) {
          $("#logs").html(response);
      }
    });
}
getlogs()
setInterval(getlogs, 2000);
