from flask import Flask, render_template, request, redirect, Markup
from configuration.index import select_configurations
from command import GenericCommand
from result.error import ValidationError
from result.web import WebResult, get_result, next_result
from command.view import ViewCommand
from command.target import TargetCommand
from command.validate import ValidateCommand
from command.execute import ExecuteCommand

app = Flask(__name__)


def run_command(command: GenericCommand):
    try:
        command.validate()
        command.execute()
    except ValidationError:
        pass
    except Exception as error:
        print(error)
        command.sink.error('Critical error executing command')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/view')
def view():
    return render_template(
        'view.html',
        configurations=list(map(
            lambda configuration: configuration.name,
            select_configurations())
        )
    )


@app.route('/command/view', methods={'POST'})
def command_view():
    configuration = request.form['name']
    view_all = configuration == '0'
    operation = 'Viewing all configurations'
    if not view_all:
        operation = 'Viewing configuration: ' + configuration
    else:
        configuration = None
    web_result = next_result(operation)
    command = ViewCommand(configuration, web_result.sink)
    run_command(command)
    return redirect('/result/' + web_result.key)


@app.route('/target')
def target():
    return render_template('target.html')


@app.route('/command/target', methods={'POST'})
def command_target():
    port = None
    if request.form['port']:
        port = int(request.form['port'])
    web_result = next_result('Editing target configuration')
    command = TargetCommand(
        request.form['name'],
        request.form['host'],
        port,
        request.form['username'],
        request.form['password'],
        request.form['group'],
        list(filter(lambda x: x, request.form.getlist('add_schema'))),
        list(filter(lambda x: x, request.form.getlist('remove_schema'))),
        web_result.sink
    )
    run_command(command)
    return redirect('/result/' + web_result.key)


@app.route('/validate')
def validate():
    return render_template(
        'validate.html',
        configurations=select_configurations()
    )


@app.route('/command/validate', methods={'POST'})
def command_validate():
    configuration = request.form['name']
    validate_all = configuration == '0'
    operation = 'Validating all configurations'
    if not validate_all:
        operation = 'Validating configuration: ' + configuration
    else:
        configuration = None
    web_result = next_result(operation)
    command = ValidateCommand(configuration, request.form['group'], validate_all, web_result.sink)
    run_command(command)
    return redirect('/result/' + web_result.key)


@app.route('/execute')
def execute():
    return render_template(
        'execute.html',
        configurations=select_configurations()
    )


@app.route('/command/execute', methods={'POST'})
def command_execute():
    configuration = request.form['name']
    validate_all = configuration == '0'
    operation = 'Executing queries on all configurations'
    if not validate_all:
        operation = 'Executing queries on: ' + configuration
    else:
        configuration = None
    web_result = next_result(operation)
    transaction = ('transaction' in request.form) and bool(request.form['transaction'])
    error_continue = ('error_continue' in request.form) and bool(request.form['error_continue'])
    command = ExecuteCommand(
        configuration,
        request.form['group'],
        request.form['query'],
        '',
        transaction,
        validate_all,
        error_continue,
        web_result.sink
    )
    run_command(command)
    return redirect('/result/' + web_result.key)


@app.route('/result/<key>')
def result(key: str):
    web_result = get_result(key)
    return render_template(
        'result.html',
        operation=web_result.operation,
        display=Markup(web_result.render()),
        name=key
    )


@app.route('/download/result/<key>')
def download_result(key: str):
    web_result = get_result(key)
    return web_result.as_json()
