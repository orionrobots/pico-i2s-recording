from invoke import task

@task
def install_libraries(c):
    """Setup the libraries needed for this to work"""
    c.run("mpremote mip install sdcard")
    c.run("mpremote mip install ucontextlib")

@task
def update(c):
    """Update all source files"""
    c.run("mpremote cp src/*.py :")

@task(install_libraries, update)
def install(c):
    pass

@task(install)
def run(c, run_target="main.py"):
    """Run the local main file for testing"""
    c.run(f"mpremote run src/{run_target}")

# Helper for MP remote to setup the SD mount
SD_MOUNT="\"import mount_sd; mount_sd.mount()\""
@task
def list_recordings(c):
    """List recordings on the SD"""
    # mount the sd card
    c.run(f"mpremote exec {SD_MOUNT} ls sd")

@task
def get_recording(c, filename):
    """Get a recording file from the SD card"""
    c.run(f"mkdir -p output")
    c.run(f"mpremote exec {SD_MOUNT} cp :sd/{filename} output/{filename}")
