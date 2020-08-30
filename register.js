const [password, confirm] = [$("#password"), $("#password-confirm")];

let password_match = () => {
    if(input_get(password) === input_get(confirm)){
        confirm.childNodes[2].innerHTML = "";
    }
    else{
        confirm.childNodes[2].innerHTML = "error passwords dont match";
    }
}

let set_check = (node, fn) =>
    node.childNodes[1].oninput = () => {
        const [value, error] = fn(node.childNodes[1].value);
        node.childNodes[2].innerHTML = error;
        node.childNodes[1].value = output
    };

password.childNodes[1].oninput = password_match
confirm.childNodes[1].oninput = password_match;

const register = () => {
    const pass = input_get(password);
    const conf = input_get(confirm);

    if(pass === conf){
        request("POST", "$register",
            {
                username: input_get($("#username")),
                password: pass,
                email: input_get($("#email")),
                name_first: input_get($("#name_first")),
                name_last: input_get($("#name_last")),
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