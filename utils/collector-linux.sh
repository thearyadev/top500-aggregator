#!/usr/bin/env bash
set -e

# ---------- GLOBAL SETTINGS ----------
# Delay used for all sleep calls (except the hard‑coded 0.1 s in tab_reset)
delay=0.1

window_selector="title:^(Overwatch)$"
target_width="1920"
target_height="1080"

assets_path=$1
mouse_device_name=$2

# -------------------------------------------------
# ------------------- FUNCTIONS -------------------
# -------------------------------------------------

get_window_info() {
	local window_info=$(hyprctl clients -j | jq '.[] | select(.title == "Overwatch")')
	if [ -z "$window_info" ]; then
		echo "Error: Couldn't get Overwatch window details" >&2
		return 1
	else
		echo "$window_info"
	fi
}

enforce_window() {
	local window_info=$(get_window_info)
	echo "Found overwatch window"

	hyprctl --quiet dispatch movecursor 10 10
	hyprctl --quiet dispatch movecursor 200 200
	hyprctl --quiet dispatch movecursor 300 300
	echo "Setting window to floating"
	hyprctl --quiet dispatch setfloating "$window_selector"
	echo "Resizing window to $target_width $target_height"
	hyprctl --quiet dispatch resizewindowpixel exact "$target_width" "$target_height", "$window_selector"
	echo "Moving to ensure on screen..."
	hyprctl --quiet dispatch movewindowpixel exact 0 0, "$window_selector"

	local window_info=$(get_window_info)

	local window_size=$(echo "$window_info" | jq '.size')
	local window_width=$(echo "$window_size" | jq '.[0]')
	local window_height=$(echo "$window_size" | jq '.[1]')
	local positionX=$(echo "$window_info" | jq '.at[0]')
	local positionY=$(echo "$window_info" | jq '.at[1]')
	local floating=$(echo "$window_info" | jq '.floating')

	if [ "$floating" != "true" ]; then
		echo "Error: Window is not floating" >&2
		return 1
	fi

	if [ "$window_width" != "$target_width" ] || [ "$window_height" != "$target_height" ]; then
		echo "Error: Window size is incorrect: $window_width x $window_height" >&2
		return 1
	fi

	if [ "$positionX" != "0" ] || [ "$positionY" != "0" ]; then
		echo "Error: Window position is incorrect: $positionX, $positionY" >&2
		return 1
	fi

	echo "Game window position verified."
	return 0
}

verify_dependency() {
	command -v "$1" >/dev/null 2>&1
}

screenshot() {
	role=$(echo "${1#switch_to_}" | tr '[:lower:]' '[:upper:]')
	region=$(echo "${2#switch_to_}" | tr '[:lower:]' '[:upper:]')
	page=$(echo "${3#switch_to_}" | tr '[:lower:]' '[:upper:]')
	grim -g "0,0 1920x1080" "$assets_path/$role-$region-$page.png"
}

# -------------------------------------------------
# Keyboard actions (all use the global $delay)
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
	echo "switching to tank"
	tab_reset
	sleep $delay
	kb_space
	sleep $delay
	kb_fwd
	sleep $delay
	kb_space
}

switch_to_damage() {
	echo "switching to damage"
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
	echo "switching to support"
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

switch_to_americas() {
	echo "switching to americas"
	# should already be on americas, after reset from anywhere else.
}

switch_to_europe() {
	echo "switching to europe"
	tab_reset
	kb_fwd
	kb_fwd
	kb_space
	kb_down
	kb_space
}

switch_to_asia() {
	echo "switching to asia"
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

# -------------------------------------------------
# Tab‑reset (hard‑coded 0.1 s delay)
# -------------------------------------------------
tab_reset() {
	# Override the global $delay with a local, hard‑coded value
	local delay=0.1
	sleep 1
	for i in $(seq 1 20); do
		kb_fwd
	done
	for i in $(seq 1 25); do
		kb_bkwd
	done
}
# -------------------------------------------------

next_page() {
	for i in $(seq 1 16); do
		kb_fwd
	done
	sleep $delay # previously 1 s
	kb_space
}

toggle_friends_list() {
	tab_reset
	for skips in $(seq 1 3); do
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
	stat "$assets_path" >/dev/null
	echo "Asset path exists"

	# setup_ydotool
	echo "ydotoold is running with pid: $ydo_pid"

	if [ -n "$(ls -A "$assets_path")" ]; then
		echo "Error: assets path contains files. Avoiding destroying existing data." >&2
		return 1
	fi

	# check deps
	REQUIRED_COMMANDS=("jq" "hyprctl" "grim" "ydotoold" "ydotool")
	for cmd in "${REQUIRED_COMMANDS[@]}"; do
		if ! verify_dependency "$cmd"; then
			echo "Error: Required command '$cmd' not found. Please install it." >&2
			return 1
		fi
	done

	echo "starting in 5 seconds..."

	# resize and position window
	enforce_window

	roles=(
		"switch_to_tank"
		"switch_to_damage"
		"switch_to_support"
	)
	regions=(
		"switch_to_americas"
		"switch_to_europe"
		"switch_to_asia"
	)

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
				echo "page: $page"
				sleep 1
				screenshot $role $region $page
				next_page
			done
		done
		reset_region
	done
}

main
