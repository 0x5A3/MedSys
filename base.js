const $ = name => {
    switch(name[0]){
        case '#': return document.getElementById(name.slice(1));
        default: return null;
    }
};
const input_get = elem => elem.childNodes[1].value;

const goto = ref => { window.location.href = ref; };

const request = (method, url, data, respond) => {
    let XHR = new XMLHttpRequest();

    XHR.onload = () => {
        if(XHR.status < 400){
            respond(XHR.response); 
        }
        else{
            goto("error");
        }
    };
    XHR.onerror = () => goto("error");

    XHR.open(method, url);
    XHR.responseType = "json";
    if (data){
        console.log(data);
        XHR.setRequestHeader("Content-Type", "application/json");
    }
    XHR.send(JSON.stringify(data));
};