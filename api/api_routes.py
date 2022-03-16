from typing import List
from flask import render_template, current_app, url_for, request
from . import API


def list_routes():
  output = []
  for rule in current_app.url_map.iter_rules():
    import urllib
    options = {}
    for arg in rule.arguments:
        options[arg] = "[{0}]".format(arg)
    methods = ','.join(rule.methods)
    url = url_for(rule.endpoint, **options)
    line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
    output.append(line)
  return output


@API.route('/')
def documentation():
  all_endpoints: List = list_routes()
  spitted_end_point = [[split for split in url.split(" ") if split != ""] for url in all_endpoints]
  kwargs = {
      "endpoints": spitted_end_point
  }
  return render_template("api_doc.html", endpoints=kwargs)
