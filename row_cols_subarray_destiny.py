import numpy as np
import matplotlib.pyplot as plt


capacity_in_mb = 576 #128 MB or it's divisors
capacity = capacity_in_mb * 2**20 * 8 #bits from MB
word_width = 256 #from 8 to 1024 (only power of 2)
associativity = 1 #fixed
stackdiecount = 1 #fixed
num_row_per_set = 1 #fixed
num_way_per_row =  int(associativity/num_row_per_set)


MuxSenseAmp = 1 #bounded from 1 to 256
# MuxOutputLev1 x MuxOutputLev2: defines number of columns connected to one sense amplifiers 
MuxOutputLev1 = 8 #bounded from 1 to 256
MuxOutputLev2 = 64 #bounded from 1 to 256

#search space: 144 overall number of mats or it's divisors
num_col_mat = 12 #equall to row_mat
num_row_mat = 12 #equall to col_mat
num_mats = num_row_mat * num_col_mat #overall number of mats
num_subarray = 1 #overall number of subarrays

num_col_mat_active = num_col_mat #only active mats in column
num_row_mat_active = num_row_mat #only active mats in row
N_active_subarrays = num_subarray #only active subarrays (col * row)

#function for calculations
Mux_levels = MuxSenseAmp * MuxOutputLev1 * MuxOutputLev2
num_address_bits = int(np.log2(capacity/word_width/associativity/stackdiecount))
num_address_bits_mat = num_address_bits - int(np.log2(num_mats/(num_col_mat_active*num_row_mat_active)))
num_address_bits_gating = int(np.log2(num_subarray/N_active_subarrays))

num_address_bits_subarray = num_address_bits_mat - num_address_bits_gating #address bits subarray via H-tree

h = int(np.log2(num_col_mat_active))
v = int(np.log2(num_row_mat_active))

row = ((2**(num_address_bits_subarray) * associativity) / Mux_levels * num_way_per_row)
col = ((word_width / 2**(h+v)) / N_active_subarrays) * Mux_levels * num_way_per_row

size = num_mats * num_subarray * row * col * stackdiecount

print("Number of address bits: ", num_address_bits_subarray)
print("Row: ", int(row))
print("Col: ", int(col))
print("Size: ", int(size))
print("Desired Size: ", capacity)
#main constrain for capacity: capacity = size
print("Difference between desired size and calculated size: ", capacity - size)
print("Caluclated Size in MB: ", size/(8*1024*1024))
print("Desired Capacity in MB: ", capacity/(8*1024*1024))


def custom_function(x):
    return int(np.log2(x) + 0.1)

range = 31
x_values = np.arange(1, range)
y_values = [custom_function(x) for x in x_values]

plt.figure(figsize=(12, 6))
plt.plot(x_values, y_values, 'b-')
plt.scatter(x_values, y_values, color='red', s=20)
plt.xlabel('x')
plt.ylabel('int(log2(x) + 0.1)')
plt.title(f'Plot of int(log2(x) + 0.1) for x from 1 to {range-1}')
plt.grid(True)
#plt.show()