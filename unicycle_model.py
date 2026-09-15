import sys
import argparse
import math
import matplotlib.pyplot as plt


class UnicycleRobot:
    """Continuous unicycle-model robot integrated via Forward Euler."""

    def __init__(self, x=0.0, y=0.0, theta=0.0, dt=0.05):
        self.x = x
        self.y = y
        self.theta = theta  # radians
        self.dt = dt

        # Fine-grained trajectory (every integration step) for smooth plotting
        self.trajectory = [(self.x, self.y, self.theta)]
        # Coarse waypoints (only at the end of each command block)
        self.waypoints = [(self.x, self.y, self.theta)]

    def pose_str(self):
        return (f"(x={self.x:.3f}, y={self.y:.3f}, "
                f"theta={self.theta:.3f} rad / {math.degrees(self.theta):.1f} deg)")

    def apply_velocity(self, v, omega, duration):
        """Integrate (v, omega) forward for `duration` seconds using Forward Euler."""
        initial = self.pose_str()

        steps = max(1, round(duration / self.dt))
        actual_dt = duration / steps  # spread evenly so we hit `duration` exactly

        for _ in range(steps):
            self.x += v * math.cos(self.theta) * actual_dt
            self.y += v * math.sin(self.theta) * actual_dt
            self.theta += omega * actual_dt
            self.trajectory.append((self.x, self.y, self.theta))

        self.waypoints.append((self.x, self.y, self.theta))

        final = self.pose_str()
        print(f"Initial Pos: {initial}")
        print(f"  Executing: v={v}, omega={omega}, duration={duration}s "
              f"(steps={steps}, dt={actual_dt:.4f}s)")
        print(f"Final Pos:   {final}\n")


def parse_command(line):
    """Parse a line of the form '<v> <omega> <duration>'."""
    parts = line.strip().split()
    if len(parts) != 3:
        return None
    try:
        v, omega, duration = (float(p) for p in parts)
    except ValueError:
        return None
    if duration <= 0:
        return None
    return v, omega, duration


def read_commands_from_file(path):
    commands = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                commands.append(line)
    return commands


def read_commands_interactively():
    print("Enter velocity commands as: <v> <omega> <duration>")
    print("Example: 1.0 0.5 3   ->  v=1.0, omega=0.5 rad/s, for 3 seconds")
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


def plot_trajectory(trajectory, waypoints, arrow_len_ratio=0.06):
    """Plot the smooth continuous path, start/end markers, and heading arrows."""
    xs = [p[0] for p in trajectory]
    ys = [p[1] for p in trajectory]

    wx = [p[0] for p in waypoints]
    wy = [p[1] for p in waypoints]
    wtheta = [p[2] for p in waypoints]

    fig, ax = plt.subplots(figsize=(8, 8))

    # Smooth continuous curve (every Euler-integrated point)
    ax.plot(xs, ys, '-', color='steelblue', linewidth=2.0,
             label='Trajectory', zorder=2)

    # Mark the end of each command block along the curve
    ax.scatter(wx[1:-1], wy[1:-1], color='dimgray', s=35, zorder=3,
               label='Block boundaries')

    # Start / end markers
    ax.scatter(wx[0], wy[0], color='green', s=160, marker='o',
               edgecolor='black', zorder=4, label='Start')
    ax.scatter(wx[-1], wy[-1], color='red', s=160, marker='X',
               edgecolor='black', zorder=4, label='End')

    # Heading arrows at each command-block waypoint
    span_x = max(xs) - min(xs) if max(xs) != min(xs) else 1.0
    span_y = max(ys) - min(ys) if max(ys) != min(ys) else 1.0
    arrow_len = max(span_x, span_y) * arrow_len_ratio
    arrow_len = arrow_len if arrow_len > 0 else 1.0

    us = [arrow_len * math.cos(t) for t in wtheta]
    vs = [arrow_len * math.sin(t) for t in wtheta]

    ax.quiver(wx, wy, us, vs, color='darkorange', angles='xy',
              scale_units='xy', scale=1, width=0.005,
              zorder=3, label='Heading')

    ax.set_title("Continuous Unicycle Model: Trajectory & Heading")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='best')

    plt.tight_layout()
    output_path = "unicycle_trajectory_plot.png"
    plt.savefig(output_path, dpi=150)
    print(f"Trajectory plot saved to: {output_path}")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Continuous Unicycle Model (v, omega)")
    parser.add_argument("-f", "--file", help="Path to a text file with '<v> <omega> <duration>' per line")
    parser.add_argument("--x0", type=float, default=0.0, help="Initial x position")
    parser.add_argument("--y0", type=float, default=0.0, help="Initial y position")
    parser.add_argument("--theta0", type=float, default=0.0, help="Initial heading (radians)")
    parser.add_argument("--dt", type=float, default=0.05, help="Integration time step (seconds)")
    args = parser.parse_args()

    robot = UnicycleRobot(x=args.x0, y=args.y0, theta=args.theta0, dt=args.dt)

    if args.file:
        raw_commands = read_commands_from_file(args.file)
    else:
        raw_commands = read_commands_interactively()

    if not raw_commands:
        print("No commands to execute. Exiting.")
        sys.exit(0)

    print(f"\n--- Executing Velocity Commands (dt={args.dt}s) ---\n")
    for line in raw_commands:
        parsed = parse_command(line)
        if parsed is None:
            print(f"  [!] Skipping invalid command: '{line.strip()}'")
            continue
        v, omega, duration = parsed
        robot.apply_velocity(v, omega, duration)

    print("--- Final Waypoints (end of each command block) ---")
    for i, p in enumerate(robot.waypoints):
        print(f"  Block {i}: (x={p[0]:.3f}, y={p[1]:.3f}, "
              f"theta={p[2]:.3f} rad / {math.degrees(p[2]):.1f} deg)")

    plot_trajectory(robot.trajectory, robot.waypoints)


if __name__ == "__main__":
    main()
