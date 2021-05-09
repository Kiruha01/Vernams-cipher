teardown() {
  if [[ -d "inputs" ]]
  then
    rm -r inputs
  fi
  if [[ -d "keys" ]]
  then
    rm -r keys
  fi
  if [[ -d "outs" ]]
  then
    rm -r outs
  fi
    if [[ -d "input_test" ]]
  then
    rm -r input_test
  fi
  if [[ -d "key_test" ]]
  then
    rm -r key_test
  fi
  if [[ -d "out_test" ]]
  then
    rm -r out_test
  fi

  if [[ -f "key" ]]
   then
    rm key
  fi

  if [[ -f "out" ]]
   then
    rm out
    if [[ -f "out.key" ]]
    then
      rm out.key
    fi
  fi

  if [[ -f "input" ]]
   then
    rm "input"
    if [[ -f "input.dec" ]]
    then
      rm input.dec
      if [[ -f "input.dec.key" ]]
      then
        rm input.dec.key
      fi
    fi
  fi
}
