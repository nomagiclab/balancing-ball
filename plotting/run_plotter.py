import sys

from plotter import Plotter


def main():
    # assert len(sys.argv) == 3
    x_pid_csv = sys.argv[1]
    # y_pid_csv = sys.argv[2]

    p = Plotter([x_pid_csv])
    p.start()


if __name__ == "__main__":
    main()
