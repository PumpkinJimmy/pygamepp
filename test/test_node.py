from framework import node


class A(node.Node):
    def on_a(self):
        print("slot a is called")


def B():
    print("slot b is called")


class C(node.Node):
    def mysend(self):
        self.send("activate")


class D(node.Node):
    def mysend(self):
        self.send("activate")


if __name__ == "__main__":
    a = A()
    b = B
    c = C()
    d = D()
    c.connect("activate", "a", a)
    c.connect("activate", b)
    d.connect("activate", a.on_a)
    c.mysend()
    d.mysend()
    print(a.get_size())
