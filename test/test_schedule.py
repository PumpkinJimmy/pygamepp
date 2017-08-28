from framework.schedule import Scheduler


if __name__ == "__main__":
    scheduler = Scheduler.instance()
    print(scheduler)
    scheduler2 = Scheduler.instance()
    print(scheduler2)