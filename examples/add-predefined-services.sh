#!/bin/bash

# This prompt script allows the addition of predefined services
# during the installation process.


predefined_services_file="./predefined-services.json"
predefined_services=$(cat $predefined_services_file)
services_count=$(echo $predefined_services | jq ". | length")

# List the available services
printf "=%.0s" {1..20} && printf " List of Services " && printf "=%.0s" {1..20} && printf "\n"
for i in $(seq 1 $services_count); do
  j=$((i - 1))
  label=$(echo $predefined_services | jq -r --argjson i $j '.[$i].label')
  description_lines=$(echo $predefined_services | jq -r --argjson i $j '.[$i].description | @text')

  echo "$i. $label"
  while read -r line; do
    echo "   $line"
  done <<< "$description_lines"
done

# Selection prompt
printf "\nAdd predefined services. Separate choices using coma (,) or space.\n"
printf "[Leave empty for none; 'a' or 'all' for all]\n"
printf "Options: "
read -r input
# Parse the user input
if [[ -z "$input" ]]; then
  selected=()
elif [[ "$input" == "a" || "$input" == "all" ]]; then
  selected=($(seq 1 $services_count))
else
  # Convert to an array
  input=$(echo "$input" | sed "s/[ ,]\+/,/g")
  IFS=',' read -r -a selected <<< "$input"
  # Keep only valid options
  valid=()
  for s in "${selected[@]}"; do
    if [[ "$s" =~ ^[0-9]+$ && "$s" -ge 1 && "$s" -le $services_count ]]; then
      valid+=("$s")
    fi
  done
  selected=("${valid[@]}")
fi

# List the selected services
echo "Selected:"
for i in ${selected[@]}; do
  j=$((i - 1))
  label=$(echo $predefined_services | jq -r --argjson i $j '.[$i].label')
  echo "  $i. $label"  
done
printf "=%.0s" {1..58} && printf "\n"


# Add services and check scripts
services_file="./services.json"
data=$(cat $services_file)
services=$(echo $data | jq -c ".[]")

new_services="["
for i in ${selected[@]}; do
  j=$((i - 1))
  label=$(echo $predefined_services | jq -r --argjson i $j '.[$i].label')
  while IFS= read -r service; do
    # For each selected service
    if [ "$label" == "$(echo $service | jq -r '.label')" ]; then
      # Add service object
      new_services+="${service},"
      # Copy check script
      check_script_filepath=$(echo $service | jq -r --arg k "check-script" '.[$k]')
      cp $check_script_filepath /etc/service-status-indicator-api/scripts/
    fi
  done < <(echo "$services") 
done
new_services=${new_services::-1} # remove the last trailing comma
new_services+="]"

# Add new services to existing services.json
existing_services_file="/etc/service-status-indicator-api/services.json"
jq ". += $new_services" "$existing_services_file" > tmp.json && mv tmp.json "$existing_services_file"
