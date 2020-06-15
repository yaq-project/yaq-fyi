"""Jinja format helpers."""


from jinja2 import Environment, BaseLoader


def config(k, v, container):
    s = """
    <p class="tab30">
    <b>{{ k }}</b> ({{ v["type"] }})
    {% if "default" in v.keys() %}<i>default: {{ v["default"] }}</i>{% endif %}
    <br>
    {% if "description" in v.keys() %} {{ v["description"] }} <br> {% endif %}
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


def method(k, v, container):
    s = """
    <p class="tab30">
    <b>{{ k }}</b>
    {% if "returns" in v.keys() %} ➜  {{ v["returns"] }} {% endif %}
    <br>
    {% if "description" in v.keys() %} {{ v["description"] }} <br> {% endif %}
    {% if "origin" in v.keys() %}
    <i>{{ container.format_origin(v["origin"]) }}</i> <br>
    {% endif %}
    {% if "args" in v.keys() %}
    arguments: <br>
    </p>
    {% for ak, av in v["args"].items() %}
    <p class="tab60">
        {{ ak }}, {{ av }} <br>
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
    {% if "description" in v.keys() %} {{ v["description"] }} <br> {% endif %}
    {% if "origin" in v.keys() %}
        <i>{{ container.format_origin(v["origin"]) }}</i>
    {% endif %}
    </p>
    """
    template = Environment(loader=BaseLoader).from_string(s)
    return template.render(k=k, v=v, container=container)


helpers = dict()
helpers["config"] = config
helpers["h2"] = h2
helpers["method"] = method
helpers["state"] = state
