import sys
import argparse
import math
import matplotlib.pyplot as plt

class Robot:
    """Simple 2D differential-drive-style robot with a discrete motion model."""

    def __init__(self, x=0.0, y=0.0, theta=0.0):
        self.x = x
        self.y = y
        self.theta = theta  # degrees

        # trajectory log: list of (x, y, theta) tuples, starting with initial pose
        self.trajectory = [(self.x, self.y, self.theta)]

    def pose(self):
        return (round(self.x, 3), round(self.y, 3), round(self.theta, 3))

    def execute(self, command_str):
        """Parse and execute a single command string, logging before/after pose."""
        parts = command_str.strip().split()
        if not parts:
            return False

        cmd = parts[0].lower()
        if cmd not in ("forward", "left", "right"):
            print(f"  [!] Unknown command: '{command_str}' (skipped)")
            return False

        if len(parts) < 2:
            print(f"  [!] Missing value for command: '{command_str}' (skipped)")
            return False

        try:
            val = float(parts[1])
        except ValueError:
            print(f"  [!] Invalid numeric value in: '{command_str}' (skipped)")
            return False

        initial = self.pose()

        if cmd == "forward":
            rad = math.radians(self.theta)
            self.x += val * math.cos(rad)
            self.y += val * math.sin(rad)
        elif cmd == "left":
            self.theta = (self.theta + val) % 360
        elif cmd == "right":
            self.theta = (self.theta - val) % 360

        final = self.pose()
        self.trajectory.append((self.x, self.y, self.theta))

        print(f"Initial Pos: {initial} | Executing: {command_str.strip()} | Final Pos: {final}")
        return True


def read_commands_from_file(path):
    with open(path, "r") as f:
        return [line for line in f if line.strip()]


def read_commands_interactively():
    print("Enter motion commands (forward/left/right <val>).")
    print("Type 'done' or press Ctrl+D / Ctrl+Z to finish.\n")
    commands = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if line.strip().lower() in ("done", "exit", "quit"):
            break
        if line.strip():
            commands.append(line)
    return commands


def plot_trajectory(trajectory, arrow_len_ratio=0.08):
    """Plot the path, start/end markers, and heading quivers at each waypoint."""
    xs = [p[0] for p in trajectory]
    ys = [p[1] for p in trajectory]
    thetas = [p[2] for p in trajectory]

    fig, ax = plt.subplots(figsize=(8, 8))

    # Path line with waypoint markers
    ax.plot(xs, ys, '-o', color='steelblue', markersize=5,
             linewidth=1.8, label='Path', zorder=2)

    # Start and end markers
    ax.scatter(xs[0], ys[0], color='green', s=160, marker='o',
               edgecolor='black', zorder=4, label='Start')
    ax.scatter(xs[-1], ys[-1], color='red', s=160, marker='X',
               edgecolor='black', zorder=4, label='End')

    # Heading arrows (quivers) at each waypoint
    span_x = max(xs) - min(xs) if max(xs) != min(xs) else 1.0
    span_y = max(ys) - min(ys) if max(ys) != min(ys) else 1.0
    arrow_len = max(span_x, span_y) * arrow_len_ratio
    arrow_len = arrow_len if arrow_len > 0 else 1.0

    us = [arrow_len * math.cos(math.radians(t)) for t in thetas]
    vs = [arrow_len * math.sin(math.radians(t)) for t in thetas]

    ax.quiver(xs, ys, us, vs, color='darkorange', angles='xy',
              scale_units='xy', scale=1, width=0.005,
              zorder=3, label='Heading')

    ax.set_title("Robot Trajectory & Heading")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='best')

    plt.tight_layout()
    output_path = "trajectory_plot.png"
    plt.savefig(output_path, dpi=150)
    print(f"\nTrajectory plot saved to: {output_path}")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Discrete Motion Model & Trajectory Tracking")
    parser.add_argument("-f", "--file", help="Path to a text file with one command per line")
    parser.add_argument("--x0", type=float, default=0.0, help="Initial x position")
    parser.add_argument("--y0", type=float, default=0.0, help="Initial y position")
    parser.add_argument("--theta0", type=float, default=0.0, help="Initial heading in degrees")
    args = parser.parse_args()

    robot = Robot(x=args.x0, y=args.y0, theta=args.theta0)

    if args.file:
        commands = read_commands_from_file(args.file)
    else:
        commands = read_commands_interactively()

    if not commands:
        print("No commands to execute. Exiting.")
        sys.exit(0)

    print("\n--- Executing Commands ---")
    for c in commands:
        robot.execute(c)

    print("\n--- Final Trajectory ---")
    for i, p in enumerate(robot.trajectory):
        print(f"  Step {i}: (x={p[0]:.3f}, y={p[1]:.3f}, theta={p[2]:.3f})")

    plot_trajectory(robot.trajectory)

if __name__ == "__main__":
    main()
