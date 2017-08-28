from framework.node import Node


class Scene(Node):
    """
    场景对象
    顶层节点，作为Layer的容器，并派发事件给各个Layer
    """
    def handle(self, event):
        """
        事件响应
        派发给每个层，并正确截断
        """
        for child in self.children:
            child.handle(event)
            if child.shallow:
                break
