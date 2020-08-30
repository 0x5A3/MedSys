const password = $("#password");
const confirm = $("#password-confirm");

confirm.childNodes[1].oninput = _ => {
    if(input_get(password) === input_get(confirm)){
        confirm.childNodes[2].innerHTML = "";
    }
    else{
        confirm.childNodes[2].innerHTML = "error passwords dont match";
    }
};

const register = () => {
    const pass = input_get(password);
    const conf = input_get(confirm);

    if(pass === conf){
        request("POST", "$register",
            {
                username: input_get($("#username")),
                password: pass,
                email: input_get($("#email"))
            },
            data => { 
                if(!data.success){
                    confirm.childNodes[2].innerHTML = data.reason;
                }
                else{
                    goto("login");
                }
            }
        )
    }
};