/*
    Press-fit end cap for 1-inch EMT conduit

    Nominal EMT outside diameter: 29.54 mm
    Print orientation: closed/flanged end on the print bed
    Units: millimeters
*/

$fn = 120;

// ---------- Fit adjustments ----------

// Actual outside diameter of 1-inch EMT
emt_od = 29.54;

// Clearance between the conduit and cap.
// Start with 0.20 mm for a snug fit.
// Increase to 0.30–0.40 mm if your printer makes holes undersized.
clearance = 0.20;

// The opening is slightly wider to help start the cap.
lead_in_extra = 0.35;

// ---------- Cap dimensions ----------

// How far the cap grips the conduit
grip_depth = 22;

// Thickness around the conduit
wall_thickness = 2.4;

// Thickness of the closed end
end_thickness = 3.0;

// Enlarged stop flange
flange_diameter = 40;
flange_thickness = 4.0;

// Length of tapered lead-in at the open end
lead_in_length = 3.0;

// Slight rounding approximation on outside edges
outside_chamfer = 1.0;


// Derived dimensions
inside_diameter = emt_od + clearance;
body_diameter = inside_diameter + 2 * wall_thickness;
total_height = flange_thickness + grip_depth;


difference() {
    // Outer cap body
    union() {
        // Enlarged flange / stop
        cylinder(
            h = flange_thickness,
            d1 = flange_diameter - 2 * outside_chamfer,
            d2 = flange_diameter
        );

        // Main sleeve
        translate([0, 0, flange_thickness])
            cylinder(
                h = grip_depth - outside_chamfer,
                d = body_diameter
            );

        // Chamfer around open end
        translate([
            0,
            0,
            flange_thickness + grip_depth - outside_chamfer
        ])
            cylinder(
                h = outside_chamfer,
                d1 = body_diameter,
                d2 = body_diameter - 2 * outside_chamfer
            );
    }

    // Hollow area that receives the EMT.
    // It stops before reaching the closed/flanged end.
    translate([
        0,
        0,
        flange_thickness + end_thickness
    ])
        cylinder(
            h = grip_depth - end_thickness - lead_in_length + 0.02,
            d = inside_diameter
        );

    // Tapered lead-in at the open end
    translate([
        0,
        0,
        total_height - lead_in_length
    ])
        cylinder(
            h = lead_in_length + 0.02,
            d1 = inside_diameter,
            d2 = inside_diameter + 2 * lead_in_extra
        );
}
