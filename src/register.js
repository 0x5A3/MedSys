const [password, confirm] = [$("#password"), $("#password-confirm")];

const not_match = (msg, exclude) => 
    (chr => {
        if(exclude.includes(chr)){
            return `Cannot contain ${msg}`;
        }
        return "";
    });

const not_bracket = not_match("brackets", "(){}[]");
const not_space = not_match("spaces", " \n\r\t");
const not_caps = not_match("caps", "ABCDEFGHIJKLMNOPQRSTUVWXYZ");

const not_op = not_match("special characters", "+-*/<=>\\^%~!&|\"`',:;#$?");
const not_misc = not_match("special characters", "@.");

const not_lst_email = [not_bracket, not_space, not_op];
const not_lst_special = not_lst_email.concat([not_misc]);
const not_number = not_match("numbers", "0123456789");

const constrain_field = {
    "#username": [not_space, not_caps].concat(not_lst_special), 
    "#email": [not_space].concat(not_lst_email),
    "#name_first": [not_space, not_number].concat(not_lst_special), 
    "#name_last": [not_space, not_number].concat(not_lst_special)
};

for(const id in constrain_field){
    const field = $(id);  

    field.childNodes[1].onkeydown = () => {
        for(let id in constrain_field){
            $(id).childNodes[2].innerHTML = "";
        }

        for(const check of constrain_field[id]){
            msg = check(event.key);
            if(msg.length > 0){
                field.childNodes[2].innerHTML = msg;
                event.preventDefault();
                break;
            }
        }
    };
}


const password_match = () => {
    if(input_get(password) === input_get(confirm)){
        confirm.childNodes[2].innerHTML = "";
    }
    else{
        confirm.childNodes[2].innerHTML = "error passwords dont match";
    }
}

const set_check = (node, fn) =>
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
                console.log(data);
                if(!data.success){
                    $(`#${data.div_id}`).childNodes[2].innerHTML = data.reason;
                }
                else{
                    console.log("GOING!");
                    goto("login");
                }
            }
        )
    }
};