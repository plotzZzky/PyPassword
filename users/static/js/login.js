function set_tabs_inactive() {
    var elements = document.getElementsByClassName('tablinks');
    for (var i in elements) {
        if (elements.hasOwnProperty(i)) {
        elements[i].id = " ";
    }
    }
}

function showLogin(tab) {
    set_tabs_inactive();
    $('#Login').show();
    $('#Signup').hide();
    tab.id = "tab-active";
}

function showSignUp(tab) {
    set_tabs_inactive();
    $('#Login').hide();
    $('#Signup').show();
    tab.id = "tab-active";
}