import ezdxf
import math

# Function to calculate the perimeter and area of a polyline
def calculate_area_and_perimeter(entities):
    total_area = 0
    total_perimeter = 0
    points = []

    for entity in entities:
        print(f"Processing entity: {entity.dxftype()}")  # Debug print
        if entity.dxftype() == 'LINE':
            # Lines have no enclosed area
            start = entity.dxf.start
            end = entity.dxf.end
            # Perimeter is just the length of the line
            perimeter = math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)
            total_perimeter += perimeter
            points.append((start.x, start.y))
            points.append((end.x, end.y))
            print(f"Added LINE points: {start.x, start.y}, {end.x, end.y}")  # Debug print

        elif entity.dxftype() == 'SPLINE':
            # For splines, we approximate the spline as a series of line segments
            perimeter = 0
            area = 0
            spline_points = entity.control_points  # Get the control points of the spline
            print(f"Spline control points: {spline_points}")  # Debug print
            
            # Approximate the spline as a polygon
            num_points = len(spline_points)
            if num_points > 1:
                for i in range(num_points):
                    x1, y1, _ = spline_points[i]
                    x2, y2, _ = spline_points[(i + 1) % num_points]  # Wrap around to the first point
                    # Calculate perimeter (distance between consecutive points)
                    perimeter += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                    points.append((x1, y1))
                    points.append((x2, y2))
                    print(f"Added SPLINE points: {x1, y1}, {x2, y2}")  # Debug print
                    
                    # Calculate area using the Shoelace Theorem
                    area += x1 * y2 - x2 * y1
                    print(f"Intermediate SPLINE area: {area}")  # Debug print

            area = abs(area) / 2  # Absolute value and divide by 2
            total_area += area
            total_perimeter += perimeter

    # Remove duplicate points
    points = list(dict.fromkeys(points))
    print(f"Unique points: {points}")  # Debug print
    # Check if the points form a closed polygon
    if points and points[0] == points[-1]:
        n = len(points)
        area = 0
        for i in range(n - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            area += x1 * y2 - x2 * y1
            print(f"Intermediate polygon area: {area}")  # Debug print
        total_area = abs(area) / 2.0

    return total_area, total_perimeter

# Load your DXF file
dxf_file = "sample.dxf"
doc = ezdxf.readfile(dxf_file)

# Check the units used in the DXF file
units = doc.header.get('$INSUNITS', 0)
units_dict = {
    0: "Unitless",
    1: "Inches",
    2: "Feet",
    3: "Miles",
    4: "Millimeters",
    5: "Centimeters",
    6: "Meters",
    7: "Kilometers",
    8: "Microinches",
    9: "Mils",
    10: "Yards",
    11: "Angstroms",
    12: "Nanometers",
    13: "Microns",
    14: "Decimeters",
    15: "Decameters",
    16: "Hectometers",
    17: "Gigameters",
    18: "Astronomical units",
    19: "Light years",
    20: "Parsecs"
}
unit_name = units_dict.get(units, "Unknown")
print(f"Units: {unit_name}")

# Calculate area and perimeter for all entities
area, perimeter = calculate_area_and_perimeter(doc.modelspace().entity_space)

# Output the results
print(f"Total Area: {area}")
print(f"Total Perimeter: {perimeter}")
