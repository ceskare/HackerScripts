import yaml


def generate_ansible_tasks(todo):
    tasks = []

    if 'install_packages' in todo['server']:
        packages = todo['server']['install_packages']
        tasks.append({'name': 'Install packages', 'apt': {'pkg': packages, 'state': 'present'}})

    if 'exploit_files' in todo['server']:
        files = todo['server']['exploit_files']
        tasks.append({'name': 'Copy over files', 'copy': {'src': files, 'dest': '../../materials'}})

    if 'exploit_files' in todo['server']:
        files = todo['server']['exploit_files']
        bad_guys = todo['bad_guys']
        for file in files:
            for bad_guy in bad_guys:
                command = f'python3 {file} -e {bad_guy}'
                tasks.append({'name': f'Run {file} for {bad_guy}', 'command': command})

    return tasks


def main():
    with open('../../materials/todo.yml', 'r') as file:
        todo = yaml.safe_load(file)

    tasks = generate_ansible_tasks(todo)

    with open('../../materials/deploy.yml', 'w') as file:
        yaml.dump(tasks, file)


if __name__ == "__main__":
    main()
