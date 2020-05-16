{% if not obj.display %}
:orphan:
{% endif %}

:mod:`{{ obj.name }}`
======={{ "=" * obj.name|length }}

.. automodule:: {{ obj.name }}
    :members:
    :ignore-module-all:

{% block subpackages %}
{% set visible_subpackages = obj.subpackages|selectattr("display")|list %}
{% if visible_subpackages %}
Subpackages
-----------

.. toctree::
    :titlesonly:
    :maxdepth: 2

{% for subpackage in visible_subpackages %}
    {{ subpackage.short_name }}/index.rst
{% endfor %}


{% endif %}
{% endblock %}

{% block submodules %}
{% set visible_submodules = obj.submodules|selectattr("display")|list %}
{% if visible_submodules %}


{{ obj.name }} Submodules
{{ "-" * obj.name|length }}------------

.. toctree::
    :titlesonly:
    :maxdepth: 1

{% for submodule in visible_submodules %}
    {{ submodule.short_name }}/index.rst
{% endfor %}

{% endif %}
{% endblock %}

{% block content %}
{% endblock %}
