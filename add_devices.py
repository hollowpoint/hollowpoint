import ast
from inventory.models import TaskState, NetDevice

def associate_tasks():
    all_tasks = TaskState.objects.all()

    # Walk every task and see if it's got devices...
    for task in all_tasks:
        kwargs = ast.literal_eval(task.kwargs)
        devices = kwargs.get('devices', [])

        # Convert the device names to objects
        objects = NetDevice.objects.filter(node_name__in=devices)

        # Associate the devices (if any) w/ the current task
        task.devices.add(*objects)
        if task.devices.exists():
            print 'Added', task.devices.count(), 'devices to task', task.task_id
