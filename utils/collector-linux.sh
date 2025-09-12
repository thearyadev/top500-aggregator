#!/usr/bin/env bash
# set -e

# ---------- GLOBAL SETTINGS ----------
delay=0.1
window_selector="title:^(Overwatch)$"
target_width="1920"
target_height="1080"

assets_path=$1

# -------------------------------------------------
# ------------------- FUNCTIONS -------------------
# -------------------------------------------------

log_info() { echo -e "[INFO] $*"; }
log_warn() { echo -e "\e[33m[WARN]\e[0m $*"; }
log_error() { echo -e "\e[31m[ERROR]\e[0m $*" >&2; }

usage() {
	echo "Usage: $0 <assets_path>"
	echo
	echo "Automates Overwatch screenshot collection in Hyprland."
	echo "Requires: jq, hyprctl, grim"
	exit 1
}

get_window_info() {
	local window_info
	window_info=$(hyprctl clients -j | jq '.[] | select(.title == "Overwatch")')
	if [ -z "$window_info" ]; then
		log_error "Couldn't get Overwatch window details."
		return 1
	fi
	echo "$window_info"
}

enforce_window() {
	log_info "Ensuring Overwatch window state..."
	get_window_info >/dev/null || return 1

	hyprctl --quiet dispatch movecursor 10 10
	hyprctl --quiet dispatch movecursor 200 200
	hyprctl --quiet dispatch movecursor 300 300

	log_info "Setting window to floating..."
	hyprctl --quiet dispatch setfloating "$window_selector"

	log_info "Resizing window to ${target_width}x${target_height}..."
	hyprctl --quiet dispatch resizewindowpixel exact "$target_width" "$target_height", "$window_selector"

	log_info "Moving window to (0,0)..."
	hyprctl --quiet dispatch movewindowpixel exact 0 0, "$window_selector"

	local window_info
	window_info=$(get_window_info)

	local window_width window_height positionX positionY floating
	window_width=$(echo "$window_info" | jq '.size[0]')
	window_height=$(echo "$window_info" | jq '.size[1]')
	positionX=$(echo "$window_info" | jq '.at[0]')
	positionY=$(echo "$window_info" | jq '.at[1]')
	floating=$(echo "$window_info" | jq '.floating')

	if [ "$floating" != "true" ]; then
		log_error "Window is not floating."
		return 1
	fi
	if [ "$window_width" != "$target_width" ] || [ "$window_height" != "$target_height" ]; then
		log_error "Window size incorrect: ${window_width}x${window_height}"
		return 1
	fi
	if [ "$positionX" != "0" ] || [ "$positionY" != "0" ]; then
		log_error "Window position incorrect: ${positionX}, ${positionY}"
		return 1
	fi

	log_info "Game window geometry verified."
}

verify_dependency() {
	if ! command -v "$1" >/dev/null 2>&1; then
		log_error "Missing required command: $1"
		return 1
	fi
}

require_hyprland_session() {
	if [ -z "$HYPRLAND_INSTANCE_SIGNATURE" ] && [ "$XDG_CURRENT_DESKTOP" != "Hyprland" ]; then
		log_error "This script must be run inside a Hyprland session."
		exit 1
	fi
}

screenshot() {
	local role region page
	role=$(echo "${1#switch_to_}" | tr '[:lower:]' '[:upper:]')
	region=$(echo "${2#switch_to_}" | tr '[:lower:]' '[:upper:]')
	page=$(echo "${3#switch_to_}" | tr '[:lower:]' '[:upper:]')
	grim -g "0,0 1920x1080" "$assets_path/$role-$region-$page.png"
}

# -------------------------------------------------
# Keyboard simulation helpers
# -------------------------------------------------

kb_fwd() {
	sleep $delay
	hyprctl --quiet dispatch sendshortcut , TAB, "$window_selector"
}

kb_bkwd() {
	sleep $delay
	hyprctl --quiet dispatch sendkeystate code:50, Shift_L, down, "$window_selector"
	hyprctl --quiet dispatch sendkeystate code:23, Tab, down, "$window_selector"
	hyprctl --quiet dispatch sendkeystate code:23, Tab, up, "$window_selector"
	hyprctl --quiet dispatch sendkeystate code:50, Shift_L, up, "$window_selector"
}

