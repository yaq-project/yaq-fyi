"""Jinja format helpers."""


from jinja2 import Environment, BaseLoader


def config(k, v, container):
    s = """
    <p class="tab30">
    <b>{{ k }}</b> ({{ v["type"] }})
    {% if "default" in v.keys() %}<i>default: {{ v["default"] }}</i>{% endif %}
    <br>
    {% if "doc" in v.keys() %} {{ v["doc"] }} <br> {% endif %}
    {% if "origin" in v.keys() %}
      <i>{{ container.format_origin(v["origin"]) }}</i>
    {% endif %}
    {% if "addendum" in v.keys() %}
      <br> <i>addendum by {{container.name}}:</i><br>
      {{ v["addendum"] }}
    {% endif %}
    </p>
    """
    template = Environment(loader=BaseLoader).from_string(s)
    return template.render(k=k, v=v, container=container)


def h2(s):
    return f"<h2 id='{s.lower()}'>{s}<a href='#{s.lower()}'> ¶</a></h2>"


def message(k, v, container):
    s = """
    <p class="tab30">
    <b>{{ k }}</b>
    {% if "response" in v.keys() %} ➜  {{ v["response"] }} {% endif %}
    <br>
    {% if "doc" in v.keys() %} {{ v["doc"] }} <br> {% endif %}
    {% if "origin" in v.keys() %}
    <i>{{ container.format_origin(v["origin"]) }}</i> <br>
    {% endif %}
    {% if v["request"] %}
    parameters: <br>
    </p>
    {% for r in v["request"] %}
    <p class="tab60">
        <b>{{ r["name"] }}</b> ({{ r["type"] }})
        {% if "default" in r.keys() %}<i>default: {{ r["default"] }}</i>{% endif %}
        <br>
        {% if "doc" in r.keys() %} {{ r["doc"] }} <br> {% endif %}
    </p>
    {% endfor %}
    {% else %} </p>
    {% endif %}
    """
    template = Environment(loader=BaseLoader).from_string(s)
    return template.render(k=k, v=v, container=container)


def state(k, v, container):
    s = """
    <p class="tab30">
    <b>{{ k }}</b> ({{ v["type"] }}) <br>
    {% if "doc" in v.keys() %} {{ v["doc"] }} <br> {% endif %}
    {% if "origin" in v.keys() %}
        <i>{{ container.format_origin(v["origin"]) }}</i>
    {% endif %}
    </p>
    """
    template = Environment(loader=BaseLoader).from_string(s)
    return template.render(k=k, v=v, container=container)


def type_(ty, container):
    s = """
    <p class="tab30">
    <b>{{ ty.name }}</b> ({{ ty["type"] }}) <br>
    {% if "default" in ty.keys() %} default: {{ ty["default"] }} <br> {% endif %}
    {% if "doc" in ty.keys() %} {{ ty["doc"] }} <br> {% endif %}
    {% if "symbols" in ty.keys() %} symbols: {{ ty["symbols"] }} <br> {% endif %}
    {% if "fields" in ty.keys() %}
    fields: <br>
        {% for f in ty["fields"] %}
        <p class="tab60">
        <b>{{ f["name"] }}</b> ({{ f["type"] }})
        {% if "default" in f.keys() %}<i>default: {{ f["default"] }}</i>{% endif %}
        <br>
        {% if "doc" in f.keys() %} {{ f["doc"] }} <br> {% endif %}
        </p>
        {% endfor %}
    {% endif %}
    {% if "origin" in ty.keys() %}
        <i>{{ container.format_origin(ty["origin"]) }}</i>
    {% endif %}
    </p>
    """
    if ty["type"] not in ("enum", "record"):
        warnings.warn(f"Unhandled type: {ty['type']}")
    template = Environment(loader=BaseLoader).from_string(s)
    return template.render(ty=ty, container=container)




helpers = dict()
helpers["config"] = config
helpers["h2"] = h2
helpers["message"] = message
helpers["state"] = state
helpers["type"] = type_
