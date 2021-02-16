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
            let data = XHR.response;
            console.log("RECIEVED ", data)
            respond(data); 
        }
        else{
            goto("error");
        }
    };
    XHR.onerror = () => goto("error");

    XHR.open(method, url);
    XHR.responseType = "json";
    if (data){
        console.log("SENDING", data);
        XHR.setRequestHeader("Content-Type", "application/json");
    }
    XHR.send(JSON.stringify(data));
};

const user_upload = (method, data, update) =>
    request("POST", method, { username: username, ...data },
        data => {
            if(data.success){ update(); }
            else{ alert("Error: ", data.reason); }
        }
    );

const goto_account = () => { goto(`/account/${username}`); };
const exit = () => { goto('/login') };