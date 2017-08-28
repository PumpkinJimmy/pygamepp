import glob, sys, re, datetime
import pygame
from pygame.locals import *


class SimpleAnimateSprite(pygame.sprite.Sprite):
    """
    简单的动画精灵
    保存一个图片序列，并保存一个当前图片id
    启动后，每一次update都切换到下一张图片
    mode = 0 -> 无限循环
    mode = 1 -> 只工作到最后一张图片就停止
    """

    def __init__(self, imgs, mode=0, *group):
        super(SimpleAnimateSprite, self).__init__(*group)
        self.imgs = imgs
        self.frameid = 0
        self.image = self.imgs[self.frameid]
        self.rect = self.image.get_rect()
        self.mode = mode  # loop
        self._start = False
        self.start()

    def _set_frame(self):
        self.image = self.imgs[self.frameid]
        rect = self.image.get_rect()
        rect.topleft = self.rect.topleft
        self.rect = rect

    def next_frame(self):
        self.frameid += 1
        if self.mode == 1 and self.frameid >= len(self.imgs):
            self.stop()
            return
        elif self.mode == 0:
            self.frameid %= len(self.imgs)
        self._set_frame()

    def start(self):
        self._start = True

    def stop(self):
        self._start = False

    def update(self, dt=None):
        if not self._start: return
        self.next_frame()


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


class AnimateSprite(pygame.sprite.Sprite):
    """
    动画精灵类
    可以独立控制帧率
    使用一个FrameIterator接口来获得下一帧
    mode: LOOP: 无限循环
          TIMES: 最多循环self._times次
    """
    LOOP = 0
    TIMES = 1

    def __init__(self, frame_iter, first_image=None, mode=LOOP, times=1, tick=None, *group):
        super(AnimateSprite, self).__init__(*group)
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

    def pause(self):
        self._start = False

    def stop(self):
        self._start = False
        self._run_times = 0

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

    def draw(self, surf):
        update_rect = surf.blit(self.image, self.rect)
        pygame.display.update(update_rect)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 255, 255))
    imgs = []
    pat = re.compile(r"resource\\run([0-9]+?)\.png")
    paths = glob.glob("resource\\run*.png")
    paths.sort(key=lambda p: int(re.search(pat, p).group(1)))
    for path in paths:
        img = pygame.image.load(path).convert_alpha()
        imgs.append(img)
    sprite = SimpleAnimateSprite(imgs, 1)  # once
    sprite.rect.topleft = (50, 250)
    # sprite.start()
    sprite2 = SimpleAnimateSprite(imgs, 0)  # loop
    sprite2.rect.topleft = (50, 50)
    # sprite2.start()
    sprite3 = AnimateSprite.create_with_images(imgs)  # loop
    sprite3.rect.topleft = (200, 50)
    # sprite3.start()
    sprite4 = AnimateSprite.create_with_images(imgs, mode=AnimateSprite.TIMES, times=2)  # twice
    sprite4.rect.topleft = (200, 250)
    # sprite4.start()
    img = pygame.image.load(r"resource\bean.jpg").convert_alpha()
    imgs = [img.subsurface(Rect(i * 80, 0, 80, 80)) for i in range(0, 5)]
    sprite5 = AnimateSprite.create_with_images(imgs)
    # sprite5.start()
    mygroup = pygame.sprite.Group(sprite, sprite2, sprite3, sprite4, sprite5)
    clock = pygame.time.Clock()
    while 1:
        dt = clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        screen.fill((255, 255, 255))
        mygroup.draw(screen)
        # screen.blit(sprite.image, sprite.rect)
        # screen.blit(sprite2.image, sprite2.rect)
        # screen.blit(sprite3.image, sprite3.rect)
        # screen.blit(sprite4.image, sprite4.rect)
        pygame.display.flip()
        mygroup.update(dt)
        # sprite.update()
        # sprite2.update()
        # sprite3.update()
        # sprite4.update()
