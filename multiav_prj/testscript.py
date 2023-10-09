import docker

def scan_file(file_data):
    try:
        # Create a Docker client
        client = docker.from_env()

        # Run the antivirus engine container, passing the file to scan
        container = client.containers.run(
            image='clamav/clamav:latest',
            command=['clamscan', '-'],
            stdin_open=True,
            tty=False,
            detach=True,
            
        )

        try:
            # Write the file data to the container's STDIN for scanning
            container.exec_run(
                cmd=['bash', '-c', f'echo "{file_data.decode()}" | clamscan -'],
                stdout=True,
                stderr=True,
            )

            # Wait for the container to finish scanning
            container.wait()

            # Get the container's exit code to determine the scan result
            exit_code = container.attrs['State']['ExitCode']

            # Handle the scan result based on the exit code
            result = 'Clean' if exit_code == 0 else 'Infected'
        finally:
            # Stop the container
            container.stop()

        # Remove the container after it has been stopped
        container.remove()

        return result

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    # Example: Read file data from a file (replace with your file handling code)
    with open('requirements.txt', 'rb') as file:
        file_data = file.read()

    scan_result = scan_file(file_data)
    print(f"Scan Result: {scan_result}")
