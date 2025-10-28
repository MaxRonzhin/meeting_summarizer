from src.controllers.meeting_controller import MeetingController


def main() -> None:
    controller = MeetingController()
    controller.run()


if __name__ == "__main__":
    main()
