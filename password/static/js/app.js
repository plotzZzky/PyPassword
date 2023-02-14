function getProps(name) {
    $.get("/pwd/props/name=" + name + "/", function(data) {
        $("#propView").html(data)
    })
}

function PwdData(title) {
    let new_title = $("#titleInput").val()
    let username = $("#usernameInput").val()
    let pwd = $("#passwordInput").val()
    let url = $("#urlInput").val()
    data = {
        title: title,
        new_title: new_title,
        username: username,
        password: pwd,
        url: url,
    }
    return data
}

function savePassword(title) {
    data = PwdData(title)
    $.post("/pwd/new/", data, function(data, status) {
    if (status == 'success') {
        $("#propView").html("")
        getPwdList()
    } else { alert("Formulario incorreto!")}
    })
}

function deletePassword() {
    let title = $("#titleInput").val()
    $.get("/pwd/del/name=" + title + "/", function() {
        $("#propView").html("")
        getPwdList()
    })
}

function getPwdList() {
    $.get("/pwd/list/", function(data) {
        $("#appBar").html(data)
    })

}

function downloadDB() {
    $.get("/pwd/download/")
}