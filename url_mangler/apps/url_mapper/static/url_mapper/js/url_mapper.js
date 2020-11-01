// prepend http:// to user-provided URLs on submit
// that don't already have a schema and invoke recaptcha
function onUrlSubmit(token) {
    var url = document.getElementById('id_destination_url');
    if ((url.value != "") && (url.value.indexOf('http://') != 0) && (url.value.indexOf('https://') != 0)) {
        url.value = "http://" + url.value
    }
    document.getElementById("id_destination_url_form").submit();
}
