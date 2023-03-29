How to test:
1. Run get_data.py (untested)
2. Measure the real distance for the saved image and add it to measured_data.txt in distance_test_data (make sure to use the correct # of spaces and commas)
3. Run test_data.py

To delete the most recently taken data:
1. Delete color_n.py
2. Delete depth_n.py
3. Decrease the number in data_counter.txt by 1

To display the data of an example:
1. Run display(example_number) in the main function of test_data.py