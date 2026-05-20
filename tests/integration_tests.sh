#!/bin/bash

# Test the modified Freerouter with KiCAD 9 and Surrogate tools
test_modified_freerouter() {
  # Set up environment variables
  export KICAD_HOME=/opt/axentx/kicad-9
  export SURROGATE_HOME=/opt/axentx/surrogate-1
  export FREEROUTER_HOME=$SURROGATE_HOME/tools/freerouter

  # Run the test
  $FREEROUTER_HOME/freerouter --kicad-home $KICAD_HOME --surrogate-home $SURROGATE_HOME
  if [ $? -eq 0 ]; then
    echo "Test passed"
  else
    echo "Test failed"
  fi
}

# Run the test
test_modified_freerouter