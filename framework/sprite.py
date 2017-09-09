from framework.node import Node


class Sprite(Node):
    """
    精灵类
    考虑继承pygame.sprite.Sprite
    考虑动作功能
    """

class FrameIterator:
    """
    帧迭代器，每次给出下一帧
    """

    def __init__(self, images, fid=-1):
        self.images = images
        self.fid = fid

    def __next__(self):
        self.fid += 1
        if self.fid >= len(self.images):
            raise StopIteration
        return self.images[self.fid]

    def __iter__(self):
        return self

    def size(self):
        return len(self.images)

    def current_frame(self):
        if self.fid == -1:
            raise Exception("No such current frame: -1")
        return self.images[self.fid]

    def go_to(self, to_id):
        if to_id >= len(self.images) or to_id < -1:
            raise Exception("Invalid frame id")
        self.fid = to_id

    def go_to_start(self):
        self.go_to(-1)

    @classmethod
    def create_with_plist(cls, texture, plist):
        return FrameIterator([])


class AnimateSprite(Sprite):
    """
    动画精灵类
    可以独立控制帧率
    使用一个FrameIterator接口来获得下一帧
    mode: LOOP: 无限循环
          TIMES: 最多循环self._times次
    """
    LOOP = 0
    TIMES = 1

    def __init__(self, frame_iter, first_image=None, mode=LOOP, times=1, tick=None,
                 parent=None, image=None, rect=None):
        super(AnimateSprite, self).__init__(parent, image, rect)
        self.frame_iter = frame_iter
        if first_image is None:
            self.image = next(self.frame_iter)
        else:
            self.image = first_image
        self.rect = self.image.get_rect()
        if tick is None:
            self.tick = self.frame_iter.size()
        else:
            self.tick = tick
        self._mode = mode
        self._times = times
        self._run_times = 0
        self._last = None
        self._start = False
        self._delay = 0
        self.start()

    @classmethod
    def create_with_plist(cls, texture, plist, **kwds):
        frame_iter = FrameIterator.create_with_plist(texture, plist)
        return cls(frame_iter, **kwds)

    @classmethod
    def create_with_images(cls, images, **kwds):
        frame_iter = FrameIterator(images)
        return cls(frame_iter, **kwds)

    def start(self):
        self._start = True
        self.schedule_update()

    def pause(self):
        self._start = False

    def stop(self):
        self._start = False
        self._run_times = 0
        self.unschedule_update()

    def set_mode(self, mode):
        self._mode = mode
        self._run_times = 0

    def set_max_times(self, times):
        self._times = times
        self._run_times = 0

    def update(self, dt):
        if not self._start:
            return
        self._delay += dt
        if self._delay > 1000 / self.tick:
            self._delay = 0
            try:
                self.image = next(self.frame_iter)
            except StopIteration:
                if self._mode == self.LOOP or \
                                        self._mode == self.TIMES and self._run_times < self._times:
                    self.frame_iter.go_to_start()
                    self.image = next(self.frame_iter)
                else:
                    self.stop()
                self._run_times += 1