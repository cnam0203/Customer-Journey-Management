var importData = [];
var table = document.getElementById('tbl-csv-data');
var submitBtn = document.getElementById("submit-file");
var keys = ['user_id','action_type','visit_time','active_time','channel_type','browser','os','device_category','geo_continent','geo_country', 'geo_city','source_name','source_url','ad_url','ad_content','campaign_url','campaign_content','store_id','employee_id','webpage_url','webpage_title','webpage_id','app_name','app_screen','app_screen_title','app_screen_id','interract_item_id','interract_item_url','user_item_content','interract_item_content','experience_score','experience_emotion','interract_item_type','user_item_id','user_item_type','user_item_url'];

function importFile() {
    refreshUpload();
    var inputFile = document.getElementById('upload-csv').files[0];

    if (checkCSVFile(inputFile)) 
        importCSV(inputFile)
    else
        importJSON(inputFile)
}

function importCSV(inputFile) {
    Papa.parse(inputFile, {
        download: true,
        header: true,
        complete: function(results) {
            var headers = results.meta.fields;

            generateTableHead(table, keys, headers, true);

            results.data.map((data)=> {
                generateCSVData(importData, keys, data);
                generateTableRows(table, keys, data);
            }); 
        }
    });
}

function importJSON(inputFile) {
    var reader = new FileReader();
    reader.addEventListener('load', function() {
        var jsonFile = JSON.parse(reader.result);
        if (jsonFile && Array.isArray(jsonFile)) {
            var results = jsonFile;
            var matchCount = generateJSONData(results);
            
            if (matchCount > 0) {
                var msg = matchCount.toString() + " object(s) matched";

                generateTableHead(table, keys, keys, false);
                importData.map((data) => {
                    generateTableRows(table, keys, data)
                })

                showMessage(msg, 1200);
                submitBtn.style.display = "inline-block";
            }
            else
                alert("No data to import")
        }
        else
            alert("Please follow JSON File Format")
    })
    reader.readAsText(inputFile);
}

function checkCSVFile(file) {
    var fileExtension = file.name.split('.').pop();
    console.log(fileExtension);
    if (fileExtension === "csv") 
        return true;
    return false;
}

function refreshUpload() {
    importData = [];
    table.innerHTML = '';
    submitBtn.style.display = 'none';
}

function generateCSVData(importData, keys, data) {
    var newData = {};

    keys.map(field => { newData[field] = data[field] ? data[field] : null; })
    importData.push(newData);
}

function generateJSONData(results) {
    results.every((data, index) => {
        var checkAvailable = true;
        var newData = {};

        Object.keys(data).every((field) => {
            if (keys.includes(field)) {
                if (data[field] == null || typeof(data[field]) !== "object") {
                    newData[field] = data[field];
                } else {
                    var msg = "At touchpoint " + index.toString() + ", field " + field + " wrong data type";
                    checkAvailable = false;
                    alert(msg);
                    return false;
                }
                return true;
            } 
            return true;
        });

        if (!checkAvailable) {
            importData = [];
            return false;
        }
        else
            if (!isEmpty(newData)) {
                importData.push(newData);
            }
        return true;
    })

    return importData.length;
}

function generateTableHead(table, keys, headers, isCsv) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    let matchCount = 0;
    for(let field of keys) {
        let th = document.createElement('th');
    	let text = document.createTextNode(field);

        th.style.textAlign = "center";
    	th.appendChild(text);
        th.style.border = "1px solid #000000";
    	row.appendChild(th);
        if (headers.includes(field)) {
            th.style.backgroundColor = "#c8f5c1";
            matchCount += 1;
        }
    }

    if (matchCount > 0 && isCsv) {
        var msg = matchCount.toString() + " column(s) matched";

        showMessage(msg, 1200);
        submitBtn.style.display = "inline-block";
    }
}

function generateTableRows(table, keys, data) {
    let newRow = table.insertRow(-1);
    for(let field of keys) {
    	let newCell = newRow.insertCell();
        let txt = data[field] ? data[field] : null;
    	let newText = document.createTextNode(txt);

    	newCell.appendChild(newText);
        newCell.style.textAlign = "center";
        newCell.style.border = "1px solid #000000";
    }
}

function showMessage(message, time) {
    setTimeout(function() {
        alert(message);
    }, time);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

function submitData() {
    if (importData.length == 0) 
        alert("No data to import!");
    else {
        console.log(importData.length);
        console.log(importData);
        const csrftoken = getCookie('csrftoken');
        fetch('http://localhost:8000/admin/cjx/upload-file', {
            method: 'post',
            mode: 'same-origin',
            headers: {
              "Accept": 'application/json',
              "Content-type": 'application/json',
              'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({data: importData})
          })
          .then(function (response) {
                return response.json();
          })
          .then(function (data) {
                alert(data.result);
                location.reload();
          })
          .catch(function (error) {
                console.log('Request failed', error);
                // location.reload();
          });
    }
}

function validateGraphForm() {
    var startDate = Date.parse(document.forms["graphForm"]["startDate"].value);
    var endDate = Date.parse(document.forms["graphForm"]["endDate"].value);
    if (startDate > endDate) {
        alert("Start date must be earlier than end date !");
        return false;
    }
}

function validateClusterForm() {
    var startDate = Date.parse(document.forms["clusterForm"]["startDate"].value);
    var endDate = Date.parse(document.forms["clusterForm"]["endDate"].value);
    var numClusters = document.forms["clusterForm"]["numClusters"].value;
    if (startDate > endDate) {
        alert("Start date must be earlier than end date !");
        return false;
    }

    if (numClusters < 2 || numClusters > 10 || isNaN(numClusters)) {
        alert("Number of clusters must be in range (2, 10)");
        return false;
    }

}