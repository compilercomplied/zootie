

import json
import click
import requests

from pathlib import Path
from datetime import datetime
from os.path import expanduser, exists, join
import sys


__home = expanduser("~")

DEFAULT_CFG_PATH = join(__home, ".zootie.json")

ZOHO_BASE = r"http://people.zoho.eu/people/api"
TIMELOG_URI = f"{ZOHO_BASE}/timetracker/addtimelog"


def post_task(task: dict, fixed_params: str):

  input_workdate = task.get("workDate")

  job_id         = task.get("jobID")
  hours          = task.get("hours")
  from_time      = task.get("fromTime")
  to_time        = task.get("toTime")
  billing_status = task.get("billingStatus")
  taskname       = task.get("name")
  work_date      = input_workdate if  input_workdate is not None else datetime.today().strftime('%Y-%m-%d')

  uri = f"{TIMELOG_URI}?{fixed_params}&jobId={job_id}&hours={hours}&workDate={work_date}&billingStatus={billing_status}"

  if (from_time is not None):
    uri += f"&fromTime={from_time}"

  if (to_time is not None):
    uri += f"&toTime={to_time}"

  print(f"Checking in job: {taskname} for date: {work_date}")
  resp = requests.post(uri)
  print(resp.json())

def parse_cfg(path: str) -> dict:

  if not exists(path):
    print(f"Config file not found: {path}")
    sys.exit(1)

  with(open(path, 'r')) as cfgfile:
    return json.load(cfgfile)


@click.command()
@click.option("-f", default=DEFAULT_CFG_PATH, help="Config file location")
@click.option("-c", default=None            , help="Context to load")
@click.option("-s", is_flag=True            , help="Show available contexts")
def cli(f, c, s):

  zoot = parse_cfg(f)

  if s:
    print(json.dumps(zoot.get("ctxt"), indent=2, sort_keys=True))
    return


  if c:
    filtered = filter( lambda _: _.get("name") == c, zoot.get("ctxt") )
    ctxt = list(filtered)[0]
  else:
    ctxt = zoot.get("ctxt")[0]

  token    = zoot.get("token")
  user_id  = zoot.get("userID")
  ctxtname = ctxt.get("name")
  tasks    = ctxt.get("tasks")

  if tasks is None:
    print(f"No tasks found for context: {ctxtname}")
    sys.exit(1)

  fixed_params =  f"authtoken={token}&user={user_id}"

  [post_task(task, fixed_params) for task in tasks]


if __name__ == "__main__":
  cli()
