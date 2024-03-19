from dados import tasks

max_id_value = max([task["id"] for task in tasks])
print(max_id_value)