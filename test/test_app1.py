from framework.scene import Scene

from framework.app import Application

if __name__ == "__main__":
    app = Application(title="Test App 1", resolution=(640, 480))
    scene = Scene()
    app.run_with_scene(scene)
