# Cinematic Studio Lighting & HDRI Engine (System 02)
**Rahul 3D Engine — Phase 3 Documentation**

---

## 1. Overview
The Cinematic Studio Lighting & HDRI Engine replaces ad-hoc, uncalibrated light placements with 10 mathematically structured lighting setups.

The engine automatically inspects the target object's 3D bounding box (or scene bounding volume) and scales light distances, softbox dimensions, and wattages dynamically to ensure optimal exposure without blown highlights or black voids.

---

## 2. FastMCP Tool Interface

### `setup_studio_lighting`
Deploys a complete lighting rig into a dedicated collection (`Lighting_Studio`), automatically cleaning up prior studio lights to prevent duplicates.
- **Parameters**:
  - `preset` (str): One of 10 lighting presets:
    - `three_point`: Classic Key (45°), softer Fill (-45°), and Rim backlight.
    - `dramatic_rim`: Dual intense rear edge kickers with minimal frontal fill (chiaroscuro).
    - `soft_interior`: Overhead diffuse ceiling softbox with warm cove ambient.
    - `product_clean`: High-key 4-point cyclorama studio lighting.
    - `cinematic`: Hollywood golden warm key (3200K) + deep cool teal fill (7500K).
    - `architectural`: Angled sunlight vector with ambient skylight dome.
    - `horror_atmosphere`: Low harsh green uplight with pitch dark shadows.
    - `daylight`: High-noon direct sun (5000W) with clear sky.
    - `night_scene`: Cool deep-blue moonlight with warm localized accent point.
    - `automotive_studio`: Elongated overhead and flanking strip softboxes for reflections.
  - `target_object` (str, optional): Target object to focus and scale lights around.
  - `energy_multiplier` (float): Global light intensity scaling factor.
  - `color_temperature` (float): Color temperature in Kelvin (e.g. 3200K, 5500K, 6500K).
  - `world_strength` (float): Ambient world background strength.
  - `collection_name` (str): Name of lighting collection (default: `Lighting_Studio`).
- **Risk**: `NON_DESTRUCTIVE`.

### `setup_environment_hdri`
Configures World shader nodes with an HDRI environment texture or a calibrated studio sky background.
- **Parameters**:
  - `hdri_path_or_preset` (str): Path to `.hdr` / `.exr` file or `'studio'`.
  - `strength` (float): World background emission strength.
  - `rotation` (float): Z-axis rotation angle in degrees.
  - `background_visibility` (bool): Whether environment is visible to direct camera rays.
- **Risk**: `NON_DESTRUCTIVE`.

### `inspect_lighting_setup`
Returns structured inventory of all scene lights (names, types, wattages, colors, locations, and collections) and World settings.
- **Risk**: `READ_ONLY`.

### `adjust_lighting_for_object`
Re-aims and adjusts existing scene lights to focus on a new target object's bounding center.
- **Parameters**:
  - `target_object` (str): Target mesh object name.
  - `key_fill_ratio` (float): Desired key-to-fill light intensity ratio.
- **Risk**: `REVERSIBLE`.
