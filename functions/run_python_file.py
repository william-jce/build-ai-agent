import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        valid_target_path = os.path.commonpath([abs_working_dir, target_file_path]) == abs_working_dir
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or it is not a regular file'
        if os.path.splitext(target_file_path)[1] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args is not None:
            command.extend(args)
        complete_comm = subprocess.run(command, cwd=abs_working_dir, capture_output=True,  timeout=30, text=True)

        output = []
        if complete_comm.returncode != 0:
            output.append(f'Process exited with code {complete_comm.returncode}')
        if not complete_comm.stdout and not complete_comm.stderr:
            output.append('No output produced')
        else:
            output.append(f'STDOUT: {complete_comm.stdout}')
            output.append(f'STDERR: {complete_comm.stderr}')
        return "\n".join(output)
    except Exception as e:
        return f'Error: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments inside the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A file path to a Python file to execute",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional arguments that will be used when calling the function"
            )
        },
        required=["file_path"]
    ),
)