kb_down() {
	sleep $delay
	hyprctl --quiet dispatch sendshortcut , DOWN, "$window_selector"
}

kb_space() {
	sleep $delay
	hyprctl --quiet dispatch sendkeystate code:65, Space, down, "$window_selector"
	sleep $delay
	hyprctl --quiet dispatch sendkeystate code:65, Space, up, "$window_selector"
}

# -------------------------------------------------
# Role / region navigation
# -------------------------------------------------
switch_to_tank() {
	log_info "Switching to role: TANK"
	tab_reset
	sleep $delay
	kb_space
	sleep $delay
	kb_fwd
	sleep $delay
	kb_space
}

switch_to_damage() {
	log_info "Switching to role: DAMAGE"
	reset_role
	sleep $delay
	kb_space
	sleep $delay
	for _ in {1..2}; do
		kb_fwd
		sleep $delay
	done
	kb_space
}

switch_to_support() {
	log_info "Switching to role: SUPPORT"
	reset_role
	sleep $delay
	kb_space
	sleep $delay
	for _ in {1..3}; do
		kb_fwd
		sleep $delay
	done
	kb_space
}

switch_to_americas() { log_info "Switching to region: AMERICAS"; }
switch_to_europe() {
	log_info "Switching to region: EUROPE"
	tab_reset
	kb_fwd
	kb_fwd
	kb_space
	kb_down
	kb_space
}
switch_to_asia() {
	log_info "Switching to region: ASIA"
	tab_reset
	kb_fwd
	kb_fwd
	kb_space
	kb_down
	kb_space
}

reset_role() {
	tab_reset
	kb_space
	sleep $delay
	kb_fwd
	sleep $delay
	kb_space
	tab_reset
}

reset_region() {
	tab_reset
	kb_fwd
	kb_fwd
	kb_space
	kb_fwd
	kb_space
	tab_reset
}

tab_reset() {
	local delay=0.1
	sleep 1
	for _ in $(seq 1 20); do kb_fwd; done
	for _ in $(seq 1 25); do kb_bkwd; done
	kb_fwd
	kb_fwd
}

next_page() {
	for _ in $(seq 1 16); do kb_fwd; done
	sleep $delay
	kb_space
}

toggle_friends_list() {
	tab_reset
	for _ in $(seq 1 3); do
		kb_fwd
		sleep $delay
	done
	kb_space
	sleep $delay
	kb_space
}

# -------------------------------------------------
# Main entry point
# -------------------------------------------------
main() {
	if [ $# -lt 1 ]; then
		usage
	fi

	require_hyprland_session

	if [ ! -d "$assets_path" ]; then
		log_error "Assets path '$assets_path' does not exist."
		exit 1
	fi
	log_info "Assets path exists: $assets_path"

	if [ -n "$(ls -A "$assets_path")" ]; then
		log_error "Assets path contains files. Avoiding overwrite."
		exit 1
	fi

	REQUIRED_COMMANDS=("jq" "hyprctl" "grim")
	for cmd in "${REQUIRED_COMMANDS[@]}"; do
		verify_dependency "$cmd" || exit 1
	done

	log_info "Starting in 5 seconds..."
	sleep 5

	enforce_window

	roles=("switch_to_tank" "switch_to_damage" "switch_to_support")
	regions=("switch_to_americas" "switch_to_europe" "switch_to_asia")

	for role in "${roles[@]}"; do
		sleep $delay
		$role
		sleep 2
		for region in "${regions[@]}"; do
			sleep $delay
			$region
			toggle_friends_list
			sleep 1
			tab_reset
			for page in $(seq 1 50); do
				echo -e "\e[34mProcessing:\e[0m ROLE=${role#switch_to_} REGION=${region#switch_to_} PAGE=$page"
				sleep 1
				screenshot $role $region $page
				next_page
			done
		done
		reset_region
	done
}

# main "$@"
