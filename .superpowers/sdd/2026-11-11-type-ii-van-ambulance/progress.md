# SDD Progress Ledger: Type II Van Ambulance (Mercedes-Benz Sprinter High-Roof)

**Project Goal:** Build an exact AAA-grade 3D ambulance model matching the uploaded 6-view blueprint reference image (`media_1794403034040_0d58cb01.jpg`) using the 90/10 Hybrid Procedural Pipeline (`bmesh` + `bpy.data` in memory).

## Master Task Checklist

- [x] **Task 1: PBR Material Library Setup**
  - File: `scripts/pipeline/setup_van_materials.py`
  - Created 13 tuned PBR automotive materials.
- [x] **Task 2: Chassis Undercarriage & Front Cab Interior**
  - File: `scripts/pipeline/build_chassis_and_cab_interior.py`
  - Undercarriage: Ladder frame, crossmembers, exhaust with expansion muffler, curbside tailpipe, rear axle, differential pumpkin, fuel tank, spare tire.
  - Interior: Dual bucket seats, headrests, dashboard binnacle, steering column & wheel, bulkhead.
- [x] **Task 3: Unibody High-Roof Shell & Aerodynamic Hood**
  - File: `scripts/pipeline/build_body_shell.py`
  - Continuous lofted quad hood, seamless front fenders, curved windshield brow, 4 longitudinal roof corrugations, window cutouts.
- [x] **Task 4: Perimeter Cladding, Grille, Wheel Arches & Bumpers**
  - File: `scripts/pipeline/build_cladding_and_bumpers.py`
  - 3-bar Sprinter grille, front bumper with fog lamps and license plate, rear step bumper with non-slip tread, 4 open semicircular wheel arches ($R=0.44\text{m}$) with flared lips.
- [x] **Task 5: Aerodynamic Glass, Doors, Commercial Mirrors & Wipers**
  - File: `scripts/pipeline/build_glass_and_doors.py`
  - Compound curved windshield, tinted side privacy glass, 50/50 barn door windows, commercial towing mirrors with amber LED signals, cowl wipers, flush handles.
- [x] **Task 6: Heavy-Duty Steel Van Wheels (Master Mesh Instancing)**
  - File: `scripts/pipeline/build_van_wheels.py`
  - Master wheel with 12 circular cooling vents, hub, radial tire, brake disc/caliper, instanced across 4 wheel positions.
- [x] **Task 7: Emergency Warning Systems, Rooftop AC & Lighting**
  - File: `scripts/pipeline/build_emergency_system.py`
  - Front & rear low-profile aerodynamic lightbars (Red/Blue), 4 corner strobe pods, rooftop AC with dual circular exhaust fans, projector headlights with LED halos, D-pillar taillights.
- [x] **Task 8: Livery Decals & True 3D Vector Typography**
  - File: `scripts/pipeline/build_livery_decals.py`
  - Continuous red waistline stripe with rear 3-step digital chevrons and checkered ladder, blue 6-pointed Star of Life with white Rod of Asclepius, true 3D vector "AMBULANCE" typography (hood, sides, rear), alternating 45° rear door safety chevrons.
- [x] **Task 9: Viewport Staging, Multi-View Alignment & Quality Verification**
  - File: `scripts/pipeline/stage_and_verify_views.py`
  - Verified Top, Bottom, Front, Rear, Left, Right orthographic views and Hero 3/4 perspective view.
  - Saved to `c:\Users\Rahul\OneDrive\Desktop\Blender MCP\Type_II_Sprinter_Ambulance.blend`.
