def print_result(task, command):
    """
    Print the output of a ``command`` from a ``task``
 
    :param task:
        An AsyncResult object representing a task
 
    :param command:
        The command output to display
    """
    for item in task.result['result']:
        print item['device'], item['commands'][0]['result'][command]
