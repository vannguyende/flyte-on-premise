

"""
.. _launchplan_schedules:
Scheduling Workflows Example
-----------------------------
:ref:`flyte:divedeep-launchplans` can be set to run automatically on a schedule using the Flyte Native Scheduler.
For workflows that depend on knowing the kick-off time, Flyte supports passing in the scheduled time (not the actual time, which may be a few seconds off) as an argument to the workflow.
Check out a demo of how the Native Scheduler works:
.. youtube:: sQoCp2qSQK4
.. note::
  Native scheduler doesn't support `AWS syntax <http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions>`__.
"""

# %%
# Consider the following example workflow:
from datetime import datetime

from flytekit import task, workflow, Slack, WorkflowExecutionPhase, Email


@task
def format_date(run_date: datetime) -> str:
    return run_date.strftime("%Y-%m-%d %H:%M")


@workflow
def date_formatter_wf(kickoff_time: datetime):
    formatted_kickoff_time = format_date(run_date=kickoff_time)
    print(formatted_kickoff_time)


# %%
# The `date_formatter_wf` workflow can be scheduled using either the `CronSchedule` or the `FixedRate` object.
#
# Cron Schedules
# ##############
#
# `Cron <https://en.wikipedia.org/wiki/Cron>`_ expression strings use this :ref:`syntax <concepts-schedules>`.
# An incorrect cron schedule expression would lead to failure in triggering the schedule.
from flytekit import CronSchedule, LaunchPlan  # noqa: E402

# creates a launch plan that runs every minute.
cron_lp = LaunchPlan.get_or_create(
    name="my_cron_scheduled_lp",
    workflow=date_formatter_wf,
    schedule=CronSchedule(
        # Note that the ``kickoff_time_input_arg`` matches the workflow input we defined above: kickoff_time
        # But in case you are using the AWS scheme of schedules and not using the native scheduler then switch over the schedule parameter with cron_expression
        schedule="*/1 * * * *",  # Following schedule runs every min
        kickoff_time_input_arg="kickoff_time",
    ),
    notifications=[
        Email(
            phases=[WorkflowExecutionPhase.FAILED],
            recipients_email=["vannh@galaxy.com.vn"],
        ),
        Email(
            phases=[WorkflowExecutionPhase.SUCCEEDED],
            recipients_email=["vannh@galaxy.com.vn"],
        ),
        Slack(
            phases=[
                WorkflowExecutionPhase.SUCCEEDED,
                WorkflowExecutionPhase.ABORTED,
                WorkflowExecutionPhase.TIMED_OUT,
            ],
            recipients_email=["vannh@galaxy.com.vn"],
        ),
    ],
)