import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import activate, LANGUAGE_SESSION_KEY, ugettext as _
from django.utils.safestring import mark_safe
from git import Repo
import pip
from django.core.management import call_command
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from functools import partial

permission_required = partial(permission_required, raise_exception=True)


def qdc_permission_denied_view(request, template_name="admin/qdc_403.html"):

    context = {}

    return render(request, template_name, context, status=403)


@login_required
def contact(request):
    # messages.success(request, _("Test !"))
    if_upgrade = False
    if check_upgrade(request):
        if_upgrade = True
        if request.user.has_perm('configuration.upgrade_rights'):
            messages.info(request, mark_safe('<a href="/home/upgrade_nes/">There is a new version of NES. Click '
                                             'for upgrade</a>'))

        else:
            messages.success(request, _("There is a new version, please contact your NES administrator to update !"))

    context = {
        'logo_institution': settings.LOGO_INSTITUTION,
        'if_upgrade': if_upgrade,
    }

    return render(request, 'quiz/contato.html', context)


@login_required
def language_change(request, language_code):

    activate(language_code)
    request.session[LANGUAGE_SESSION_KEY] = language_code

    return HttpResponseRedirect(request.GET['next'])


@login_required
def password_changed(request):

    messages.success(request, _('Password changed successfully.'))

    return contact(request)


@login_required
def check_upgrade(request):
    path_git_repo_local = get_nes_directory_path()
    list_dir = os.listdir(path_git_repo_local)
    new_version = False
    if '.git' in list_dir:
        repo = Repo(path_git_repo_local)
        git = repo.git
        current_tag = git.describe()
        if 'TAG' in current_tag:
            new_version_tag = \
                sorted(git.tag().split('\n'), key=lambda s: list(map(int, s.replace('-', '.').split('.')[1:])))[-1]

            # for remote in repo.remotes:
            #     remote.fetch()

            new_version = nes_new_version(current_tag.split('-')[-1], new_version_tag.split('-')[-1])

    else:
        messages.success(request, _("You dont have NES Git installation. Automatic upgrade can be done with git "
                                    "installation. "
                                    "Please contact your system administrator to upgrade NES to a new version."))

    return new_version


def nes_new_version(current_tag, new_version_tag):
    new_version = False
    local_version = list(map(int, current_tag.split('-')[-1].split('.')))
    origin_version = list(map(int, new_version_tag.split('-')[-1].split('.')))

    if origin_version[0] > local_version[0]:
        new_version = True
    elif origin_version[0] == local_version[0]:
        if origin_version[1] > local_version[1]:
            new_version = True
        elif origin_version[1] == local_version[1]:
            if origin_version[2] > local_version[2]:
                new_version = True
    return new_version


def get_nes_directory_path():
    path_repo = '/'
    base_dir = settings.BASE_DIR.split('/')
    if 'nes' in base_dir:
        path_git_repo = []
        for item in base_dir:
            if item != 'nes' and item != '':
                path_git_repo.append(item)
            if item == 'nes':
                path_git_repo.append(item)
                break

        for item in path_git_repo:
            path_repo = path_repo + item + '/'

    return path_repo


def get_pending_migrations():
    connection = connections[DEFAULT_DB_ALIAS]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return executor.migration_plan(targets)


@login_required
@permission_required('configuration.upgrade_rights')
def upgrade_nes(request):
    # log = open("upgrade.log", "a")
    # sys.stdout = log

    text_log = ""

    path_git_repo_local = get_nes_directory_path()
    list_dir = os.listdir(path_git_repo_local)
    if '.git' in list_dir:
        repo = Repo(path_git_repo_local)
        git = repo.git
        # current_tag = git.describe()
        new_version_tag = \
            sorted(git.tag().split('\n'), key=lambda s: list(map(int, s.replace('-', '.').split('.')[1:])))[-1]
        # branch = repo.active_branch
        # if 'TAG' in branch.name.split('-'):
        for remote in repo.remotes:
            remote.fetch()
            text_log += 'fetch-'

        # tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        # if tags:
            # if nes_new_version(tags):
        # last_tag = str(tags[-1])  # last version [-1] before last version [-2]
        repo_version = new_version_tag.split('-')[-1]
        print("repository last version: " + repo_version)
        git.checkout(new_version_tag)

        text_log += 'checkout-'

        try:
            pip.main(['install', '-r', 'requirements.txt'])
            text_log += 'requirements-'
        except SystemExit as e:
            pass

        call_command('collectstatic', interactive=False, verbosity=0)
        text_log += 'collectstatic-'

        if get_pending_migrations():
            call_command('migrate')
            text_log += 'migrate-'

        # TODO start apache (opcao colocar um flag no setting local)
        # check the current branch - a tag mais nova last_tag
        # if repo.active_branch.name == last_tag:
        #     messages.success(request, _("Upgrade to version " + repo_version + " was sucessful!"))
        # else:
        #     messages.success(request, _("An error ocurred when upgrade to the new version ! Please contact "
        #                                 "your administrator system."))
        # else:
        #     messages.success(request, _("NES git branch different: " + branch.name + ". Please contact your system "
        #                                 "administrator to upgrade NES to the new version."))
        # Restart apache Não precisa
        # sudo service apache2 restart
        # atualizar a data de modificacao do wsgi.py com: touch wsgi.py
        os.system('touch qdc/wsgi.py')
        text_log += 'touch-'

        messages.info(request, text_log)
        messages.success(request, _("Updated!!! Enjoy the new version of NES  :-)"))

    context = {
        'if_upgrade': False,
    }

    return render(request, 'quiz/contato.html', context)
