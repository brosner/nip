#!/usr/bin/env python
import optparse
import os
import shutil
import subprocess
import sys


if "NIP_ENV_DIR" not in os.environ:
    ENV_DIR = os.path.expanduser("~/.nipenvs")
else:
    ENV_DIR = os.environ["NIP_ENV_DIR"]


class CommandDispatcher(object):
    
    def __init__(self, args, **kwargs):
        self.commands = {}
        self.args = args
        self.context = kwargs.get("context")
        self.env = kwargs.get("env")
        self.parser = optparse.OptionParser()
        self.parser.disable_interspersed_args()
    
    def add(self, klass, wrapper=None):
        self.commands[klass.name] = (klass, wrapper)
    
    def dispatch(self):
        options, args = self.parser.parse_args(self.args)
        if not args:
            self.error("You must provide a command.")
        command = args[0]
        if not command in self.commands:
            self.error("Unknown command: '%s'" % command)
        klass, wrapper = self.commands[command]
        command_instance = klass(args[1:],
            env = self.env,
            wrapper = wrapper,
        )
        if hasattr(command_instance, "setup_dispatcher"):
            dispatcher = CommandDispatcher(args[1:],
                env = self.env,
                context = command_instance.context(),
            )
            command_instance.setup_dispatcher(dispatcher)
            dispatcher.dispatch()
        else:
            command_instance.pre_run()
            command_instance.run()
    
    def error(self, msg):
        sys.stderr.write("%s%s\n" % (build_context(self.context), msg))
        sys.exit(1)


class Command(object):
    require_env = False
    ensure_env_exists = False
    
    def __init__(self, args, **kwargs):
        self.args = args
        self.wrapper = kwargs.get("wrapper")
        self.env = kwargs.get("env")
    
    def pre_run(self):
        ensure_env_exists = self.ensure_env_exists
        if self.require_env:
            ensure_env_exists = True
            if not self.env:
                self.error("You must in an environment to install.")
        if ensure_env_exists and self.env:
            env_dir = os.path.join(ENV_DIR, self.env)
            if not os.path.exists(env_dir):
                self.error("The environment '%s' does not exist." % self.env)
    
    def context(self):
        ctx = ""
        if self.wrapper:
            ctx += "%s/" % self.wrapper.context()
        ctx += self.name
        return ctx
    
    def error(self, msg):
        sys.stderr.write("%s%s\n" % (build_context(self.context()), msg))
        sys.exit(1)
    
    def notify(self, msg):
        sys.stdout.write("%s%s\n" % (build_context(self.context()), msg))


class CommandEnv(Command):
    name = "env"
    
    def setup_dispatcher(self, dispatcher):
        dispatcher.add(CommandEnvCreate, wrapper=self)
        dispatcher.add(CommandEnvDelete, wrapper=self)
        dispatcher.add(CommandEnvList, wrapper=self)


class CommandEnvCreate(Command):
    name = "create"
    
    def run(self):
        if not self.args:
            self.error("You must provide an environment name.")
        env_name = self.args[0]
        env_dir = os.path.join(ENV_DIR, env_name)
        if os.path.exists(env_dir):
            self.error("Environment '%s' exists." % env_name)
        os.makedirs(env_dir)
        self.notify("Created environment '%s'" % env_name)


class CommandEnvDelete(Command):
    name = "delete"
    
    def run(self):
        if not self.args:
            self.error("You must provide an environment name.")
        env_name = self.args[0]
        env_dir = os.path.join(ENV_DIR, env_name)
        if os.path.exists(env_dir):
            shutil.rmtree(env_dir)
            self.notify("Deleted environment '%s'" % env_name)


class CommandEnvList(Command):
    name = "list"
    
    def run(self):
        for env in os.listdir(ENV_DIR):
            print env


class CommandInstall(Command):
    name = "install"
    require_env = True
    
    def run(self):
        self.notify("installing stuff in '%s' (no idea how this will work yet)" % self.env)


class CommandRun(Command):
    name = "run"
    ensure_env_exists = True
    
    def run(self):
        cmd = [
            "node",
        ]
        cmd.extend(self.args)
        process_env = os.environ.copy()
        if "NIP_ENV" not in process_env and self.env:
            process_env.update({"NIP_ENV": self.env})
        if self.env:
            env_dir = os.path.join(ENV_DIR, self.env)
            process_env.update({"NODE_PATH": env_dir})
        proc = subprocess.Popen(cmd, env=process_env)
        proc.communicate()


def build_context(ctx):
    if ctx:
        return "[%s] " % ctx
    else:
        return ""


def main():
    global ENV_DIR
    
    parser = optparse.OptionParser()
    parser.add_option("-d",
        dest = "env_dir",
        help = "Override environment directory."
    )
    parser.add_option("-E",
        dest = "env",
        default = os.environ.get("NIP_ENV"),
        help = "Environment to run in."
    )
    parser.disable_interspersed_args()
    options, args = parser.parse_args()
    
    if options.env_dir:
        ENV_DIR = options.env_dir
    
    dispatcher = CommandDispatcher(args, env=options.env)
    dispatcher.add(CommandEnv)
    dispatcher.add(CommandInstall)
    dispatcher.add(CommandRun)
    dispatcher.dispatch()
    
    return 0


if __name__ == "__main__":
    main()