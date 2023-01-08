from typing import NamedTuple

from parse import parse

from adventofcode2022.utils.abstract import FileReaderSolution
from adventofcode2022.utils.point import XYPoint as Point


class Line(NamedTuple):
    sensor: Point
    beacon: Point
    distance: int


class Day15:
    lines: list[Line]

    def parse(self, input_lines: list[str]):
        """Parse line:
        Sensor at x=2, y=0: closest beacon is at x=2, y=10
        """
        self.lines = []
        for line in input_lines:
            p = parse(
                "Sensor at x={sx:d}, y={sy:d}: closest beacon is at x={bx:d}, y={by:d}",
                line,
            )
            sensor = Point(p["sx"], p["sy"])
            beacon = Point(p["bx"], p["by"])
            distance = abs(sensor.distance(beacon))
            self.lines.append(Line(sensor=sensor, beacon=beacon, distance=distance))

    @staticmethod
    def remaining_on_line(line, y):
        """Calculate the distance between the sensor and the row we are measuring"""
        return line.distance - abs(line.sensor.y - y)


class Day15PartA(Day15, FileReaderSolution):
    def find_positions(self, row) -> int:
        invalid_points = set()
        # Exclude the beacons on this lines
        beacons_on_row = set()

        for line in self.lines:
            if line.beacon.y == row:
                # We do not calculate the beacons.
                beacons_on_row.add(line.beacon)

            # Calculate the distande between the sensor and the row we are measuring
            remainder = self.remaining_on_line(line, row)

            # Skip sensors too far away
            if remainder < 0:
                continue

            for i in range(remainder + 1):
                invalid_points.add(line.sensor.x + i)
                invalid_points.add(line.sensor.x - i)

        return len(invalid_points) - len(beacons_on_row)

    def execute(self, input_data, row=2000000) -> int:
        self.parse(input_data.splitlines())
        return self.find_positions(row)

    def solve(self, input_data: str) -> int:
        return self.execute(input_data, row=2000000)


class Day15PartB(Day15, FileReaderSolution):
    def find_frequency(self, max: int) -> int:
        """Find the tuning frequency"""
        y = 0
        # for y in range(max+1):
        for y in range(11, 12):
            # Loop over every line (y)
            print(f"New line {y}")
            x = 0
            while x <= max:
                # Loop over every x coordinate.
                new_x = x
                for line in self.lines:
                    new_x = self.skip_over_line(line, x, y)
                    # print(f"{new_x=}")
                    if x != new_x:
                        break
                if new_x == x:
                    # Return here?
                    res = (x * max) + y
                    print(f"Result ?? {res=} ({x=} , {y=}")
                    return res
                x = new_x

        raise ValueError("No known solution")

    def skip_over_line(self, line, x, y):
        remaining = self.remaining_on_line(line, y)
        if x >= (line.sensor.x - remaining) and x <= (line.sensor.x + remaining):
            return line.sensor.x + 1
        return x
        # if line[0].x - remaining <= x <= line[0].x + remaining:
        #     return line[0].x + remaining + 1
        # return x

    def execute(self, input_data: str, factor: int) -> int:
        self.parse(input_data.splitlines())
        return self.find_frequency(factor)

    def solve(self, input_data: str) -> int:
        return self.execute(input_data, factor=4_000_000)
