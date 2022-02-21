# Control binaries are located in <gus_epaxos_control_src_directory>/bin and <gryff_control_src_directory>/bin.
# Remote binaries are stored in <remote_bin_directory>/gus-epaxos and <remote_bin_directory>/gryff.
# Control experiment directories are located in <base_control_experiment_directory>/<timestamp of experiment>
# Remote experiment directories are located in <base_remote_experiment_directory>/<timestamp of experiment>

import concurrent
import os
import subprocess
import time

from remote_util import *


def setup_nodes(config, executor):
    make_binaries(config)
    timestamp = prepare_control_exp_directory(config)
    prepare_remote_exp_and_bin_directories(config, timestamp, executor)
    copy_binaries_to_machines(config, executor)
    return timestamp


def make_binaries(config):
    print("making binaries")
    make_repo_binaries(config['gus_epaxos_control_src_directory'])
    make_repo_binaries(config['gryff_control_src_directory'])


def make_repo_binaries(repo_directory):
    # Add temporary environment variables to be used when compiling binaries.
    e = os.environ.copy()
    e["GOPATH"] = repo_directory # the bin directory will be located inside the repo

    # Make binaries in bin directory (located at <repo_directory>/bin).
    subprocess.call(["go", "install", "master"], cwd=repo_directory, env=e)
    subprocess.call(["go", "install", "server"], cwd=repo_directory, env=e)
    subprocess.call(["go", "install", "client"], cwd=repo_directory, env=e)


def prepare_control_exp_directory(config, config_file=None):
    print("making control experiment directory")

    timestamped_exp_directory = get_timestamped_exp_dir(config)
    os.makedirs(timestamped_exp_directory)
    # shutil.copy(config_file, os.path.join(exp_directory, os.path.basename(config_file)))
    return os.path.basename(timestamped_exp_directory)


# TODO include type of experiment (latency, throughput, etc.) here
def get_timestamped_exp_dir(config):
    now_string = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
    return os.path.join(config['base_control_experiment_directory'], now_string)


def prepare_remote_exp_and_bin_directories(config, timestamp, executor):
    print("preparing remote directories")

    # Prepare remote out directory with timestamped experiment directory folder
    remote_directory = os.path.join(config['base_remote_experiment_directory'], timestamp)

    # Prepare remote binary directory
    remote_binary_directory = config['remote_bin_directory']

    futures = []
    for server_name in config['server_names']:
        futures.append(executor.submit(prepare_remote_exp_and_bin_directory, config, server_name,
                                       remote_directory, remote_binary_directory))

    futures.append(executor.submit(prepare_remote_exp_and_bin_directory, config, 'client',
                                   remote_directory, remote_binary_directory))

    concurrent.futures.wait(futures)
    return remote_directory


def prepare_remote_exp_and_bin_directory(config, machine_name, remote_out_directory, remote_bin_directory):
    machine_url = get_machine_url(config, machine_name)

    run_remote_command_sync('mkdir -p %s' % remote_out_directory, machine_url)

    gus_epaxos_remote_bin_directory = os.path.join(remote_bin_directory, "gus-epaxos")
    gryff_remote_bin_directory = os.path.join(remote_bin_directory, "gryff")
    run_remote_command_sync('mkdir -p %s' % gus_epaxos_remote_bin_directory, machine_url)
    run_remote_command_sync('mkdir -p %s' % gryff_remote_bin_directory, machine_url)


def copy_binaries_to_machines(config, executor):
    print("copying binaries")

    control_binary_directory = os.path.join(config['control_src_directory'], 'bin')
    remote_binary_directory = config['remote_bin_directory']

    futures = []
    for server_name in config['server_names']:
        server_url = get_machine_url(config, server_name)
        futures.append(executor.submit(copy_local_directory_to_remote,
                                       control_binary_directory, server_url, remote_binary_directory))

    client_url = get_machine_url(config, 'client')
    futures.append(executor.submit(copy_local_directory_to_remote,
                                   control_binary_directory, client_url, remote_binary_directory))

    concurrent.futures.wait(futures)