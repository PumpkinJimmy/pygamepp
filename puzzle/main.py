from framework.app import Application
from scenes import StartUp
if __name__ == "__main__":
    app = Application(title="Puzzle",
                      resolution=(825, 675),
                      font_size=72)
    scene = StartUp().create_scene()
    app.run_with_scene(scene)