from GameLayer import GameLayer

from framework.app import Application

if __name__ == "__main__":
    app = Application(
        title="Game1",
        resolution=(800, 600)
    )
    scene = GameLayer.create_scene()
    app.run_with_scene(scene)
