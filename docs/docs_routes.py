from logging import getLogger
from typing import List
from flask import render_template, current_app, url_for
from . import DOCS
from urllib.parse import unquote
from werkzeug.routing import Rule

logger = getLogger(__name__)


def _rule_filtering(rules: List[Rule]) -> List[Rule]:
  return [rule for rule in rules if rule.endpoint not in 'static']


def _get_list_routes() -> List[str]:
  output = []
  rules = _rule_filtering(list(current_app.url_map.iter_rules()))
  for rule in rules:
    options = {}
    for arg in rule.arguments:
      options[arg] = f"[{arg}]"
    assert rule.methods is not None
    valid_methods = [method for method in rule.methods if method not in ["OPTIONS", "HEAD"]]
    methods = ','.join(valid_methods)
    url = url_for(rule.endpoint, **options)
    line = unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
    output.append(line)
  return output


@DOCS.route('/')
def api_documentation():
  all_endpoints: List = _get_list_routes()
  spitted_end_point = [[split for split in url.split(" ") if split != ""] for url in all_endpoints]
  kwargs = {
      "endpoints": spitted_end_point
  }
  logger.info(f"[API]: Rendered API documentation with {kwargs}")
  return render_template("api_doc.html", endpoints=kwargs)
