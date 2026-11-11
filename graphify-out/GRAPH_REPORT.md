# Graph Report - Blender MCP  (2026-11-11)

## Corpus Check
- 82 files · ~149,303 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 5, .lock 1)

## Summary
- 2803 nodes · 5727 edges · 146 communities (102 shown, 44 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 301 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6dc42191`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- addon.py
- bundled/addon.py
- TrajectoryRecorder
- test_meshy.py
- test_polyhaven.py
- get_blender_connection
- test_compat_matrix.py
- test_export_scene.py
- update_cli.py
- ._polyhaven_import_texture
- BlenderMCPServer
- test_addon_autostart.py
- CustomPropMixin
- premium_request
- test_setup_cli.py
- test_tripo.py
- get_telemetry
- server.py
- generation.py
- TelemetryCollector
- Context
- test_generation.py
- test_openai_apps.py
- PTLASManager
- premium_active
- FakeResponse
- _Validator
- Capabilities
- setup_cli.py
- generate_3d
- BlenderMCPServer
- _material
- addon_manager.py
- ._get_config_value
- GenerationError
- test_polypizza.py
- _blendermcp_ensure_server_running
- consent_prompt.py
- FrameReceiver
- Pending
- test_consolidated_tools.py
- FakeObject
- test_connection_args.py
- FakeBlender
- server
- context_log.py
- Job
- Any
- UserEditRecorder
- telemetry.py
- numpy
- UserEditRecorder
- clas_tensor_shaper.py
- test_safe_mode.py
- premium_integration_status
- ViewportStore
- premium_integration_status
- _polyhaven_api_get
- detect_clients
- README.md
- _install_search
- test_server_threading.py
- test_context_log.py
- Blender MCP - Terms of Use and Privacy Policy
- test_addon_updater.py
- test_hunyuan_api_profile.py
- tripo_endpoints
- ._polyhaven_import_model
- safe_mode.py
- Review Focus
- sdf_visual_hull.py
- SandboxViolation
- re
- tripo_endpoints
- test_socket_unicode.py
- premium_active
- _polyhaven_api_get
- curvature_pbr_compiler.py
- FakeSocketCollection
- .download_polypizza_model
- .download_polypizza_model
- _asset
- _register_edit_capture_handlers
- .execute_command
- _exchange
- _downloaded
- ._get_sketchfab_api_key
- json
- ._get_sketchfab_api_key
- _premium_meshy
- .execute_command
- guides.py
- MCP Client Setup
- Installation
- Blender DXR Kernel Architect
- _load_server_class
- check_for_addon_update
- ._polyhaven_import_texture
- .set_texture
- blender_mcp/__init__.py
- Scene design
- _download_polyhaven
- claude_code_state
- .download_polyhaven_asset
- .pick_viewport_object
- .pick_viewport_object
- Animation
- Materials and texturing
- Retopology and mesh cleanup
- Rigging
- _polyhaven_category_paths
- _polypizza_filter_params
- mcp-for-blender
- _polypizza_filter_params
- Writing bpy that works on any Blender
- Level design
- test_addon_compat.py
- _load_addon
- _polyhaven_available
- run_setup
- FakeObject
- ._polyhaven_material_info
- Usage
- premium_enabled_generators
- _polyhaven_blend_version
- 10. Intellectual Property
- test_disabled_polypizza_hides_the_commands_but_keeps_status
- toml_reader
- Install-McpForBlender
- install.sh script
- Technical Details
- test_repeating_an_unfinished_request_resumes_instead_of_paying_again
- test_server_resolves_names_aliases_and_ids
- mcp-for-blender

## God Nodes (most connected - your core abstractions)
1. `BlenderMCPServer` - 112 edges
2. `BlenderMCPServer` - 112 edges
3. `_install_requests()` - 70 edges
4. `get_blender_connection()` - 45 edges
5. `server()` - 39 edges
6. `GenerationError` - 38 edges
7. `TrajectoryRecorder` - 34 edges
8. `Job` - 32 edges
9. `Pending` - 32 edges
10. `submit()` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Limitations & Security Considerations` --references--> `execute_blender_code()`  [INFERRED]
  README.md → src/blender_mcp/server.py
- `Capabilities` --references--> `get_addon_status()`  [INFERRED]
  README.md → src/blender_mcp/server.py
- `Capabilities` --references--> `disable_telemetry()`  [INFERRED]
  README.md → src/blender_mcp/server.py
- `Capabilities` --references--> `look()`  [INFERRED]
  README.md → src/blender_mcp/server.py
- `Capabilities` --references--> `generate_3d()`  [INFERRED]
  README.md → src/blender_mcp/server.py

## Import Cycles
- None detected.

## Communities (146 total, 44 thin omitted)

### Community 0 - "addon.py"
Cohesion: 0.03
Nodes (59): addon_version_label(), BLENDERMCP_AddonPreferences, BLENDERMCP_OT_OpenTerms, BLENDERMCP_OT_PremiumActivate, BLENDERMCP_OT_PremiumDeactivate, BLENDERMCP_OT_PremiumOpenAccount, BLENDERMCP_OT_PremiumRefresh, BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey (+51 more)

### Community 1 - "bundled/addon.py"
Cohesion: 0.04
Nodes (57): addon_release_key(), _addon_update_check_on_startup(), addon_version_label(), _blendermcp_bind_address(), _blendermcp_depsgraph_post(), _blendermcp_ensure_server_running(), _blendermcp_load_post(), BLENDERMCP_OT_CheckAddonUpdate (+49 more)

### Community 2 - "TrajectoryRecorder"
Cohesion: 0.06
Nodes (15): _cap_text(), compute_state_delta(), _enforce_db_size_guard(), _exceeds(), _fit_snapshot(), _json_size(), _normalize_goal(), semantic_action_for_operator() (+7 more)

### Community 3 - "test_meshy.py"
Cohesion: 0.06
Nodes (53): _gets(), _posts(), _resolve(), _Response, test_addon_checks_every_redirect(), test_addon_follows_public_redirects_to_an_image(), test_addon_refuses_a_downloaded_non_image(), test_addon_refuses_local_and_private_image_hosts() (+45 more)

### Community 4 - "test_polyhaven.py"
Cohesion: 0.04
Nodes (43): _blend_bytes(), _blend_with_includes(), _file(), _install_requests(), _props(), test_a_blend_with_no_matching_collection_still_imports(), test_a_category_filter_uses_the_taxonomy_parameter_not_the_legacy_one(), test_a_compressed_blend_header_is_read() (+35 more)

### Community 5 - "get_blender_connection"
Cohesion: 0.05
Nodes (33): _app_error(), _capture_viewport(), clas_boolean_carve(), clas_eval_bezier_patch(), clas_loft_splines(), disable_telemetry(), _download_polypizza(), export_game_asset() (+25 more)

### Community 6 - "test_compat_matrix.py"
Cohesion: 0.06
Nodes (33): AddonHandshake, handshake_addon(), _stale_addon_source(), test_bundled_addon_exists_and_has_protocol(), test_handshake_missing_command_on_old_addon(), test_handshake_outdated_protocol(), test_handshake_up_to_date(), test_install_addon_copies_into_target_dir() (+25 more)

### Community 7 - "test_export_scene.py"
Cohesion: 0.06
Nodes (27): premium_generation_guidance(), _load_addon(), export(), _Object, _Objects, test_command_is_always_routed(), test_missing_objects_and_bad_input_are_rejected_before_exporting(), test_named_objects_export_with_their_children_as_glb() (+19 more)

### Community 8 - "update_cli.py"
Cohesion: 0.08
Nodes (27): addon_release_key(), addon_version_label(), update_installed_addons(), current_version(), fetch_latest_version(), find_uv(), run_update(), _update_addon() (+19 more)

### Community 9 - "._polyhaven_import_texture"
Cohesion: 0.07
Nodes (15): _polyhaven_asset_record(), _polyhaven_asset_url(), _polyhaven_authors(), _polyhaven_available(), _polyhaven_dimensions_mm(), _polyhaven_download(), _polyhaven_mapping_node(), _polyhaven_preview_url() (+7 more)

### Community 11 - "test_addon_autostart.py"
Cohesion: 0.11
Nodes (28): _load_autostart_helpers(), _manual_connect(), _Server, _set_bind_preferences(), test_auto_start_does_not_bind_when_configuration_is_rejected(), test_auto_start_uses_the_configured_bind_address(), test_background_mode_does_not_schedule_retries(), test_bind_address_validation() (+20 more)

### Community 12 - "CustomPropMixin"
Cohesion: 0.06
Nodes (16): CustomPropMixin, FakeCollection, FakeCollections, FakeColorspace, FakeImage, FakeImages, FakeLink, FakeLinks (+8 more)

### Community 13 - "premium_request"
Cohesion: 0.07
Nodes (24): BLENDERMCP_AddonPreferences, BLENDERMCP_OT_PremiumActivate, BLENDERMCP_OT_PremiumDeactivate, BLENDERMCP_OT_PremiumOpenAccount, BLENDERMCP_OT_SetFreeTrialHyper3DAPIKey, BLENDERMCP_PT_Panel, get_blendermcp_addon_preferences(), premium_api_url() (+16 more)

### Community 14 - "test_setup_cli.py"
Cohesion: 0.15
Nodes (32): _cli_commands(), _cli_key(), _cli_server_names(), Client, client_state(), ClientResult, ClientState, configure_cli_client() (+24 more)

### Community 15 - "test_tripo.py"
Cohesion: 0.11
Nodes (28): _capture_posts(), post(), _install_bpy_stubs(), _JsonResponse, _load_addon(), _premium(), _ready(), test_tripo_commands_stay_unregistered_until_enabled() (+20 more)

### Community 16 - "get_telemetry"
Cohesion: 0.10
Nodes (22): _append_note(), classify_tool_result(), _consent_note(), _drain_human_activity(), _extract_tool_params(), _maybe_snapshot_world_state(), _note_client_and_goal(), _record_observe_step() (+14 more)

### Community 17 - "server.py"
Cohesion: 0.09
Nodes (11): main(), viewport_html(), viewport_icon(), premium_hint_once(), _addon_protocol(), collection_resource(), material_resource(), object_resource() (+3 more)

### Community 18 - "generation.py"
Cohesion: 0.09
Nodes (16): default_name(), import_result(), is_image_bytes(), poll(), process_bbox(), _relay(), request_key(), _rodin_images() (+8 more)

### Community 20 - "Context"
Cohesion: 0.09
Nodes (17): _OpenAIFormRequest, pick_asset(), picked_reply(), PickerOption, PickResult, _download_sketchfab(), _format_scene_summary(), get_scene_info() (+9 more)

### Community 21 - "test_generation.py"
Cohesion: 0.10
Nodes (21): choose_provider(), _MeshyStatusBlender, _pose_call(), _StatusBlender, test_auto_falls_back_to_own_keys(), test_auto_prefers_premium_generators(), test_explicit_provider_must_be_on_in_premium(), test_meshy_handles_name_a_meshy_task_kind() (+13 more)

### Community 22 - "test_openai_apps.py"
Cohesion: 0.10
Nodes (19): picker_schema(), _ctx(), _fake_blender(), _search_polypizza(), test_a_bad_or_failed_picker_falls_back_to_the_listing(), test_closing_the_picker_is_reported(), test_consent_prompt_only_counts_an_explicit_yes(), elicit_form() (+11 more)

### Community 23 - "PTLASManager"
Cohesion: 0.11
Nodes (8): audit_script_ast(), compute_mesh_hash(), PTLASManager, test_ast_audit_blocks_factory_reset(), test_ast_audit_blocks_global_select_all_delete(), test_ast_audit_safe_code(), test_compute_mesh_hash_consistency(), test_ptlas_manager_transactions()

### Community 24 - "premium_active"
Cohesion: 0.09
Nodes (6): _check_public_url(), _fetch_public_image(), hunyuan_api_profile(), _is_image_bytes(), premium_active(), _read_image_file()

### Community 25 - "FakeResponse"
Cohesion: 0.07
Nodes (19): FakeResponse, _install_preview(), fake_get(), fake_get(), fake_get(), _install_taxonomy(), fake_get(), test_a_preview_keeps_the_thumbnails_cache_busting_version() (+11 more)

### Community 27 - "Capabilities"
Cohesion: 0.09
Nodes (19): Global Constraints, Capabilities, Hunyuan3D on Tencent Cloud (Official API mode), Meshy, Poly Haven, Poly Pizza, Tripo, _addon_lacks() (+11 more)

### Community 28 - "setup_cli.py"
Cohesion: 0.11
Nodes (19): blender_config_base(), addon_module_name(), AddonOutcome, blender_is_running(), blender_version(), _codex_home(), codex_plugin_installed(), codex_state() (+11 more)

### Community 29 - "generate_3d"
Cohesion: 0.10
Nodes (13): format_handshake_log(), BlenderConnection, generate_3d(), _generation_reply(), _generation_send(), get_addon_status(), _integrations(), _maybe_handshake_addon() (+5 more)

### Community 31 - "_material"
Cohesion: 0.10
Nodes (17): _link_into(), _material(), _node_of_type(), test_a_downloaded_material_is_not_given_a_fake_user(), test_a_textures_real_world_size_is_saved_into_the_file(), test_an_albedo_not_called_diffuse_is_still_connected(), test_base_colour_roughness_and_metallic_are_connected(), test_displacement_is_connected_to_the_material_output() (+9 more)

### Community 32 - "addon_manager.py"
Cohesion: 0.13
Nodes (13): addon_file_needs_update(), AddonInstallResult, AddonStatusReport, AddonUpdate, _backup_addon_file(), check_addon_status_on_startup(), discover_blender_addon_dirs(), find_existing_addon_installs() (+5 more)

### Community 34 - "._get_config_value"
Cohesion: 0.10
Nodes (5): _check_public_url(), _fetch_public_image(), hunyuan_api_profile(), _is_image_bytes(), _read_image_file()

### Community 35 - "GenerationError"
Cohesion: 0.14
Nodes (22): GenerationError, submit(), FakeAddon, test_failed_import_is_an_error(), test_hunyuan_failure_says_why(), test_hunyuan_polls_tencent_shapes_and_imports_the_glb(), test_meshy_long_prompts_are_rejected_before_sending(), test_meshy_pose_mode_is_sent_only_when_set() (+14 more)

### Community 36 - "test_polypizza.py"
Cohesion: 0.19
Nodes (17): FakeResponse, _record_requests(), _server(), test_animated_is_omitted_unless_animated_only_was_asked_for(), test_api_key_is_never_sent_to_the_cdn(), test_attribution_is_written_onto_the_imported_object(), test_cloudflare_challenge_gets_its_own_error(), test_enabled_polypizza_with_a_key_reports_ready() (+9 more)

### Community 37 - "_blendermcp_ensure_server_running"
Cohesion: 0.10
Nodes (14): _addon_update_check_on_startup(), _blendermcp_bind_address(), _blendermcp_ensure_server_running(), _blendermcp_load_post(), BLENDERMCP_OT_CheckAddonUpdate, BLENDERMCP_OT_StartServer, _blendermcp_port_has_listener(), _blendermcp_register_auto_start() (+6 more)

### Community 38 - "consent_prompt.py"
Cohesion: 0.14
Nodes (10): _already_answered(), _apply_consent(), _client_supports_elicitation(), _current_consent(), maybe_prompt_for_consent(), _read_state(), reset_for_tests(), _session_key() (+2 more)

### Community 39 - "FrameReceiver"
Cohesion: 0.16
Nodes (10): encode_frame(), FrameReceiver, receive_framed_message(), send_framed_message(), test_encode_frame_dict(), test_frame_receiver_fragmented_chunks(), test_frame_receiver_large_payload(), test_frame_receiver_legacy_unframed_fallback() (+2 more)

### Community 40 - "Pending"
Cohesion: 0.20
Nodes (16): Pending, _count(), _meshy(), _run(), _start_meshy(), test_meshy_api_errors_are_relayed_without_retrying(), test_meshy_failed_preview_says_why_and_clears_pending(), test_meshy_failed_refine_says_why_and_clears_pending() (+8 more)

### Community 41 - "test_consolidated_tools.py"
Cohesion: 0.11
Nodes (10): _Blender, _look_text(), test_a_missing_library_command_means_switched_off_or_outdated(), test_image_mode_never_falls_back_to_the_viewport(), test_look_passes_directions_and_distance_through(), test_look_rejects_bad_views_before_touching_blender(), test_retired_look_modes_point_to_their_replacements(), test_scene_info_sends_only_the_requested_fields() (+2 more)

### Community 42 - "FakeObject"
Cohesion: 0.09
Nodes (9): FakeLibraries, FakeLibraryLoad, FakeMesh, FakeObject, test_set_texture_credits_the_artist(), test_set_texture_needs_the_texture_downloaded_first(), test_set_texture_reports_the_node_that_decides_the_tiling(), test_set_texture_reports_the_node_tree_it_built() (+1 more)

### Community 43 - "test_connection_args.py"
Cohesion: 0.13
Nodes (15): main(), parse_connection_args(), resolve_connection(), _clear_env(), test_cli_host_and_port_override_independently(), test_cli_overrides_environment(), test_defaults_when_nothing_is_configured(), test_empty_env_port_falls_back() (+7 more)

### Community 44 - "FakeBlender"
Cohesion: 0.09
Nodes (7): FakeBlender, test_a_models_three_axis_size_is_reported_in_full(), test_a_texture_with_no_published_size_says_nothing_about_tiling(), test_the_download_message_says_how_big_the_texture_is_and_how_to_tile_it(), test_the_tool_response_says_where_the_asset_came_from(), test_tool_boundary_converts_names_to_numeric_ids(), test_zero_tri_count_is_reported_as_unknown_not_zero()

### Community 45 - "server"
Cohesion: 0.11
Nodes (15): test_meshy_switched_off_relays_the_addon_setup_steps(), test_missing_meshy_commands_explain_the_setup(), test_tripo_switched_off_relays_the_addon_setup_steps(), send_command(), _fresh_store(), test_captures_say_which_file_and_scene_they_show(), test_clicking_empty_space_or_an_unpickable_capture(), test_clicking_the_viewport_returns_a_link_to_the_object() (+7 more)

### Community 46 - "context_log.py"
Cohesion: 0.16
Nodes (11): context_log_enabled(), context_log_path(), _image_entry(), install(), logged_call(), logged_list(), _jpeg_size(), _json_chars() (+3 more)

### Community 47 - "Job"
Cohesion: 0.22
Nodes (7): Job, _start_refine(), test_bad_handles_are_rejected(), test_errors_after_submit_keep_the_handle(), test_meshy_refine_records_outlive_completion_but_age_out(), test_old_or_unreadable_pending_entries_are_ignored(), test_running_out_of_time_returns_a_resumable_handle()

### Community 48 - "Any"
Cohesion: 0.15
Nodes (14): _client_capabilities(), client_extensions(), _env_flag(), is_app_only(), supports_apps(), supports_openai_forms(), _list_tools_for_client(), _log_client_features() (+6 more)

### Community 50 - "telemetry.py"
Cohesion: 0.11
Nodes (6): server_lifespan(), EventType, get_package_version(), is_telemetry_enabled(), record_startup(), record_tool_usage()

### Community 51 - "numpy"
Cohesion: 0.19
Nodes (9): normal_to_track_quaternion(), raycast_surface_point(), unproject_pixel_ray(), test_normal_to_track_quaternion(), test_raycast_surface_point_plane(), test_unproject_pixel_ray_ortho_front(), test_extract_sdf_isosurface(), test_generate_hull_mesh_synthetic() (+1 more)

### Community 53 - "clas_tensor_shaper.py"
Cohesion: 0.15
Nodes (9): apply_blender_version_compatibility(), _bernstein_basis_and_derivs(), eval_bicubic_bezier_patch(), loft_spline_sections(), test_apply_blender_version_compatibility_shim(), __init__(), test_eval_bicubic_bezier_patch_curved_dome(), test_eval_bicubic_bezier_patch_flat_plane() (+1 more)

### Community 54 - "test_safe_mode.py"
Cohesion: 0.13
Nodes (9): safe_mode_enabled(), test_allows_legitimate_script(), test_blocks_escape(), test_disabled_by_default(), test_disabled_values(), test_enabled_values(), test_execute_blender_code_passes_valid_code_through(), test_execute_blender_code_short_circuits() (+1 more)

### Community 56 - "ViewportStore"
Cohesion: 0.12
Nodes (6): ViewportStore, test_an_edit_during_a_capture_leaves_the_image_stale(), test_every_blender_command_is_counted_even_when_it_fails(), fail(), test_viewport_capture_reports_blender_errors_to_the_app(), test_viewport_result_only_sends_the_image_when_it_changed()

### Community 58 - "_polyhaven_api_get"
Cohesion: 0.12
Nodes (8): _polyhaven_api_get(), _polyhaven_cache_key(), _polyhaven_cache_touch(), _polyhaven_category_paths(), _polyhaven_keyword_match(), _polyhaven_search(), _polyhaven_taxonomy(), PolyHavenAPIError

### Community 59 - "detect_clients"
Cohesion: 0.18
Nodes (13): _antigravity_config(), _appdata(), _claude_desktop_dir(), detect_clients(), _devin_config(), _opencode_config(), _vscode_user_dir(), _xdg_config() (+5 more)

### Community 60 - "README.md"
Cohesion: 0.12
Nodes (16): Components, Contributing, Disclaimer, Features, Feedback, Installing the Blender Addon, Join the Community, Limitations & Security Considerations (+8 more)

### Community 61 - "_install_search"
Cohesion: 0.12
Nodes (9): _install_search(), test_a_query_is_answered_by_the_search_endpoint(), test_a_rate_limited_search_says_how_long_to_wait(), test_a_search_hit_outside_the_category_filter_is_dropped(), test_an_unavailable_search_index_falls_back_to_keywords(), test_search_asks_for_the_whole_ranking_not_the_first_page(), test_search_order_is_the_ranking_and_is_not_re_sorted(), test_search_results_carry_the_metadata_the_api_already_returned() (+1 more)

### Community 63 - "test_server_threading.py"
Cohesion: 0.19
Nodes (8): bpy_timer_registered(), _free_port(), _make_server(), _pump(), test_client_thread_never_registers_a_timer(), test_command_is_queued_not_executed_on_client_thread(), test_restart_rebinds_port_cleanly(), test_stop_releases_client_threads()

### Community 64 - "test_context_log.py"
Cohesion: 0.20
Nodes (9): _entries(), log_path(), _png(), _run(), _server(), snap(), test_disabled_by_default(), test_keeps_existing_tools_list_filter() (+1 more)

### Community 66 - "Blender MCP - Terms of Use and Privacy Policy"
Cohesion: 0.12
Nodes (15): 11. No Warranty, 12. Limitation of Liability, 13. Changes, 14. Contact, 15. Consent, 1. About This Project, 2. Data I Collect, 3. How I May Use Your Data (+7 more)

### Community 67 - "test_addon_updater.py"
Cohesion: 0.23
Nodes (11): _serve(), test_a_protocol_bump_alone_counts_as_newer(), test_bad_downloads_are_errors_not_updates(), test_install_refuses_anything_but_a_valid_addon(), test_install_replaces_the_file_and_keeps_a_backup(), test_newer_main_is_offered(), test_offline_is_an_error_not_a_crash(), test_release_key_reads_version_and_protocol() (+3 more)

### Community 68 - "test_hunyuan_api_profile.py"
Cohesion: 0.32
Nodes (13): _capture_post(), fake_post(), _load_addon(), _Response, _scene(), _server_with_credentials(), test_poll_uses_the_matching_query_profile(), test_profile_defaults_to_the_mainland_ai3d_service() (+5 more)

### Community 70 - "._polyhaven_import_model"
Cohesion: 0.16
Nodes (4): _polyhaven_asset_url(), _polyhaven_download(), _polyhaven_summarize_asset(), _polyhaven_tag()

### Community 71 - "safe_mode.py"
Cohesion: 0.18
Nodes (5): _attr_chain(), _check_depth(), _check_module_value_use(), _collect_bindings(), _path_is_blocked()

### Community 72 - "Review Focus"
Cohesion: 0.13
Nodes (12): DXR-Inspired Blender MCP Graphics Kernel Implementation Plan, Review Focus, Task 10: Full Regression & Integration Verification, Task 1: Length-Prefixed Binary Socket Framing Protocol, Task 2: PTLAS Scene Partitioning & Copy-on-Write Isolation Kernel, Task 3: Visual Hull Space-Carving & OpenVDB SDF Engine, Task 4: CLAS Cluster Templates & Zero-Copy Tensor Shaper, Task 5: G-Buffer Vision Sensor & 2D-to-3D Raycast Unprojector (+4 more)

### Community 73 - "sdf_visual_hull.py"
Cohesion: 0.19
Nodes (4): compute_visual_hull_tensor(), extract_sdf_isosurface(), generate_hull_mesh_data(), _resize_2d()

### Community 74 - "SandboxViolation"
Cohesion: 0.16
Nodes (8): _guard_source(), is_safe(), SandboxViolation, validate_code(), test_is_safe_returns_reason(), test_size_limit(), test_syntax_error_is_a_violation(), test_violation_carries_line_number()

### Community 75 - "re"
Cohesion: 0.14
Nodes (10): _codex_mcp_sections(), add(), add_keys(), _parse_selection(), safe_to_save_prefs(), _strip_jsonc(), test_codex_regex_fallback_ignores_other_tables(), test_parse_selection() (+2 more)

### Community 77 - "test_socket_unicode.py"
Cohesion: 0.19
Nodes (5): _make_server(), _ScriptedSocket, _split_after_lead_byte(), test_split_multibyte_utf8_boundary_is_not_dropped(), test_split_multibyte_utf8_boundary_keeps_handler_loop_alive()

### Community 79 - "_polyhaven_api_get"
Cohesion: 0.15
Nodes (6): _polyhaven_api_get(), _polyhaven_cache_key(), _polyhaven_cache_touch(), _polyhaven_keyword_match(), _polyhaven_search(), PolyHavenAPIError

### Community 80 - "curvature_pbr_compiler.py"
Cohesion: 0.19
Nodes (6): build_triplanar_pbr_spec(), calculate_bottom_pivot_offset(), compute_laplacian_curvature(), test_build_triplanar_pbr_spec(), test_calculate_bottom_pivot_offset(), test_compute_laplacian_curvature_cube()

### Community 81 - "FakeSocketCollection"
Cohesion: 0.15
Nodes (4): FakeNode, FakeNodes, FakeSocket, FakeSocketCollection

### Community 82 - ".download_polypizza_model"
Cohesion: 0.17
Nodes (3): get_all_mesh_children(), _polypizza_cdn_error(), _polypizza_summarize_model()

### Community 84 - ".download_polypizza_model"
Cohesion: 0.17
Nodes (3): get_all_mesh_children(), _polypizza_cdn_error(), _polypizza_summarize_model()

### Community 86 - "_asset"
Cohesion: 0.17
Nodes (7): _asset(), test_a_size_floor_excludes_what_publishes_no_size(), test_a_size_floor_leaves_out_textures_that_would_tile(), test_a_size_floor_narrows_a_ranked_search_without_reordering_it(), test_a_size_floor_that_matches_nothing_says_so_rather_than_looking_empty(), test_search_ranks_before_truncating(), test_the_result_limit_is_capped()

### Community 87 - "_register_edit_capture_handlers"
Cohesion: 0.29
Nodes (7): _blendermcp_depsgraph_post(), _blendermcp_redo_post(), _blendermcp_undo_post(), _register_edit_capture_handlers(), sync_edit_capture_handlers(), _telemetry_consent_enabled(), _unregister_edit_capture_handlers()

### Community 89 - "_exchange"
Cohesion: 0.29
Nodes (9): _exchange(), reply_to(), send(), _list_tools(), step(), test_app_only_tools_are_hidden_from_clients_without_mcp_apps(), test_app_only_tools_are_listed_for_mcp_apps_clients(), test_picker_round_trip_over_the_wire() (+1 more)

### Community 90 - "_downloaded"
Cohesion: 0.18
Nodes (7): _downloaded(), _mkdir(), test_a_blend_newer_than_this_blender_falls_back_to_gltf(), test_formats_other_than_blend_are_rejected_before_downloading(), test_model_includes_cannot_escape_the_download_directory(), test_models_default_to_blend(), test_only_the_maps_the_material_uses_are_downloaded()

### Community 92 - "json"
Cohesion: 0.27
Nodes (3): build(), parse_result(), main()

### Community 94 - "_premium_meshy"
Cohesion: 0.20
Nodes (8): poll(), _premium_meshy(), _reply_for(), test_meshy_premium_failure_is_relayed(), test_meshy_premium_job_resumes_from_its_handle(), test_meshy_premium_reply_keeps_its_real_world_scale(), test_meshy_reply_keeps_its_real_world_scale(), test_other_generators_still_get_the_rescale_advice()

### Community 96 - "guides.py"
Cohesion: 0.39
Nodes (5): all_guides(), get(), Guide, index(), _parse()

### Community 97 - "MCP Client Setup"
Cohesion: 0.22
Nodes (9): Antigravity, Claude for Desktop, Codex, Codex plugin (recommended), Cursor, MCP Client Setup, OpenCode, Plain MCP server (+1 more)

### Community 98 - "Installation"
Cohesion: 0.22
Nodes (9): Automatic setup, Environment Variables, Install without uv, Installation, Make your client find uvx, Pin the Python version, Prerequisites, Run with Docker (+1 more)

### Community 99 - "Blender DXR Kernel Architect"
Cohesion: 0.22
Nodes (8): Anti-Patterns & Rationalizations, Blender DXR Kernel Architect, FastMCP Tool Reference, Overview, Standard Workflows, The 4 Core Architectural Laws, Workflow 1: Aerodynamic Vehicle (e.g. Ambulance, Sports Car), Workflow 2: Large Architecture / Multi-Room Scene (e.g. 50-Room Hospital)

### Community 101 - "check_for_addon_update"
Cohesion: 0.25
Nodes (4): addon_release_key(), BLENDERMCP_OT_UpdateAddon, check_for_addon_update(), install_addon_update()

### Community 103 - ".set_texture"
Cohesion: 0.29
Nodes (3): _polyhaven_asset_record(), _polyhaven_authors(), _polyhaven_dimensions_mm()

### Community 105 - "Scene design"
Cohesion: 0.25
Nodes (7): After every import, Composition, Getting assets, Lighting, Render settings, Scene design, Workflow

### Community 106 - "_download_polyhaven"
Cohesion: 0.25
Nodes (4): _download_polyhaven(), _polyhaven_credit(), _polyhaven_scale_note(), _set_texture()

### Community 107 - "claude_code_state"
Cohesion: 0.25
Nodes (5): claude_code_state(), _claude_json_path(), _entry_text(), servers_state(), test_servers_state()

### Community 114 - "Animation"
Cohesion: 0.29
Nodes (6): Animation, Checking motion, Keyframes, Making it feel alive, Organizing, Reaching fcurves

### Community 115 - "Materials and texturing"
Cohesion: 0.29
Nodes (6): Believable values, Check it, Creating materials, Materials and texturing, Procedural, Textures

### Community 116 - "Retopology and mesh cleanup"
Cohesion: 0.29
Nodes (6): Bake detail back, Clean up, Diagnose, Reduce, Retopology and mesh cleanup, UVs

### Community 117 - "Rigging"
Cohesion: 0.29
Nodes (6): Before rigging, Humanoids: Rigify, Rigging, Simple or non-humanoid rigs, Skinning, Verify

### Community 119 - "_polypizza_filter_params"
Cohesion: 0.33
Nodes (3): _polypizza_category_id(), _polypizza_filter_params(), _polypizza_licence_id()

### Community 120 - "mcp-for-blender"
Cohesion: 0.33
Nodes (5): BLENDER_MCP_APPS, BLENDER_MCP_OPENAI_FORMS, mcp-for-blender, uvx, mcp-for-blender

### Community 121 - "_polypizza_filter_params"
Cohesion: 0.33
Nodes (3): _polypizza_category_id(), _polypizza_filter_params(), _polypizza_licence_id()

### Community 122 - "Writing bpy that works on any Blender"
Cohesion: 0.33
Nodes (5): Data API over operators, Look things up instead of guessing, Portability rules, Working style, Writing bpy that works on any Blender

### Community 123 - "Level design"
Cohesion: 0.33
Nodes (5): Blockout, Engine-ready output, Level design, Metrics first, Modular kits

### Community 124 - "test_addon_compat.py"
Cohesion: 0.53
Nodes (3): _connect(), test_hunyuan_quality_reaches_only_addons_that_accept_it(), test_tripo_explains_itself_when_the_addon_has_no_tripo()

### Community 125 - "_load_addon"
Cohesion: 0.40
Nodes (4): addon(), test_addon_lists_and_ranks_scene_items(), _load_addon(), _scene()

### Community 126 - "_polyhaven_available"
Cohesion: 0.40
Nodes (3): _polyhaven_available(), _polyhaven_resolution_rank(), _polyhaven_sorted_resolutions()

### Community 127 - "run_setup"
Cohesion: 0.40
Nodes (4): _ask(), find_uvx(), run_setup(), test_run_setup_needs_uvx()

### Community 131 - "Usage"
Cohesion: 0.50
Nodes (4): Example Commands, Starting the Connection, Usage, Using with Claude

### Community 134 - "10. Intellectual Property"
Cohesion: 0.50
Nodes (4): 10. Intellectual Property, AI-Generated Content, Blender MCP, Your Content

### Community 136 - "test_disabled_polypizza_hides_the_commands_but_keeps_status"
Cohesion: 0.50
Nodes (3): test_bare_search_without_filters_is_rejected_before_the_network(), request_should_not_run(), test_disabled_polypizza_hides_the_commands_but_keeps_status()

### Community 140 - "Technical Details"
Cohesion: 0.67
Nodes (3): Communication Protocol, Connecting from another machine, Technical Details

## Knowledge Gaps
- **5 isolated node(s):** `uvx`, `mcp-for-blender`, `BLENDER_MCP_APPS`, `BLENDER_MCP_OPENAI_FORMS`, `mcp-for-blender`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1070 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BlenderMCPServer` connect `BlenderMCPServer` to `addon.py`, `.gbuffer_quad_capture`, `._polyhaven_material_info`, `._get_config_value`, `_blendermcp_ensure_server_running`, `premium_integration_status`, `._get_aabb`, `tripo_endpoints`, `._polyhaven_import_model`, `premium_active`, `_polyhaven_api_get`, `.download_polypizza_model`, `.get_world_state_snapshot`, `._get_sketchfab_api_key`, `.execute_command`, `._polyhaven_import_texture`, `.set_texture`, `.describe_node_type`, `.download_polyhaven_asset`, `.pick_viewport_object`, `_polyhaven_category_paths`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `server()` (e.g. with `_connect()` and `addon()`) actually correct?**
  _`server()` has 36 INFERRED edges - model-reasoned connections that need verification._
- **What connects `uvx`, `mcp-for-blender`, `BLENDER_MCP_APPS` to the rest of the system?**
  _5 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `addon.py` be split into smaller, more focused modules?**
  _Cohesion score 0.03406593406593406 - nodes in this community are weakly interconnected._
- **Why does `BlenderMCPServer` connect `BlenderMCPServer` to `bundled/addon.py`, `._get_aabb`, `._execute_command_internal`, `premium_enabled_generators`, `._polyhaven_import_texture`, `tripo_endpoints`, `.describe_node_type`, `.pick_viewport_object`, `.download_polypizza_model`, `.get_world_state_snapshot`, `premium_active`, `premium_integration_status`, `_polyhaven_api_get`, `.execute_command`, `._get_sketchfab_api_key`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Should `bundled/addon.py` be split into smaller, more focused modules?**
  _Cohesion score 0.04322845417236662 - nodes in this community are weakly interconnected._
- **Why does `execute_blender_code()` connect `Capabilities` to `get_blender_connection`, `SandboxViolation`, `get_telemetry`, `server.py`, `Context`, `test_safe_mode.py`, `README.md`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._