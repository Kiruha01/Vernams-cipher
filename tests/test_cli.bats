load bats_helpers

@test "Encrypt one file" {
  run python ../ver.py encrypt -i files/input1 -o out -k key -s 1
  [ "$output" = "encrypting files/input1...done" ]
  run cmp -s key files/key1
  [ "$status" -eq 0 ]
  run cmp -s out files/out1
  [ "$status" -eq 0 ]
}

@test "Decrypt one file" {
  run python ../ver.py decrypt -i files/out1 -o input -k files/key1
  [ "$output" = "decrypting files/out1...done" ]
  run cmp -s input files/input1
  [ "$status" -eq 0 ]
}

@test "Encrypt file with default key_name" {
  run python ../ver.py encrypt -i files/input1 -o out -s 1
  [ "$output" = "encrypting files/input1...done" ]
  run cmp -s out.key files/key1
  [ "$status" -eq 0 ]
  run cmp -s out files/out1
  [ "$status" -eq 0 ]
}

@test "Decrypt file with default key_name" {
  python ../ver.py encrypt -i files/input1 -o out -s 1
  run python ../ver.py decrypt -i out -o input
  [ "$output" = "decrypting out...done" ]
  run cmp -s input files/input1
  [ "$status" -eq 0 ]
}

@test "Encrypt file with default key_name and out_name" {
  cp files/input1 input
  run python ../ver.py encrypt -i input -s 1
  [ "$output" = "encrypting input...done" ]
  run cmp -s input.dec files/out1
  [ "$status" -eq 0 ]
  run cmp -s input.dec.key files/key1
  [ "$status" -eq 0 ]
}

@test "Decrypt file with default key_name and out_name" {
  cp files/out1 input.dec
  cp files/key1 input.dec.key
  run python ../ver.py decrypt -i input.dec
  [ "$output" = "decrypting input.dec...done" ]
  run cmp -s input files/input1
  [ "$status" -eq 0 ]
}

@test "Encrypt dir" {
  skip "key1 is diff"
  ./create_directories.sh
  run python ../ver.py encrypt -i inputs -o out_test -k key_test -s 1
  [ "$status" -eq 0 ]
  run diff outs out_test
  [ "$status" -eq 0 ]
  run diff keys key_test
  [ "$status" -eq 0 ]
}

@test "Decrypt dir" {
  ./create_directories.sh
  run python ../ver.py decrypt -i outs -k keys -o input_test
  [ "$status" -eq 0 ]
  run diff inputs input_test
  [ "$status" -eq 0 ]
}