
def make_prop(prop):
    prop_lst = ""
    for key, value in prop.items():
        prop_lst += f' {key}="{value}"'
    return prop_lst


def leaf(name, prop={}):
    return f"<{name}{make_prop(prop)}/>"


def node(name, inner=[], prop={}):
    return f"<{name}{make_prop(prop)}>{''.join(inner)}</{name}>"


def div(inner, prop={}):
    return node("div", inner, prop)


def span(inner, prop={}):
    return node("span", inner, prop)


def text_input(text, in_type="text", div_id="", style="", onkeydown="", value=""):
    return div([
        div([text]),
        leaf("input", {
            "type": in_type,
            "onkeydown": onkeydown,
            "value": value
        }),
        span([])],
        {"id": div_id, "class": "form" + style}
    )


def button(text, onclick="", style=""):
    return leaf("input", {
        "value": text,
        "type": "submit",
        "class": "button " + style,
        "onclick": onclick
    })


def title(name):
    return node("header", name, {
        "style": "font-size: 150%; margin: 5%"
    })


def subtitle(name):
    return node("header", name, {
        "style": "font-size: 100%; margin: 5%"
    })


def card(body, styleclass="card"):
    return node("div", body, {"class": styleclass})


def html_files(path_lst, node_type):
    lst = []
    for path in path_lst:
        try:
            with open(path) as file:
                lst.append(node(node_type, file.read()))
        except:
            pass
    return lst


def page(title, body="", scripts=[], css=[]):
    return "<!DOCTYPE html>" + node("html", [
        node("head", [
            leaf("meta", {"charset": "utf-8"}),
            node("title", [title]),
            node("link", prop={
                "href": "https://fonts.googleapis.com/css2?family=Noto+Sans&display=swap",
                "rel": "stylesheet"
            })
        ] + html_files(css, "style")),
        node("body", body + html_files(scripts, "script"))
    ])
