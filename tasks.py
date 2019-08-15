import os

from invoke import Collection, tasks
from invoke.util import LOG_FORMAT

from action.vote import command as vote_cmd
from recipe import command as recipe_cmd

def add_tasks_in_module(mod, ns):
    functions = [(name, val) for name, val in mod.__dict__.items() if callable(val)]
    for (name, method) in functions:
        # only add the method if it's of type invoke.tasks.Task
        if type(method) == tasks.Task:
            ns.add_task(method, name)
    return ns

vote_ns = add_tasks_in_module(vote_cmd, Collection('vote'))
recipe_ns = add_tasks_in_module(recipe_cmd, Collection('recipe'))

ns = Collection(
    vote_ns,
    recipe_ns
)

ns.configure({'conflicted': 'default value'})
